from django.db import models


class Apple(models.Model):
    
    name = models.CharField(max_length=50)
