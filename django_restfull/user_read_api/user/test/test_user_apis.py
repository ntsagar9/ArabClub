from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

user_model = get_user_model()

# TODO
"""
List All users with out user admin
list user details with out auth
change/update user data with out owner
"""
ip = "http://127.0.0.1:8000"
urls = {
    "list": f"{ip}users/list",
    "details": f"{ip}/users/",
}


class CreateUserTestCase(APITestCase):
    def setUp(self) -> None:
        user_data = {
            "username": "user_test_case",
            "email": "user@test.case.com",
            "date_of_birth": "1998-7-13",
            "password": "123",
        }
        other_user = {
            "username": "other_test_case",
            "email": "other@test.case.com",
            "date_of_birth": "1998-7-13",
            "password": "123",
        }
        self.user = user_model.objects.create_user(**user_data)
        self.other_user = user_model.objects.create_user(**other_user)
        self.client = APIClient()

    def test_check_is_user_create(self):
        user = self.user.username
        other = self.other_user.username
        self.assertEqual(user, "user_test_case")
        self.assertEqual(other, "other_test_case")

    # def test_list_users_details_with_out_admin(self):
    #     response = self.client.get(urls["list"], HTTP_AUTHORIZATION=self.token) # noqa E501
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_details_with_annymous(self):
        url = f'{urls["details"]}{self.user.username}'
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
