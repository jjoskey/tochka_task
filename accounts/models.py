from uuid import uuid4

from django.db import models
from django.utils.translation import gettext as _


class Account(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        verbose_name=_('UUID')
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('ФИО')
    )
    balance = models.IntegerField(
        default=0,
        verbose_name='Баланс'
    )
    hold = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Замороженные средства')
    )
    is_opened = models.BooleanField(
        default=True,
        verbose_name=_('Статус')
    )

    class Meta:
        verbose_name = _('Счёт')
        verbose_name_plural = _('Счёта')
