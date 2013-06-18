from django.contrib.auth.models import Permission
from django.test import TestCase
from olp.models import ObjectPermission
from ..models import Apple


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

    def test_real_obj_permission(self):
        apple = Apple(name="test")
        apple.save()

        with self.assertNumQueries(4):
            result = self.user.assign_perm("test.can_be_awesome", apple)

        self.assertEqual(result, True)
        self.assertEqual(ObjectPermission.objects.count(), 1)

    def test_fake_obj_permission(self):
        apple = Apple(name="test")
        apple.save()

        with self.assertNumQueries(2):
            result = self.user.assign_perm("test.does_not_exist", apple)

        self.assertEqual(result, False)
        self.assertEqual(ObjectPermission.objects.count(), 0)


class TestRemovePermNotSet(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.user.save()

    def test_real_normal_permission(self):
        result = self.user.remove_perm("test.can_be_awesome")

        self.assertEquals(result, True)

    def test_fake_normal_permission(self):
        result = self.user.remove_perm("test.does_not_exist")

        self.assertEqual(result, False)

    def test_normal_permission_instance(self):
        permission = Permission.objects.all()[0]

        result = self.user.remove_perm(permission)

        self.assertEqual(result, True)

    def test_real_obj_permission(self):
        apple = Apple(name="test")
        apple.save()

        with self.assertNumQueries(2):
            result = self.user.remove_perm("test.can_be_awesome", apple)

        self.assertEqual(result, True)
