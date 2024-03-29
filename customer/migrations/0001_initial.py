# Generated by Django 3.1.6 on 2021-02-09 05:23

from django.db import migrations, models
import django.utils.timezone
import mapbox_location_field.models
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('location', mapbox_location_field.models.LocationField(map_attrs={'center': [28.2096, 83.9856], 'cursor_style': 'pointer', 'fullscreen_button': False, 'geocoder': False, 'marker_color': 'red', 'navigation_buttons': True, 'placeholder': 'Pick a location on map below', 'readonly': True, 'rotate': False, 'style': 'mapbox://styles/mapbox/outdoors-v11', 'track_location_button': True, 'zoom': 13})),
                ('shop_name', models.CharField(blank=True, max_length=200, null=True)),
                ('vat_no', models.IntegerField(blank=True, null=True, verbose_name='VAT No.')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
