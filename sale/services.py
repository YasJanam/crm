from .models import *
from .serializers import *
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db.models import F, Func, FloatField, Avg
from django.db.models import Q
from decimal import Decimal

class DateTimeDifference(Func):
    function = 'EXTRACT'
    template = "EXTRACT(EPOCH FROM %(function)s::timestamp - %(expressions)s::timestamp) / 86400" # محاسبه تفاضل بر حسب روز
    output_field = FloatField()



    
class FunnelAnalytics:
    
    @classmethod
    def leadToDealRate(cls,start_time=None,end_time=None):
        lead_filter = Q()

        if start_time:
            lead_filter &= Q(created_at__gte = start_time)
        if end_time:
            lead_filter &= Q(created_at__lte = end_time)

        leads = Lead.objects.filter(lead_filter).count()


        deal_filter =  Q()

        if start_time:
            deal_filter &= Q(lead__created_at__gte = start_time)
        if end_time:
            deal_filter &= Q(lead__created_at__lte = end_time)

        deals = Deal.objects.filter(deal_filter).count()
    
        return (deals/leads)*100 if leads > 0 else 0
    

    
   
    
    @classmethod
    def winRates(cls,start_time=None,end_time=None):
        time_filter =  Q()

        if start_time:
            time_filter &= Q(created_at__gte = start_time)
        if end_time:
            time_filter &= Q(created_at__lte = end_time)

        wins = Deal.objects.filter(
            status = Deal.Status.WON
        ).filter(time_filter).count()

        close_filter = ~Q(status= Deal.Status.OPEN)
        closed = Deal.objects.filter(
            close_filter
        ).filter(time_filter).count()

        return (wins /  closed) * 100 if closed > 0 else 0
    

    

    @classmethod
    def dropRatePerStageX(cls,stage,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q(entered_at__gte = start_time)
        if end_time:
            time_filter &= Q(entered_at__lte = end_time)

        losts = DealStageHistory.objects.filter(
            stage=stage,
            is_lost=True,
        ).filter(time_filter).count()

        all = DealStageHistory.objects.filter(
            stage=stage,
        ).filter(time_filter).count()
        
        return (losts/all) * 100 if all!=0 else 0


    

    @classmethod
    def stageConversionRate(cls,stage,start_time=None,end_time=None):
        time_filter = Q()
        if start_time:
            time_filter &= Q(entered_at__gte = start_time)
        if end_time:
            time_filter &= Q(entered_at__lte = end_time)        

        next_stage = Stage.objects.filter(
            order__gt=stage.order
        ).order_by('order').first()

        if not next_stage:
            return 0.0

        entered_next_stage = DealStageHistory.objects.filter(
            stage=next_stage,
            #is_deleted=False,
        ).filter(time_filter).count()

        entered_stage = DealStageHistory.objects.filter(
            stage=stage,
            #is_deleted=False,
        ).filter(time_filter).count()

        return (entered_next_stage/entered_stage) * 100 if entered_stage != 0 else 0


    

    @classmethod
    def averageDealSize(cls,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q( created_at__gte = start_time)
        if end_time:
            time_filter &= Q(created_at__lte = end_time)  
            
        deals = Deal.objects.filter(
            #is_deleted=False,
            status = Deal.Status.WON,
        ).filter(time_filter).count()

        totalRevenue = cls.totalRevenue(start_time,end_time)

        return (Decimal(totalRevenue) / Decimal(deals)) if deals!=0 else Decimal(0)
    

  

    @classmethod
    def totalRevenue(cls,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q( created_at__gte = start_time)
        if end_time:
            time_filter &= Q(created_at__lte = end_time)  
            
        return Deal.objects.filter(
            #is_deleted=False,
            status = Deal.Status.WON,
        ).filter(time_filter).aggregate(
            total=Sum('amount')
        )['total'] or 0      
    


    
    @classmethod
    def forecastRevenue(cls,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q( created_at__gte = start_time)
        if end_time:
            time_filter &= Q(created_at__lte = end_time) 
            
        return Deal.objects.filter(
            #is_deleted = False,
            status = Deal.Status.OPEN,
        ).filter(
            time_filter
        ).annotate(
            mul = F('amount') * (F('probability')/100)
        ).aggregate(
            total=Sum('mul')
        )['total'] or 0


 


    @classmethod
    def averageSalesCycle(cls,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q( created_at__gte = start_time)
        if end_time:
            time_filter &= Q(created_at__lte = end_time) 
            
        sales_cycles = Deal.objects.filter(
            #is_deleted=False,
            closed_at__isnull = False,
            status = Deal.Status.WON,
        ).filter(
            time_filter
        ).annotate(
            time_difference = DateTimeDifference(F('closed_at'),F('created_at'))
        ).aggregate(average_time_difference=Avg('time_difference'))

        return sales_cycles['average_time_difference'] if sales_cycles['average_time_difference'] else 0





    @classmethod
    def averageTimeInStageX(cls,stage,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q(entered_at__gte = start_time)
        if end_time:
            time_filter &= Q(entered_at__lte = end_time) 
            
        deal_stages = DealStageHistory.objects.filter(
            entered_at__isnull=False,
            exited_at__isnull=False,
            stage = stage,
        ).filter(
            time_filter
        ).annotate(
            time_difference = DateTimeDifference(F('exited_at'),F('entered_at'))
        ).aggregate(average_time = Avg('time_difference'))

        return deal_stages['average_time'] if deal_stages['average_time'] else 0
    


   
    
    
    @classmethod
    def salesRepWinRate(cls,user,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q(created_at__gte = start_time)
        if end_time:
            time_filter &= Q(created_at__lte = end_time) 
            
        wons = Deal.objects.filter(
            #is_deleted=False,
            status = Deal.Status.WON,
            assigned_to = user,
        ).filter(
            time_filter
        ).count()

        total = Deal.objects.filter(
            #is_deleted=False,
            assigned_to = user,
        ).filter(
            time_filter
        ).count()

        return (wons/total)*100 if total > 0 else 0

    

    @classmethod
    def revenuePerRep(cls,start_time=None,end_time=None):
        time_filter = Q()
        

        if end_time:
            time_filter &= Q(date_joined__lt = end_time)

        total_revenue = cls.totalRevenue(start_time,end_time)

        salers = User.objects.filter(
            groups__name__in = ['saler'],
        ).filter(
            time_filter
        ).count()

        return total_revenue/salers if salers > 0 else 0


   
    
    @classmethod
    def conversionByLeadSource(cls,source,start_time=None,end_time=None):
        deal_filter = Q()
        if start_time:
            deal_filter &= Q(lead__created_at__gte = start_time)
        if end_time:
            deal_filter &= Q(lead__created_at__lte = end_time)

        wons = Deal.objects.filter(
            #is_delete=False,
            status = Deal.Status.WON,
            lead__source = source,
        ).filter(
            deal_filter
        ).count()

        lead_filter = Q()
        if start_time:
            lead_filter &= Q(created_at__gte = start_time)
        if end_time:
            lead_filter &= Q(created_at__lte = end_time)

        leads = Lead.objects.filter(
            #is_delete=False,
            source=source,
        ).filter(
            lead_filter
        ).count()

        return (wons/leads)*100 if leads > 0 else 0



    @classmethod
    def stuckDealRate(cls,stage,days,start_time=None,end_time=None):
        time_filter = Q()
        if start_time:
            time_filter &= Q(entered_at__gte = start_time)
        if end_time:
            time_filter &= Q(entered_at__lte = end_time)        

        deals = DealStageHistory.objects.filter( 
            #is_deleted = False,
            stage = stage,
            spent_time__gt = days,
        ).filter(
            time_filter
        ).values_list('deal',flat=True).distinct().count()


        closed = DealStageHistory.objects.filter(
            #is_deleted=False,
            stage=stage,         
        ).filter(
            time_filter
        ).values_list('deal',flat=True).distinct().count()

        return (deals/closed)*100 if closed > 0 else 0


        
    @classmethod
    def LostReasonPercentage(cls,reason,start_time=None,end_time=None):
        time_filter = Q()
        
        if start_time:
            time_filter &= Q(created_at__gte = start_time)
        if end_time:
            time_filter &= Q(created_at__lte = end_time)
            
        reason_deals = Deal.objects.filter(
            #is_deleted=False,
            status = Deal.Status.LOST,
            lost_reason = reason,
        ).filter(
            time_filter
        ).count()

        lost_deals = Deal.objects.filter(
            #is_deleted=False,
            status=Deal.Status.LOST,
        ).filter(
            time_filter
        ).count()

        return (reason_deals / lost_deals)*100 if lost_deals > 0 else 0 
