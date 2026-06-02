from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

class AuditLog(models.Model):
    message = models.CharField(max_length=200)