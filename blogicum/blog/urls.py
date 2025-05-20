from django.urls import path

from blog.views import PostListView, category_posts, PostDetailView, PostCreateView, UserPostListView


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path(
        'category/<slug:category_slug>/',
        category_posts,
        name='category_posts'
    ),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name ='create'),
    path('profile/<str:username>/', UserPostListView.as_view(), name = 'profile')
]
