from django.urls import path, re_path, include

from newsfeed.views import (
    PostListView,
    PostDetailsView,
)

app_name = "newsfeed"

urlpatterns = [
    # Get posts with limit posts count or get all posts by default count
    re_path(r"(?:limit=(?P<count>\d+)/)?$", PostListView.as_view(),
            name="post_list"),

    path("<str:slug>-<int:pk>", PostDetailsView.as_view(),
         name="post_details"),

    # Comment Sys Urls
    path('comment/', include('comments_system.urls'))
]
