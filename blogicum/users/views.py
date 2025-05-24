from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from users.forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

class UserCreateView(CreateView):
    model = User
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            login(self.request, user)
            return redirect('blog:profile', username=username)
        
        return response


class UserUpdateView(UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = CustomUserChangeForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        username = self.request.user
        return reverse("blog:profile", kwargs={"username": username})