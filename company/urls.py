
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import *
#from .apis import *


router = DefaultRouter()
router.register(r'leads',LeadViewSet,basename='leads')

router.register(r'companies',CompanyViewSet,basename='companies')
router.register(r'company/contacts',CompanyContactViewSet,basename='company/contacts')



urlpatterns = [
        path('',include(router.urls)),
        
]