from django.urls import path

from comments.views import (CommentCreateView, CommentDeliteView,
                            CommentUpdateView)

app_name = 'comments'

urlpatterns = [
    path(
        'comment/',
        CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        'edit_comment/<int:comment_id>/',
        CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        'delete_comment/<int:comment_id>/',
        CommentDeliteView.as_view(),
        name='delete_comment'
    )
]
