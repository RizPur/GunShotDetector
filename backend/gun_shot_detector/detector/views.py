from rest_framework import viewsets
from detector.models import GunShot, GunShotDetector
from detector.serializer import GunShotSerializer, GunShotStationSerializer
from websocket import create_connection
import json


class GunShotViewSet(viewsets.ModelViewSet):
    queryset = GunShot.objects.all()
    serializer_class = GunShotSerializer

    def perform_create(self, serializer):

        if serializer.validated_data.get('prob') > 60.00:
            gunShotDetector = GunShotDetector.objects.get(
                pk=serializer.validated_data.get('gun_detector').pk)

            data = {
                "ID": gunShotDetector.pk,
                "prob": str(serializer.validated_data.get('prob')),
                "geo": [
                    str(gunShotDetector.latitude),
                    str(gunShotDetector.longitude)
                ],
                "dateTime": str(serializer.validated_data.get('created_at')),
                "parish": gunShotDetector.parish,
                "location": gunShotDetector.location,
                "probs": {
                    "ak12_gun": str(serializer.validated_data.get('ak12_gun')),
                    "m4_gun": str(serializer.validated_data.get('m4_gun')),
                    "imi_desert_eagle_gun": str(serializer.validated_data.get('imi_desert_eagle_gun')),
                    "other_gun": str(serializer.validated_data.get('other_gun'))
                }
            }

            initiate_client(data)

        return serializer.save()


class GunShotStationViewSet(viewsets.ModelViewSet):
    queryset = GunShotDetector.objects.all()
    serializer_class = GunShotStationSerializer


def initiate_client(data):
    # ws = create_connection("ws://localhost:8000/ws/chat/gunsession/")
    ws = create_connection("ws://192.168.4.108:8000/ws/chat/gunsession/")
    ws.send(json.dumps({"message": data}))
    ws.close()
