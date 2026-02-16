
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from .models import *
from .serializers import *



class UserDealsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    # /user/deals/{user_id}/
    def get(self,userid):
        try:
            deals = Deal.objects.filter(
                assigned_to__id=userid,
                is_delete=False
            )
            data = DealSerializer(deals,many=True)
            return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({e})
    

    # /my/deals/
    def get(self):
        try:
            user = self.request.user
            deals = Deal.objects.filter(
                assigned_to__id = user.id,
                is_delete=False
            )
            data = DealSerializer(deals,many=True)
            return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({e})
        




class UserSalesAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # /user/sales/{userid}/
    def get(self,userid):
        try:
            sales = Sale.objects.filter(
                saler__id=userid,
                is_deleted=False
            )
            data = SaleSerializer(sales,many=True)
            return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({e})
    
    # /my/sales/
    def get(self):
        try:
            user = self.request.user
            sales = Sale.objects.filter(
                saler__id=user.id,
                is_deleted=False
            )
            data = SaleSerializer(sales,many=True)
            return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({e})
