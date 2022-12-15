import random

from django.contrib.auth.models import Permission

from alarm_systems.forms import *
from alarm_systems.models import *


def test_home_page_get(client):
    endpoint = reverse('alarm_systems:home')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>ADE</h1>' in str(response.content)


def test_acces_with_no_permission_to_mainview(db, client, user):
    client.force_login(user)
    endpoint = reverse('alarm_systems:main_view')
    response = client.get(endpoint)
    assert response.status_code == 403


def test_acces_with_permission_to_mainview(client, user):
    client.force_login(user)
    permission = Permission.objects.get(name='Can add camera')
    user.user_permissions.add(permission)
    endpoint = reverse('alarm_systems:main_view')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>All customers listed below:</h1>' in str(response.content)


def test_add_customer_get(client):
    endpoint = reverse('alarm_systems:add_customer')
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, AddCustomerForm)
    assert '<button type="submit" class="btn btn-success">Add new customer</button>' in str(response.content)


def test_add_customer_post(db, client):
    form_url = reverse('alarm_systems:add_customer')
    data = {'first_name': 'TestFirstName', 'last_name': 'TestLastName',
            'address': 'Test, Address 1',
            'email': 'form@test.com', 'phone_number': '123456789',
            'description': 'Test1'}
    response = client.post(form_url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:main_view'))
    assert Customer.objects.get(first_name='TestFirstName', description='Test1')


def test_delete_customer_get(db, client, customer_id, user, user_with_permission):
    client.force_login(user)
    endpoint = reverse('alarm_systems:delete_customer', kwargs={'customer_id': customer_id})
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, DeleteCustomerForm)
    assert '<button type="submit" class="btn btn-outline-danger">Yes. Delete.</button>' in str(response.content)


def test_delete_customer_post(db, client, customer_id, user, user_with_permission):
    client.force_login(user)
    form_url = reverse('alarm_systems:delete_customer', kwargs={'customer_id': customer_id})
    response = client.post(form_url)
    customer = Customer.objects.all()
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:main_view'))
    assert len(customer) == 0

def test_acces_with_no_permission_to_delete_customer(db, client, customer_id, user):
    client.force_login(user)
    endpoint = reverse('alarm_systems:delete_customer', kwargs={'customer_id': customer_id})
    response = client.get(endpoint)
    assert response.status_code == 302
    assert response.url.startswith(reverse('users:login_view'))

