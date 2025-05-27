from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Кастомная модель пользователя, расширяющая стандартную AbstractUser.

    Может быть дополнена дополнительными полями по мере необходимости.
    В текущей реализации сохраняет все функциональность стандартного
    пользователя Django.
    """

    pass
