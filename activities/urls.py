
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import *



router = DefaultRouter()
router.register(r'tasks',TaskViewSet,basename='tasks')

router.register(r'interactions',InteractionViewSet,basename='interactions')
router.register(r'reminders',ReminderViewSet,basename='reminders')



urlpatterns = [
        path('',include(router.urls)),
        
]