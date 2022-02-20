from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.serializers import (
    PhoneSerializer,
    Phone,
    GitHubAccount,
    GitHubSerializer,
    Skills,
    SkillsSerializer,
    Address,
    AddressSerializer,
    Bio,
    BioSerializer,
    NameSerializer,
    FirstNameAndLastName,
)
from users.models import (
    Phone,
    Skills,
    GitHubAccount,
    Bio,
    FirstNameAndLastName,
    Address,
)

user_model = get_user_model()

# TODO
"""
List All users with out user admin
list user details with out auth
change/update user data with out owner
"""

urls = {
    "list": "/account/list",
    "details": "/account/user/",
    "token": "/api/token/",
    "register": "/account/register/",
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

        data = {"username": self.user.username, "password": "123"}
        response = self.client.post(urls["token"], data, format="json")
        self.token = "Bearer " + response.data["access"]
        self.refresh = "Bearer" + response.data["refresh"]

    def test_check_is_user_create(self):
        user = self.user.username
        other = self.other_user.username

        self.assertEqual(user, "user_test_case")
        self.assertEqual(other, "other_test_case")

    def test_get_user_token(self):
        data = {"username": self.user.username, "password": "123"}
        response = self.client.post(urls["token"], data, format="json")
        token = response.data["access"]
        refresh_token = response.data["refresh"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_details_with_out_admin(self):
        response = self.client.get(urls["list"], HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_details_with_annymous(self):
        url = f'{urls["details"]}{self.user.username}/'
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_change_data_with_annymous(self):
        url = f'{urls["details"]}{self.user.username}/'
        response = self.client.put(
            url, data={"username": "anny_mous_change"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_data_with_out_owner(self):
        data = {"username": self.other_user.username, "password": "123"}
        response = self.client.post(urls["token"], data=data, format="json")
        token = response.data["access"]
        data = {"username": self.other_user.username}
        url = f'{urls["details"]}{self.user.username}/'
        # HTTP_AUTHORIZATION
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_more_data_with_aut(self):
        data = {"skills": {"skill_name": "Python"}, "phone": {"phone": "01066373279"}}
        url = f'{urls["details"]}{self.user.username}/'

        response = self.client.put(
            url, data=data, HTTP_AUTHORIZATION=self.token, format="json"
        )

        phone = Phone.objects.get(user_id=self.user.id)
        skills = Skills.objects.get(user_id=self.user.id)
        self.assertEqual(str(phone), data["phone"]["phone"])
        self.assertEqual(str(skills), data["skills"]["skill_name"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(phone.phone, data["phone"]["phone"])
        self.assertEqual(skills.skill_name, data["skills"]["skill_name"])

    def test_change_data_with_auth(self):
        data = {"phone": {"phone": "01120393742"}}
        url = f'{urls["details"]}{self.user.username}/'
        response = self.client.put(
            url, data=data, HTTP_AUTHORIZATION=self.token, format="json"
        )

        phone = Phone.objects.get(user_id=self.user.id)

        self.assertEqual(str(phone), data["phone"]["phone"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(phone.phone, data["phone"]["phone"])

    def test_create_data(self):
        data = {
            "name": {"first_name": "python", "last_name": "Django"},
            "username": "test.admin.user",
            "email": "islam@admin.arabclub",
            "date_of_birth": "1998-7-13",
            "bio": {"bio": "python, Django"},
            "skills": {"skill_name": "python, Django"},
            "github_url": {"url": "https://github.cosm/"},
            "phone": {"phone": "01066373457"},
            "address": {"country": "Egyp", "city": "qus", "street_name": "Qus"},
        }
        url = f'{urls["details"]}{self.user.username}/'
        response = self.client.put(
            url, data=data, format="json", HTTP_AUTHORIZATION=self.token
        )

        phone = Phone.objects.get(user_id=self.user.id)
        skills = Skills.objects.get(user_id=self.user.id)
        github = GitHubAccount.objects.get(user_id=self.user.id)
        address = Address.objects.get(user_id=self.user.id)
        name = FirstNameAndLastName.objects.get(user_id=self.user.id)
        bio = Bio.objects.get(user_id=self.user.id)

        full_address = (
            f'{data["address"]["street_name"]}, '
            f'{data["address"]["city"]}, '
            f'{data["address"]["country"]}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(phone), data["phone"]["phone"])
        self.assertEqual(str(skills), data["skills"]["skill_name"])
        self.assertEqual(str(github), data["github_url"]["url"])
        self.assertEqual(address.get_full_address, full_address)
        self.assertEqual(name.first_name, data["name"]["first_name"])
        self.assertEqual(name.last_name, data["name"]["last_name"])
        self.assertEqual(str(bio), data["bio"]["bio"])

        phone = {"phone": {"phone": "01120393742"}}

        instance = Phone.objects.get(user_id=self.user.id)
        PhoneSerializer.update(self, instance=instance, validated_data=phone)

        address = {"address": {"country": "egypt"}}

        instance = Address.objects.get(user_id=self.user.id)
        AddressSerializer.update(self, instance=instance, validated_data=address)

        skills = {"skills": {"skill_name": "Docker"}}

        instance = Skills.objects.get(user_id=self.user.id)
        SkillsSerializer.update(self, instance=instance, validated_data=skills)

        github = {"github_url": {"url": "https://www.github.com/user"}}

        instance = GitHubAccount.objects.get(user_id=self.user.id)
        GitHubSerializer.update(self, instance=instance, validated_data=github)

        name = {"name": {"first_name": "Whiskey"}}

        instance = FirstNameAndLastName.objects.get(user_id=self.user.id)
        NameSerializer.update(self, instance=instance, validated_data=name)

        bio = {"bio": {"bio": "Hello Friend"}}

        instance = Bio.objects.get(user_id=self.user.id)
        BioSerializer.update(self, instance=instance, validated_data=bio)

    def test_validator_username(self):
        url = f'{urls["details"]}{self.user.username}/'

        error_change = {
            "username": "valid",
        }

        response = self.client.put(
            url, data=error_change, format="json", HTTP_AUTHORIZATION=self.token
        )

    def test_raise_errors(self):
        data = {"phone": {"phone": "01120"}}
        url = f'{urls["details"]}{self.user.username}/'
        response = self.client.put(
            url, data=data, HTTP_AUTHORIZATION=self.token, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_super_user_permissions(self):
        user = get_user_model()
        user.objects.create_superuser(
            email="super@test.com",
            username="super.case",
            date_of_birth="1998-7-13",
            password="123456",
        )
        data = {"username": "super.case", "password": "123456"}
        response = self.client.post(urls["token"], data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = "Bearer " + response.data["access"]
        response = self.client.get(
            urls["list"], format="json", HTTP_AUTHORIZATION=token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_with_apis(self):
        data = {
            "username": "test_api_endpoint",
            "email": "end@point.com",
            "date_of_birth": "1998-7-13",
            "password": "123456",
        }

        response = self.client.put(urls["register"], data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model()
        user = user.objects.get(username=response.data["username"])
        self.assertEqual(str(user), data["username"])

    def test_create_user_with_errors(self):
        data = {
            "username": "short",
            "email": "end@point.com",
            "date_of_birth": "1998-7-13",
            "password": "123456",
        }

        response = self.client.put(urls["register"], data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
