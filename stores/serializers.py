from rest_framework import serializers

from .models import *
class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        
class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
