from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from sales.models import Payment

from .models import (
    CreditPayment,
    PaymentHistory,
)


@receiver(pre_save, sender=CreditPayment)
def log_credit_payment(sender, instance, **kwargs):

    customer = instance.customer
    amount = instance.amount
    payment_type = PaymentHistory.PaymentType.DUE_PAYMENT
    description = '{} {} transaction on paid due amount of Rs.{} of at {} .'
    if instance.id is None:
        # If object is newly created.
        timestamp = instance.created
        transaction = 'created'

    else:
        # If object is being modified.
        current = instance
        previous = CreditPayment.objects.get(id=instance.id)
        if current.amount == previous.amount:
            return
        timestamp = instance.modified
        transaction = 'modified'

    # Localizing Time
    timestamp = timezone.localtime(timestamp)

    PaymentHistory.objects.create(
        customer=customer,
        payment_type=payment_type,
        amount=amount,
        description=description.format(
            customer,
            transaction,
            amount,
            timestamp.strftime('%a %H:%M  %d/%m/%y'),
        ),
    )


@receiver(pre_save, sender=Payment)
def log_payment(sender, instance, **kwargs):

    customer = instance.sale.customer
    salesman = instance.sale.salesman
    payment = instance
    if instance.id is None:
        # If object is newly created.
        timestamp = instance.created
        transaction = 'created'
    else:
        # If object is being modified.
        current = instance
        previous = Payment.objects.get(id=instance.id)
        if current.amount == previous.amount and current.type == previous.type:
            return
        timestamp = instance.modified
        transaction = 'modified'

    # Localizing Time
    timestamp = timezone.localtime(timestamp)

    amount = payment.amount
    description = '{} {} transaction on {} amount of Rs.{} of at {} with Salesman {}.'

    if payment.type == Payment.Type.CASH:
        payment_type = PaymentHistory.PaymentType.CASH
        action = 'paid cash'
    elif payment.type == Payment.Type.CREDIT:
        payment_type = PaymentHistory.PaymentType.CREDIT
        action = 'left due'
    elif payment.type == Payment.Type.CHEQUE:
        payment_type = PaymentHistory.PaymentType.CHEQUE
        action = 'paid cheque'

    PaymentHistory.objects.create(
        customer=customer,
        payment_type=payment_type,
        amount=amount,
        description=description.format(
            customer,
            transaction,
            action,
            amount,
            timestamp.strftime('%a %H:%M  %d/%m/%y'),
            salesman,
        ),
    )
