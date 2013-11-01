from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.query import QuerySet


class ObjectPermissionManager(models.Manager):

    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)

    def get_query_set(self):
        return ObjectPermissionQuerySet(self.model)


class ObjectPermissionQuerySet(QuerySet):

    def for_base(self, obj):
        ct = ContentType.objects.get_for_model(obj)

        return self.filter(base_object_ct=ct, base_object_id=obj.id)

    def for_base_model(self, model):
        ct = ContentType.objects.get_for_model(model)

        return self.filter(base_object_ct=ct)

    def for_base_id(self, id):
        return self.filter(base_object_id=id)
    
    def for_base_ids(self, ids):
        return self.filter(base_object_id__in=ids)

    def for_permission(self, permission):
        return self.filter(permission=permission)

    def for_target(self, obj):
        ct = ContentType.objects.get_for_model(obj)

        return self.filter(target_object_ct=ct, target_object_id=obj.id)

    def for_target_model(self, model):
        ct = ContentType.objects.get_for_model(model)

        return self.filter(target_object_ct=ct)


class ObjectPermission(models.Model):
    base_object_ct = models.ForeignKey(ContentType, related_name="+")
    base_object_id = models.PositiveIntegerField()

    base_object = generic.GenericForeignKey("base_object_ct", "base_object_id")

    target_object_ct = models.ForeignKey(ContentType, related_name="+")
    target_object_id = models.PositiveIntegerField()

    target_object = generic.GenericForeignKey("target_object_ct", "target_object_id")

    permission = models.ForeignKey(Permission)

    objects = ObjectPermissionManager()
