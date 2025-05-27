from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils import timezone


class PublishedPostManager(models.Manager):
    """
    Менеджер для получения опубликованных постов с оптимизированными
    запросами и счетчиком комментариев.
    Включает только посты:
    - с is_published=True
    - с опубликованной категорией (category__is_published=True)
    - с датой публикации не в будущем (pub_date__lte=now)
    """

    def get_queryset(self) -> QuerySet:
        return (
            super().get_queryset()
            .select_related('author', 'category', 'location')
            .annotate(comment_count=Count('comments'))
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            )
            .order_by('-pub_date')
        )
