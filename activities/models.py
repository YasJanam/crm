from django.db import models
from company.models import Company
from sale.models import Deal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator , MaxValueValidator


class Interaction(models.Model):
    saler = models.ForeignKey(User,on_delete=models.CASCADE,related_name='interactions')
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='interactions')

    class Type(models.TextChoices):
        CALL = 'call' , 'Call'
        MEETING = 'meeting' , 'Meeting'
        EMAIL = 'email', 'Email'
        SUPPORT = 'support','Support'
        
    

    type = models.CharField(max_length=100,choices=Type.choices,default=Type.EMAIL)

    title = models.CharField(max_length=300,blank=True,null=True)
    objective = models.TextField(blank=True,null=True) # هدف از تعامل
    note = models.TextField(blank=True,null=True)
    start_date = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)

    score = models.IntegerField(validators=[
        MinValueValidator(0),MaxValueValidator(100)
    ],blank=True,default=0)

    is_deleted = models.BooleanField(default=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)



class Task(models.Model):

    class Status(models.TextChoices):
        TODO = 'todo', 'TODO'
        IN_PROGRESS = 'in-progress' ,'In-progress'
        DONE = 'done' , 'Done'
        CANCELLED = 'cancelled' , 'Cancelled'

    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='tasks')
    deal = models.ForeignKey(Deal,on_delete=models.CASCADE,blank=True,null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)

    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,
                                    blank=True,null=True,related_name='tasks')

    due_data = models.DateTimeField()
    status = models.CharField(max_length=25,choices=Status.choices,default=Status.TODO)

    is_deleted = models.BooleanField(default=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)




"""
class Reminder(models.Model):

"""