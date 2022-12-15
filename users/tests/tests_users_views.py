from django.urls import reverse


def test_login_page_get(client):
    endpoint = reverse('users:login_view')
    response = client.get(endpoint)

    assert response.status_code == 200
    assert '<h1>Login</h1>' in str(response.content)

def test_registration_page_get(client):
    endpoint = reverse('users:registration_view')
    response = client.get(endpoint)

    assert response.status_code == 200
    assert '<h1>Registration</h1>' in str(response.content)