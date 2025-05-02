from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse

from blog.models import Post, Category


def index(request: HttpRequest) -> HttpResponse:
    post_list = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True, category__is_published=True, pub_date__lte=timezone.now()
    ).only(
        'title', 'text', 'pub_date',
        'author__username',
        'location__name', 'location__is_published',
        'category__title', 'category__slug'
    )[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.select_related(
            'category', 'location', 'author'
        ).only(
            'title', 'text', 'pub_date',
            'author__username',
            'location__name', 'location__is_published',
            'category__title', 'category__slug'
        ).filter(
            is_published=True, category__is_published=True, pub_date__lte=timezone.now()
        ),
        pk=id
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)

def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    post_list = Post.objects.select_related(
        'category', 'location', 'author'
    ).only(
        'title', 'id', 'text', 'pub_date',
        'author__username',
        'location__is_published', 'location__name',
        'category__title','category__description', 'category__slug'
    ).filter(
        category__slug = category_slug, is_published=True, pub_date__lte=timezone.now()
    )
    category = get_object_or_404(
        Category.objects.only(
            'title', 'description'
        ).filter(is_published=True),
        slug=category_slug
    )
    context = {'post_list': post_list,
               'category': category}
    return render(request, 'blog/category.html', context)
