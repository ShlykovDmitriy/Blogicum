from django.contrib.auth import get_user_model
from django.db import models

from core.models import Title, IsPublishedAndCreatedAt


User = get_user_model()


class Category(Title, IsPublishedAndCreatedAt):
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор', help_text='Идентификатор страницы для URLж разрешены символы латиницы, цифры, дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(IsPublishedAndCreatedAt):
    name = models.CharField(max_length=256, verbose_name='Название места', help_text='Максимальная длинна 256 символов.')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
    
    def __str__(self):
        return self.name
    

class Post(Title, IsPublishedAndCreatedAt):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дава и время публикации', help_text='Если установить дату и время в будущем - можно делать отложенные публикации.')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор публикации')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts', verbose_name='Местоположение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts', verbose_name='Категория')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
