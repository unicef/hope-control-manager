import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def user():
    from testutils.factories import UserFactory

    return UserFactory()


@pytest.fixture
def group(user):
    from extras.testutils.factories import GroupFactory

    g = GroupFactory()
    g.user_set.add(user)
    return g


def test_user_list(client, group):
    url = reverse("api:group-list")
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()["count"] == 1


def test_user_detail(client, group):
    url = reverse("api:group-detail", kwargs={"pk": group.pk})
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()["name"] == group.name
