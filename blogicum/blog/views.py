from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.forms import PostForm
from blog.models import Post, Category, User
from core.constants import POSTS_IN_PAGE


'''def index(request: HttpRequest) -> HttpResponse:
    """Возвращает главную страницу с 5 последними опубликованными постами.

    Использует кастомный менеджер PublishedPostManager для оптимизированного
    запроса. Посты сортируются по дате публикации (новые первые).

    Args:
        request: Объект HTTP-запроса.

    Returns:
        HttpResponse: Рендер шаблона blog/index.html с контекстом:
            - post_list: QuerySet[Post] - 5 последних опубликованных постов
    """
    post_list = Post.published.all()[:POSTS_IN_INDEX]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


    def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Отображает детальную страницу поста по его ID.

    Проверяет, что пост:
    - Опубликован (is_published=True)
    - Имеет опубликованную категорию
    - Не отложен (pub_date <= текущее время)
    Если пост не найден или не соответствует условиям - возвращает 404.

    Args:
        request: Объект HTTP-запроса.
        id: ID запрашиваемого поста.

    Returns:
        HttpResponse: Рендер шаблона blog/detail.html с контекстом:
            - post: Post - найденный объект поста

    Raises:
        Http404: Если пост не существует или не опубликован.
    """
    post = get_object_or_404(
        Post.published.all(),
        pk=id
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)'''


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Отображает все опубликованные посты указанной категории.

    Проверяет, что категория:
    - Существует
    - Опубликована (is_published=True)
    Если категория не найдена - возвращает 404.

    Args:
        request: Объект HTTP-запроса.
        category_slug: Slug категории из URL.

    Returns:
        HttpResponse: Рендер шаблона blog/category.html с контекстом:
            - post_list: QuerySet[Post] - посты категории
            - category: Category - объект текущей категории

    Raises:
        Http404: Если категория не существует или не опубликована.
    """
    post_list = Post.published.filter(category__slug=category_slug)
    category = get_object_or_404(
        Category.objects.only(
            'title', 'description'
        ).filter(is_published=True),
        slug=category_slug
    )
    context = {'post_list': post_list,
               'category': category}
    return render(request, 'blog/category.html', context)



class PostListView(ListView):
    pass


class PostCreateView(CreateView):
    pass


class PostDetailView(DetailView):
    pass


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.published.filter(author__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = list(context["object_list"])
        if posts:
            context["profile"] = posts[0].author
        return context
    

