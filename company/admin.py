from django.contrib import admin
from .models import *



@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست نمایش داده می‌شوند
    list_display = ('name','abbreviation','is_deleted',
                    'phone','type',
                    'industry','email','address','description',
                    'created_at','updated_at','created_by',)
 


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
   
    list_display = ('name','phone','email',
                    'assigned_to','company_name',
                    'status','description','is_deleted',
                    'is_converted','converted_at',
                    'source',
                    'created_at','updated_at','created_by',)


@admin.register(CompanyContact)
class CompanyContactAdmin(admin.ModelAdmin):
    list_display = (
        'name','phone','email',
        'company','role',
        'is_active',  'is_deleted',
       'created_at','updated_at','created_by',
    )
