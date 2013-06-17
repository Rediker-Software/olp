def assign_perm(self, permission, obj=None):
    pass


def patch_user():
    from django.contrib.auth.models import User

    setattr(User, "assign_perm", assign_perm)
