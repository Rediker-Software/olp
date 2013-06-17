from django.contrib.auth.models import Permission
from django.test import TestCase


class TestAssignPerm(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.user.save()

    def test_real_normal_permission(self):
        result = self.user.assign_perm("test.can_be_awesome")

        self.assertEqual(result, True)

    def test_fake_normal_permission(self):
        result = self.user.assign_perm("test.does_not_exist")

        self.assertEqual(result, False)

    def test_normal_permission_instance(self):
        permission = Permission.objects.all()[0]

        result = self.user.assign_perm(permission)

        self.assertEqual(result, True)
