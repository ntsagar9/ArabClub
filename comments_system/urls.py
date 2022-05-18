from django.urls import re_path

from comments_system.views import (
    CommentUpdateDetailView,
    CommentView,
    RelpyView,
)

app_name = "comment_sys"
urlpatterns = [
    re_path(
        r"^(?P<pk>\d+)$", CommentUpdateDetailView.as_view(), name="comment_put"
    ),
    re_path(
        r"^(?P<post_slug>[-\w]+)(?:-(?P<pk>[-\w]+))$",
        CommentView.as_view(),
        name="create_comment",
    ),
    re_path(r"^reply/(?P<pk>\d+)", RelpyView.as_view()),
]
