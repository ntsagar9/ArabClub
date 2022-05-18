from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from rest_framework.test import APIClient

from newsfeed.models import Post

user_model = get_user_model()

urls = {
    "token": "/api/v1/token/",
    "reply": "/api/v1/posts/comment/reply/",
    "update_comment": "/api/v1/posts/comment/",
    "create_comment": "/api/v1/posts/comment/",
    "post": "/api/v1/posts/",
}


class PostModelsTestCase(TestCase):
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
            "title": "Hello, TestCase!",
            "content": "this is post create from news feed test case!",
            "user_id": self.user.pk,
        }
        self.response = self.client.post(
            urls["post"],
            data=post,
            HTTP_AUTHORIZATION=self.token,
            format="json",
        )

        self.slug = slugify(self.response.data["title"])
        self.post = Post.objects.get(slug=self.slug)

    def test_title(self):
        url = f'{urls["post"]}{self.slug}-{self.post.pk}'
        url = reverse("newsfeed:post_details", args=[self.slug, self.post.pk])

        self.assertEqual(url, self.post.get_absolute_url())
        self.assertEqual(self.post.__str__(), self.post.title)
