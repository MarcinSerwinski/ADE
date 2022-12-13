import pytest
from random import randint
from alarm_systems.models import Customer, Location


@pytest.fixture()
def user(db, django_user_model):
    """Create django user"""
    yield django_user_model.objects.create_user(email='test2@admin.com', fullname='Test User', password='TestPass123')


# @pytest.fixture()
# def user_with_permission(db, django_user_model):
#     django_user_model.objects.create_user(email='test3@admin.com', fullname='Test User Permission',
#                                           password='TestPass123')
#

@pytest.fixture()
def create_customer():
    customer = Customer.objects.create()
    yield customer


@pytest.fixture()
def customer_id():
    customer_id = (Customer.objects.create()).id
    yield customer_id


@pytest.fixture()
def create_location():
    location = Location.objects.create()
    yield location


@pytest.fixture()
def location_id():
    location_id = (Location.objects.create()).id
    yield location_id

@pytest.fixture()
def location_customers_id(customer_id):
    location_customers_id = Location.objects.create(customer_id=customer_id)
    yield location_customers_id
