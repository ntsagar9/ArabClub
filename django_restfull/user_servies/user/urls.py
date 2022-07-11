from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import CreateUserView, ListUserView, UserDetailsView

url_path = "user/<str:username>/"
api_version = "v1"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register_user"),
    path("users/list", ListUserView.as_view()),
    path(url_path, UserDetailsView.as_view(), name="user_details"),
    path(
        f"{api_version}/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        f"{api_version}/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
