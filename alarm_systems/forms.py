from django import forms
from . import models


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('first_name', 'last_name', 'address', 'email', 'phone_number', 'description')


class DeleteCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ()


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('first_name', 'last_name', 'address', 'email', 'phone_number', 'description')


class AddLocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        fields = ('name', 'address', 'description')


class EditLocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        fields = ('name', 'address', 'description')


class AddSystemForm(forms.ModelForm):
    class Meta:
        model = models.System
        fields = ()


class AddSystemTypeForm(forms.ModelForm):
    class Meta:
        model = models.SystemType
        fields = ('name',)


class EditSystemNameForm(forms.ModelForm):
    class Meta:
        model = models.SystemType
        fields = ('name',)


class AddRegistratorForm(forms.ModelForm):
    class Meta:
        model = models.Registrator
        fields = ('brand', 'model', 'serial_number', 'description')


class AddCameraForm(forms.ModelForm):
    class Meta:
        model = models.Camera
        fields = ('brand', 'model', 'serial_number', 'placement', 'description', 'registrator')


class AddCentralForm(forms.ModelForm):
    class Meta:
        model = models.Central
        fields = ('brand', 'model', 'serial_number', 'description')


class AddMotionSensorForm(forms.ModelForm):
    class Meta:
        model = models.MotionSensor
        fields = ('brand', 'model', 'serial_number', 'placement', 'description', 'central')
