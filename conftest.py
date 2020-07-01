import os

import django
import pytest
from django.core.cache import caches
from django.test import TransactionTestCase

TransactionTestCase.serialized_rollback = True


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture()
def anon_api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_user():
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
    user = user_model(username='test')
    user.set_password('test_password')
    user.save()
    return user


@pytest.fixture
def api_client(api_user):
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_login(api_user)
    return client


@pytest.fixture
def client_for_class(request, api_client):
    request.cls.api_client = api_client


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "source.settings")
    django.setup()


@pytest.fixture(autouse=True)
def clear_caches():
    for cache in caches.all():
        cache.clear()