def test_edit_customer_get(db, client, customer_id):
    endpoint = reverse('alarm_systems:edit_customer_all_view', kwargs={'pk': customer_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<button type="submit" value="Update" class="btn btn-success">Edit</button>' in str(response.content)


def test_edit_customer_post(db, client, customer_id):
    form_url = reverse('alarm_systems:edit_customer_all_view', kwargs={'pk': customer_id})
    data = {'first_name': 'EditedFirstName', 'last_name': 'TestLastName',
            'address': 'Test, Address 1',
            'email': 'form@test.com', 'phone_number': 'edited123456789',
            'description': 'Test1'}
    response = client.post(form_url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:main_view'))
    assert Customer.objects.get(first_name='EditedFirstName', phone_number='edited123456789')


def test_details_customer_get(db, client, customer_id, user, user_with_permission):
    client.force_login(user)
    endpoint = reverse('alarm_systems:details_customer', kwargs={'customer_id': customer_id})
    response = client.get(endpoint)
    customer_in_view = response.context['customer']
    assert customer_in_view.id in response.context
    assert response.status_code == 200
    assert "<h1>Locations listed below:</h1>" in str(response.content)

def test_acces_with_no_permission_to_details_customer(db, client, customer_id, user):
    client.force_login(user)
    endpoint = reverse('alarm_systems:details_customer', kwargs={'customer_id': customer_id})
    response = client.get(endpoint)
    assert response.status_code == 302
    assert response.url.startswith(reverse('users:login_view'))

def test_add_location_get(db, client, customer_id):
    endpoint = reverse('alarm_systems:add_location_customer', kwargs={'customer_id': customer_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<button type="submit" class="btn btn-success">Add new ' in str(response.content)


def test_add_location_post(db, client, customer_id):
    form_url = reverse('alarm_systems:add_location_customer', kwargs={'customer_id': customer_id})
    data = {'name': 'TestLocationName', 'address': 'Test Location, Address 2', 'description': 'Test2'}
    response = client.post(form_url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:details_customer', kwargs={'customer_id': customer_id}))
    assert Location.objects.get(name='TestLocationName', description='Test2')


def test_delete_location_get(db, client, customer_id, location_customers_id):
    endpoint = reverse('alarm_systems:delete_location', kwargs={'location_id': location_customers_id})
    response = client.get(endpoint)
    location = Location.objects.all()
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:main_view'))
    assert len(location) == 0


def test_edit_location_get(db, client, customer_id, location_customers_id):
    endpoint = reverse('alarm_systems:edit_location', kwargs={'pk': customer_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>Edit Location</h1>' in str(response.content)


def test_edit_location_post(db, client, customer_id, location_customers_id):
    form_url = reverse('alarm_systems:edit_location', kwargs={'pk': customer_id})
    data = {'name': 'TestLocationEditedName', 'address': 'Edited Test Location, Address 2', 'description': 'Test2'}
    response = client.post(form_url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:details_customer', kwargs={'customer_id': customer_id}))
    assert Location.objects.get(name='TestLocationEditedName', address='Edited Test Location, Address 2')


def test_details_location_get(db, client, customer_id, location_customers_id):
    endpoint = reverse('alarm_systems:location_details', kwargs={'location_id': location_customers_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>Systems in this location</h1>' in str(response.content)


def test_add_system_for_location_get(db, client, customer_id, location_customers_id):
    endpoint = reverse('alarm_systems:add_system_for_location', kwargs={'location_id': location_customers_id})
    response = client.get(endpoint)
    form_in_view = response.context['system_type_form']
    assert response.status_code == 200
    assert isinstance(form_in_view, AddSystemTypeForm)


def test_add_system_for_location_post(db, client, customer_id, location_customers_id):
    form_url = reverse('alarm_systems:add_system_for_location', kwargs={'location_id': location_customers_id})
    data_system_type_form = {'name': 'TestSystemTypeName'}
    response = client.post(form_url, data_system_type_form)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:location_details', kwargs={'location_id': location_customers_id}))
    assert SystemType.objects.get(name='TestSystemTypeName')


def test_edit_system_name_get(db, client, system_id):
    endpoint = reverse('alarm_systems:edit_system_name', kwargs={'system_id': system_id})
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, EditSystemNameForm)
    assert '<button type="submit" class="btn btn-success">Edit system name</button>' in str(response.content)


def test_edit_system_name_post(db, client, customer_id, location_customers_id, system_id):
    form_url = reverse('alarm_systems:edit_system_name', kwargs={'system_id': system_id})
    data = {'name': 'TestEditedSystemTypeName'}
    response = client.post(form_url, data)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:location_details', kwargs={'location_id': location_customers_id}))
    assert SystemType.objects.get(name='TestEditedSystemTypeName')


def test_delete_system_get(db, client, customer_id, location_customers_id, system_id):
    endpoint = reverse('alarm_systems:delete_system', kwargs={'system_id': system_id})
    response = client.get(endpoint)
    system = System.objects.all()
    systemtype = SystemType.objects.all()
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:details_customer', kwargs={'customer_id': customer_id}))
    assert len(system) == 0
    assert len(systemtype) == 0


def test_details_system_when_empty_get(db, client, system_id):
    endpoint = reverse('alarm_systems:details_system', kwargs={'system_id': system_id})
    response = client.get(endpoint)
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:empty_system', kwargs={'system_id': system_id}))


def test_details_system_with_video_surveillance_get(db, client, system_id, create_system):
    endpoint = reverse('alarm_systems:details_system', kwargs={'system_id': system_id})
    Registrator.objects.create(system_types=create_system)
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '>Add registrator</a>' in str(response.content)


def test_details_system_with_alarm_get(db, client, system_id, create_system):
    endpoint = reverse('alarm_systems:details_system', kwargs={'system_id': system_id})
    Central.objects.create(system_types=create_system)
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '>Add central</a>' in str(response.content)


def test_add_registrator_get(db, client, system_id):
    endpoint = reverse('alarm_systems:add_registrator', kwargs={'system_id': system_id})
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, AddRegistratorForm)


def test_add_registrator_post(db, client, system_id):
    form_url = reverse('alarm_systems:add_registrator', kwargs={'system_id': system_id})
    data_registrator_form = {'brand': 'TestBrandRegistratorName', 'model': 'TestModel', 'serial_number': '123abc',
                             'description': 'TestDescription'}
    response = client.post(form_url, data_registrator_form)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert Registrator.objects.get(brand='TestBrandRegistratorName')


def test_delete_registrator_get(db, client, system_id, registrator_id):
    endpoint = reverse('alarm_systems:delete_registrator', kwargs={'registrator_id': registrator_id})
    response = client.get(endpoint)
    registrator1 = Registrator.objects.all()
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert len(registrator1) == 0


def test_edit_registrator_get(db, client, system_id, registrator_id):
    endpoint = reverse('alarm_systems:edit_registrator', kwargs={'pk': registrator_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>Edit registrator</h1>' in str(response.content)


def test_edit_registrator_post(db, client, system_id, registrator_id):
    form_url = reverse('alarm_systems:edit_registrator', kwargs={'pk': registrator_id})
    data_registrator_form = {'brand': 'TestEditBrandRegistratorName', 'model': 'TestModel', 'serial_number': '123abc',
                             'description': 'TestDescription'}
    response = client.post(form_url, data_registrator_form)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert Registrator.objects.get(brand='TestEditBrandRegistratorName')


def test_add_camera_get(db, client, system_id):
    endpoint = reverse('alarm_systems:add_camera', kwargs={'system_id': system_id})
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, AddCameraForm)


def test_add_camera_post(db, client, system_id, registrator_id):
    form_url = reverse('alarm_systems:add_camera', kwargs={'system_id': system_id})
    data_registrator_form = {'brand': 'TestBrandCameraName', 'model': 'TestModel', 'serial_number': '123abc',
                             'placement': random.randint(1, 2), 'description': 'TestCameraDescription',
                             'registrator': registrator_id}

    response = client.post(form_url, data_registrator_form)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert Camera.objects.get(brand='TestBrandCameraName', description='TestCameraDescription')


def test_edit_camera_get(db, client, system_id, create_camera):
    endpoint = reverse('alarm_systems:edit_camera', kwargs={'pk': system_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>Edit camera</h1>' in str(response.content)


def test_edit_camera_post(db, client, system_id, registrator_id, create_camera):
    form_url = reverse('alarm_systems:edit_camera', kwargs={'pk': create_camera.id})
    data_camera_form = {'brand': 'TestBrandEditedCameraName', 'model': 'TestModel', 'serial_number': '123abc',
                        'placement': random.randint(1, 2), 'description': 'TestCameraDescription',
                        'registrator': registrator_id}
    response = client.post(form_url, data_camera_form)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert Camera.objects.get(brand='TestBrandEditedCameraName')


def test_delete_camera_get(db, client, system_id, create_camera):
    endpoint = reverse('alarm_systems:delete_camera', kwargs={'camera_id': create_camera.id})
    response = client.get(endpoint)
    central = Camera.objects.all()
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert len(central) == 0


def test_add_central_get(db, client, system_id):
    endpoint = reverse('alarm_systems:add_central', kwargs={'system_id': system_id})
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, AddCentralForm)


def test_add_central_post(db, client, system_id):
    form_url = reverse('alarm_systems:add_central', kwargs={'system_id': system_id})
    data_central_form = {'brand': 'TestBrandCentralName', 'model': 'TestModel', 'serial_number': '123abc',
                         'description': 'TestDescription'}
    response = client.post(form_url, data_central_form)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert Central.objects.get(brand='TestBrandCentralName')


def test_delete_central_get(db, client, system_id, central_id):
    endpoint = reverse('alarm_systems:delete_central', kwargs={'central_id': central_id})
    response = client.get(endpoint)
    central = Registrator.objects.all()
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert len(central) == 0


def test_edit_central_get(db, client, system_id, central_id):
    endpoint = reverse('alarm_systems:edit_central', kwargs={'pk': central_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>Edit central</h1>' in str(response.content)


def test_edit_central_post(db, client, system_id, central_id):
    form_url = reverse('alarm_systems:edit_central', kwargs={'pk': central_id})
    data_central_form = {'brand': 'TestEditBrandCentralName', 'model': 'TestModel', 'serial_number': '123abc',
                         'description': 'TestDescription'}
    response = client.post(form_url, data_central_form)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert Central.objects.get(brand='TestEditBrandCentralName')


def test_add_motionsensor_get(db, client, system_id):
    endpoint = reverse('alarm_systems:add_motionsensor', kwargs={'system_id': system_id})
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, AddMotionSensorForm)


def test_add_motionsensor_post(db, client, system_id, central_id):
    form_url = reverse('alarm_systems:add_motionsensor', kwargs={'system_id': system_id})
    data_registrator_form = {'brand': 'TestBrandMotionSensorName', 'model': 'TestModel', 'serial_number': '123abc',
                             'placement': random.randint(1, 2), 'description': 'TestMSDescription',
                             'central': central_id}

    response = client.post(form_url, data_registrator_form)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert MotionSensor.objects.get(brand='TestBrandMotionSensorName', description='TestMSDescription')


def test_edit_motionsensor_get(db, client, system_id, create_motionsensor):
    endpoint = reverse('alarm_systems:edit_motionsensor', kwargs={'pk': system_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>Edit motionsensor</h1>' in str(response.content)


def test_edit_motionsensor_post(db, client, system_id, central_id, create_motionsensor):
    form_url = reverse('alarm_systems:edit_motionsensor', kwargs={'pk': create_motionsensor.id})
    data_motionsensor_form = {'brand': 'TestBrandEditedMSName', 'model': 'TestModel', 'serial_number': '123abc',
                              'placement': random.randint(1, 2), 'description': 'TestCameraDescription',
                              'central': central_id}
    response = client.post(form_url, data_motionsensor_form)
    assert response.status_code == 302
    assert response.url.startswith(
        reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert MotionSensor.objects.get(brand='TestBrandEditedMSName')


def test_delete_motionsensor_get(db, client, system_id, create_motionsensor):
    endpoint = reverse('alarm_systems:delete_motionsensor', kwargs={'motionsensor_id': create_motionsensor.id})
    response = client.get(endpoint)
    central = MotionSensor.objects.all()
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:details_system', kwargs={'system_id': system_id}))
    assert len(central) == 0


def test_empty_syystem_get(db, client, system_id):
    endpoint = reverse('alarm_systems:empty_system', kwargs={'system_id': system_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h3>Nothing in this system! Consider creating new one:</h3>' in str(response.content)


def test_send_email_page(db, client, customer_id):
    endpoint = reverse('alarm_systems:send_email', kwargs={'customer_id': customer_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<button type="submit" class="btn btn-success">Send an email</button>' in str(response.content)
