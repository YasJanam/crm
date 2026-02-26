
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import *

class UserRoleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self,request):
        user = request.user
        groups = list(user.groups.values_list('name',flat=True))
        role = groups[0] if groups else None
        return Response({
            'id':user.id,
            'username':user.username,
            'role':role
        })