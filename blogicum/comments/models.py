from django.db import models
from django.contrib.auth import get_user_model

from blog.models import Post

User = get_user_model()

class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')

    class Meta:
        ordering = ('created_at',)