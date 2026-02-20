
from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import *
from .apis.kpi_views import *



urlpatterns = [
    

    # Funnel Analytics 
    path('analytics/lead-to-deal/', lead_to_deal_rate),
    path('analytics/win-rate/', win_rate),
    path('analytics/stage-drop-rate/', drop_rate_per_stage_x),
    path('analytics/stage-conversion/', stage_conversion_rate),
    path('analytics/deal-size/avg/', average_deal_size),
    path('analytics/revenue/total/', total_revenue),
    path('analytics/revenue/forecast/', forecast_revenue),
    path('analytics/sales-cycle/avg/', average_sales_cycle),
    path('analytics/stage-time/avg/', average_time_in_stage_x),
    path('analytics/salesrep/win-rate/', sales_rep_win_rate),
    path('analytics/salesrep/revenue/', revenue_per_rep),
    path('analytics/source/conversion/', conversion_by_lead_source),
    path('analytics/deals/stuck-rate/', stuck_deal_rate),
    path('analytics/deals/lost-reasons/', lost_reason_percentage),
        

        
]