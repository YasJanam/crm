
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import *
from .apis import *



router = DefaultRouter()
router.register(r'sales',SaleViewSet,basename='sales')
router.register(r'deals',DealViewSet,basename='deals')



urlpatterns = [
    path('',include(router.urls)),
]