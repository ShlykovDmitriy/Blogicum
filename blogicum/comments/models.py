from django.contrib.auth import get_user_model
from django.db import models

from blog.models import Post

User = get_user_model()


class Comment(models.Model):
    """Модель комментария к посту.

    Атрибуты:
        text (TextField): Текст комментария.
        post (ForeignKey): Связь с постом, к которому относится комментарий.
        author (ForeignKey): Связь с автором комментария.
        created_at (DateTimeField): Дата и время создания комментария.

    Мета:
        ordering: Сортировка комментариев по дате создания (от старых к новым).
        verbose_name (str): Человекочитаемое имя модели в единственном числе.
        verbose_name_plural (str):
            Человекочитаемое имя модели во множественном числе.
    """

    text = models.TextField(
        verbose_name='Комментарий'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ('created_at',)
