
from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import *
from .apis import *



urlpatterns = [
    

    # Funnel Analytics 
    path('kpis/lead-to-deal/', lead_to_deal_rate),
    path('kpis/win-rate/', win_rate),
    path('kpis/deal-size/avg/', average_deal_size),
    path('kpis/revenue/total/', total_revenue),
    path('kpis/revenue/forecast/', forecast_revenue),
    path('kpis/sales-cycle/avg/', average_sales_cycle),  
    path('kpis/revenue-per-rep/', revenue_per_rep),
    
        

    # strategic CRM KPIs
    path('kpis/active-deal/revenue/',revenue_per_active_deal),
    path('kpis/revenue/growth-rate/',revenue_growth_rate),
    path('kpis/forecast/accuracy/',forecast_accuracy),
    path('kpis/pipeline/velocity/',pipeline_velocity),
    path('kpis/pipeline/coverage-ratio/',pipeline_coverage_ratio),
    path('kpis/weighted-pipeline/',weighted_pipeline),
    
  


    # sale-rep kpis
    path('kpis/salesrep/win-rate/', sales_rep_win_rate),
    path('kpis/salesrep/revenue/',rep_revenue),
    path('kpis/quota/attainment-rate/',quota_attainment_rate),



    # stage kpis
    path('kpis/stage-time/avg/', average_time_in_stage_x), 
    path('kpis/stage-drop-rate/', drop_rate_per_stage_x),
    path('kpis/stage-conversion/', stage_conversion_rate),
    path('kpis/deals/stuck-rate/', stuck_deal_rate),



    # company kpis
    path('kpis/customer/concentration/',customer_concentration),
    path('kpis/customers/concentration/',top_customer_concentration),


    # source kpis
    path('kpis/source/conversion/', conversion_by_lead_source),


    # lost reason kpis
    path('kpis/deals/lost-reasons/', lost_reason_percentage),
]