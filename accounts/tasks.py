from celery import shared_task
from django.db import transaction
from django.db.models import F

from .models import Account


@shared_task
def write_off_holds_from_balances() -> None:
    with transaction.atomic():
        accounts = Account.objects.select_for_update().filter(hold__gt=0)
        accounts.update(balance=F('balance') - F('hold'), hold=0)
