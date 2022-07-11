from django.urls import path

from users.views import CreateUserView, ListUserView, UserDetailsView

url_path = "user/<str:username>/"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register_user"),
    path("list", ListUserView.as_view()),
    path(url_path, UserDetailsView.as_view(), name="user_details"),
]
