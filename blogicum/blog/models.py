from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from blog.managers import PublishedPostManager
from core.constants import MAX_LEN_TITLE_NAME
from core.models import IsPublishedAndCreatedAt, Title

User = get_user_model()


class Category(Title, IsPublishedAndCreatedAt):
    """Модель категории для публикаций.

    Attributes:
        description (TextField): Подробное описание категории.
        slug (SlugField): Уникальный идентификатор для URL.

    Inherits:
        Title: Абстрактная модель с заголовком.
        IsPublishedAndCreatedAt: Абстрактная модель с флагом
            публикации и датой создания.
    """

    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.title


class Location(IsPublishedAndCreatedAt):
    """Модель местоположения для публикаций.

    Attributes:
        name (CharField): Название места (макс. 256 символов).

    Inherits:
        IsPublishedAndCreatedAt: Абстрактная модель с флагом
            публикации и датой создания.
    """

    name = models.CharField(
        max_length=MAX_LEN_TITLE_NAME,
        verbose_name='Название места',
        help_text='Максимальная длинна 256 символов.'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(Title, IsPublishedAndCreatedAt):
    """Модель публикации/поста.

    Attributes:
        text (TextField): Основной текст публикации.
        pub_date (DateTimeField): Дата и время публикации
            (возможна отложенная публикация).
        author (ForeignKey): Ссылка на автора публикации.
        location (ForeignKey): Местоположение, опционально.
        category (ForeignKey): Категория, обязательно.

    Managers:
        objects (Manager): Стандартный менеджер Django.
        published (PublishedPostManager): Кастомный менеджер для получения
            только опубликованных постов. Фильтрует посты по условиям:
            - is_published=True
            - category__is_published=True
            - pub_date__lte=current_time
            Оптимизирует запросы через select_related и only.

    Inherits:
        Title: Абстрактная модель с заголовком.
        IsPublishedAndCreatedAt: Абстрактная модель с флагом публикации и
            датой создания.

    Relationships:
        - Связь с User: один автор - много публикаций.
        - Связь с Location: одно место - много публикаций.
        - Связь с Category: одна категория - много публикаций.
    """

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — можно '
                   'делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )
    image = models.ImageField(
        'Изображение',
        blank=True,
        upload_to='post_images'
    )
    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def get_absolute_url(self):
        return reverse('blog:profile', kwargs={'username': self.author.username})
    
