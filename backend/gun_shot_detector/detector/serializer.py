from rest_framework import serializers
from detector.models import GunShot


class GunShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = GunShot
        fields = '__all__'
