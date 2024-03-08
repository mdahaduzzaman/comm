from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_active', 'is_staff']
    
    def delete_queryset(self, request, queryset):
        """To delete the respective image from the storage"""
        for obj in queryset:
            obj.delete()
