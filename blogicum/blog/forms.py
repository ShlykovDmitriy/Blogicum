from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = ('is_published', 'created_at', 'author')