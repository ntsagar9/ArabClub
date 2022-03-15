from django.urls import path, re_path

from newsfeed.views import (
    PostListView,
    PostDetailsView,
    CommentDetailView,
    CommentView,
    RelpyView,
)

app_name = "newsfeed"

urlpatterns = [
    re_path(
        r"(?:limit=(?P<post_count>\d+)/)?$", PostListView.as_view(), name="post_list"
    ),
    path("<str:slug>-<int:pk>", PostDetailsView.as_view(), name="post_details"),
    path("comment/<int:pk>", CommentDetailView.as_view(), name="comment_put"),
    path("comment/<str:slug>-<int:pk>", CommentView.as_view(), name="create_comment"),
    # path('comment/reply/<int:pk>', RelpyView.as_view(), name='reply_create')
    re_path(r"^comment/reply/(?P<pk>[0-9]*)", RelpyView.as_view()),
]
