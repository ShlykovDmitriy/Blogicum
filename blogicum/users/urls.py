from django.urls import path, include

from users.views import UserCreateView, UserUpdateView


app_name = 'users'

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('profile/edit/', UserUpdateView.as_view(), name='edit_profile'),
    path('', include('django.contrib.auth.urls')),
]
