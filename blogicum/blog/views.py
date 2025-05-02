from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse

from blog.models import Post, Category


def index(request: HttpRequest) -> HttpResponse:
    post_list = Post.published.all()[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(
        Post.published.all(),
        pk=id
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    post_list = Post.published.filter(category__slug=category_slug)
    category = get_object_or_404(
        Category.objects.only(
            'title', 'description'
        ).filter(is_published=True),
        slug=category_slug
    )
    context = {'post_list': post_list,
               'category': category}
    return render(request, 'blog/category.html', context)
