from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .services import *

from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction



class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.filter(is_deleted=False)

    @action(detail=True,methods=['delete'],url_path='delete')
    def delete_object(self,request,pk=None):
        try:
            with transaction.atomic():
                obj = self.get_object()  
                obj.is_deleted = True
                obj.save()
                return Response(status=status.HTTP_204_NO_CONTENT) 
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        



class DealViewSet(ModelViewSet):
    queryset = Deal.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = DealSerializer

    def get_queryset(self):
        return Deal.objects.filter(
            is_deleted=False,
            #status = 'open',
            )
    
    @action(detail=True,methods=['delete'],url_path='delete')
    def delete_object(self,request,pk=None):
        try:
            with transaction.atomic():
                obj = self.get_object()  
                obj.is_deleted = True
                obj.save()
                return Response(status=status.HTTP_204_NO_CONTENT) 
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    @action(detail=True,methods=['post'],url_path='close')
    def close_deal(self,request,pk=None):
        try:
            with transaction.atomic():
                obj = self.get_object()
                obj.status = obj.Status.CLOSED
                obj.save()
                data = DealSerializer(obj)
                return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    @action(detail=True,methods=['post'],url_path='open')
    def open_deal(self,request,pk=None):
        try:
            with transaction.atomic():
                obj = self.get_object()
                obj.status = obj.Status.OPEN
                obj.save()
                data = DealSerializer(obj)
                return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    """
    حرکت به هر استیجی که میخاهیم
    مدل آزاد
    """
    @action(detail=True,methods=['post'],url_path='move-stage')
    def move_stage(self,request,pk=None):
        try:
            with transaction.atomic():
                obj = self.get_object()
                stageid = request.data.get('stage_id')
                stage = Stage.objects.get(
                    id = stageid
                )
                if stage.is_lost or stage.is_won:
                    raise ValidationError({
                        "error":"deal_closed",
                        "detail":"Cannot move stage because this deal is already closed"
                    })
                obj.move_to_stage(stage) 
                data = DealSerializer(obj)
                return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    """
    حرکت به استیج بعدی
    مدل خطی
    """
    @action(detail=True,methods=['post'],url_path='next-stage')
    def next_stage(self,request,pk=None):
        try:
            with transaction.atomic():
                obj = self.get_object()
                stage_order = request.data.get('stage_order')
                
                stage = Stage.objects.get(order=stage_order)
                if stage.is_lost or stage.is_won:
                    raise ValidationError({
                        "error":"deal_closed",
                        "detail":"Cannot move stage because this deal is already closed"
                    })
                
                next_stage = Stage.objects.filter(order__gt=stage_order).order_by('order').first()
                if not next_stage:
                    return Response(
                        {"error": "No next stage found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                obj.move_to_stage(next_stage)
                obj.save()
                data = DealSerializer(obj)
                return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

    @action(detail=True,methods=['post'],url_path='assign-user')
    def assign_user_byid(self,request,pk=None,userid=None):
        try:
            with transaction.atomic():
                deal = Deal.objects.get(id=pk)
                user = User.objects.get(id=userid)
                deal.assigned_to = user
                deal.save()
                data = DealSerializer(deal)
                return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        