from django.shortcuts import get_object_or_404
from django.urls import reverse

from blog.models import Post
from comments.forms import CommentForm
from comments.models import Comment


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
