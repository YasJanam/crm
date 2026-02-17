from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .services import *
from sale.serializers import DealSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction





class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.filter(is_deleted=False)
    
    @action(detail=True,methods=['delete'],url_path='delete')
    def delete_company(self,request,pk=None):
        try:
            with transaction.atomic():
                company = self.get_object()  
                company.is_deleted = True
                company.save()
                return Response(status=status.HTTP_204_NO_CONTENT) 
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    



class CompanyContactViewSet(ModelViewSet):
    queryset = CompanyContact.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyContactSerializer

    def get_queryset(self):
        qs = CompanyContact.objects.filter(is_deleted=False)
        company_id = self.request.query_params.get('company_id')
        if company_id:
            qs = CompanyContact.objects.filter(
                company__id=company_id,
                is_deleted=False
            )
        return qs
    
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
        


class LeadViewSet(ModelViewSet):
    queryset = Lead.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LeadSerializer

    def get_queryset(self):
        qs = Lead.objects.filter(
            is_deleted=False
        )
        user_id = self.request.query_params.get('user_id')
        if user_id:
            qs = Lead.objects.filter(
                is_deleted=False,
                assigned_to__id=user_id
            )
        return qs
           
    @action(detail=True,methods=['delete'],url_path='delete')
    def delete(self,request,pk=None):
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
        
    
    @action(detail=True,methods=['post'],url_path='convert-to-deal')
    def convert_lead_to_deal(self,request,pk=None):
        try:
            _ , lead ,_ = ConvertLeadService.main(request.data,pk)
            data =LeadSerializer(lead)
            return Response(data.data,status=status.HTTP_200_OK)
        
        except Exception as e:
           return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
      

    @action(detail=True,methods=['post'],url_path='qualify')
    def qualify(self,request,pk=None):
        try:
            obj = self.get_object()
            obj.status = obj.Status.QUALIFIED
            obj.save()
            data =LeadSerializer(lead)
            return Response(data.data,status=status.HTTP_200_OK)
        
        except Exception as e:
           return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        
      
    @action(detail=True,methods=['post'],url_path='disqualify')
    def disqualify(self,request,pk=None):
        try:
            obj = self.get_object()
            obj.status = obj.Status.DISQUALIFIED
            obj.save()
            data =LeadSerializer(lead)
            return Response(data.data,status=status.HTTP_200_OK)
        
        except Exception as e:
           return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 

    @action(detail=False,methods=['get'],url_path='mine')
    def my_leads(self,request):
        try:
            leads = Lead.objects.filter(
                assigned_to=request.user,
                is_deleted=False
                )
            data = LeadSerializer(leads,many=True)
            return Response(data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )