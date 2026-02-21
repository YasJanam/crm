
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from datetime import date
from sale.models import *
from sale.serializers import *
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
@api_view(['POST'])
def lead_to_deal_rate(request):
    start_time , end_time = _get_start_end_times(request)   
    rate = FunnelAnalytics.leadToDealRate(start_time,end_time)  
    return Response({"rate": rate}, status=status.HTTP_200_OK)


# win-rate/
@api_view(['POST'])
def win_rate(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.winRates(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)



@api_view(['POST'])
def drop_rate_per_stage_x(request):
    stage = _get_stage(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.dropRatePerStageX(stage,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)



@api_view(['POST'])
def stage_conversion_rate(request):
    stage = _get_stage(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.stageConversionRate(stage,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)



@api_view(['POST'])
def average_deal_size(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.averageDealSize(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)



@api_view(['POST'])
def total_revenue(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.totalRevenue(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)


@api_view(['POST'])
def forecast_revenue(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.forecastRevenue(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)



@api_view(['POST'])
def average_sales_cycle(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.averageSalesCycle(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)



@api_view(['POST'])
def average_time_in_stage_x(request):
    stage = _get_stage(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.averageTimeInStageX(stage,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)


@api_view(['POST'])
def sales_rep_win_rate(request):
    user = _get_user(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.salesRepWinRate(user,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)


@api_view(['POST'])
def revenue_per_rep(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.revenuePerRep(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)



@api_view(['POST'])
def conversion_by_lead_source(request):
    source = request.data.get('source')

    if source not in Lead.Source.choices:
        raise ValidationError("منبع شده تعریف نشده است")
    
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.conversionByLeadSource(source,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)  


@api_view(['POST'])
def stuck_deal_rate(request):
    days = request.data.get('days')

    if not isinstance(days,int):
        raise ValidationError("تعداد روز باید عدد باشد")
    if days < 0 :
        raise ValidationError("تعداد روز ها نمیتواند منفی باشد")
    
    stage = _get_stage(request)
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.stuckDealRate(stage,days,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)  


@api_view(['POST'])
def lost_reason_percentage(request):
    reason = request.data.get('reason')
    if reason not in Deal.LostReason.choices:
        raise ValidationError("علت شکست تعریف نشده است")
    
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.LostReasonPercentage(reason,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 


# ============================================================================
# --------------------------- strategic CRM KPIs -----------------------------

@api_view(['POST'])
def pipeline_velocity(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.pipeline_velocity(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK)     


@api_view(['POST'])
def revenue_growth_rate(request):
    days = request.data.get('days')
    if not days:
        days = 30

    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.revenue_growth_rate(days,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 



@api_view(['POST'])
def forecast_accuracy(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.forecast_accuracy(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 


@api_view(['POST'])
def customer_concentration(request):
    company_id = request.data.get('company_id')
    if not company_id:
        raise ValidationError("مشتری مربوطه را مشخص کنید")

    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise ValidationError("مشتری مربوطه را مشخص کنید")
    
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.customer_concentration(company,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 


@api_view(['POST'])
def top_customer_concentration(request):
    top_n = request.data.get('top_n')
    if not top_n:
        raise ValidationError("تعداد مشتری ها را مشخص کنید")

    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.top_customer_concentration(top_n,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 



@api_view(['POST'])
def pipeline_coverage_ratio(request):
    goal = request.data.get('goal')
    if not goal:
        raise ValidationError("هدف فروش را مشخص کنید")
    
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.pipeline_coverage_ratio(goal,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 


@api_view(['POST'])
def weighted_pipeline(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.weighted_pipeline(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 


@api_view(['POST'])
def rep_revenue(request):
    user_id = request.data.get('user_id')
    if not user_id:
        raise ValidationError("لطفا فرد مورد نظر را مشخص کنید")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValidationError('فرد مورد نظر وجود ندارد')
    
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.rep_revenue(user,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 


@api_view(['POST'])
def quota_attainment_rate(request):
    user_id = request.data.get('user_id')
    if not user_id:
        raise ValidationError("لطفا فرد مورد نظر را مشخص کنید")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValidationError('فرد مورد نظر وجود ندارد')
    
    qouta = request.data.get('qouta')
    if not qouta:
        raise ValidationError("مقدار سهمیه فروش فرد را مشخص کنید")
    
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.quota_attainment_rate(user,qouta,start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 


@api_view(['POST'])
def revenue_per_active_deal(request):
    start_time , end_time = _get_start_end_times(request) 
    rate = FunnelAnalytics.revenue_per_active_deal(start_time,end_time)
    return Response({"rate": rate}, status=status.HTTP_200_OK) 