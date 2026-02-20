from sale.models import *
from sale.serializers import *
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
    
    """
    simple OCR : created deals / created leads
    """
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
            time_filter &= Q( closed_at__gte = start_time)
        if end_time:
            time_filter &= Q(closed_at__lte = end_time)  
            
        return Deal.objects.filter(
            #is_deleted=False,
            status = Deal.Status.WON,
        ).filter(time_filter).aggregate(
            total=Sum('amount')
        )['total'] or 0   

    
    # شرط اینو باید درست کنم ---> یک مشکلی داره فیلتر زمانش
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

    # ==================================================================================================
    # --------------------------------------- STRATEGIC CRM KPIs ---------------------------------------

    """
    pipeline velocity :
    (number of deals * average deal size * win rate) / length of sale cycle
    """
    @classmethod
    def pipeline_velocity(cls,start_time=None,end_time=None):
        deal_time_filter = Q()

        if start_time:
            deal_time_filter &= Q(closed_at__gt = start_time) | Q(closed_at__isnull=True)
        if end_time:
            deal_time_filter &= Q(created_at__lt = end_time) 

        deals = Deal.objects.filter(
            deal_time_filter
        ).count() 

        average_deal_size = cls.averageDealSize(start_time,end_time)

        win_rate = cls.winRates(start_time,end_time)

        sale_cycle = cls.averageSalesCycle(start_time,end_time)

        if sale_cycle == 0:
            return 0
        return (deals * average_deal_size * win_rate) / sale_cycle
        


    """
    اگر زمان ها خالی باشند به طور خودکار مقدار دهی میشوند
    برای این فرمول مقادیر بازهِ زمانی لازم هست. چون یک مقایسه صورت میگیرد

    """
    @classmethod
    def revenue_growth_rate(cls,days=30,start_time=None,end_time=None,default_days=60):
        if not end_time:
            end_time = timezone.now()
        if not start_time:
            start_time = end_time - timedelta(default_days)

        previous_start = start_time - timedelta(days)
        previous_end = end_time - timedelta(days)

        revenue = cls.totalRevenue(start_time,end_time)
        previos_revenue = cls.totalRevenue(previous_start,previous_end)

        if previos_revenue == 0:
            return 0
        return ((revenue - previos_revenue) / previos_revenue) * 100
    


    """
    forecast_accuracy:
    (Actual-Revenue / Forecast-Revanue) * 100   
    """
    @classmethod
    def forecast_accuracy(cls,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q(closed_at__gt=start_time)
        if end_time:
            time_filter &= Q(closed_at__lt = end_time)

        closed_deals = Deal.objects.filter(
            status__in = [Deal.Status.WON,Deal.Status.LOST]
        ).filter(
            time_filter
        )

        forecast = closed_deals.aggregate(
            total = Sum(F('amount')*F('probability')/100)
        )['total'] or 0

        actual = closed_deals.filter(
            status = Deal.Status.WON
        ).aggregate(
            total = Sum(F('amount'))
        )['total'] or 0

        if forecast == 0:
            return 0
        
        return (actual / forecast) * 100
    


    @classmethod
    def customer_concentration(cls,company,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q(closed_at__gt=start_time)
        if end_time:
            time_filter &= Q(closed_at__lt=end_time)

        customer_revenue = Deal.objects.filter(
            status = Deal.Status.WON,
            company = company
        ).filter(
            time_filter
        ).aggregate(
            total = Sum(F('amount'))
        )['total'] or 0

        revenue = cls.totalRevenue(start_time,end_time)

        if revenue == 0:
            return 0
        
        return (customer_revenue/revenue) * 100
    

    @classmethod
    def top_customer_concentration(cls,top_n=5,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q(closed_at__gt=start_time)
        if end_time:
            time_filter &= Q(closed_at__lt = end_time)

        customer_revenues = Deal.objects.filter(
            status = Deal.Status.WON
        ).filter(
            time_filter
        ).values('company').annotate(
            total = Sum('amount')
        ).order_by('-total')[:top_n]

        total_top = sum([item['total'] for item in customer_revenues])
        total_revenue = cls.totalRevenue(start_time,end_time)

        if total_revenue == 0:
            return 0
        
        return (total_top / total_revenue) * 100
    


    @classmethod
    def pipeline_coverage_ratio(cls,goal,start_time,end_time):
        time_filter = Q()
        """
        این فیلتر برای پیدا کردن دیل هایی هست که توی باز گفته شده باز بودن
        """
        if start_time:
            time_filter &= Q(closed_at__gt = start_time) | Q(closed_at__isnull=True)
        if end_time:
            time_filter &= Q(created_at__lt = end_time) 

        pipeline_value = Deal.objects.filter(
            time_filter,
            Q(amount__isnull=False)
        ).aggregate(
            total = Sum(F('amount'))
        )['total'] or 0

        if goal == 0:
            return float('inf') if pipeline_value > 0 else 0
        
        return pipeline_value / goal
    


    @classmethod
    def weighted_pipeline(cls,start_time=None,end_time=None):
        time_filter = Q()
        """
        این فیلتر برای پیدا کردن دیل هایی هست که توی باز گفته شده باز بودن
        """
        if start_time:
            time_filter &= Q(closed_at__gt = start_time) | Q(closed_at__isnull=True)
        if end_time:
            time_filter &= Q(created_at__lt = end_time) 
        
        amount = Deal.objects.filter(
            time_filter,
            Q(amount__isnull=False),
            Q(probability__isnull=False)
        ).annotate(
            weighted = F('amount')*F('probability')/100
        ).aggregate(
            total = Sum('weighted')
        )['total'] or 0

        return amount  


    @classmethod
    def rep_revenue(cls,user,start_time=None,end_time=None):
        time_filter = Q()

        if start_time:
            time_filter &= Q(closed_at__gt = start_time) 
        if end_time:
            time_filter &= Q(closed_at__lt = end_time)   

        revene = Deal.objects.filter(
            assigned_to = user,
            status = Deal.Status.WON
        ).filter(
            time_filter
        ).aggregate(
            total = Sum('amount')
        )['total'] or 0

        return revene

    """
    (rep revenue / assigned quota) * 100
    """
    @classmethod
    def quota_attainment_rate(cls,user_rep,quota,start_time=None,end_time=None):
        rep_revenue = cls.rep_revenue(user_rep,start_time,end_time)    

        if quota == 0:
            return float('inf') if rep_revenue > 0 else 0
        return (rep_revenue / quota) * 100  
    

    """
    sale-productivity -> (revenue / sale time)

    دو متد زیر باید چک شوند
    حذف شود ؟؟ sale آیا نیاز هست مدل 
    """
    @classmethod
    def sale_productivity(cls,sale):
        sale_hours = DateTimeDifference(sale.deal.closed_at,sale.deal.created_at)
        return sale.deal.amount / sale_hours if sale_hours!=0 else 0
    
    @classmethod
    def sales_productivity_average(cls,start_time=None,end_time=None):
        time_filter = Q()
        if start_time:
            time_filter &= Q(deal__created_at__gt=start_time)
        if end_time:
            time_filter &= Q(deal__created_at__lt=end_time)

        average = Sale.objects.filter(
            deal__closed_at__isnull =False,
            deal__amount__isnull =False
        ).filter(
            time_filter
        ).annotate(
            times = DateTimeDifference(F('deal.closed_at'),F('deal.created_at'))
        ).aggregate(
            total_amount = Sum('deal__amount'),
            total_time = Sum('times')
        )

        amount = average['total_amount']
        time = average['total_time']

        return amount/time if time!=0 else 0
    

    """
    revenue per active deal -> active = open
    (total revenue / open deals)
    پتانسیل درآمدی آینده
    این فرمول روی دیل های باز کار میکنه

    """
    @classmethod  
    def revenue_per_active_deal(cls,start_time,end_time):
        time_filter = Q()

        if start_time:
            time_filter &= Q( created_at__gte = start_time)
        if end_time:
            time_filter &= Q(created_at__lte = end_time)  
            
        return Deal.objects.filter(
            status = Deal.Status.OPEN,
        ).filter(time_filter).aggregate(
            total=Avg('amount')
        )['total'] or 0  