from .models import ObjectPermission


class PermissionBackend(object):

    def authenticate(self):
        return None

    def get_all_permissions(self, user, obj=None):
        if user.is_anonymous():
            return set()

        objs = ObjectPermission.objects.for_base(user)

        perms_list = objs.select_related("permission__content_type", "permission")\
            .values_list("permission__content_type__app_label", "permission__codename")

        group_permissions = self.get_group_permissions(user, obj)

        permissions = set(["%s.%s" % (perm[0], perm[1]) for perm in perms_list])
        permissions.update(group_permissions)

        return permissions

    def get_group_permissions(self, user, obj=None):
        if user.is_anonymous():
            return set()

        return set()

    def get_user(self):
        return None

    def has_perm(self, user, perm, obj=None):
        if not user.is_active:
            return False

        return perm in self.get_all_permissions(user, obj)
