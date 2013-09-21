Object-level permissions (OLP)
==============================
Django has supported object-level permissions since Django 1.2, but it
requires a custom authentication backend to implement it.  There are
`tons of implementations <https://www.djangopackages.com/grids/g/perms/>`_
out there, but most of them are meant to handle specific situations.

Features
========
Like most other implementations, OLP is meant to handle a few specific cases
which we encountered.

Different types of "groups"
---------------------------
Django has a concept of "users" and "groups" which the authentication system
is built upon.  These groups only consist of a single model and cannot be
built upon to have different, distinct types.  OLP allows you to have multiple
models contribute to an individual user's permissions, even on the object
level.

The different models can have independent permissions, and do not need to be
directly attached to a user.  If they are attached to a user (and specified
in the settings), they can contribute to a user's overall permissions.

Direct integration
------------------
OLP is directly integrated with Django's authentication backends.  While it
is not required to use OLP, it is recommended as it makes it easier to use
OLP.

Normalization of methods
------------------------
Only the user and groups models have `has_perm` functions, and that becomes a
quick limitation when working with other models.  OLP patches the other
models (as specified in the settings) and gives them ``has_perm`` methods
which act the same way as the ones given to users and groups.

In order to make assigning and removing permissions as easy as checking them,
OLP will also patch all of the models with ``assign_perm`` and ``remove_perm``
methods.

Settings
========
OLP determines the settings from the Django settings file using the key
``OLP_SETTINGS``.  This must be a dictionary which contains the key ``models``,
as shown below.

.. code :: python

   OLP_SETTINGS = {
       "models": (
       ),
   }

The ``models`` key should contain a tuple of tuples containing the string path
to the model and the queryset filter used to filter by a user.

Example
=======
example/settings.py

.. code :: python

   OLP_SETTINGS = {
       "models": (
           ("django.contrib.auth.models.Group", "users"),
       ),
   }

example/models.py

.. code :: python

   from django.db import models

   class Apple(models.Model):
       owner = models.ForeignKey("auth.User")

       class Meta:
           permissions = (
               ("can_see_apple", "User can see the apple."),
           )

python shell

.. code :: python

   >>> from olp.utils import patch_models
   >>> patch_models()
   >>> from example.models import Apple
   >>> from django.contrib.auth import Group, User
   >>> user = User.objects.all()[0]
   >>> group = Group.objects.all()[0]
   >>> apple = Apple(owner=user)
   >>> apple.save()
   >>> user.has_perm("example.can_see_apple", apple)
   False
   >>> user.assign_perm("can_see_apple", apple)
   True
   >>> user.has_perm("example.can_see_apple", apple)
   True
   >>> user.remove_perm("example.can_see_apple", apple)
   True
   >>> user.has_perm("example.can_see_apple", apple)
   False
   >>> group.has_perm("example.can_see_apple", apple)
   False
   >>> group.assign_perm("example.can_see_apple", apple)
   True
   >>> group.has_perm("example.can_see_apple", apple)
   True
   >>> user.has_perm("example.can_see_apple", apple)
   True
