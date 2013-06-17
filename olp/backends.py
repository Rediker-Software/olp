class PermissionBackend(object):

    def authenticate(self):
        return None

    def get_all_permissions(self, user, obj=None):
        return set()

    def get_group_permissions(self, user, obj=None):
        return set()

    def get_user(self):
        return None
