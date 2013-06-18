from .models import ObjectPermission


class PermissionBackend(object):

    def authenticate(self):
        return None

    def get_all_permissions(self, user, obj=None):
        if user.is_anonymous():
            return ()

        group_permissions = self.get_group_permissions(user, obj)

        permissions = ()
        permissions += group_permissions

        return permissions

    def get_group_permissions(self, user, obj=None):
        if user.is_anonymous():
            return ()

        return ()

    def get_user(self):
        return None
