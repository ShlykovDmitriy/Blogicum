from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from users.forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class UserCreateView(CreateView):
    """Представление для регистрации нового пользователя.

    После успешной регистрации автоматически авторизует пользователя
    и перенаправляет на его профиль.

    Attributes:
        model (Type[User]): Модель пользователя Django.
        template_name (str): Путь к шаблону формы регистрации.
        form_class (Type[CustomUserCreationForm]): Кастомная форма регистрации.
        success_url (str): URL для перенаправления по умолчанию.
    """

    model = User
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form: CustomUserCreationForm):
        """Обработка валидной формы регистрации.

        Args:
            form (CustomUserCreationForm):
                Валидная форма с данными пользователя.

        Returns:
            HttpResponse:
                - Перенаправление на профиль при успешной авторизации
                - Стандартный ответ при ошибке аутентификации
        """
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
    """Представление для редактирования профиля пользователя.

    Позволяет авторизованному пользователю редактировать свой профиль.
    Автоматически использует текущего авторизованного пользователя.

    Attributes:
        model (Type[User]): Модель пользователя Django.
        template_name (str): Путь к шаблону формы редактирования.
        form_class (CustomUserChangeForm): Кастомная форма редактирования.
    """

    model = User
    template_name = 'blog/user.html'
    form_class = CustomUserChangeForm

    def dispatch(self, request, *args, **kwargs):
        """Обработка входящего запроса с проверкой авторизации.

        Args:
            request (HttpRequest): Входящий HTTP-запрос.
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.

        Returns:
            HttpResponse:
                - Перенаправление на страницу входа для неавторизованных
                - Стандартная обработка для авторизованных
        """
        if not request.user.is_authenticated:
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Возвращает текущего авторизованного пользователя.

        Args:
            queryset (Optional[QuerySet[User]]): Базовый QuerySet

        Returns:
            User: Текущий авторизованный пользователь.
        """
        return self.request.user

    def get_success_url(self) -> str:
        """Генерирует URL для перенаправления после успешного редактирования.

        Returns:
            str: URL страницы профиля пользователя.
        """
        username = self.request.user
        return reverse("blog:profile", kwargs={"username": username})
