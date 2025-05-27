from typing import Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def page_not_found_view(
        request: HttpRequest,
        exception: Exception
) -> HttpResponse:
    """Кастомный обработчик для ошибки 404 (Страница не найдена).

    Args:
        request: Объект HTTP-запроса.
        exception: Исключение, вызвавшее ошибку.

    Returns:
        HttpResponse: Рендер шаблона 404.html с HTTP-статусом 404.
    """
    return render(request, 'pages/404.html', status=404)


def permission_denied(
        request: HttpRequest,
        exception: Exception
) -> HttpResponse:
    """Кастомный обработчик для ошибки 403 (Доступ закрыт).

    Args:
        request: Объект HTTP-запроса.
        exception: Исключение, вызвавшее ошибку.

    Returns:
        HttpResponse: Рендер шаблона 403.html с HTTP-статусом 403.
    """
    return render(request, 'pages/403.html', status=403)


def server_error_view(
        request: HttpRequest,
        exception: Optional[Exception] = None
) -> HttpResponse:
    """Кастомный обработчик для ошибки 500 (Внутренняя ошибка сервера).

    Args:
        request: Объект HTTP-запроса.
        exception: Опциональное исключение (если передано middleware).

    Returns:
        HttpResponse: Рендер шаблона 500.html с HTTP-статусом 500.
    """
    return render(request, 'pages/500.html', status=500)


def csrf_failure_view(
        request: HttpRequest,
        reason: str = ''
) -> HttpResponse:
    """Кастомный обработчик для ошибки 403 CSRF (Отказ верификации).

    Args:
        request: Объект HTTP-запроса.
        reason: Причина ошибки (например, 'CSRF token missing').

    Returns:
        HttpResponse: Рендер шаблона 403csrf.html с HTTP-статусом 403.
    """
    return render(request, 'pages/403csrf.html', status=403)
