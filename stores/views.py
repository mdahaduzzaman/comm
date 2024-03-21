from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrAdminOrReadOnly

from .models import *
from .serializers import *

class ShopModelViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        if 'is_active' in request.data and request.data.get('is_active') == "True" and request.user.is_staff == False:
            # Is active can be set True by only AdminUser
            return Response({'is_active': "Can set True by admin user only"}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'owner' in request.data and str(instance.owner.id) != str(request.data.get('owner')):
            return Response({'owner': "owner can't be changed"}, status=status.HTTP_403_FORBIDDEN)

        if 'is_active' in request.data and str(request.data.get('is_active')).lower() == 'true' and instance.owner.is_staff == False:
            """Is active can be set True by only AdminUser"""
            return Response({'is_active': "Can changed by admin user only"}, status=status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.owner or request.user.is_staff:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this product."}, status=status.HTTP_403_FORBIDDEN)
    
class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUserOrReadOnly]