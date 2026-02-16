
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *



class UserLeadsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # /user/leads/{user_id}/
    def get(self,userid):
        try:
            leads = Lead.objects.filter(
                assigned_to__id=userid,
                is_delete=False
            )
            data = LeadSerializer(leads,many=True)
            return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({e})
    

    # /my/leads/
    def get(self):
        try:
            user = self.request.user
            leads = Lead.objects.filter(
                assigned_to__id = user.id,
                is_delete=False
            )
            data = LeadSerializer(leads,many=True)
            return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({e})






class CompanyConcatsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    # /company/{company_id}/concats/
    def get(self,comany_id):
        try:
            concats = Company.objects.filter(
                company__id=comany_id,
                is_deleted=False,
                is_active=True,
            )
            data = CompanyContactSerializer(concats,many=True)
            return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({e})
        
    