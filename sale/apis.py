
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
from .services import FunnelAnalytics

  
def _get_start_end_times(request):

    start_time_str = request.data.get('start_time')
    end_time_str = request.data.get('end_time')

    try:
        start_time = date.fromisoformat(start_time_str) if start_time_str else None
        end_time = date.fromisoformat(end_time_str) if end_time_str else None
    except ValueError:
        raise ValidationError("Invalid date format. Use YYYY-MM-DD.")
    
    if start_time and end_time:
        if start_time > end_time:
            raise ValidationError("Start date must be before end date")
    return start_time , end_time


def _get_stage(request):
    try:
        stage = Stage.objects.get(
            id = request.data.get('stage_id')
        )
    except Stage.DoesNotExist:
        raise ValidationError("stage not found")
    return stage   


def _get_user(request):
    try:
        user = User.objects.get(
            id = request.data.get('user_id')
        )
    except User.DoesNotExist:
        raise ValidationError("user not found")
    return user
        

# lead-to-deal-rate
@api_view(['GET'])
def lead_to_deal_rate(request):
    start_time , end_time = _get_start_end_times(request)   
    rate = FunnelAnalytics.leadToDealRate(start_time,end_time)  
    return rate


# win-rate/
@api_view(['GET'])
def win_rate(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.winRates(start_time,end_time)
    return rate



@api_view(['GET'])
def drop_rate_per_stage_x(request):
    stage = _get_stage(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.dropRatePerStageX(stage,start_time,end_time)
    return rate



@api_view(['GET'])
def stage_conversion_rate(request):
    stage = _get_stage(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.stageConversionRate(stage,start_time,end_time)
    return rate



@api_view(['GET'])
def average_deal_size(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.averageDealSize(start_time,end_time)
    return rate



@api_view(['GET'])
def total_revenue(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.totalRevenue(start_time,end_time)
    return rate


@api_view(['GET'])
def forecast_revenue(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.forecastRevenue(start_time,end_time)
    return rate



@api_view(['GET'])
def average_sales_cycle(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.averageSalesCycle(start_time,end_time)
    return rate



@api_view(['GET'])
def average_time_in_stage_x(request):
    stage = _get_stage(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.averageTimeInStageX(stage,start_time,end_time)
    return rate


@api_view(['GET'])
def sales_rep_win_rate(request):
    user = _get_user(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.salesRepWinRate(user,start_time,end_time)
    return rate


@api_view(['GET'])
def revenue_per_rep(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.revenuePerRep(start_time,end_time)
    return rate



@api_view(['GET'])
def conversion_by_lead_source(request):
    source = request.data.get('source')

    if source not in Lead.Source.choices:
        raise ValidationError("منبع شده تعریف نشده است")
    
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.conversionByLeadSource(source,start_time,end_time)
    return rate  


@api_view(['GET'])
def stuck_deal_rate(request):
    days = request.data.get('days')

    if not isinstance(days,int):
        raise ValidationError("تعداد روز باید عدد باشد")
    if days < 0 :
        raise ValidationError("تعداد روز ها نمیتواند منفی باشد")
    
    stage = _get_stage(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.stuckDealRate(stage,days,start_time,end_time)
    return rate  


@api_view(['GET'])
def lost_reason_percentage(request):
    reason = request.data.get('reason')
    if reason not in Deal.LostReason.choices:
        raise ValidationError("علت شکست تعریف نشده است")
    
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.LostReasonPercentage(reason,start_time,end_time)
    return rate 


