from django.db import models


class IsPublishedAndCreatedAt(models.Model):
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Title(models.Model):
    title = models.CharField(max_length=256, help_text='Максимальная длинна 256 символов.')

    class Meta:
        abstract = True
