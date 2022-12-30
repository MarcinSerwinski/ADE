from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from config.settings import EMAIL_HOST_USER
from . import forms
from alarm_systems.models import *


def home(request):
    return render(request, 'home/home.html')


class MainView(LoginRequiredMixin, View):
    """
    This view generates a list of customers. Permission and login are required.
    """

    def get(self, request):
        customers_all = Customer.objects.filter(user_id=request.user)
        return render(
            request,
            'home/customer_main_page/alarm_systems_main_view.html',
            context={
                'customers_all': customers_all
            })


@login_required()
def add_customer_view(request):
    """
    User is headed to form, which creates new customer. Data is saved in class Customer in alarm_systems/models.py
    Redirects to alarm_systems:main_view, when data submitted.
    """

    form = forms.AddCustomerForm(request.POST)
    user = request.user
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = user
            form.save()
            return redirect('alarm_systems:main_view')

    return render(request,
                  'home/customer_main_page/add_customer.html',
                  context={'form': form})


@login_required()
def delete_customer_view(request, customer_id):
    """
    Firstly, User will be directed to a view with warning message. Data about customer will be deleted if Yes option
    will be chosen. No option will redirect User to alarm_systems:main_view.
    """
    form = forms.DeleteCustomerForm(request.POST)
    customer_to_be_deleted = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'GET':
        return render(
            request,
            'home/customer_main_page/delete_customer_warning.html',
            context={
                'customer_to_be_deleted': customer_to_be_deleted,
                'form': form})
    else:
        customer_to_be_deleted.delete()

    return redirect('alarm_systems:main_view')


class CustomerEditView(LoginRequiredMixin, UpdateView):
    """
    Form to edit customer's data. Redirect to alarm_systems:main_view, when form is submitted.
    """
    model = Customer
    fields = ['first_name', 'last_name', 'address', 'email', 'phone_number', 'description']
    template_name = 'home/customer_main_page/customer_update_form.html'

    def get_success_url(self):
        return reverse_lazy('alarm_systems:main_view')


