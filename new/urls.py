
# urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', CustomerUserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path("user/", get_user, name="get_user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

  
    path("user/update/", UpdateUserView.as_view(), name="update_user"),
    path("user/delete/", DeleteUserView.as_view(), name="delete_user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
]