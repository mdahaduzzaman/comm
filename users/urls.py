from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_registration),
    path('activate-account/<uidb64>/<token>/', user_registration, name='activate_account'),
]
