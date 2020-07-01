from uuid import UUID

from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from .models import Account


class AccountBusinessLogic:
    def __init__(self, account_uuid: UUID) -> None:
        self.account_uuid = account_uuid

    def validate_account_balance(
            self, account: Account, substraction: int) -> None:
        if account.balance - account.hold - substraction < 0:
            raise ValidationError(
                _('Account balance is less than 0'),
                code='invalid_balance')

    def validate_account_is_opened(self, account: Account) -> None:
        if not account.is_opened:
            raise ValidationError(
                _('Account is closed'),
                code='invalid_account')

    def add(self, amount: int) -> Account:
        with transaction.atomic():
            account = Account.objects.select_for_update().get(
                uuid=self.account_uuid)
            self.validate_account_is_opened(account)
            account.balance += amount
            account.save()
        return account

    def substract(self, amount: int) -> Account:
        with transaction.atomic():
            account = Account.objects.select_for_update().get(
                uuid=self.account_uuid)
            self.validate_account_is_opened(account)
            self.validate_account_balance(account, amount)
            account.hold += amount
            account.save()
        return account
