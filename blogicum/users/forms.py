from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta): # type: ignore
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # type: ignore


class CustomUserChangeForm(UserChangeForm):
    password:None = None

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)
        