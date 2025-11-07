import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


def test_user_list(client):
    url = reverse("api:user-list")
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()["count"] == 1


def test_user_detail(client, admin_user):
    url = reverse("api:user-detail", kwargs={"pk": admin_user.pk})
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()["username"] == admin_user.username
