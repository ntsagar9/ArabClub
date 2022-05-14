from django.urls import path, re_path, include

from newsfeed.views import (
    PostListView,
    PostDetailsView,
)

app_name = "newsfeed"

urlpatterns = [
    re_path(r"(?:limit=(?P<post_count>\d+)/)?$", PostListView.as_view(),
            name="post_list"),
    path("<str:slug>-<int:pk>", PostDetailsView.as_view(), name="post_details"),

    # Comment Sys Urls
    path('comment/', include('comments_system.urls'))
]
