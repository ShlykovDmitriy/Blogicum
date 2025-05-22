from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

from users.forms import CustomUserCreationForm

User = get_user_model()

class UserCreateView(CreateView):
    model = User
    template_name = 'registration.registration_form.html'
    form_class = CustomUserCreationForm