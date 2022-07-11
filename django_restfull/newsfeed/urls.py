from django.urls import include, path, re_path

from newsfeed.views import PostDetailsView, PostListView

app_name = "newsfeed"

urlpatterns = [
    # Get posts with limit posts count or get all posts by default count
    re_path(
        r"(?:page=(?P<page_number>\d+)/)?$",
        PostListView.as_view(),
        name="post_list",
    ),
    path(
        "<str:slug>-<int:pk>", PostDetailsView.as_view(), name="post_details"
    ),
    # Comment Sys Urls
    path("comment/", include("comments_system.urls")),
]
