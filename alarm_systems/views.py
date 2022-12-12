from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from config.settings import EMAIL_HOST_USER
from . import forms
from alarm_systems.models import Customer, Location, System, SystemType, Camera, Registrator, Central, MotionSensor


def home(request):
    return render(request, 'home/home.html')


class MainView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'users.add_choice'

    def get(self, request):
        customers_all = Customer.objects.all().order_by('last_name')
        return render(
            request,
            'home/customer_main_page/alarm_systems_main_view.html',
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
                  'home/customer_main_page/add_customer.html',
                  context={'form': form})


def delete_customer_view(request, customer_id):
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


class CustomerEditView(UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'address', 'email', 'phone_number', 'description']
    template_name = 'home/customer_main_page/customer_update_form.html'

    def get_success_url(self):
        return reverse_lazy('alarm_systems:main_view')


def details_customer(request, customer_id):
    locations = Location.objects.filter(customer_id=customer_id).order_by('name')
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(
        request,
        'home/customer_details/customer_details_main_page.html',
        context={
            'locations': locations,
            'customer': customer})


def add_location(request, customer_id):
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


def delete_location(request, location_id):
    if request.method == 'GET':
        location_to_be_deleted = Location.objects.get(pk=location_id)
        location_to_be_deleted.delete()
        return redirect('alarm_systems:main_view')


class LocationEditView(UpdateView):
    model = Location
    fields = ['name', 'address', 'description']
    template_name = 'home/customer_main_page/location_update_form.html'

    def get_success_url(self):
        customer_id = self.object.customer.id
        return reverse_lazy('alarm_systems:details_customer', kwargs={'customer_id': customer_id})


def location_details(request, location_id):
    systems = System.objects.filter(location_id=location_id)
    locations = Location.objects.filter(pk=location_id)

    return render(
        request,
        'home/location_details/location_details_main_page.html',
        context={
            'systems': systems,
            'locations': locations})


def add_system_for_location(request, location_id):
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


def delete_system(request, system_id):
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


def system_name_edit_view(request, system_id):
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


def details_system(request, system_id):
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


def add_registrator(request, system_id):
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


def delete_registrator(request, registrator_id):
    if request.method == 'GET':
        registrator_to_be_deleted = Registrator.objects.get(pk=registrator_id)
        system_id = registrator_to_be_deleted.system_types_id
        registrator_to_be_deleted.delete()
        return redirect('alarm_systems:details_system', system_id)


class RegistratorEditView(UpdateView):
    model = Registrator
    fields = ['brand', 'model', 'serial_number', 'description']
    template_name = 'home/system_details/registrator_update_form.html'

    def get_success_url(self):
        system_id = self.object.system_types.id
        return reverse_lazy('alarm_systems:details_system', kwargs={'system_id': system_id})


def add_camera(request, system_id):
    form = forms.AddCameraForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('alarm_systems:details_system', system_id)

    return render(request,
                  'home/system_details/add_camera.html',
                  context={
                      'form': form})


def delete_camera(request, camera_id):
    if request.method == 'GET':
        camera_to_be_deleted = Camera.objects.get(pk=camera_id)
        registrator = camera_to_be_deleted.registrator_id
        registrator_id = Registrator.objects.get(pk=registrator)
        system_id = registrator_id.system_types_id
        camera_to_be_deleted.delete()
        return redirect('alarm_systems:details_system', system_id)


class CameraEditView(UpdateView):
    model = Camera
    fields = ['brand', 'model', 'serial_number', 'description', 'placement']
    template_name = 'home/system_details/camera_update_form.html'

    def get_success_url(self):
        registrator_id = self.object.registrator.id
        print(registrator_id)
        system = Registrator.objects.get(pk=registrator_id)
        system_id = system.system_types_id
        return reverse_lazy('alarm_systems:details_system', kwargs={'system_id': system_id})


def add_central(request, system_id):
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


def delete_central(request, central_id):
    if request.method == 'GET':
        central_to_be_deleted = Central.objects.get(pk=central_id)
        system_id = central_to_be_deleted.system_types_id
        central_to_be_deleted.delete()
        return redirect('alarm_systems:details_system', system_id)


class CentralEditView(UpdateView):
    model = Central
    fields = ['brand', 'model', 'serial_number', 'description']
    template_name = 'home/system_details/central_update_form.html'

    def get_success_url(self):
        system_id = self.object.system_types.id
        return reverse_lazy('alarm_systems:details_system', kwargs={'system_id': system_id})


def add_motionsensor(request, system_id):
    form = forms.AddMotionSensorForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('alarm_systems:details_system', system_id)

    return render(request,
                  'home/system_details/add_motionsensor.html',
                  context={
                      'form': form})


def delete_motionsensor(request, motionsensor_id):
    if request.method == 'GET':
        motionsensor_to_be_deleted = MotionSensor.objects.get(pk=motionsensor_id)
        central = motionsensor_to_be_deleted.central_id
        central_id = Central.objects.get(pk=central)
        system_id = central_id.system_types_id
        motionsensor_to_be_deleted.delete()
        return redirect('alarm_systems:details_system', system_id)


class MotionsensorEditView(UpdateView):
    model = MotionSensor
    fields = ['brand', 'model', 'serial_number', 'description', 'placement']
    template_name = 'home/system_details/motionsensor_update_form.html'

    def get_success_url(self):
        central_id = self.object.central.id

        system = Central.objects.get(pk=central_id)
        system_id = system.system_types_id
        return reverse_lazy('alarm_systems:details_system', kwargs={'system_id': system_id})


def empty_system(request, system_id):
    systems = System.objects.filter(pk=system_id)
    return render(request,
                  'home/system_details/add_new_systemtype_for_empty_system.html',
                  context={
                      'systems': systems})


def email_sending(request, customer_id):
    email = forms.Email(request.POST)
    customer_email = (Customer.objects.get(pk=customer_id)).email
    if request.method == 'POST':
        email_subject = request.POST['email_subject']
        email_message = request.POST['email_message']
        recipient = customer_email
        send_mail(email_subject, email_message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        return redirect('alarm_systems:main_view')
    return render(request, 'home/email-page.html', {"email": email})
