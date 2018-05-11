from django.test import TestCase


class TestMiddleware(TestCase):

    def test_auto_patches(self):
        from django.contrib.auth.models import User
        from django.utils.encoding import force_text
        from olp.utils import assign_perm

        response = self.client.get('/test')

        self.assertEqual(force_text(response.content), 'ok')

        self.assertIs(getattr(User.assign_perm, "__func__", User.assign_perm), assign_perm)