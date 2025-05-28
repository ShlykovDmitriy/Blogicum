from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils import timezone


class PostManager(models.Manager):
    """
    Кастомизированный менеджер для модели Post.
        - Получения оптимизированного запроса
        - Получение оптимизированого опубликованого запроса
    """

    def with_optimization(self) -> QuerySet:
        """Базовый QuerySet с оптимизированными связями и аннотацией"""
        return (
            self.get_queryset()
            .select_related('author', 'category', 'location')
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )

    def visible(self) -> QuerySet:
        """Только опубликованные посты (с оптимизацией)"""
        return (
            self.with_optimization()
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            )
        )
