from django.urls import path
from users.views import (
    ListUserView,
    UserDetailsView,
    PersonInfoView,
    BioView,
    SkillsView,
    AddressView,
    GitHubView,
    PhoneView,
)

url_path = "user/<str:username>/"

urlpatterns = [
    path("list", ListUserView.as_view()),
    path(url_path, UserDetailsView.as_view(), name="user_details"),
    path(url_path + "person-info/", PersonInfoView.as_view(), name="person_info"),
    path(url_path + "bio/", BioView.as_view(), name="bio"),
    path(url_path + "skills/", SkillsView.as_view()),
    path(url_path + "address/", AddressView.as_view()),
    path(url_path + "github/", GitHubView.as_view()),
    path(url_path + "phone/", PhoneView.as_view()),
]
