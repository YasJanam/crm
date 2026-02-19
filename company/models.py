from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=350)

    # نام اختصاری اگر داره
    abbreviation = models.CharField(max_length=200,blank=True,null=True)

    phone = models.CharField(max_length=12)
    
    email = models.CharField(max_length=400)
    address = models.TextField()

    class Type(models.TextChoices):
        PROSPECT = 'prospect','Prospect'
        CUSTOMER = 'Customer','customer'

    type = models.CharField(max_length=20,choices=Type.choices,default=Type.PROSPECT)


    # صنعت 
    industry = models.CharField(max_length=200,blank=True,null=True)

    description = models.TextField(blank=True,null=True)
    is_deleted = models.BooleanField(default=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)





class CompanyContact(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="contacts")

    name = models.CharField(max_length=250)
    phone = models.CharField()
    email = models.CharField(max_length=400)
    role = models.CharField(max_length=250 ,blank=True,null=True)

    
    is_deleted = models.BooleanField(default=False,blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)

    is_active = models.BooleanField(default=True,blank=True)

    @property
    def is_deleted(self):
        return self.person.is_deleted or self.company.is_deleted    



class Lead(models.Model):
    name = models.CharField(max_length=60)
    company_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=60)
    assigned_to =  models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='leads')

    class Status(models.TextChoices):
        NEW = 'تازه وارد' , 'New' 
        QUALIFIED = 'تایید شده' , 'Qualified'
        CONTACTED = 'تماس گرفته شده' , 'Contacted'
        DISQUALIFIED = 'غیر قابل پیگیری','DisQualified'

    status = models.CharField(choices=Status.choices,verbose_name='status',
                              default=Status.NEW,blank=True)
    
    class Source(models.TextChoices):
        GOOGLE_ADS = 'google_ads','Google Ads'
        CONTENT_MARKETING = 'content_marketing','Content Marketing'
        REFERRAL = 'referral','Refferal'

    source = models.CharField(max_length=200,choices=Source.choices,default=Source.GOOGLE_ADS)
    
    # convert to deal
    is_converted = models.BooleanField(default=False,blank=True)
    converted_at = models.DateTimeField(blank=True,null=True,default=None)

    description = models.TextField(blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
"""
    def converte(self):
        self.is_converted = True
        self.converted_at = timezone.now()
        self.save(update_fields=["is_converted","converted_at"])"""
        

"""
    def save(self, *args, **kwargs):
        # Deal ثبت زمان تبدیل به 
        if self.pk:  
            original = Lead.objects.get(pk=self.pk)
            if original.is_converted != self.is_converted: 
                self.converted_at = timezone.now()
            
        super().save(*args, **kwargs)"""
