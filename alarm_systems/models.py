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
    description = models.TextField(blank=True, null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)


class System(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    date_installed = models.DateField(auto_now_add=True)
    last_check = models.DateTimeField(auto_now=True)
    system_type = models.ForeignKey('SystemType', on_delete=models.CASCADE)


class SystemType(models.Model):
    name = models.CharField(max_length=100)


class Camera(models.Model):
    location_types = [(1, 'Zewnętrzna'),
                      (2, 'Wewnętrzna')]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    placement = models.IntegerField(choices=location_types, default=1)
    description = models.TextField(blank=True, null=True)
    registrator = models.ForeignKey('Registrator', on_delete=models.CASCADE)


class Registrator(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    system_types = models.ForeignKey('System', on_delete=models.CASCADE)


class MotionSensor(models.Model):
    location_types = [(1, 'Zewnętrzny'),
                      (2, 'Wewnętrzny')]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    placement = models.IntegerField(choices=location_types, default=1)
    description = models.TextField(blank=True, null=True)
    central = models.ForeignKey('Central', on_delete=models.CASCADE)


class Central(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    system_types = models.ForeignKey('System', on_delete=models.CASCADE)
