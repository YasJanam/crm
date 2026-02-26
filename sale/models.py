from django.db import models
from django.contrib.auth.models import User
from company.models import  Company , Lead
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django.db import transaction
from datetime import datetime,timedelta



class Stage(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ],unique=True)
    is_terminal = models.BooleanField(default=False,blank=True)
    #is_won = models.BooleanField(default=False,blank=True)
    #is_lost = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return f"{self.name}({self.order})"



class Deal(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='deals')
    current_stage = models.ForeignKey(Stage,on_delete=models.SET_NULL,null=True,blank=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    amount = models.DecimalField(max_digits=15,decimal_places=2,blank=True,null=True)
    probability = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(100)],blank=True,null=True)
    class Status(models.TextChoices):
        OPEN = "open","Open" 
        #CLOSED = "closed","Closed"
        WON = 'won', 'Won'
        LOST = 'lost', 'Lost'


    status = models.CharField(max_length=15,choices=Status.choices,
                              default=Status.OPEN,blank=True)  
     
    """
    price(قیمت): مشتری به دلیل قیمت بالاتر از رقبا، خرید را انجام نداد.
    Competition (رقابت): مشتری محصول یا خدمات رقبا را انتخاب کرد.
    No Need (نیاز نداشت): مشتری در نهایت متوجه شد که به محصول یا خدمات شما نیازی ندارد.
    Lack of Budget (کمبود بودجه): مشتری بودجه کافی برای خرید محصول یا خدمات شما را ندارد.
    Poor Product/Service Fit (تناسب ضعیف محصول/خدمات): محصول یا خدمات شما با نیازهای مشتری مطابقت ندارد.
    Lost Contact (از دست دادن ارتباط): نتوانستیم با مشتری ارتباط برقرار کنیم.
    Technical Issues (مشکلات فنی): مشکلات فنی مانع از بستن قرارداد شد.
    """
    class LostReason(models.TextChoices):
        PRICE = 'price','Price'
        COMPETITION = 'competition','Competition'
        NO_NEED = 'no_need','No Need'
        LACK_OF_BUDGET = 'lack_of_budget','Lack Of Budget'
        POOR_PRODUCT_SERVICE_WEEK = 'poor_product_service_week','Poor Product/Service Week'
        LOST_CONTACT = 'lost_contact','Lost Contact'
        TECHNICAL_ISSUES = 'technical_issues','Technical Issues'
        OTHER = 'other','Other'

    lost_reason = models.CharField(max_length=255,choices=LostReason.choices,
                                   null=True,blank=True)

    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,null=True,blank=True)

    # کارشناس فروش
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='deals')
    # زمان قراردادی پایان کار
    expected_close_date = models.DateTimeField(blank=True,null=True)
    
    closed_at = models.DateTimeField(blank=True,null=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return f"{self.title}({self.company.name})"


    def move_to_stage(self,new_stage):
        if self.current_stage == new_stage:
            return
        
        DealStageHistory.objects.filter(
            deal=self,
            stage=self.current_stage,
            exited_at__isnull=True
        ).update(exited_at=timezone.now(),is_lost= (self.status == self.Status.LOST))
       

        DealStageHistory.objects.create(
            deal=self,
            stage=new_stage,
            entered_at=timezone.now()
        )

        self.current_stage=new_stage
        self.save(update_fields=["current_stage"])



class DealStageHistory(models.Model):
    stage = models.ForeignKey(Stage,on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal,on_delete=models.CASCADE,related_name='stages')
    entered_at = models.DateTimeField(null=True,blank=True,default=None)
    exited_at = models.DateTimeField(null=True,blank=True,default=None)
    is_lost = models.BooleanField(default=False,blank=True)

    @property
    def spent_time(self,mode='day'):
        if self.entered_at and self.exited_at:
            time_difference = self.exited_at - self.entered_at
            return time_difference.days
        else:
            return None




class Negotiation(models.Model):
    deal = models.ForeignKey(Deal,on_delete=models.CASCADE)
    negotiator = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='negotiates')

    proposed_amount = models.DecimalField(max_digits=15,decimal_places=2,
                                          blank=True,null=True)
    discount_percent = models.FloatField(default=0)
    
    class Result(models.TextChoices):
        pending = 'pending','Pending'
        accepted = 'accepted' , 'Accepted'
        rejected = 'rejected','Rejected'

    title = models.CharField(max_length=255,blank=True,null=True)
    goal = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True,null=True)
    result = models.TextField(blank=True)

    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)





class Sale(models.Model):
    deal = models.ForeignKey(Deal,on_delete=models.CASCADE,blank=True,null=True)

    company = models.ForeignKey(Company,on_delete=models.SET_NULL,blank=True,null=True)
    saler = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sales') 
    amount = models.IntegerField(blank=True,null=True)


    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)

