from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.forms import PostForm
from comments.forms import CommentForm
from blog.models import Post
from core.constants import POSTS_IN_PAGE



class PostListView(ListView):
    model = Post
    queryset = Post.published.all()
    template_name = 'blog/index.html'
    paginate_by = POSTS_IN_PAGE


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        if not form.instance.pub_date:
            form.instance.pub_date = timezone.now()
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        if not form.instance.pub_date:
            form.instance.pub_date = timezone.now()
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_IN_PAGE

    def get_queryset(self):
        return Post.published.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = list(context['object_list'])
        if posts:
            context['category'] = posts[0].category
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POSTS_IN_PAGE

    def get_queryset(self):
        return Post.published.filter(author__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = list(context['object_list'])
        if posts:
            context['profile'] = posts[0].author
        return context
