from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class GunShotDetector(models.Model):
    latitude = models.DecimalField(max_digits=20, decimal_places=17)
    longitude = models.DecimalField(max_digits=20, decimal_places=17)
    location = models.CharField(max_length=200)
    parish = models.CharField(max_length=30)


class GunShot(models.Model):
    created_at = models.DateTimeField()
    prob = models.DecimalField(
        max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR)
    gun_detector = models.ForeignKey(
        GunShotDetector, on_delete=models.CASCADE, verbose_name='Gun Shut Detector', null=True)
    carbine_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    pistol_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    revolver_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
        0), validators=PERCENTAGE_VALIDATOR)
    # m4_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
    #     0), validators=PERCENTAGE_VALIDATOR)
    # m16_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
    #     0), validators=PERCENTAGE_VALIDATOR)
    # m249_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
    #     0), validators=PERCENTAGE_VALIDATOR)
    # mg_42_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
    #     0), validators=PERCENTAGE_VALIDATOR)
    # mp5_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
    #     0), validators=PERCENTAGE_VALIDATOR)
    # zastava_m92_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
    #     0), validators=PERCENTAGE_VALIDATOR)
    # other_gun = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(
    #     0), validators=PERCENTAGE_VALIDATOR)
