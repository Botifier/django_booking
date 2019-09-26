import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)


class Property(models.Model):
    property_name = models.CharField(max_length=256)
    property_id = models.CharField(max_length=64)
    city = models.CharField(max_length=256)


class Booking(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
