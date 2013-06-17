def assign_perm(user, permission, obj=None):
    """
    Assign a permission to a user
    """

    from django.contrib.auth.models import Permission

    # Check if the given permission is a Permission object
    # If the permission is given as a string, get the corresponding Permission object

    if not hasattr(permission, "pk"):
        app_label, codename = permission.aplit(".")

        permissions = Permission.objects.filter(codename=codename)

        if len(permissions) != 1:
            permission = permissions.get(content_type__app_label=app_label)
        else:
            permission = permissions.get()

    if obj:
        pass
    else:
        user.user_permissions.add(permission)


def patch_user():
    from django.contrib.auth.models import User

    setattr(User, "assign_perm", assign_perm)
