from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    Sum,
    base,
)
from django.utils.translation import ugettext_lazy as _
from jsignature.fields import JSignatureField
from mapbox_location_field.models import LocationField
from model_utils.models import TimeStampedModel


class EggType(models.Model):

    type = models.CharField(
        _('Egg Type'),
        max_length=4,
        unique=True,
    )

    def __str__(self):
        return self.type

    class Meta:
        ordering = ('type', )


class Sale(TimeStampedModel):

    date = models.DateField()
    customer = models.ForeignKey(
        'customer.Customer',
        verbose_name=_('Customer'),
        on_delete=models.CASCADE,
        related_name='sale',
        related_query_name='sale',
    )
    descriptive_location = models.CharField(
        _('Descriptive Location'),
        max_length=100,
        null=True,
        blank=True,
        help_text='Eg: Parshyang, Malepatan',
    )
    location = LocationField(map_attrs=settings.MAP_ATTRS)
    signature = JSignatureField()

    salesman = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='salesman',
        related_query_name='salesman',
        null=True,
    )

    def __str__(self):
        return f'{self.date} -> {self.customer}'

    def save(self, *args, **kwargs):
        self.descriptive_location = self.customer.sale_location.location
        super(Sale, self).save(*args, **kwargs)

    @property
    def total_price(self):
        '''Return total payable price for the individual sale.

        Returns:
            float: Total payable price
        '''
        total = 0.0
        for payment in self.payments.all():
            total += payment.amount
        return total

    @property
    def amount_received(self):
        '''Return amount received for the individual sale.

        Returns:
            float: Amount received for individual sale.
        '''
        amount_received = self.payments.all().filter(type='CA').aggregate(
            sum=Sum('amount')).get('sum') or 0.0
        return amount_received

    @property
    def cheque_balance(self):
        '''Return cheque balance received for the individual sale.

        Returns:
            float: cheque balance received for individual sale.
        '''
        cheque_balance = self.payments.all().filter(type='CH').aggregate(
            sum=Sum('amount')).get('sum') or 0.0
        return cheque_balance

    @property
    def due_balance(self):
        '''Return due balance for the individual sale.

        Returns:
            float: Due balance for individual sale.
        '''
        due_balance = self.payments.all().filter(type='CR').aggregate(
            sum=Sum('amount')).get('sum') or 0.0
        return due_balance


class Payment(TimeStampedModel):
    class Type(models.TextChoices):
        CASH = 'CA', _('Cash')
        CHEQUE = 'CH', _('Cheque')
        CREDIT = 'CR', _('Credit')

    type = models.CharField(
        max_length=2,
        choices=Type.choices,
        default=Type.CASH,
    )

    sale = models.ForeignKey(
        Sale,
        verbose_name=_('Payment'),
        on_delete=models.CASCADE,
        related_name='payments',
        related_query_name='payments',
    )

    amount = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.type} -> {self.amount}'


class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        verbose_name=_('Sale Item'),
        on_delete=models.CASCADE,
        related_name='sales',
        related_query_name='sales',
    )

    egg_type = models.ForeignKey(EggType, on_delete=models.CASCADE)
    quantity = models.IntegerField(_('In Crate'))
    amount = models.FloatField(
        _('Sale Item Amount'),
        default=0.0,
    )

    def __str__(self):
        return f'{self.egg_type} -> {self.quantity}'
