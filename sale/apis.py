
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from datetime import date
from .models import *
from .serializers import *
#from .services import FunnelAnalytics



@api_view(['GET']) 
def get_lost_reasons(request):
    try:
        reasons = Deal.LostReason
        lost_reasons = [
            {'value':reason.value,'label':reason.label}
            for reason in reasons
        ]
        return Response(lost_reasons)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )     
  