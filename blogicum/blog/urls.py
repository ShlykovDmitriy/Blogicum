from django.urls import include, path

from blog.views import (CategoryPostListView, PostCreateView, PostDeleteView,
                        PostDetailView, PostListView, PostUpdateView,
                        UserPostListView)

app_name = 'blog'

urlpatterns = [
    path(
        '',
        PostListView.as_view(),
        name='index'
    ),
    path(
        'category/<slug:category_slug>/',
        CategoryPostListView.as_view(),
        name='category_posts'
    ),
    path(
        'posts/create/',
        PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:post_id>/',
        include('comments.urls', namespace='comments')
    ),
    path(
        'posts/<int:post_id>/',
        PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        'posts/<int:post_id>/edit/',
        PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'profile/<str:username>/',
        UserPostListView.as_view(),
        name='profile'
    ),
]
