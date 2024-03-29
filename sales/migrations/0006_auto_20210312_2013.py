# Generated by Django 3.1.6 on 2021-03-12 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_auto_20210310_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=200, verbose_name='Sale Location')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='sale_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.salelocation'),
        ),
    ]
