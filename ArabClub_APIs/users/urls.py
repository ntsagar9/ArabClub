from django.urls import path
from users.views import ListUserView

urlpatterns = [
    path('list', ListUserView.as_view())
]