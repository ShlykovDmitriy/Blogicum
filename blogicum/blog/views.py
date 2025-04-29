from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """
    Отображает главную страницу блога с постами в обратном хронологическом
    порядке.

    Returns:
        HttpResponse: HTML-страница с лентой постов
    """
    context = {'posts': list(reversed(posts))}
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Отображает детальную страницу конкретного поста.

    Args:
        request: Объект HTTP-запроса
        id: Идентификатор поста

    Returns:
        HttpResponse: HTML-страница с полным текстом поста
    """
    context = {'post': posts[id]}
    return render(request, 'blog/detail.html', context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Пока отображает страницу с названием категории.

    Args:
        request: Объект HTTP-запроса
        category_slug: URL-идентификатор категории

    Returns:
        HttpResponse: Страница с названием категории
    """
    context = {'category': category_slug}
    return render(request, 'blog/category.html', context)
