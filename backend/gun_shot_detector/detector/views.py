from django.shortcuts import render
from rest_framework import viewsets
from detector.models import GunShot
from detector.serializer import GunShotSerializer


class GunShotViewSet(viewsets.ModelViewSet):
    queryset = GunShot.objects.all()
    serializer_class = GunShotSerializer
