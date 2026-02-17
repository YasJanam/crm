from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *



class InteractionViewSet(ModelViewSet):
    queryset = Interaction.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = InteractionSerializer

    def get_queryset(self):
        qs = Interaction.objects.filter(
            is_deleted=False
        )
        return qs
    


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = Task.objects.filter(
            is_deleted=False
        )
        return qs    
    

    
class ReminderViewSet(ModelViewSet):
    queryset = Reminder.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ReminderSerializer