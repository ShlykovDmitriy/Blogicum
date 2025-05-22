from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(required=False)
    
    class Meta:
        model = Post
        exclude = ('is_published', 'created_at', 'author')
        widgets = {
            "text": forms.Textarea({"rows": "5"}),
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }