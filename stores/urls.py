from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register('shop', ShopModelViewSet)
router.register('category', CategoryModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]