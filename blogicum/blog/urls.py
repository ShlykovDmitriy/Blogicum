from django.urls import path

from blog.views import PostListView, CategoryPostListView, PostDetailView, PostCreateView, UserPostListView, PostDeleteView, PostUpdateView


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path(
        'category/<slug:category_slug>/',
        CategoryPostListView.as_view(),
        name='category_posts'
    ),   
    path('posts/create/', PostCreateView.as_view(), name ='create_post'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/delete/', PostDeleteView.as_view(), name='delete'),
    path('posts/<int:post_id>/edit/', PostUpdateView.as_view(), name='edit'),
    path('profile/<str:username>/', UserPostListView.as_view(), name = 'profile')
]
