from django.test import TestCase
from olp.backends import PermissionBackend


class TestBackend(TestCase):

    def test_no_authenticate(self):
        backend = PermissionBackend()

        result = backend.authenticate()

        self.assertEqual(result, None)

    def test_get_user(self):
        backend = PermissionBackend()

        result = backend.get_user()

        self.assertEqual(result, None)
