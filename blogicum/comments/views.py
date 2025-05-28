from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView

from comments.mixins import BaseCommentMixin, CommentFormMixin
from core.mixins import AuthorRequiredMixin, CachedObjectMixin


class CommentCreateView(LoginRequiredMixin,
                        BaseCommentMixin,
                        CommentFormMixin,
                        CreateView):
    """Представление для создания нового комментария.

    Наследует функциональность:
    - LoginRequiredMixin: Требует аутентификации пользователя
    - BaseCommentMixin: Базовые настройки работы с комментариями
    - CommentFormMixin: Обработка формы комментария
    - CreateView: Стандартная логика создания объекта

    Attributes:
        template_name (str):
            Унаследован от BaseCommentMixin ('blog/comment.html')
        form_class (CommentForm): Унаследован от CommentFormMixin
        model (Comment): Унаследован от BaseCommentMixin

    Methods:
        form_valid:
            Автоматически вызывается при валидной форме
            (обрабатывается в CommentFormMixin)
    """

    pass


class CommentUpdateView(AuthorRequiredMixin,
                        CachedObjectMixin,
                        BaseCommentMixin,
                        CommentFormMixin,
                        UpdateView):
    """Представление для редактирования существующего комментария.

    Наследует функциональность:
    - AuthorRequiredMixin: Проверка авторства комментария
    - CachedObjectMixin: Кеширует обьект в рамках запроса
    - BaseCommentMixin: Базовые настройки работы с комментариями
    - CommentFormMixin: Обработка формы комментария
    - UpdateView: Стандартная логика обновления объекта

    Attributes:
        template_name (str):
            Унаследован от BaseCommentMixin ('blog/comment.html')
        form_class (CommentForm): Унаследован от CommentFormMixin
        model (Comment): Унаследован от BaseCommentMixin
        pk_url_kwarg (str): Унаследован от BaseCommentMixin ('comment_id')

    Methods:
        dispatch:
            Проверка прав доступа (обрабатывается в AuthorRequiredMixin)
        form_valid:
            Автоматически вызывается при валидной форме
            (обрабатывается в CommentFormMixin)
    """

    pass


class CommentDeliteView(AuthorRequiredMixin,
                        CachedObjectMixin,
                        BaseCommentMixin,
                        DeleteView):
    """Представление для удаления комментария.

    Наследует функциональность:
    - AuthorRequiredMixin: Проверка авторства комментария
    - CachedObjectMixin: Кеширует обьект в рамках запроса
    - BaseCommentMixin: Базовые настройки работы с комментариями
    - DeleteView: Стандартная логика удаления объекта

    Attributes:
        template_name (str):
            Унаследован от BaseCommentMixin ('blog/comment.html')
        model (Comment): Унаследован от BaseCommentMixin
        pk_url_kwarg (str): Унаследован от BaseCommentMixin ('comment_id')

    Methods:
        dispatch:
            Проверка прав доступа (обрабатывается в AuthorRequiredMixin)
        get_success_url:
            Перенаправление после удаления (обрабатывается в BaseCommentMixin)
    """

    pass
