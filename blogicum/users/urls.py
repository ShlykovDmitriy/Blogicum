from django.urls import path, include

from users.views import UserCreateView


app_name = 'users'

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('', include('django.contrib.auth.urls')),
]
