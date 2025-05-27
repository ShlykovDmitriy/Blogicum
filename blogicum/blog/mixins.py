from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from core.constants import POSTS_IN_PAGE
from blog.forms import PostForm
from blog.models import Post


class PostMixin:
    """Базовый миксин для представлений, работающих с моделью Post.

    Предоставляет общие настройки для отображения постов:
    - Указывает модель Post
    - Задает количество постов на странице

    Attributes:
        model (Type[Post]): Модель Post для работы представления.
        paginate_by (int): Количество постов на странице пагинации.
    """

    model = Post
    paginate_by = POSTS_IN_PAGE


class PostFormMixin:
    """Миксин для обработки форм создания/редактирования поста.

    Обеспечивает:
    - Автоматическое назначение автора поста
    - Установку текущей даты, если дата публикации не указана

    Attributes:
        model (Type[Post]): Модель Post для работы формы.
        form_class (Type[PostForm]): Класс формы для редактирования поста.
    """

    model = Post
    form_class = PostForm

    def form_valid(self, form: PostForm):
        """Обработка валидной формы.

        Args:
            form (PostForm): Валидная форма поста.

        Returns:
            HttpResponse: Ответ после успешного сохранения формы.

        Notes:
            - Автоматически назначает текущего пользователя автором поста
            - Устанавливает текущее время как дату публикации, если не указано
        """
        form.instance.author = self.request.user
        if not form.instance.pub_date:
            form.instance.pub_date = timezone.now()
        return super().form_valid(form)


class PostAuthorRequiredMixin:
    """Миксин для проверки авторства поста.

    Ограничивает доступ к редактированию/удалению постов только их авторам.
    Неавторизованных пользователей и не-авторов перенаправляет
    на страницу поста.

    Attributes:
        pk_url_kwarg (str): Имя параметра URL, содержащего ID поста.
    """

    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        """Обработка запроса с проверкой прав доступа.

        Args:
            request (HttpRequest): Входящий HTTP-запрос.
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.

        Returns:
            HttpResponse:
                - Для авторизованного автора - продолжает обработку запроса
                - Для остальных случаев - перенаправление на страницу поста

        Raises:
            Http404: Если пост не найден.
        """
        if not request.user.is_authenticated:
            return redirect(self.get_redirect_url())
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self) -> str:
        """Генерирует URL для перенаправления при отказе в доступе.

        Returns:
            str: URL страницы просмотра поста.
        """
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})
