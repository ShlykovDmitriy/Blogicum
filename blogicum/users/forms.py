from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма для создания пользователя,
    расширяющая стандартную UserCreationForm.

    Добавляет поле email к стандартным полям формы регистрации.

    Attributes:
        Meta (class): Вложенный класс для конфигурации формы.
            model (AbstractUser): Модель пользователя.
            fields: Поля формы (username, password1, password2, email).
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class CustomUserChangeForm(UserChangeForm):
    """Кастомная форма для редактирования пользователя,
    расширяющая UserChangeForm.

    Убирает поле password из формы и добавляет поля для редактирования.

    Attributes:
        password (None): Явное указание, что поле пароля не требуется.
        Meta (class): Вложенный класс для конфигурации формы.
            model (AbstractUser): Модель пользователя.
            fields: Поля формы (username, email, first_name, last_name).
    """

    password: None = None

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)
