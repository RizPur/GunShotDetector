# Generated by Django 4.2.5 on 2023-09-14 01:24

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0002_rename_baretta_model_92_gun_gunshot_ak_12_gun_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gunshot',
            name='ak_12_gun',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='gunshot',
            name='ak_47_gun',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
