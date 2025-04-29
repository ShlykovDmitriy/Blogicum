from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    pass


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    pass


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    pass
