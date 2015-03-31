from django.contrib.auth.models import Permission
from django.test import TestCase
from olp.models import ObjectPermission
from olp.utils import get_objs_for_user
from ..models import Apple, Orange


class TestAssignPerm(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.user.save()

    def test_real_normal_permission(self):
        result = self.user.assign_perm("tests.can_be_awesome")

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

        with self.assertNumQueries(1):
            result = self.user.assign_perm("tests.can_be_awesome", apple)

        self.assertEqual(result, True)
        self.assertEqual(ObjectPermission.objects.count(), 1)

    def test_fake_obj_permission(self):
        apple = Apple(name="test")
        apple.save()

        with self.assertNumQueries(1):
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
        self.user.assign_perm("tests.can_be_awesome")

        result = self.user.remove_perm("tests.can_be_awesome")

        self.assertEqual(result, True)

    def test_normal_permission_instance(self):
        permission = Permission.objects.all()[0]

        self.user.assign_perm(permission)

        result = self.user.remove_perm(permission)

        self.assertEqual(result, True)

    def test_real_obj_permission(self):
        apple = Apple(name="test")
        apple.save()

        self.user.assign_perm("tests.can_be_awesome", apple)

        result = self.user.remove_perm("tests.can_be_awesome", apple)

        self.assertEqual(result, True)
        self.assertEqual(ObjectPermission.objects.count(), 0)

    def test_obj_permission_instance(self):
        permission = Permission.objects.all()[0]

        apple = Apple(name="test")
        apple.save()

        self.user.assign_perm(permission, apple)

        result = self.user.remove_perm(permission, apple)

        self.assertEqual(result, True)
        self.assertEqual(ObjectPermission.objects.count(), 0)

class TestRemovePermNotSet(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user("test", "test@test.com", "test")
        self.user.save()

    def test_real_normal_permission(self):
        result = self.user.remove_perm("tests.can_be_awesome")

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

        with self.assertNumQueries(1):
            result = self.user.remove_perm("tests.can_be_awesome", apple)

        self.assertEqual(result, True)

    def test_fake_obj_permission(self):
        apple = Apple(name="test")
        apple.save()

        with self.assertNumQueries(1):
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

    def test_single_model_same_permission(self):
        first = Apple(name="test")
        first.save()

        second = Apple(name="other")
        second.save()

        self.user.assign_perm("tests.can_be_awesome", first)

        apples = get_objs_for_user(self.user, "tests.can_be_awesome")

        self.assertEqual(apples.count(), 1)

    def test_multiple_models_same_permission(self):
        apple = Apple(name="test")
        apple.save()

        orange = Orange(name="test")
        orange.id = apple.id
        orange.save()

        result = self.user.assign_perm("tests.can_be_awesome", apple)

        oranges = get_objs_for_user(self.user, "tests.can_be_awesome",
                                    model_class=Orange)
        apples = get_objs_for_user(self.user, "tests.can_be_awesome",
                                   model_class=Apple)

        self.assertEqual(oranges.count(), 0)
        self.assertEqual(apples.count(), 1)

    def test_single_model_different_permission(self):
        first = Apple(name="test")
        first.save()

        second = Apple(name="other")
        second.save()

        self.user.assign_perm("tests.can_eat", first)

        apples = get_objs_for_user(self.user, "tests.can_be_awesome")

        self.assertEqual(apples.count(), 0)

    def test_multiple_models_different_permission(self):
        apple = Apple(name="test")
        apple.save()

        orange = Orange(name="test")
        orange.save()

        self.user.assign_perm("tests.can_eat", orange)

        apples = get_objs_for_user(self.user, "tests.can_eat")

        self.assertEqual(apples.count(), 0)
