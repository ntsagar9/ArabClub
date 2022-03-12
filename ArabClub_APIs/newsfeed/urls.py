from django.urls import path

from newsfeed.views import PostListView, PostDetailsView, CommentView

app_name = 'newsfeed'

urlpatterns = [
    path('/', PostListView.as_view(), name='post_list'),
    path('/<str:slug>-<int:pk>', PostDetailsView.as_view(),
         name='post_details'),
    path('/comment/<int:pk>', CommentView.as_view(), name='comment_put')

]
