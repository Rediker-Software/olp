from .models import ObjectPermission


class PermissionBackend(object):

    def authenticate(self):
        return None

    def get_all_permissions(self, user, obj=None):
        if user.is_anonymous():
            return set()

        objs = ObjectPermission.objects.for_base(user)

        if obj is not None:
            objs = objs.for_target(obj)

        perms_list = objs.select_related("permission__content_type", "permission")\
            .values_list("permission__content_type__app_label", "permission__codename")

        group_permissions = self.get_group_permissions(user, obj)

        permissions = set(["%s.%s" % (perm[0], perm[1]) for perm in perms_list])
        permissions.update(group_permissions)

        return permissions

    def get_group_permissions(self, user, obj=None):
        from django.conf import settings

        if user.is_anonymous():
            return set()

        objs = ObjectPermission.objects.none()

        model_dict = settings.OLP_SETTINGS.get("models")

        for model_path, filter_path in model_dict:
            import_path = ".".join(model_path.split(".")[:-1])
            model_name = model_path.split(".")[-1]

            model_module = __import__(import_path, {}, {}, str(model_name[-1]))
            model = getattr(model_module, model_name)

            model_objs = model.objects.filter(**{filter_path: user})

            objs = objs | ObjectPermission.objects.for_base_id(model_objs).for_base_model(model)

        perms_list = objs.select_related("permission__content_type", "permission")\
            .values_list("permission__content_type__app_label", "permission__codename")

        return set(["%s.%s" % (perm[0], perm[1]) for perm in perms_list])

    def get_user(self):
        return None

    def has_perm(self, user, perm, obj=None):
        if not user.is_active:
            return False

        return perm in self.get_all_permissions(user, obj)
