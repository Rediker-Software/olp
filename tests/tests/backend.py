from django.test import TestCase
from olp.backends import PermissionBackend
from ..models import Apple


class TestBackendBasic(TestCase):

    def setUp(self):
        from django.contrib.auth.models import Group, User

        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.user.save()

        self.group = Group(name="group")
        self.group.save()

        self.user.groups.add(self.group)
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

    def test_user_no_group_permissions(self):
        result = self.backend.get_group_permissions(self.user)

        self.assertEqual(result, set())

    def test_user_no_obj_group_permissions(self):
        apple = Apple(name="test")
        apple.save()

        result = self.backend.get_group_permissions(self.user, apple)

        self.assertEqual(result, set())

    def test_user_has_perm(self):
        apple = Apple(name="test")
        apple.save()

        self.user.assign_perm("tests.can_be_awesome", apple)

        result = self.backend.has_perm(self.user, "tests.can_be_awesome")

        self.assertEqual(result, True)

    def test_user_has_obj_perm(self):
        apple = Apple(name="test")
        apple.save()

        self.user.assign_perm("tests.can_be_awesome", apple)

        result = self.backend.has_perm(self.user, "tests.can_be_awesome", apple)

        self.assertEqual(result, True)

    def test_user_has_group_obj_perm(self):
        apple = Apple(name="test")
        apple.save()

        self.group.assign_perm("tests.can_be_awesome", apple)

        result = self.backend.has_perm(self.user, "tests.can_be_awesome", apple)

        self.assertEqual(result, True)
