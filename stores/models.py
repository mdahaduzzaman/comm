import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shop_owner")
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Shop'
        verbose_name = _('Shop')
        verbose_name_plural = _('Shops')

    def __str__(self):
        return self.name

    
def category_image_upload_path(instance, filename):
    """A utility function for generating category image upload path"""
    return f'Category/Image/{instance.name}_{filename}'

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=70, unique=True)
    category_image = models.ImageField(upload_to=category_image_upload_path)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        print("delete category")
        # Delete the image file from the file system
        if self.category_image:
            storage, path = self.category_image.storage, self.category_image.path
            if path and storage.exists(path):
                storage.delete(path)
        # Call the superclass delete method to delete the instance
        super().delete(*args, **kwargs)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    short_description = models.TextField(max_length=300)
    long_description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.OneToOneField('stores.ProductImage', null=True, blank=True, on_delete=models.CASCADE, related_name='main_product')

    class Meta:
        db_table = 'Product'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title[:15]

def product_image_upload_path(instance, filename):
    """A utility function for generating category image upload path"""
    return f'Product/Image/{instance.product.title[:10]}_{filename}'

class ProductImage(models.Model):
    image = models.ImageField(upload_to=product_image_upload_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ProductImage'
        verbose_name = _('ProductImage')
        verbose_name_plural = _('ProductImages')
