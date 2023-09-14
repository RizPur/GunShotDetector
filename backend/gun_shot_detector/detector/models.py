from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class GunShot(models.Model):
    created_at = models.DateTimeField()
    location = models.CharField(max_length=200)
    ak_12_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    ak_47_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    imi_desert_eagle_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    m4_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    m16_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    m249_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    mg_42_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    mp5_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    zastava_m92_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    other_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
