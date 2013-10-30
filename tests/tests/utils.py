from django.contrib.auth.models import Permission
from django.test import TestCase
from olp.models import ObjectPermission
from ..models import Apple, Orange


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

        with self.assertNumQueries(2):
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

    def test_obj_permission_instance(self):
        permission = Permission.objects.all()[0]

        apple = Apple(name="test")
        apple.save()

        with self.assertNumQueries(3):
            result = self.user.assign_perm(permission, apple)

        self.assertEqual(result, True)
        self.assertEqual(ObjectPermission.objects.count(), 1)


class TestHasPerm(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.user.save()

    def test_invalid_perm(self):
        from olp.utils import has_perm

        result = has_perm(self.user, "invalid.perm_name")

        self.assertEqual(result, False)


class TestRemovePerm(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.user.save()

    def test_real_normal_permission(self):
        self.user.assign_perm("test.can_be_awesome")

        result = self.user.remove_perm("test.can_be_awesome")

        self.assertEqual(result, True)

    def test_normal_permission_instance(self):
        permission = Permission.objects.all()[0]

        self.user.assign_perm(permission)

        result = self.user.remove_perm(permission)

        self.assertEqual(result, True)

    def test_real_obj_permission(self):
        apple = Apple(name="test")
        apple.save()

        self.user.assign_perm("test.can_be_awesome", apple)

        with self.assertNumQueries(3):
            result = self.user.remove_perm("test.can_be_awesome", apple)

        self.assertEqual(result, True)
        self.assertEqual(ObjectPermission.objects.count(), 0)

    def test_obj_permission_instance(self):
        permission = Permission.objects.all()[0]

        apple = Apple(name="test")
        apple.save()

        self.user.assign_perm(permission, apple)

        with self.assertNumQueries(2):
            result = self.user.remove_perm(permission, apple)

        self.assertEqual(result, True)
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

    def test_fake_obj_permission(self):
        apple = Apple(name="test")
        apple.save()

        with self.assertNumQueries(2):
            result = self.user.remove_perm("test.does_not_exist", apple)

        self.assertEqual(result, False)

    def test_obj_permission_instance(self):
        permission = Permission.objects.all()[0]

        apple = Apple(name="test")
        apple.save()

        with self.assertNumQueries(1):
            result = self.user.remove_perm(permission, apple)

        self.assertEqual(result, True)

class TestGetObjsForUser(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.user.save()

    def test_get_objs_for_user_fail(self):
        from olp.utils import get_objs_for_user

        apple = Apple(name="test")
        apple.save()
        orange = Orange(name="test")
        orange.id = apple.id
        orange.save()

        result = self.user.assign_perm("test.can_be_awesome", apple)

        objs = get_objs_for_user(self.user, "test.can_be_awesome", model_class=Orange)
        self.assertEqual(len(objs), 0)



