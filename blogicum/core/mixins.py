from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import QuerySet
from django.db import models

User = get_user_model()


class AuthorRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки авторства объекта с редиректом на указанный URL.

    Проверяет два условия:
    1. Пользователь аутентифицирован (через LoginRequiredMixin)
    2. Пользователь является автором объекта

    При невыполнении условий:
    - Перенаправляет на URL, указанный в redirect_url_name

    Attributes:
        author_field (str):
            Название поля модели, содержащего автора (default: 'author').
        redirect_url_name (str):
            Имя URL-паттерна для редиректа (default: 'blog:post_detail').
        redirect_id_param (str):
            Имя параметра URL для ID объекта (default: 'post_id').
    """

    author_field = 'author'
    redirect_url_name = 'blog:post_detail'
    redirect_id_param = 'post_id'

    def get_author(self, obj) -> User:
        """Получает автора объекта.

        Args:
            obj: Объект модели, для которого проверяется авторство.

        Returns:
            Автор объекта (обычно User instance).
        """
        return getattr(obj, self.author_field)

    def check_author_or_admin(self, request, obj) -> bool:
        """Проверяет, является ли пользователь автором объекта.

        Args:
            request: HttpRequest объект.
            obj: Объект модели для проверки.

        Returns:
            bool: True если пользователь является автором, иначе False.
        """
        return self.get_author(obj) == request.user or request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        """Обрабатывает запрос:
        Неаутентифицированный пользователь или Аутентифицированный
        не-автор - редирект на redirect_url_name
        Автор - продолжает обработку запроса

        Args:
            request: HttpRequest объект.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Результат обработки запроса.
        """
        obj = getattr(self, 'object', None) or self.get_object()
        if (not self.check_author_or_admin(request, obj)
           or not request.user.is_authenticated):
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self) -> str:
        """Генерирует URL для перенаправления.

        Алгоритм определения ID объекта:
        1. Сначала пытается получить из параметров URL (self.kwargs)
        2. Затем из атрибута pk самого объекта

        Returns:
            str: Абсолютный URL для перенаправления
        """
        object_id = (self.kwargs.get(self.redirect_id_param)
                     or getattr(self.get_object(), 'pk', None))
        return reverse(
            self.redirect_url_name,
            kwargs={self.redirect_id_param: object_id}
        )


class CachedObjectMixin:
    """Миксин для кеширования объекта в рамках запроса (опциональный)"""

    def get_object(self, queryset: Optional[QuerySet] = None) -> models.Model:
        if not hasattr(self, '_object'):
            self._object = super().get_object(queryset)
        return self._object

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
