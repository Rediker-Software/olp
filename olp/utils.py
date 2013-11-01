def assign_perm(user, permission, obj=None):
    """
    Assign a permission to a user, optionally tie it to an object.

    This assigns both the standard Django permissions, and the custom
    object-level permissions.
    """

    from olp.models import ObjectPermission

    # Check if the given permission is a Permission object
    # If the permission is given as a string, get the corresponding
    # Permission object

    if not hasattr(permission, "pk"):
        permission = _get_perm_for_codename(permission)

        if permission is None:
            return False

    if obj:
        permission = ObjectPermission(base_object=user, target_object=obj,
                                      permission=permission)
        permission.save()
    else:
        user.user_permissions.add(permission)

    return True


def has_perm(base, permission, target=None):
    """
    Determines if a base object has a permission on a target object.
    """

    from olp.models import ObjectPermission

    if not hasattr(permission, "pk"):
        permission = _get_perm_for_codename(permission)

        if permission is None:
            return False

    objs = ObjectPermission.objects.for_base(base)

    if target is not None:
        objs = objs.for_target(target)

    perms_list = objs.select_related("permission__content_type",
        "permission").values_list("permission__content_type__app_label",
                                  "permission__codename")

    permissions = set(["%s.%s" % (perm[0], perm[1]) for perm in perms_list])

    permission_codename = "%s.%s" % (permission.content_type.app_label,
                                     permission.codename)

    return permission_codename  in permissions


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
        permission = ObjectPermission.objects.for_base(user).for_target(obj) \
            .for_permission(permission)

        if permission.count():
            permission.delete()
    else:
        user.user_permissions.remove(permission)

    return True


def patch_models():
    """
    Add three possible methods to Django models in order to make them
    compatible with the object-level permissions.

    The Django User and Group models will only get the `assign_perm` and
    `remove_perm` methods, as they already have a `has_perm` method.  Other
    models which are listed in the `models` key of the settings will get the
    `assign_perm`, `remove_perm`, and `has_perm` methods.
    """

    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()
    except ImportError:
        from django.contrib.auth.models import User

    from django.conf import settings

    setattr(User, "assign_perm", assign_perm)
    setattr(User, "remove_perm", remove_perm)

    model_dict = settings.OLP_SETTINGS.get("models")

    for model_path, filter_path in model_dict:
        import_path = ".".join(model_path.split(".")[:-1])
        model_name = model_path.split(".")[-1]

        model_module = __import__(import_path, {}, {}, str(model_name[-1]))
        model = getattr(model_module, model_name)

        setattr(model, "assign_perm", assign_perm)
        setattr(model, "remove_perm", remove_perm)

        if not hasattr(model, "has_perm"):
            setattr(model, "has_perm", has_perm)


def get_objs_for_user(user, permission, model_class=None):
    """
    Gets the objects that a user has a specific permission on.
    """
    
    from django.conf import settings
    from .models import ObjectPermission
    
    if not hasattr(permission, "pk"):
        permission = _get_perm_for_codename(permission)
        
        if permission is None:
            return set()


    if model_class:
        final_model = model_class
    else:
        ct = permission.content_type
        final_model = ct.model_class()

    objs = final_model.objects.none()
    
    model_dict = settings.OLP_SETTINGS.get("models")
        
    for model_path, filter_path in model_dict:
        model_objs = _get_model_objs_for_user(user, model_path, filter_path)
        model = model_objs.model
        
        perms = ObjectPermission.objects.for_base_ids(model_objs) \
                .for_base_model(model).for_target_model(final_model) \
                .for_permission(permission)
        
        obj_ids = perms.values_list("target_object_id", flat=True)
        
        path_objs = final_model.objects.filter(id__in=obj_ids)
        
        objs = objs | path_objs
    
    user_perms = ObjectPermission.objects.for_base(user) \
        .for_target_model(final_model).for_permission(permission)
    user_obj_ids = user_perms.values_list("target_object_id", flat=True)
    
    user_objs = final_model.objects.filter(id__in=user_obj_ids)
    
    objs = objs | user_objs
        
    return objs


def _get_model_objs_for_user(user, model_path, filter_path):
    import_path = ".".join(model_path.split(".")[:-1])
    model_name = model_path.split(".")[-1]
    
    model_module = __import__(import_path, {}, {}, str(model_name))
    model = getattr(model_module, model_name)
    
    model_objs = model.objects.filter(**{filter_path: user})
    
    return model_objs


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
