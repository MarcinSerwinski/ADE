from django.test import TestCase
import pytest

from django.urls import reverse

from alarm_systems.models import Customer


def test_home_page(client):
    endpoint = reverse('alarm_systems:home')
    response = client.get(endpoint)

    assert response.status_code == 200
    assert '<h1>ADE</h1>' in str(response.content)



# def test_auth_view(db, client, create_user, test_password):
#     user = create_user()
#     url = reverse('alarm_systems:main_view')
#     client.login(
#         username=user.username, password=test_password
#     )
#     response = client.get(url)
#     assert response.status_code == 200




def test_send_email_page(db, client):
    customer = Customer.objects.create()
    endpoint = reverse('alarm_systems:send_email', kwargs={'customer_id': customer.pk})
    response = client.get(endpoint)

    assert response.status_code == 200

