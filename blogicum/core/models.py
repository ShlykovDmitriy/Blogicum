from django.db import models


class IsPublishedAndCreatedAt(models.Model):
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано', help_text='Снимите галочку, что бы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        abstract = True


class Title(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
