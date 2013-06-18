def assign_perm(user, permission, obj=None):
    """
    Assign a permission to a user
    """

    from olp.models import ObjectPermission

    # Check if the given permission is a Permission object
    # If the permission is given as a string, get the corresponding Permission object

    if not hasattr(permission, "pk"):
        permission = _get_perm_for_codename(permission)

        if permission is None:
            return False

    if obj:
        permission = ObjectPermission(base_object=user, target_object=obj, permission=permission)
        permission.save()
    else:
        user.user_permissions.add(permission)

    return True


def remove_perm(user, permission, obj=None):
    """
    Remove a permission from a user
    """

    from olp.models import ObjectPermission

    if not hasattr(permission, "pk"):
        permission = _get_perm_for_codename(permission)

        if permission is None:
            return False

    if obj:
        permission = ObjectPermission.objects.for_base(user).for_target(obj).for_permission(permission)

        if permission.count():
            permission.delete()
    else:
        user.user_permissions.remove(permission)

    return True


def patch_user():
    from django.contrib.auth.models import User

    setattr(User, "assign_perm", assign_perm)
    setattr(User, "remove_perm", remove_perm)


def _get_perm_for_codename(permission_codename):
    from django.contrib.auth.models import Permission

    app_label, codename = permission_codename.split(".")

    permissions = Permission.objects.filter(codename=codename)

    try:
        if len(permissions) != 1:
            permission = permissions.get(content_type__app_label=app_label)
        else:
            permission = permissions[0]

        return permission
    except Permission.DoesNotExist:
        return None
