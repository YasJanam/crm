
from rest_framework import serializers
from .models import * 

from django.contrib.auth.models import User
from accounts.serializers import UserSerializer
from company.serializers import CompanySerializer , LeadSerializer
from sale.serializers import DealSerializer



class InteractionSerializer(serializers.ModelSerializer):
    saler = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    saler_id = serializers.IntegerField(write_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Interaction
        fields = ['saler', 'company', 'type', 'title', 'objective',
                   'note', 'start_date', 'end_time', 'score',
                   'is_deleted', 'created_at', 'updated_at',
                    'created_by','saler_id',
                    'saler_id','company_id',]
        
        read_only_fields = ['created_at', 'updated_at','created_by',]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['company'] = Company.objects.get(
            id = validated_data.pop('company_id')
        )
        validated_data['saler'] = User.objects.get(
            id = validated_data.pop('saler_id')
        )
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'company' in validated_data:
            validated_data['company'] = Company.objects.get(
                id = validated_data.pop('company_id')
            )
        if 'saler' in validated_data:
            validated_data['saler'] = User.objects.get(
                id = validated_data.pop('saler_id')
            )       
        return super().update(instance, validated_data)




class TaskSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    deal = DealSerializer(read_only=True)
    lead = LeadSerializer(read_only=True)

    company_id = serializers.IntegerField(write_only=True)
    deal_id = serializers.IntegerField(write_only=True)
    lead_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Task
        fields = ['company', 'deal', 'lead',
            'title', 'description', 'assigned_to',
          'due_data', 'status', 'is_deleted',
          'company_id','deal_id','lead_id',
            'created_at', 'updated_at', 'created_by',]
        read_only_fields = ['created_at', 'updated_at', 'created_by',]


    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        if 'company_id' in validated_data:
            validated_data['copmany'] = Company.objects.get(
                id = validated_data.pop('company_id')
            )
        if 'deal_id' in validated_data:
            validated_data['deal'] = Deal.objects.get(
                id = validated_data.pop('deal_id')
            )
        if 'lead_id' in validated_data:
            validated_data['lead'] = Lead.objects.get(
                id = validated_data.pop('lead_id')
            )
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        if 'company_id' in validated_data:
            validated_data['copmany'] = Company.objects.get(
                id = validated_data.pop('company_id')
            )
        if 'deal_id' in validated_data:
            validated_data['deal'] = Deal.objects.get(
                id = validated_data.pop('deal_id')
            )
        if 'lead_id' in validated_data:
            validated_data['lead'] = Lead.objects.get(
                id = validated_data.pop('lead_id')
            )        
        return super().update(instance, validated_data)
    


class ReminderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Reminder
        fields = ['title', 'description', 'remind_at', 
                    'user', 'is_sent', 'method', 'created_at',]
        
    def create(self, validated_data):
        validated_data['user_id'] = User.objects.get(
            id = validated_data.pop('user_id')
        )
        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        if 'user_id' in validated_data:
            validated_data['user_id'] = User.objects.get(
                id = validated_data.pop('user_id')
            )           
        return super().update(instance, validated_data)