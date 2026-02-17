from django.contrib import admin
from .models import *



@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('saler', 'company', 'type', 'title',
                     'objective', 'note', 'start_date', 
                    'end_time', 'score', 'is_deleted', 'created_at', 
                    'updated_at', 'created_by',)
    

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'company', 'deal', 'lead',
        'title', 'description', 'assigned_to',
          'due_data', 'status', 'is_deleted',
            'created_at', 'updated_at', 'created_by',
    )


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'remind_at', 
                    'user', 'is_sent', 'method', 'created_at',)