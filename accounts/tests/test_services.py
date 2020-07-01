import unittest

import faker
import pytest
from rest_framework.exceptions import ValidationError

from .factories import AccountFactory
from ..services import AccountBusinessLogic


class AccountBusinessLogicTestCase(unittest.TestCase):
    def setUp(self):
        self.fake = faker.Faker()

    def test_validate_account_balance(self):
        account = AccountFactory(balance=1000, hold=500)
        substraction = self.fake.random_element([500, 499])
        try:
            AccountBusinessLogic(account.uuid).validate_account_balance(
                account, substraction)
        except ValidationError:
            pytest.fail()

    def test_validate_account_balance_validation_error(self):
        account = AccountFactory(balance=1000, hold=500)
        substraction = self.fake.random_element(
            [501, self.fake.pyint(min_value=502, max_value=600)])
        with pytest.raises(ValidationError):
            AccountBusinessLogic(account.uuid).validate_account_balance(
                account, substraction)

    def test_validate_account_is_opened(self):
        account = AccountFactory()
        try:
            AccountBusinessLogic(account.uuid).validate_account_is_opened(
                account)
        except ValidationError:
            pytest.fail()

    def test_validate_account_is_opened_validation_error(self):
        account = AccountFactory(is_opened=False)
        with pytest.raises(ValidationError):
            AccountBusinessLogic(account.uuid).validate_account_is_opened(
                account)

    def test_add(self):
        account = AccountFactory()
        initial_balance = account.balance
        amount = self.fake.pyint(min_value=1)
        AccountBusinessLogic(account.uuid).add(amount)
        account.refresh_from_db()
        assert account.balance == initial_balance + amount

    def test_add_is_opened_validation_error(self):
        account = AccountFactory(is_opened=False)
        initial_balance = account.balance
        amount = self.fake.pyint(min_value=1)
        with pytest.raises(ValidationError):
            AccountBusinessLogic(account.uuid).add(amount)
        account.refresh_from_db()
        assert account.balance == initial_balance

    def test_substract(self):
        account = AccountFactory()
        initial_balance, initial_hold = account.balance, account.hold
        substraction = self.fake.pyint(min_value=1,
                                 max_value=initial_balance - initial_hold)
        AccountBusinessLogic(account.uuid).substract(substraction)
        account.refresh_from_db()
        assert account.balance == initial_balance
        assert account.hold == initial_hold + substraction

    def test_substract_is_opened_validation_error(self):
        account = AccountFactory(is_opened=False)
        initial_balance, initial_hold = account.balance, account.hold
        substratcion = self.fake.pyint(min_value=1)
        with pytest.raises(ValidationError):
            AccountBusinessLogic(account.uuid).substract(substratcion)
        account.refresh_from_db()
        assert account.balance == initial_balance
        assert account.hold == initial_hold

    def test_substract_balance_validation_error(self):
        account = AccountFactory(balance=1000, hold=500)
        substraction = self.fake.random_element(
            [501, self.fake.pyint(min_value=502, max_value=600)])
        initial_balance, initial_hold = account.balance, account.hold
        with pytest.raises(ValidationError):
            AccountBusinessLogic(account.uuid).substract(substraction)
        assert account.balance == initial_balance
        assert account.hold == initial_hold
