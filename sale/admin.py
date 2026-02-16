from django.contrib import admin
from .models import *


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    list_display = ('company','saler','amount','description',
                    'created_at','updated_at','created_by',
                    )
 

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('company', 'title', 'amount', 'status', 
                     'assigned_to', 'is_deleted','probability',
                    'created_at', 'updated_at', 'created_by',
                    'lead',
                    )
    
@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = (
        'name','order','is_won','is_lost',
    )

@admin.register(DealStageHistory)
class DealStageHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'stage','deal','entered_at','exited_at',
    )

@admin.register(Negotiation)
class NegotiationAdmin(admin.ModelAdmin):
    list_display = ('deal', 'negotiator', 'proposed_amount', 'description', 
                    'result', 'is_deleted', 'created_at', 
                    'updated_at', 'created_by',)


