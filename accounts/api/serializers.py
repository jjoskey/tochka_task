from collections import OrderedDict
from typing import Optional

from rest_framework import serializers
from rest_framework import status

from ..models import Account


class AccountUUIDMixin(serializers.Serializer):
    account_uuid = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), required=True,
        source='account')


class AccountOperationSerializer(AccountUUIDMixin,
                                 serializers.Serializer):
    amount = serializers.IntegerField(min_value=0, required=True)


class AccountStatusSerializer(AccountUUIDMixin):
    pass


def get_answer(account: Optional[Account], operation: str, **kwargs) -> dict:
    if account:
        addition = OrderedDict([
            ('uuid', str(account.uuid)),
            ('name', account.name),
            ('balance', account.balance),
            ('hold', account.hold),
            ('is_opened', account.is_opened)
        ])
    else:
        addition = {}
    return {
        'status': status.HTTP_200_OK,
        'result': True,
        'addition': addition,
        'description': OrderedDict({
            'operation': operation,
            **kwargs
        })
    }
