from django.contrib.auth import get_user_model
from django.test import TestCase


class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model()
        self.user.objects.create_superuser(
            email="super@test.com",
            username="super.case",
            date_of_birth="1998-7-13",
            password="123456",
        )

        self.user.objects.create(
            email="test_case@test.com",
            username="test.case",
            date_of_birth="1998-7-13",
            password="123456",
        )

    def test_create_user(self):
        user = self.user.objects.get(username="test.case")
        self.assertEqual(str(user), "test.case")
        self.assertEqual(str(user.date_of_birth), "1998-07-13")
        self.assertEqual(user.email, "test_case@test.com")

        superuser = self.user.objects.get(username="super.case")
        self.assertEqual(str(superuser), "super.case")
        self.assertTrue(superuser.is_staff, True)
