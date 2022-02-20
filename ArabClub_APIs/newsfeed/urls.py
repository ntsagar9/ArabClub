from django.urls import path
from newsfeed.views import PostListView

app_name = 'newsfeed'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list')
]