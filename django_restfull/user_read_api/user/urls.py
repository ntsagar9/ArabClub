from django.urls import path
from user.views import ListUserView, UserDetailsView

url_path = "users/<str:username>"
api_version = "v1"

urlpatterns = [
    path("users/list", ListUserView.as_view()),
    path(url_path, UserDetailsView.as_view(), name="user_details"),
]
