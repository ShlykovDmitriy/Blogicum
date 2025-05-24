from django.views.generic import CreateView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse

from blog.models import Post
from comments.models import Comment
from comments.forms import CommentForm


class BaseCommentMixin:
    """Базовый миксин для всех операций с комментариями"""
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        """Получаем пост и сохраняем его в атрибуте"""
        self.current_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """URL для редиректа после успешного действия"""
        return reverse('blog:post_detail', kwargs={'post_id': self.current_post.pk})


class CommentFormMixin:
    """Миксин для операций, связанных с формами"""
    form_class = CommentForm

    def form_valid(self, form):
        """Устанавливаем автора и пост перед сохранением"""
        form.instance.post = self.current_post
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentCreateView(BaseCommentMixin, CommentFormMixin, CreateView):
    pass

class CommentUpdateView(BaseCommentMixin, CommentFormMixin, UpdateView):
    pass

class CommentDeliteView(BaseCommentMixin, DeleteView):
    pass