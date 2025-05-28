from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.mixins import PostDetailDeleteMixin, PostFormMixin, PostMixin
from blog.models import Category, Post
from comments.forms import CommentForm
from core.mixins import AuthorRequiredMixin

User = get_user_model()


class PostListView(PostMixin, ListView):
    """Представление для отображения списка опубликованных постов.

    Attributes:
        queryset (QuerySet[Post]): QuerySet опубликованных постов.
        template_name (str): Путь к шаблону страницы.
    """

    queryset = Post.published.all()
    template_name = 'blog/index.html'


class CategoryPostListView(PostMixin, ListView):
    """Представление для отображения постов конкретной категории.

    Attributes:
        template_name (str): Путь к шаблону страницы.
    """

    template_name = 'blog/category.html'

    def get_queryset(self) -> QuerySet[Post]:
        """Получает QuerySet постов для указанной категории.

        Returns:
            QuerySet[Post]: Посты указанной опубликованной категории.

        Raises:
            Http404: Если категория не найдена или не опубликована.
        """
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return Post.published.filter(category=self.category)

    def get_context_data(self, **kwargs):
        """Добавляет категорию в контекст шаблона.

        Returns:
            Dict[str, Any]: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class UserPostListView(PostMixin, ListView):
    """Представление для отображения постов конкретного пользователя.

    Attributes:
        template_name (str): Путь к шаблону страницы.
    """

    template_name = 'blog/profile.html'

    def get_queryset(self) -> QuerySet[Post]:
        """Получает QuerySet постов пользователя.

        Для автора возвращает все посты с дополнительными аннотациями.
        Для других пользователей - только опубликованные посты.

        Returns:
            QuerySet[Post]: Посты указанного пользователя.
        """
        self.profile_user = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        if self.profile_user == self.request.user:
            return Post.objects.select_related(
                'author', 'category', 'location'
            ).filter(
                author=self.profile_user
            ).annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')
        return Post.published.filter(author=self.profile_user)

    def get_context_data(self, **kwargs):
        """Добавляет профиль пользователя в контекст шаблона.

        Returns:
            Dict[str, Any]: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile_user
        return context


class PostCreateView(LoginRequiredMixin, PostFormMixin, CreateView):
    """Представление для создания нового поста.

    Attributes:
        template_name (str): Путь к шаблону формы.
    """

    pass


class PostDeleteView(AuthorRequiredMixin, PostDetailDeleteMixin, DeleteView):
    """Представление для удаления поста (только для автора).

    Attributes:
        template_name (str): Путь к шаблону подтверждения.
        success_url (str): URL для перенаправления после удаления.
    """

    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class PostUpdateView(AuthorRequiredMixin, PostFormMixin, UpdateView):
    """Представление для редактирования поста (только для автора).

    Attributes:
        template_name (str): Путь к шаблону формы.
    """

    pass


class PostDetailView(PostDetailDeleteMixin, DetailView):
    """Представление для просмотра деталей поста.

    Attributes:
        template_name (str): Путь к шаблону страницы.
    """

    template_name = 'blog/detail.html'

    def get_object(self, queryset: Optional[QuerySet[Post]] = None) -> Post:
        """Получает объект поста с проверкой прав доступа.

        Args:
            queryset: Базовый QuerySet.

        Returns:
            Post: Запрошенный пост.

        Raises:
            Http404: Если пост не найден.
        """
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            Post.published.all(), pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        """Добавляет форму комментария и список комментариев в контекст.

        Returns:
            Dict[str, Any]: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context
