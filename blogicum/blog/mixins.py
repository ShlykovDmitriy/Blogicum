from django.utils import timezone

from core.constants import POSTS_IN_PAGE
from blog.forms import PostForm
from blog.models import Post


class PostMixin:
    """Базовый миксин для представлений, работающих с моделью Post.

    Предоставляет общие настройки для отображения постов:
    - Указывает модель Post
    - Задает количество постов на странице

    Attributes:
        model (Post): Модель Post для работы представления.
        paginate_by (int): Количество постов на странице пагинации.
        queryset: Опубликованные посты
    """

    model = Post
    paginate_by = POSTS_IN_PAGE
    queryset = Post.optimized.visible()


class PostDetailDeleteMixin(PostMixin):
    """Миксин для Отображения поста или удаления его

    Наследуется от PostMixin

    Attributes:
        pk_url_kwarg: Первичный ключ для постов
    """

    pk_url_kwarg = 'post_id'


class PostFormMixin(PostDetailDeleteMixin):
    """Миксин для обработки форм создания/редактирования поста.

    Обеспечивает:
    - Автоматическое назначение автора поста
    - Установку текущей даты, если дата публикации не указана

    Наследуется от PostDetailDeleteMixin

    Attributes:
        template_name: Название шаблона
        form_class: Класс формы для редактирования поста.
    """

    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form: PostForm):
        """Обработка валидной формы.

        Args:
            form (PostForm): Валидная форма поста.

        Returns:
            HttpResponse: Ответ после успешного сохранения формы.

        Notes:
            - Автоматически назначает текущего пользователя автором поста
            - Устанавливает текущее время как дату публикации, если не указано
        """
        form.instance.author = self.request.user
        if not form.instance.pub_date:
            form.instance.pub_date = timezone.now()
        return super().form_valid(form)
