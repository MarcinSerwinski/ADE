from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from . import forms
from alarm_systems.models import Customer, Location


def home(request):
    return render(request, 'home/home.html')


class MainView(PermissionRequiredMixin, LoginRequiredMixin, View):
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


def edit_customer_all_view(request, customer_id):
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
        'home/customer_edit/edit_customer_all.html',
        context={
            'customer_to_be_edited': customer_to_be_edited,
            'form': form})


def edit_customer_first_name(request, customer_id):
    customer_to_be_edited = get_object_or_404(Customer, pk=customer_id)
    form = forms.EditCustomerFirstNameForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            customer_to_be_edited.first_name = form.cleaned_data['first_name']
            customer_to_be_edited.save()
            return redirect('alarm_systems:main_view')

    return render(
        request,
        'home/customer_edit/edit_customer_first_name.html',
        context={
            'customer_to_be_edited': customer_to_be_edited,
            'form': form})


def edit_customer_last_name(request, customer_id):
    customer_to_be_edited = get_object_or_404(Customer, pk=customer_id)
    form = forms.EditCustomerLastNameForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            customer_to_be_edited.last_name = form.cleaned_data['last_name']
            customer_to_be_edited.save()
            return redirect('alarm_systems:main_view')

    return render(
        request,
        'home/customer_edit/edit_customer_last_name.html',
        context={
            'customer_to_be_edited': customer_to_be_edited,
            'form': form})


def edit_customer_address(request, customer_id):
    customer_to_be_edited = get_object_or_404(Customer, pk=customer_id)
    form = forms.EditCustomerAddressForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            customer_to_be_edited.address = form.cleaned_data['address']
            customer_to_be_edited.save()
            return redirect('alarm_systems:main_view')

    return render(
        request,
        'home/customer_edit/edit_customer_address.html',
        context={
            'customer_to_be_edited': customer_to_be_edited,
            'form': form})


def edit_customer_email(request, customer_id):
    customer_to_be_edited = get_object_or_404(Customer, pk=customer_id)
    form = forms.EditCustomerEmailForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            customer_to_be_edited.email = form.cleaned_data['email']
            customer_to_be_edited.save()
            return redirect('alarm_systems:main_view')

    return render(
        request,
        'home/customer_edit/edit_customer_email.html',
        context={
            'customer_to_be_edited': customer_to_be_edited,
            'form': form})


def edit_customer_phone_number(request, customer_id):
    customer_to_be_edited = get_object_or_404(Customer, pk=customer_id)
    form = forms.EditCustomerPhoneNumberForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            customer_to_be_edited.phone_number = form.cleaned_data['phone_number']
            customer_to_be_edited.save()
            return redirect('alarm_systems:main_view')

    return render(
        request,
        'home/customer_edit/edit_customer_phone_number.html',
        context={
            'customer_to_be_edited': customer_to_be_edited,
            'form': form})


def edit_customer_description(request, customer_id):
    customer_to_be_edited = get_object_or_404(Customer, pk=customer_id)
    form = forms.EditCustomerDescriptionForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            customer_to_be_edited.description = form.cleaned_data['description']
            customer_to_be_edited.save()
            return redirect('alarm_systems:main_view')

    return render(
        request,
        'home/customer_edit/edit_customer_description.html',
        context={
            'customer_to_be_edited': customer_to_be_edited,
            'form': form})


def details_customer(request, customer_id):
    locations = Location.objects.filter(customer_id=customer_id).order_by('name')
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(
        request,
        'home/customer_details/customer_details_main_page.html',
        context={
            'locations': locations,
            'customer': customer})


def add_location_view(request, customer_id):
    form = forms.AddLocationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.customer_id = customer_id
            form.save()
            return redirect('alarm_systems:details_customer', customer_id)

    return render(request,
                  'home/customer_details/add_location_customer.html',

                  context={
                      'form': form})
