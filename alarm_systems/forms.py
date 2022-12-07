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


class EditCustomerFirstNameForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('first_name',)


class EditCustomerLastNameForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('last_name',)


class EditCustomerAddressForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('address',)


class EditCustomerEmailForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('email',)


class EditCustomerPhoneNumberForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('phone_number',)


class EditCustomerDescriptionForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ('description',)
