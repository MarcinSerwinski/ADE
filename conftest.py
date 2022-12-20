import pytest

from django.contrib.auth.models import Permission

from alarm_systems.models import *


@pytest.fixture()
def user(db, django_user_model):
    """Create django user"""
    return django_user_model.objects.create_user(email='test2@admin.com', fullname='Test User', password='TestPass123')


@pytest.fixture()
def user_with_permission(user):
    permission = Permission.objects.get(name='Can add camera')
    return user.user_permissions.add(permission)


@pytest.fixture()
def create_customer():
    return Customer.objects.create()


@pytest.fixture()
def customer_id(create_customer):
    return create_customer.id


@pytest.fixture()
def create_location():
    return Location.objects.create(customer_id=customer_id)


@pytest.fixture()
def location_id(create_location):
    return create_location.id


@pytest.fixture()
def location_customers_id(customer_id):
    return (Location.objects.create(customer_id=customer_id)).id

@pytest.fixture()
def create_systemtype():
    return SystemType.objects.create()


@pytest.fixture()
def systemtype_id(create_systemtype):
    return create_systemtype.id

@pytest.fixture()
def create_system(location_customers_id, create_systemtype):
    return System.objects.create(location_id=location_customers_id, system_type=create_systemtype)


@pytest.fixture()
def system_id(create_system):
    return create_system.id

@pytest.fixture()
def create_registrator(create_system):
    return Registrator.objects.create(system_types=create_system)
@pytest.fixture()
def registrator_id(create_registrator):
    return create_registrator.id
@pytest.fixture()
def create_central(create_system):
    return Central.objects.create(system_types=create_system)
@pytest.fixture()
def central_id(create_central):
    return create_central.id
@pytest.fixture()
def create_camera(registrator_id):
    return Camera.objects.create(registrator_id=registrator_id)

@pytest.fixture()
def create_motionsensor(central_id):
    return MotionSensor.objects.create(central_id=central_id)