from django.db import models


class Apple(models.Model):

    name = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ("can_be_awesome", "Can be an awesome to the apple"),
            ("can_eat", "Can eat the apple"),
        )

class Orange(models.Model):

    name = models.CharField(max_length=50)


