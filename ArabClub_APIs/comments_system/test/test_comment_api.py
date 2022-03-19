from django.contrib.auth import get_user_model
from django.utils.text import slugify
from rest_framework.test import APITestCase, APIClient

from comments_system.models import Comment
from newsfeed.models import Post

urls = {
    "token": "/api/v1/token/",
    "reply": '/api/v1/posts/comment/reply/',
    'update_comment': '/api/v1/posts/comment/',
    'create_comment': '/api/v1/posts/comment/',
    'post': '/api/v1/posts/',

}
user_model = get_user_model()


class CommentTestCase(APITestCase):
    def setUp(self) -> None:
        user_data = {
            "username": "user_test_case",
            "email": "user@test.case.com",
            "date_of_birth": "1998-7-13",
            "password": "123",
        }
        self.user = user_model.objects.create_user(**user_data)
        self.client = APIClient()

        data = {"username": self.user.username, "password": "123"}
        response = self.client.post(urls["token"], data, format="json")
        self.token = "Bearer " + response.data["access"]
        self.refresh = "Bearer" + response.data["refresh"]

        # Create Post
        post = {
            'title': 'Hello, TestCase!',
            'content': 'this is post create from news feed test case!',
            'user_id': self.user.pk
        }
        response = self.client.post(urls['post'], data=post,
                                    HTTP_AUTHORIZATION=self.token,
                                    format='json')

        self.slug = slugify(response.data['title'])
        self.post = Post.objects.get(slug=self.slug)

        # Test Comment

        data = {
            'comment': 'This is comment from TestCase.!',
            'post': self.post.pk
        }
        self.url = f"{urls['create_comment']}{self.post.slug}-{self.post.pk}"

        self.response = self.client.post(self.url, data=data, format='json',
                                         HTTP_AUTHORIZATION=self.token)
        # print(response.data)
        self.comment = Comment.objects.all().first()

    def test_create_comment(self):
        self.assertEqual(self.response.status_code, 201)

    def test_update_comment(self):
        data = {
            'comment': 'hello, edite comment form TestCase.!'
        }
        url = f'{urls["update_comment"]}{self.comment.pk}'
        response = self.client.put(url, data=data,
                                   HTTP_AUTHORIZATION=self.token, format='json')
        print()
        self.assertEqual(response.status_code, 200)
