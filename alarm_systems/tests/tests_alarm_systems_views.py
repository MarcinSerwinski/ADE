from django.contrib.auth.models import Permission
import pytest
from django.urls import reverse

from alarm_systems.forms import AddCustomerForm, DeleteCustomerForm, AddSystemTypeForm
from alarm_systems.models import Customer, Location, SystemType


def test_home_page_get(client):
    endpoint = reverse('alarm_systems:home')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>ADE</h1>' in str(response.content)


@pytest.mark.django_db
def test_acces_with_no_permission_to_mainview(client, user):
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


def test_delete_customer_get(db, client, customer_id):
    endpoint = reverse('alarm_systems:delete_customer', kwargs={'customer_id': customer_id})
    response = client.get(endpoint)
    form_in_view = response.context['form']
    assert response.status_code == 200
    assert isinstance(form_in_view, DeleteCustomerForm)
    assert '<button type="submit" class="btn btn-outline-danger">Yes. Delete.</button>' in str(response.content)


def test_delete_customer_post(db, client, customer_id):
    form_url = reverse('alarm_systems:delete_customer', kwargs={'customer_id': customer_id})
    response = client.post(form_url)
    customer = Customer.objects.all()
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:main_view'))
    assert len(customer) == 0


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


def test_details_customer_get(db, client, customer_id):
    endpoint = reverse('alarm_systems:details_customer', kwargs={'customer_id': customer_id})
    response = client.get(endpoint)
    customer_in_view = response.context['customer']
    assert customer_in_view.id in response.context
    assert response.status_code == 200
    assert "<h1>Locations listed below:</h1>" in str(response.content)


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


def test_details_location_get(db, client, customer_id):
    location = Location.objects.create(customer_id=customer_id)
    location_id = location.id
    endpoint = reverse('alarm_systems:location_details', kwargs={'location_id': location_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<h1>Systems in this location</h1>' in str(response.content)


def test_add_system_for_location_get(db, client, customer_id):
    location = Location.objects.create(customer_id=customer_id)
    location_id = location.id
    endpoint = reverse('alarm_systems:add_system_for_location', kwargs={'location_id': location_id})
    response = client.get(endpoint)
    form_in_view = response.context['system_type_form']
    assert response.status_code == 200
    assert isinstance(form_in_view, AddSystemTypeForm)


def test_add_system_for_location_post(db, client, customer_id):
    location = Location.objects.create(customer_id=customer_id)
    location_id = location.id
    form_url = reverse('alarm_systems:add_system_for_location', kwargs={'location_id': location_id})
    data_system_type_form = {'name': 'TestSystemTypeName'}
    response = client.post(form_url, data_system_type_form)
    assert response.status_code == 302
    assert response.url.startswith(reverse('alarm_systems:location_details', kwargs={'location_id': location_id}))
    assert SystemType.objects.get(name='TestSystemTypeName')


def test_send_email_page(db, client, customer_id):
    endpoint = reverse('alarm_systems:send_email', kwargs={'customer_id': customer_id})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<button type="submit" class="btn btn-success">Send an email</button>' in str(response.content)
