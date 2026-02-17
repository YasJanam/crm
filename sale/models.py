from django.db import models
from django.contrib.auth.models import User
from company.models import  Company , Lead
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django.db import transaction




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
    
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,null=True,blank=True)

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

