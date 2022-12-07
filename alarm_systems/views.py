from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from . import forms
from alarm_systems.models import Customer


# Create your views here.


def home(request):
    return render(request, 'home/home.html')


class MainView(PermissionRequiredMixin, View):
    permission_required = 'users.add_choice'

    def get(self, request):
        customers_all = Customer.objects.all().order_by('last_name')
        return render(
            request,
            'home/alarm_systems_main_view.html',
            context={
                'customers_all': customers_all
            })


def add_customer_view(request):
    form = forms.AddCustomerForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('alarm_systems:main_view')

    return render(request,
                  'home/add_customer.html',
                  context={'form': form})


def delete_customer_view(request, customer_id):
    form = forms.DeleteCustomerForm(request.POST)
    customer_to_be_deleted = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'GET':
        return render(
            request,
            'home/delete_customer_warning.html',
            context={
                'customer_to_be_deleted': customer_to_be_deleted,
                'form': form})
    else:
        customer_to_be_deleted.delete()

    return redirect('alarm_systems:main_view')


def edit_customer_view(request, customer_id):
    customer_to_be_edited = get_object_or_404(Customer, pk=customer_id)
    form = forms.EditCustomerForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            customer_to_be_edited.first_name = form.cleaned_data['first_name']
            customer_to_be_edited.last_name = form.cleaned_data['last_name']
            customer_to_be_edited.address = form.cleaned_data['address']
            customer_to_be_edited.email = form.cleaned_data['email']
            customer_to_be_edited.phone_number = form.cleaned_data['phone_number']
            customer_to_be_edited.description = form.cleaned_data['description']
            customer_to_be_edited.save()
            return redirect('alarm_systems:main_view')

    return render(
        request,
        'home/edit_customer.html',
        context={
            'customer_to_be_edited': customer_to_be_edited,
            'form': form})
