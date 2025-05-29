## Blogicum

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-3.2+-green.svg)](https://djangoproject.com)

Проект блога с системой комментариев, реализующий CRUD для постов и комментариев с авторизацией и проверкой прав доступа.

## 🌟 Особенности

- **Авторизация пользователей** 
  - Регистрация
  - Вход/выход
  - Профиль
  - Редактирование профиля
  - Изменение пароля
- **CRUD для постов** 
  - Создание поста (для авторизированных пользователей)
  - Удаление/редактирование поста (для авторов)
- **Комментарии** с проверкой авторства:
  - Добавление (для авторизованных)
  - Редактирование/удаление (только для авторов)
- **Кастомизированные миксины**:
  - `AuthorRequiredMixin` - проверка авторства


## 🛠 Технологии

- Python 3.11
- Django 3.2+
- Django Templates

## 🚀 Запуск проекта

1. Клонировать репозиторий:
   ```bash
   git clone git@github.com:ShlykovDmitriy/django_sprint1.git
   cd blogicum/
2. Настроить виртуальное окружение:

   ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    sourse venv\Scripts\activate     # Windows
3. Установить зависимости:

   ```bash
    pip install -r requirements.txt
4. Настройка БД (SQLite по умолчанию):

   ```bash
    python manage.py makemigrations
    python manage.py migrate
5. Создать суперпользователя:

   ```bash
    python manage.py createsuperuser
6. Запустить сервер:

   ```bash
    python manage.py runserver



## 🔒 Система прав доступа
- Действие:	Аноним	Авторизованный	Автор
- Просмотр постов	✓	✓	✓
- Создание поста	✗	✓	✓
- Редактирование поста	✗	✗	✓
- Добавление комментария	✗	✓	✓
- Редактирование коммента	✗	✗	✓

## 🌍 URL-структура проекта
1. **Основные маршруты**
- URL	 - Метод - 	Назначение
- /admin/	- GET -	Админ-панель Django
- /auth/registration/	- GET/POST -	Регистрация пользователя
- /auth/login/ -	GET/POST -	Авторизация пользователя
- /auth/logout/ -	GET -	Выход из системы
- /auth/password_change/	- GET/POST -	Смена пароля
- /auth/password_reset/ -	GET/POST -	Сброс пароля
- /auth/profile/edit/ - GET/POST -	Редактирование профиля
- /about/	 -GET -	Статическая страница "О проекте"
- /rules/	- GET -	Статическая страница "Правила"
2. **Посты (blog)**
- URL	- Метод	- Назначение
- / -	GET -	Главная страница (все посты)
- /category/<slug:category_slug>/	- GET -	Посты по категории
- /posts/create/ -	GET/POST -	Создание нового поста
- /posts/<int:post_id>/ -	GET -	Детализация поста
- /posts/<int:post_id>/edit/	- GET/POST -	Редактирование поста
- /posts/<int:post_id>/delete/ -	GET/POST -	Удаление поста
- /profile/<str:username>/ -	GET	 - Профиль пользователя (все его посты)
3. **Комментарии**
- URL	Метод	Назначение
- /posts/<int:post_id>/comment/	- POST	- Добавление комментария к посту
- /posts/<int:post_id>/edit_comment/<int:comment_id>/ -	GET/POST - 	Редактирование комментария
- /posts/<int:post_id>/delete_comment/<int:comment_id>/ -	GET/POST -	Удаление комментария





## 📧 Контакты
- Автор: [Шлыков Дмитрий](https://github.com/ShlykovDmitriy)
- Email: atea_ohe@yandex.ru
- Лицензия: MIT
