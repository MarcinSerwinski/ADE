import pytest

from django.contrib.auth.models import Permission

from alarm_systems.models import *


@pytest.fixture()
def user(db, django_user_model):
    """Create django user"""
    yield django_user_model.objects.create_user(email='test2@admin.com', fullname='Test User', password='TestPass123')


@pytest.fixture()
def user_with_permission(user):
    permission = Permission.objects.get(name='Can add camera')
    yield user.user_permissions.add(permission)


@pytest.fixture()
def create_customer():
    yield Customer.objects.create()


@pytest.fixture()
def customer_id(create_customer):
    yield create_customer.id


@pytest.fixture()
def create_location():
    yield Location.objects.create(customer_id=customer_id)


@pytest.fixture()
def location_id(create_location):
    yield create_location.id


@pytest.fixture()
def location_customers_id(customer_id):
    yield (Location.objects.create(customer_id=customer_id)).id

@pytest.fixture()
def create_systemtype():
    yield SystemType.objects.create()


@pytest.fixture()
def systemtype_id(create_systemtype):
    yield create_systemtype.id

@pytest.fixture()
def create_system(location_customers_id, create_systemtype):
    yield System.objects.create(location_id=location_customers_id, system_type=create_systemtype)


@pytest.fixture()
def system_id(create_system):
    yield create_system.id

@pytest.fixture()
def create_registrator(create_system):
    yield Registrator.objects.create(system_types=create_system)
@pytest.fixture()
def registrator_id(create_registrator):
    yield create_registrator.id
@pytest.fixture()
def create_central(create_system):
    yield Central.objects.create(system_types=create_system)
@pytest.fixture()
def central_id(create_central):
    yield create_central.id
@pytest.fixture()
def create_camera(registrator_id):
    yield Camera.objects.create(registrator_id=registrator_id)

@pytest.fixture()
def create_motionsensor(central_id):
    yield MotionSensor.objects.create(central_id=central_id)