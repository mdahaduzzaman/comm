from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_registration),
    path('activate-account/<uidb64>/<token>/', activate_account, name='activate_account'),
    
    path('token/', CustomTokenObtainPairView.as_view(), name='CustomTokenObtainPairView'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='CustomTokenRefreshView'),
    path('logout/', logout, name='logout'),
    
    path('request-password-reset/', request_password_reset, name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
]
