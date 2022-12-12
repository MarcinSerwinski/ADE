import os
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.test import TestCase

import pytest

from django.urls import reverse

from alarm_systems.models import Customer


def test_home_page(client):
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


def test_add_customer_page(client):
    endpoint = reverse('alarm_systems:add_customer')
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<button type="submit" class="btn btn-success">Add new customer</button>' in str(response.content)


def test_send_email_page(db, client):
    customer = Customer.objects.create()
    endpoint = reverse('alarm_systems:send_email', kwargs={'customer_id': customer.pk})
    response = client.get(endpoint)
    assert response.status_code == 200
    assert '<button type="submit" class="btn btn-success">Send an email</button>' in str(response.content)
