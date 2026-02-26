
from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import *
from .apis import *



router = DefaultRouter()
router.register(r'sales',SaleViewSet,basename='sales')
router.register(r'deals',DealViewSet,basename='deals')
router.register(r'stages',StageViewSet,basename='stages')
router.register(r'deal/stages/histories',DealStageHistoryViewSet,basename='deal/stages/histories')



urlpatterns = [
    path('',include(router.urls)),

    path('deal-lost/reasons/',get_lost_reasons),


]