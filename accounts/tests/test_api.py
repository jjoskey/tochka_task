import json
import unittest
from collections import OrderedDict

import faker
import pytest
from django.urls import reverse
from rest_framework import status

from .factories import AccountFactory


@pytest.mark.usefixtures('client_for_class')
class AddApiTestCase(unittest.TestCase):
    def setUp(self):
        self.fake = faker.Faker()
        self.url = reverse('add')

    def test_add(self):
        account = AccountFactory()
        initial_balance = account.balance
        amount = self.fake.pyint(min_value=1)
        data = {
            'account_uuid': str(account.uuid),
            'amount': amount
        }
        response = self.api_client.post(self.url, data=json.dumps(data),
                                        content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        account.refresh_from_db()
        assert response.data == {
            'status': status.HTTP_200_OK,
            'result': True,
            'addition': OrderedDict([
                ('uuid', str(account.uuid)),
                ('name', account.name),
                ('balance', account.balance),
                ('hold', account.hold),
                ('is_opened', account.is_opened)
            ]),
            'description': OrderedDict([
                ('operation', 'add'),
                ('add_amount', amount)
            ])
        }
        assert account.balance == initial_balance + amount

    def test_add_is_opened_validation(self):
        account = AccountFactory(is_opened=False)
        initial_balance = account.balance
        data = {
            'account_uuid': str(account.uuid),
            'amount': self.fake.pyint(min_value=1)
        }
        response = self.api_client.post(self.url, data=json.dumps(data),
                                        content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0].code == 'invalid_account'
        account.refresh_from_db()
        assert account.balance == initial_balance


@pytest.mark.usefixtures('client_for_class')
class SubstractApiTestCase(unittest.TestCase):
    def setUp(self):
        self.fake = faker.Faker()
        self.url = reverse('substract')

    def test_substract(self):
        account = AccountFactory()
        initial_balance, initial_hold = account.balance, account.hold
        amount = self.fake.pyint(min_value=1,
                                 max_value=initial_balance - initial_hold)
        data = {
            'account_uuid': str(account.uuid),
            'amount': amount
        }
        response = self.api_client.post(self.url, data=json.dumps(data),
                                        content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        account.refresh_from_db()
        assert response.data == {
            'status': status.HTTP_200_OK,
            'result': True,
            'addition': OrderedDict([
                ('uuid', str(account.uuid)),
                ('name', account.name),
                ('balance', account.balance),
                ('hold', account.hold),
                ('is_opened', account.is_opened)
            ]),
            'description': OrderedDict([
                ('operation', 'substract'),
                ('substract_amount', amount)
            ])
        }
        assert account.balance == initial_balance
        assert account.hold == initial_hold + amount

    def test_substract_is_opened_validation_error(self):
        account = AccountFactory(is_opened=False)
        initial_balance, initial_hold = account.balance, account.hold
        data = {
            'account_uuid': str(account.uuid),
            'amount': self.fake.pyint(min_value=1)
        }
        response = self.api_client.post(self.url, data=json.dumps(data),
                                        content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0].code == 'invalid_account'
        account.refresh_from_db()
        assert account.balance == initial_balance
        assert account.hold == initial_hold

    def test_substract_account_balance_validation_error(self):
        account = AccountFactory()
        substraction = account.balance - account.hold + 1
        initial_balance, initial_hold = account.balance, account.hold
        data = {
            'account_uuid': str(account.uuid),
            'amount': substraction
        }
        response = self.api_client.post(self.url, data=json.dumps(data),
                                        content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0].code == 'invalid_balance'
        account.refresh_from_db()
        assert account.balance == initial_balance
        assert account.hold == initial_hold


@pytest.mark.usefixtures('client_for_class')
class StatusApiTestCase(unittest.TestCase):
    def setUp(self):
        self.fake = faker.Faker()
        self.url = reverse('status')

    def test_status(self):
        account = AccountFactory(is_opened=self.fake.pybool())
        data = {'account_uuid': str(account.uuid)}
        response = self.api_client.get(self.url, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'status': status.HTTP_200_OK,
            'result': True,
            'addition': OrderedDict([
                ('uuid', str(account.uuid)),
                ('name', account.name),
                ('balance', account.balance),
                ('hold', account.hold),
                ('is_opened', account.is_opened)
            ]),
            'description': OrderedDict([
                ('operation', 'status'),
            ])
        }

    def test_status_no_account_validation_error(self):
        data = {'account_uuid': str(self.fake.uuid4())}
        response = self.api_client.get(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['account_uuid'][0].code == 'does_not_exist'


def test_ping(api_client):
    url = reverse('ping')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'status': status.HTTP_200_OK,
        'result': True,
        'addition': {},
        'description': OrderedDict([
            ('operation', 'ping'),
        ])
    }
