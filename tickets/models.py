from django.db import models

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
