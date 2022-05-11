from django.test import TestCase
from django.contrib.auth import get_user_model


class TeamAccountTests(TestCase):

    def test_new_superuser_works(self):
        user_model = get_user_model()
        super_user = user_model.objects.create_superuser(
            "test_super_user@super.com", "username", "first_name",
            "last_name", "password"
        )
        self.assertEqual(super_user.email, "test_super_user@super.com")
        self.assertEqual(super_user.username, "username")
        self.assertEqual(super_user.first_name, "first_name")
        self.assertEqual(super_user.last_name, "last_name")
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_active, True)
        self.assertEqual(super_user.is_superuser, True)
        self.assertEqual(str(super_user), "First_name Last_name")

    def test_new_doesnt_work_if_is_superuser_false(self):
        user_model = get_user_model()
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email="test_super_user@super.com", username="username",
                first_name="first_name", last_name="last_name",
                password="password", is_superuser=False
                )
