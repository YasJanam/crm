
from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import *
from .apis import *



router = DefaultRouter()
router.register(r'sales',SaleViewSet,basename='sales')
router.register(r'deals',DealViewSet,basename='deals')
router.register(r'stages',StageViewSet,basename='stages')
router.register(r'deal-stage-histories',DealStageHistoryViewSet,basename='deal-stage-histories')



urlpatterns = [
    path('',include(router.urls)),

        
]