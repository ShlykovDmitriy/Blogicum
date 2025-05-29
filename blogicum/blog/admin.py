from django.contrib import admin
from django.utils.text import Truncator

from blog.models import Category, Post, Location
from core.constants import LEN_TEXT_FOR_ADMIN


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Структура интерфейса поста для админ зоны."""

    list_display = ('pk', 'title', 'short_text', 'pub_date',
                    'author', 'is_published', 'category', 'location', )
    list_editable = ('is_published', 'category', 'location')
    search_fields = ('title',)
    list_filter = ('pub_date', 'author', 'category')
    list_display_links = ('title',)
    empty_value_display = '-пусто-'

    def short_text(self, obj):
        """Укорачивает текст в админ зоне."""
        return Truncator(obj.text).chars(LEN_TEXT_FOR_ADMIN)
    short_text.short_description = 'Текст (кратко)'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Структура интерфейса категории для админ панели."""

    list_display = ('pk', 'title', 'short_description', 'is_published',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('created_at',)
    list_display_links = ('title',)

    def short_description(self, obj):
        """Укорачивает описание в админ зоне."""
        return Truncator(obj.description).chars(LEN_TEXT_FOR_ADMIN)
    short_description.short_description = 'Описание (кратко)'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Структура интерфейса местоположения в админ панели."""

    list_display = ('pk', 'name', 'is_published',)
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('created_at',)
    list_display_links = ('name',)
