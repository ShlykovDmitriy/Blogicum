from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


posts: list[dict[str, int | str]] = [
    {
        'id': 0,
        'location': 'Остров отчаянья',
        'date': '30 сентября 1659 года',
        'category': 'travel',
        'text': '''Наш корабль, застигнутый в открытом море
                страшным штормом, потерпел крушение.
                Весь экипаж, кроме меня, утонул; я же,
                несчастный Робинзон Крузо, был выброшен
                полумёртвым на берег этого проклятого острова,
                который назвал островом Отчаяния.''',
    },
    {
        'id': 1,
        'location': 'Остров отчаянья',
        'date': '1 октября 1659 года',
        'category': 'not-my-day',
        'text': '''Проснувшись поутру, я увидел, что наш корабль сняло
                с мели приливом и пригнало гораздо ближе к берегу.
                Это подало мне надежду, что, когда ветер стихнет,
                мне удастся добраться до корабля и запастись едой и
                другими необходимыми вещами. Я немного приободрился,
                хотя печаль о погибших товарищах не покидала меня.
                Мне всё думалось, что, останься мы на корабле, мы
                непременно спаслись бы. Теперь из его обломков мы могли бы
                построить баркас, на котором и выбрались бы из этого
                гиблого места.''',
    },
    {
        'id': 2,
        'location': 'Остров отчаянья',
        'date': '25 октября 1659 года',
        'category': 'not-my-day',
        'text': '''Всю ночь и весь день шёл дождь и дул сильный
                порывистый ветер. 25 октября.  Корабль за ночь разбило
                в щепки; на том месте, где он стоял, торчат какие-то
                жалкие обломки,  да и те видны только во время отлива.
                Весь этот день я хлопотал  около вещей: укрывал и
                укутывал их, чтобы не испортились от дождя.''',
    },
]


def index(request: HttpRequest) -> HttpResponse:
    """
    Отображает главную страницу блога с постами в обратном хронологическом
    порядке.

    Returns:
        HttpResponse: HTML-страница с лентой постов
    """
    context = {'posts': list(reversed(posts))}
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Отображает детальную страницу конкретного поста.

    Args:
        request: Объект HTTP-запроса
        id: Идентификатор поста

    Returns:
        HttpResponse: HTML-страница с полным текстом поста
    """
    context = {'post': posts[id]}
    return render(request, 'blog/detail.html', context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Пока отображает страницу с названием категории.

    Args:
        request: Объект HTTP-запроса
        category_slug: URL-идентификатор категории

    Returns:
        HttpResponse: Страница с названием категории
    """
    context = {'category': category_slug}
    return render(request, 'blog/category.html', context)
