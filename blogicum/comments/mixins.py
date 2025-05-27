from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse

from blog.models import Post
from comments.forms import CommentForm
from comments.models import Comment

User = get_user_model()


class AuthorRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки авторства объекта.

    Проверяет, является ли текущий пользователь автором объекта перед
    выполнением действия. Расширяет функциональность LoginRequiredMixin.

    Attributes:
        author_field (str):
            Название поля с автором объекта (по умолчанию 'author').
        raise_exception (bool):
            Вызывать исключение при отказе в доступе (True).
        permission_denied_message (str):
            Сообщение об ошибке при отказе в доступе.

    Methods:
        get_author: Получает автора объекта.
        check_author:
            Проверяет соответствие автора объекта текущему пользователю.
        dispatch: Основной метод обработки запроса с проверкой автора.
    """

    author_field = 'author'
    raise_exception = True
    permission_denied_message = "Доступ запрещен"

    def get_author(self, obj) -> User:
        """Получает автора объекта.

        Args:
            obj: Объект модели, для которого проверяется авторство.

        Returns:
            Автор объекта (обычно User instance).
        """
        return getattr(obj, self.author_field)

    def check_author(self, request, obj) -> bool:
        """Проверяет, является ли пользователь автором объекта.

        Args:
            request: HttpRequest объект.
            obj: Объект модели для проверки.

        Returns:
            bool: True если пользователь является автором, иначе False.
        """
        return self.get_author(obj) == request.user

    def dispatch(self, request, *args, **kwargs):
        """Обрабатывает запрос с проверкой автора объекта.

        Args:
            request: HttpRequest объект.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Результат обработки запроса.

        Raises:
            PermissionDenied: Если пользователь не является автором объекта.
        """
        obj = self.get_object()
        if not self.check_author(request, obj):
            raise PermissionDenied(self.permission_denied_message)
        return super().dispatch(request, *args, **kwargs)


class BaseCommentMixin:
    """Базовый миксин для операций с комментариями.

    Предоставляет общую функциональность для работы с комментариями:
    - Получение связанного поста
    - Базовые настройки (модель, шаблон, URL параметр)

    Attributes:
        model (Type[Comment]): Модель комментария.
        template_name (str): Путь к шаблону.
        pk_url_kwarg (str): Имя параметра URL с ID комментария.
        current_post (Post): Текущий пост (устанавливается в dispatch).
    """

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        """Обрабатывает запрос и сохраняет текущий пост.

        Args:
            request: HttpRequest объект.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Результат обработки запроса.
        """
        self.current_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        """Генерирует URL для перенаправления после успешного действия.

        Returns:
            str: URL страницы детального просмотра поста.
        """
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.current_post.pk})


class CommentFormMixin:
    """Миксин для обработки форм комментариев.

    Предоставляет функциональность для работы с формами комментариев:
    - Установка автора и поста перед сохранением
    - Базовая форма комментария

    Attributes:
        form_class: Класс формы комментария.
    """

    form_class = CommentForm

    def form_valid(self, form: CommentForm):
        """Обрабатывает валидную форму, устанавливая автора и пост.

        Args:
            form: Валидная форма комментария.

        Returns:
            HttpResponse: Результат обработки валидной формы.
        """
        form.instance.post = self.current_post
        form.instance.author = self.request.user
        return super().form_valid(form)
