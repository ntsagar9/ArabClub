from django.urls import path, re_path
from comments_system.views import CommentDetailView, CommentView, RelpyView

app_name = 'comment_sys'
urlpatterns = [
    path("<int:pk>", CommentDetailView.as_view(), name="comment_put"),
    path("<str:slug>-<int:pk>", CommentView.as_view(),
         name="create_comment"),
    re_path(r"^reply/(?P<pk>[0-9]*)", RelpyView.as_view()),
]
