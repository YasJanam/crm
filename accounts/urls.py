
from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .apis import *

urlpatterns = [
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path('user-role/',UserRoleAPIView.as_view(),name="user-role"),
]