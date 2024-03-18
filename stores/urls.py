from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register('shops', ShopModelViewSet, basename='shop')
router.register('categories', CategoryModelViewSet)
router.register('products', ProductModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]