from django.contrib import admin
from django.utils.text import Truncator

from comments.models import Comment
from core.constants import LEN_TEXT_FOR_ADMIN


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Структура интерфейса комментариев для админ панели."""

    list_display = ('pk', 'short_text', 'author', 'created_at', 'post')
    search_fields = ('post__title', 'post__id')
    list_filter = ('created_at', 'author')
    list_display_links = ('short_text',)

    def short_text(self, obj):
        return Truncator(obj.text).chars(LEN_TEXT_FOR_ADMIN)
    short_text.short_description = 'Текст (кратко)'
