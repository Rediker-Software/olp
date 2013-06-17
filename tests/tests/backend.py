from django.test import TestCase
from olp.backends import PermissionBackend
from ..models import Apple


class TestBackend(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.user.save()

        self.backend = PermissionBackend()

    def test_no_authenticate(self):
        result = self.backend.authenticate()

        self.assertEqual(result, None)

    def test_get_user(self):
        result = self.backend.get_user()

        self.assertEqual(result, None)

    def test_user_no_permissions(self):
        result = self.backend.get_all_permissions(self.user)

        self.assertEqual(result, set())

    def test_user_no_obj_permissions(self):
        apple = Apple(name="test")
        apple.save()

        result = self.backend.get_all_permissions(self.user, apple)

        self.assertEqual(result, set())
