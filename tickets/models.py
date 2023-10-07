from django.db import models

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.


class Opera(models.Model):
    hall = models.CharField(max_length=10)
    opera = models.CharField(max_length=10)
    

    def __str__(self):
        return self.opera



class Guest (models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservation', on_delete=models.CASCADE)
    opera = models.ForeignKey(Opera, related_name='reservation', on_delete=models.CASCADE)
    date = models.DateTimeField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.opera.opera

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)