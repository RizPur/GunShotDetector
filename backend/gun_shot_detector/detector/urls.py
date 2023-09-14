from rest_framework.routers import DefaultRouter
from django.urls import path
from detector.views import GunShotViewSet

app_name = 'detector'

router = DefaultRouter(trailing_slash=True)

router.register(r'gunshot', GunShotViewSet)

urlpatterns = []


urlpatterns += router.urls
