from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования постов.

    Позволяет управлять публикацией постов, включая отложенную публикацию.
    Если поле pub_date не заполнено, публикация происходит немедленно.

    Attributes:
        pub_date (forms.DateTimeField): Поле для указания даты/времени поста.
            Если оставить пустым, публикация будет произведена при сохранении.
    """

    pub_date = forms.DateTimeField(
        required=False,
        label='Дата публикации',
        help_text='Оставьте пустым для немедленной публикации',
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control datetimepicker',
                'placeholder': 'Выберите дату и время'
            }
        )
    )

    class Meta:
        model = Post
        exclude = ('is_published', 'created_at', 'author')
        widgets = {
            "text": forms.Textarea({"rows": "5"}),
        }
