from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet


class PublishedPostManager(models.Manager):
    """
    Менеджер для получения опубликованных постов с оптимизированными запросами.
    Включает только посты:
    - с is_published=True
    - с опубликованной категорией (category__is_published=True)
    - с датой публикации не в будущем (pub_date__lte=now)
    """
    def get_queryset(self) -> QuerySet:
        return (
            super().get_queryset()
            .select_related('author', 'category', 'location')
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            )
            .order_by('-pub_date')
        )
