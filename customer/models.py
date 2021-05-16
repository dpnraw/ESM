from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mapbox_location_field.models import LocationField
from model_utils.models import TimeStampedModel


class SaleLocation(models.Model):

    location = models.CharField(
        _('Sale Location'),
        max_length=200,
    )

    def __str__(self):
        return self.location


class Customer(TimeStampedModel):

    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    shop_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Optional',
    )
    vat_no = models.IntegerField(
        'VAT No.',
        null=True,
        blank=True,
        help_text='Optional',
    )
    sale_location = models.ForeignKey(
        SaleLocation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Select from dropdown or create a new location.',
    )
    location = LocationField(map_attrs=settings.MAP_ATTRS)

    def __str__(self):
        appendable_string = ''
        if self.sale_location:
            appendable_string = f' from {self.sale_location.location}'
        return f'{self.name}{appendable_string}'

    def __unicode__(self):
        # We need to add this to show the name of the customer
        # in raw_id_fields.
        return f'{self.name}'


class CreditPayment(TimeStampedModel):

    customer = models.ForeignKey(
        Customer,
        related_name='credit_payment',
        related_query_name='credit_payment',
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(help_text='Enter amount greater than zero.')

    def __str__(self):
        return f'{self.customer} pays Rs.{self.amount}'

    class Meta:
        verbose_name = 'Due Payment'
        verbose_name_plural = 'Due Payments'


class PaymentHistory(TimeStampedModel):
    class PaymentType(models.TextChoices):

        CASH = ('CA', 'Cash')
        CREDIT = ('CR', 'Credit')
        CHEQUE = ('CH', 'Cheque')
        DUE_PAYMENT = ('DP', 'Due Payment')

    customer = models.ForeignKey(
        Customer,
        related_name='payment_history',
        related_query_name='payment_history',
        on_delete=models.SET_NULL,
        null=True,
    )
    payment_type = models.CharField(
        choices=PaymentType.choices,
        default=PaymentType.CASH,
        max_length=2,
    )
    amount = models.FloatField()
    description = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.description

    class Meta:
        verbose_name_plural = 'Payment Histories'
