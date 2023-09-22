from rest_framework import serializers
from detector.models import GunShot, GunShotDetector


class GunShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = GunShot
        fields = '__all__'


class GunShotStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GunShotDetector
        fields = '__all__'
