from django.urls import path
from users.views import (
    ListUserView,
    UserDetailsView,
    PersonInfoView,
    BioView,
    SkillsView,
    AddressView,
    GitHubView,
    PhoneView
)

urlpatterns = [
    path('list', ListUserView.as_view()),
    path('user/<str:username>', UserDetailsView.as_view(),
         name='user_details'),
    path('user/<str:username>/person-info', PersonInfoView.as_view()),
    path('user/<str:username>/bio', BioView.as_view()),
    path('user/<str:username>/skills', SkillsView.as_view()),
    path('user/<str:username>/address', AddressView.as_view()),
    path('user/<str:username>/github', GitHubView.as_view()),
    path('user/<str:username>/phone', PhoneView.as_view())
]
