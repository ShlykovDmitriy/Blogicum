from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    """Форма для создания и редактирования комментариев.

    Атрибуты:
        Meta (class): Вложенный класс для конфигурации формы.
            model (Comment): Модель, с которой связана форма.
            fields: Поля, включаемые в форму (только text).
    """

    class Meta:
        model = Comment
        fields = ('text',)
