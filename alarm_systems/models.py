from django.db import models


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=80, null=True)
    phone_number = models.CharField(max_length=24, unique=True)
    description = models.TextField(null=True)
    date_joined = models.DateField(auto_now_add=True)


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField(null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)


class System(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    date_installed = models.DateField(auto_now_add=True)
    last_check = models.DateTimeField(auto_now=True)


class SystemType(models.Model):
    name = models.CharField(max_length=100)


class Camera(models.Model):
    location_types = [(1, 'Zewnętrzna'),
                      (2, 'Wewnętrzna')]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    placement = models.IntegerField(choices=location_types, default=1)
    description = models.TextField()
    system_types = models.ManyToManyField('SystemType')
    registrator = models.ForeignKey('Registrator', on_delete=models.CASCADE)


class Registrator(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    system_types = models.ManyToManyField('SystemType')

class MotionSensor(models.Model):
    location_types = [(1, 'Zewnętrzny'),
                      (2, 'Wewnętrzny')]

    name = models.CharField(max_length=100)
    placement = models.IntegerField(choices=location_types, default=1)
    description = models.TextField()
    system_types = models.ManyToManyField('SystemType')
    central = models.ForeignKey('Central', on_delete=models.CASCADE)


class Central(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    system_types = models.ManyToManyField('SystemType')
