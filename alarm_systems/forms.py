from django import forms
from . import models


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('first_name', 'last_name', 'address', 'email', 'phone_number', 'description')
