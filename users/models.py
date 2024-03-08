from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

from .managers import UserManager

def user_avatar_upload_path(instance, filename):
    """A utility function for generating User avatar upload path"""
    return f'User/Avatar/{instance.full_name}_{instance.id}_{filename}'

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model for adding avatar and email field is the username field and take the full name"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('Email address'), unique=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_path, blank=True, null=True, verbose_name=_('Avatar'))
    is_active = models.BooleanField(_('Active status'), default=False)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    full_name = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(_('Date joined'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modification time'),auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'User'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def delete(self, *args, **kwargs):
        print("The object")
        # Delete the image file from the file system
        if self.avatar:
            storage, path = self.avatar.storage, self.avatar.path
            if path and storage.exists(path):
                storage.delete(path)
        # Call the superclass delete method to delete the instance
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
   
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
        
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

