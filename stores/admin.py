from django.contrib import admin

from .models import *

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'is_active']
    
    def delete_queryset(self, request, queryset):
        """To delete the respective image from the storage"""
        for obj in queryset:
            obj.delete()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    
    def delete_queryset(self, request, queryset):
        """To delete the respective image from the storage"""
        for obj in queryset:
            obj.delete()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'is_active']
    
    def delete_queryset(self, request, queryset):
        """To delete the respective image from the storage"""
        for obj in queryset:
            obj.delete()

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'is_active']
    
    def delete_queryset(self, request, queryset):
        """To delete the respective image from the storage"""
        for obj in queryset:
            obj.delete()