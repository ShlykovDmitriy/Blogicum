from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def about(request: HttpRequest) -> HttpResponse:
    """Отображает страницу о сайте

    Returns:
        HttpResponse: HTML-страница с информацией о сайте
    """
    return render(request, 'pages/about.html')


def rules(request: HttpRequest) -> HttpResponse:
    """Отображает страницу с правилами сайта

    Returns:
        HttpResponse: HTML-страница с правилами сайта
    """
    return render(request, 'pages/rules.html')
