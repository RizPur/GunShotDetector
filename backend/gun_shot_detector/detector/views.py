from rest_framework import viewsets
from detector.models import GunShot, GunShotDetector
from detector.serializer import GunShotSerializer, GunShotStationSerializer
from websocket import create_connection
import json


class GunShotViewSet(viewsets.ModelViewSet):
    queryset = GunShot.objects.all()
    serializer_class = GunShotSerializer

    def perform_create(self, serializer):

        # commented line below to allow all audio to be classified
        # if serializer.validated_data.get('prob') > 60.00:
        if serializer.validated_data.get('prob'):
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
                    "carbine_gun": str(serializer.validated_data.get('carbine_gun')),
                    "pistol_gun": str(serializer.validated_data.get('pistol_gun')),
                    "revolver_gun": str(serializer.validated_data.get('revolver_gun'))
                }
            }

            initiate_client(data)

        return serializer.save()


class GunShotStationViewSet(viewsets.ModelViewSet):
    queryset = GunShotDetector.objects.all()
    serializer_class = GunShotStationSerializer


def initiate_client(data):
    ws = create_connection("ws://localhost:8000/ws/chat/gunsession/")
    ws.send(json.dumps({"message": data}))
    ws.close()
