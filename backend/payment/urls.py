from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import CollectdonateViewSet, PaymentViewSet

router = DefaultRouter()


router.register('collect-donate', CollectdonateViewSet)
router.register('payment', PaymentViewSet, basename='payment')


urlpatterns = [
    path('', include(router.urls)),
]
