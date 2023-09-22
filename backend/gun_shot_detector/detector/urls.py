from rest_framework.routers import DefaultRouter
from detector.views import GunShotViewSet, GunShotStationViewSet

app_name = 'detector'

router = DefaultRouter(trailing_slash=True)

router.register(r'gunshot', GunShotViewSet)
router.register(r'station', GunShotStationViewSet)

urlpatterns = []


urlpatterns += router.urls