@login_required()
def details_customer(request, customer_id):
    """
    View directs User to details about dedicated customer.
    """
    locations = Location.objects.filter(customer_id=customer_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(
        request,
        'home/customer_details/customer_details_main_page.html',
        context={
            'locations': locations,
            'customer': customer})


@login_required()
def add_location(request, customer_id):
    """
    Form to add new location for customer. Data is saved in class Location in alarm_systems/models.py
    Redirects to alarm_systems:main_view, when form submitted.
    """
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


@login_required()
def delete_location(request, location_id):
    """
    View is removing location and every child of it. Uses delete button in template.
    """
    if request.method == 'GET':
        location_to_be_deleted = Location.objects.get(pk=location_id)
        location_to_be_deleted.delete()
        return redirect('alarm_systems:main_view')


class LocationEditView(LoginRequiredMixin, UpdateView):
    """
    Form to edit dedicated fields of location.
    """
    model = Location
    fields = ['name', 'address', 'description']
    template_name = 'home/customer_main_page/location_update_form.html'

    def get_success_url(self):
        customer_id = self.object.customer.id
        return reverse_lazy('alarm_systems:details_customer', kwargs={'customer_id': customer_id})


@login_required()
def location_details(request, location_id):
    """
    View directs User to systems list in specific location.
    """
    systems = System.objects.filter(location_id=location_id)
    locations = Location.objects.filter(pk=location_id)

    return render(
        request,
        'home/location_details/location_details_main_page.html',
        context={
            'systems': systems,
            'locations': locations})


@login_required()
def add_system_for_location(request, location_id):
    """
    Two forms are used to create new system for location. Forms are using class System and class SystemType from
    alarm_systems.models.py. System and SystemType are connected by many-to-one relation. Have to create field "name"
    in class SystemType in prior to populate System.system_type_id with SystemType.id.
    """
    system_form = forms.AddSystemForm(request.POST)
    system_type_form = forms.AddSystemTypeForm(request.POST)
    if request.method == 'POST':
        if system_type_form.is_valid():
            if system_type_form.save():
                system_form.instance.location_id = location_id
                latest_created_system_type = SystemType.objects.latest('pk')
                system_form.instance.system_type_id = latest_created_system_type.id
                system_form.save()

            return redirect('alarm_systems:location_details', location_id)

    return render(request,
                  'home/location_details/add_system_for_location.html',

                  context={
                      'system_form': system_form,
                      'system_type_form': system_type_form})


@login_required()
def system_name_edit_view(request, system_id):
    """
    Form to edit name field of SystemType. Need to collect SystemType.name based on System.id.
    Class System and class SystemType are from alarm_systems.models.py.
    System and SystemType are connected by many-to-one relation.
    """
    form = forms.EditSystemNameForm(request.POST)
    systems = System.objects.filter(pk=system_id)
    if request.method == 'POST':
        if form.is_valid():
            for system in systems:
                system_type_pk = system.system_type_id
                selected_systemtype = SystemType.objects.get(pk=system_type_pk)
                location_id = system.location_id
                selected_systemtype.name = form.cleaned_data['name']
                selected_systemtype.save()
                return redirect('alarm_systems:location_details', location_id)

    return render(request,
                  'home/system_details/system_update_form.html',

                  context={
                      'form': form,
                      'systems': systems})


@login_required()
def delete_system(request, system_id):
    """
    Deleting of chosen system. Need to collect SystemType.id based on System.id.
    Class System and class SystemType are from alarm_systems.models.py.
    System and SystemType are connected by many-to-one relation.
    """
    if request.method == 'GET':
        system_to_be_deleted = System.objects.get(pk=system_id)
        system_type = system_to_be_deleted.system_type.id
        system_type_to_be_deleted = SystemType.objects.get(pk=system_type)
        location_id = system_to_be_deleted.location.id
        customer = Location.objects.get(pk=location_id)
        customer_id = customer.customer_id
        system_type_to_be_deleted.delete()
        system_to_be_deleted.delete()
        return redirect('alarm_systems:details_customer', customer_id)


@login_required()
def details_system(request, system_id):
    """
    View presents details of chosen system. Also gives user a possibility to add registrator and cameras to it or
    centrals along with motion sensors. User is redirected to  'alarm_systems:empty_system' view, if there are no
    records ( no registrators or centrals ).
    """

    systems = System.objects.filter(pk=system_id)
    registrators = Registrator.objects.filter(system_types_id=system_id)
    centrals = Central.objects.filter(system_types_id=system_id)
    if registrators:
        cameras = []
        for registrator in registrators:
            cameras.extend(Camera.objects.filter(registrator_id=registrator))

        return render(request,
                      'home/system_details/details_system.html',
                      context={'registrators': registrators,
                               'cameras': cameras,
                               'systems': systems})
    elif centrals:
        motionsensors = []
        for central in centrals:
            motionsensors.extend(MotionSensor.objects.filter(central_id=central))

        return render(request,
                      'home/system_details/details_system.html',
                      context={'motionsensors': motionsensors,
                               'centrals': centrals,
                               'systems': systems})
    else:
        return redirect('alarm_systems:empty_system', system_id)


@login_required()
def add_registrator(request, system_id):
    """
    Form allows to add a new registrator to chosen system. Data is saved in class Registrator in alarm_systems/models.py
    """
    form = forms.AddRegistratorForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.system_types_id = system_id
            form.save()
            return redirect('alarm_systems:details_system', system_id)

    return render(request,
                  'home/system_details/add_registrator.html',

                  context={
                      'form': form})


@login_required()
def delete_registrator(request, registrator_id):
    """
    Registrator is erased from database, when button 'delete' is clicked on a website.
    """
    if request.method == 'GET':
        registrator_to_be_deleted = Registrator.objects.get(pk=registrator_id)
        system_id = registrator_to_be_deleted.system_types_id
        registrator_to_be_deleted.delete()
        return redirect('alarm_systems:details_system', system_id)


class RegistratorEditView(LoginRequiredMixin, UpdateView):
    """
    Form allows to edit fields from class Registrator in alarm_systems/models.py.
    """
    model = Registrator
    fields = ['brand', 'model', 'serial_number', 'description']
    template_name = 'home/system_details/registrator_update_form.html'

    def get_success_url(self):
        system_id = self.object.system_types.id
        return reverse_lazy('alarm_systems:details_system', kwargs={'system_id': system_id})


@login_required()
def add_camera(request, system_id):
    """
    Form allows to add a new camera to chosen system. Data is saved in class Camera in alarm_systems/models.py
    """
    form = forms.AddCameraForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('alarm_systems:details_system', system_id)

    return render(request,
                  'home/system_details/add_camera.html',
                  context={
                      'form': form})


@login_required()
def delete_camera(request, camera_id):
    """
    Camera is erased from database, when button 'delete' is clicked on a website.
    """
    if request.method == 'GET':
        camera_to_be_deleted = Camera.objects.get(pk=camera_id)
        registrator = camera_to_be_deleted.registrator_id
        registrator_id = Registrator.objects.get(pk=registrator)
        system_id = registrator_id.system_types_id
        camera_to_be_deleted.delete()
        return redirect('alarm_systems:details_system', system_id)


class CameraEditView(LoginRequiredMixin, UpdateView):
    """
        Form allows to edit fields from class Camera in alarm_systems/models.py.
    """
    model = Camera
    fields = ['brand', 'model', 'serial_number', 'description', 'placement']
    template_name = 'home/system_details/camera_update_form.html'

    def get_success_url(self):
        registrator_id = self.object.registrator.id
        system = Registrator.objects.get(pk=registrator_id)
        system_id = system.system_types_id
        return reverse_lazy('alarm_systems:details_system', kwargs={'system_id': system_id})


@login_required()
def add_central(request, system_id):
    """
    Form allows to add a new central to chosen system. Data is saved in class Central in alarm_systems/models.py
    """
    form = forms.AddCentralForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.system_types_id = system_id
            form.save()
            return redirect('alarm_systems:details_system', system_id)

    return render(request,
                  'home/system_details/add_central.html',

                  context={
                      'form': form})


@login_required()
def delete_central(request, central_id):
    """
    Registrator is erased from database, when button 'delete' is clicked on a website.
    """
    if request.method == 'GET':
        central_to_be_deleted = Central.objects.get(pk=central_id)
        system_id = central_to_be_deleted.system_types_id
        central_to_be_deleted.delete()
        return redirect('alarm_systems:details_system', system_id)


class CentralEditView(LoginRequiredMixin, UpdateView):
    """
    Form allows to edit fields from class Central in alarm_systems/models.py.
    """
    model = Central
    fields = ['brand', 'model', 'serial_number', 'description']
    template_name = 'home/system_details/central_update_form.html'

    def get_success_url(self):
        system_id = self.object.system_types.id
        return reverse_lazy('alarm_systems:details_system', kwargs={'system_id': system_id})


@login_required()
def add_motionsensor(request, system_id):
    """
     Form allows to add a new motion sensor to chosen system. Data is saved in class MotionSensor
     in alarm_systems/models.py
    """
    form = forms.AddMotionSensorForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('alarm_systems:details_system', system_id)

    return render(request,
                  'home/system_details/add_motionsensor.html',
                  context={
                      'form': form})


@login_required()
def delete_motionsensor(request, motionsensor_id):
    """
    Motionsensor is erased from database, when button 'delete' is clicked on a website.
    """
    if request.method == 'GET':
        motionsensor_to_be_deleted = MotionSensor.objects.get(pk=motionsensor_id)
        central = motionsensor_to_be_deleted.central_id
        central_id = Central.objects.get(pk=central)
        system_id = central_id.system_types_id
        motionsensor_to_be_deleted.delete()
        return redirect('alarm_systems:details_system', system_id)


class MotionsensorEditView(LoginRequiredMixin, UpdateView):
    """
    Form allows to edit fields from class MotionSensor in alarm_systems/models.py.
    """
    model = MotionSensor
    fields = ['brand', 'model', 'serial_number', 'description', 'placement']
    template_name = 'home/system_details/motionsensor_update_form.html'

    def get_success_url(self):
        central_id = self.object.central.id

        system = Central.objects.get(pk=central_id)
        system_id = system.system_types_id
        return reverse_lazy('alarm_systems:details_system', kwargs={'system_id': system_id})


@login_required()
def empty_system(request, system_id):
    """
    Gives User an option to create either video surveillance or alarm system types, if there's none in the system.
    """
    systems = System.objects.filter(pk=system_id)

    return render(request,
                  'home/system_details/add_new_systemtype_for_empty_system.html',
                  context={
                      'systems': systems,
                  })


@permission_required('alarm_systems.add_camera')
def email_sending(request, customer_id):
    """
    Can send email to chosen customer. Django Email system is used. See config.settings.py.
    """
    email = forms.Email(request.POST)
    customer_email = (Customer.objects.get(pk=customer_id)).email
    if request.method == 'POST':
        email_subject = request.POST['email_subject']
        email_message = request.POST['email_message']
        recipient = customer_email
        send_mail(email_subject, email_message, EMAIL_HOST_USER, [recipient], fail_silently=False)
        return redirect('alarm_systems:main_view')
    return render(request, 'home/email-page.html', {"email": email})
