from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly

from .models import *
from .serializers import *

class ShopModelViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        if 'is_active' in request.data and request.data.get('is_active') == "True" and request.user.is_staff == False:
            # Is active can be set True by only AdminUser
            return Response({'is_active': "Can set True by admin user only"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'owner' in request.data and str(instance.owner.id) != str(request.data.get('owner')):
            return Response({'owner': "owner can't be changed"}, status=status.HTTP_403_FORBIDDEN)
        if 'is_active' in request.data and request.data.get('is_active') == "True" and instance.owner.is_staff == False:
            """Is active can be set True by only AdminUser"""
            return Response({'is_active': "Can changed by admin user only"}, status=status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

