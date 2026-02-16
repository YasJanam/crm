from django.db import models
from django.contrib.auth.models import User
from company.models import  Company
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django.db import transaction


class Sale(models.Model):
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,blank=True,null=True)
    saler = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sales') # created by = sale agent
    amount = models.IntegerField(blank=True,null=True)


    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)



class Stage(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ],unique=True)
    #is_terminal = models.BooleanField(default=False,blank=True)
    is_won = models.BooleanField(default=False,blank=True)
    is_lost = models.BooleanField(default=False,blank=True)



class Deal(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='deals')
    current_stage = models.ForeignKey(Stage,on_delete=models.SET_NULL,null=True,blank=True)
    title = models.CharField(255,blank=True,null=True)
    amount = models.DecimalField(max_digits=15,decimal_places=2,blank=True,null=True)
    probability = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(100)],blank=True,null=True)
    class Status(models.TextChoices):
        OPEN = "open","Open" 
        CLOSED = "closed","Closed"
       
    status = models.CharField(max_length=15,choices=Status.choices,
                              default=Status.OPEN,blank=True)

    # کارشناس فروش
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='deals')
    # زمان قراردادی پایان کار
    expected_close_date = models.DateTimeField(blank=True,null=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)


    def move_to_stage(self,new_stage):
        if self.current_stage == new_stage:
            return
        
        DealStageHistory.objects.filter(
            deal=self,
            exited_at__isnull=True
        ).update(exited_at=timezone.now())

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


"""
    def save(self, *args, **kwargs):
    
        if self.pk:  
            original = Deal.objects.get(pk=self.pk)
            if original.is_current_stage == False and self.is_current_stage == True: 
                self.start_at = timezone.now()
                self.end_at = None

            if original.is_current_stage == True and self.is_current_stage == False:
                    self.end_at = timezone.now()
        super().save(*args, **kwargs)"""




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

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)


