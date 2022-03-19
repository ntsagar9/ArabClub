from django.contrib.auth import get_user_model
from django.utils.text import slugify
from rest_framework.test import APITestCase, APIClient

from newsfeed.models import Post

user_model = get_user_model()
urls = {
    "token": "/api/v1/token/",
    "reply": '/api/v1/posts/comment/reply/',
    'update_comment': '/api/v1/posts/comment/',
    'create_comment': '/api/v1/posts/comment/',
    'post': '/api/v1/posts/',

}


class PostAPITestCase(APITestCase):

    def setUp(self) -> None:
        user_data = {
            "username": "user_test_case",
            "email": "user@test.case.com",
            "date_of_birth": "1998-7-13",
            "password": "123",
        }
        self.post = None
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
        self.response = self.client.post(urls['post'], data=post,
                                         HTTP_AUTHORIZATION=self.token,
                                         format='json')

        self.slug = slugify(self.response.data['title'])
        self.post = Post.objects.get(slug=self.slug)

    def test_create_post(self):
        self.assertEqual(self.response.status_code, 201)

    def test_update_title(self):
        date = {
            'title': 'Hello, Edite from TestCase'
        }
        url = f"{urls['post']}{self.slug}-{self.post.pk}"
        response = self.client.put(url, data=date,
                                   HTTP_AUTHORIZATION=self.token, format='json')
        self.post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.title, date['title'])

    def test_update_content(self):
        date = {
            'content': 'Hello, Edite from TestCase.!'
        }
        url = f"{urls['post']}{self.slug}-{self.post.pk}"
        response = self.client.put(url, data=date,
                                   HTTP_AUTHORIZATION=self.token, format='json')
        self.post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.content, date['content'])

    def test_delete_post(self):
        url = f"{urls['post']}{self.slug}-{self.post.pk}"
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token,
                                      format='json')

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Post.DoesNotExist):
            post = Post.objects.get(pk=self.post.pk)


