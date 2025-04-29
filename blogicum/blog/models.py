from django.contrib.auth import get_user_model
from django.db import models

from core.models import Title, IsPublishedAndCreatedAt


User = get_user_model()


class Category(Title, IsPublishedAndCreatedAt):
    description = models.TextField()
    slug = models.SlugField(unique=True)


class Location(IsPublishedAndCreatedAt):
    name = models.CharField(max_length=256, help_text='Максимальная длинна 256 символов.')


class Post(Title, IsPublishedAndCreatedAt):
    text = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
