# Generated by Django 3.1.6 on 2021-03-09 15:41

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20210309_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('amount', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_payment', related_query_name='credit_payment', to='customer.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
