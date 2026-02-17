
from rest_framework import serializers
from .models import * 
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer
from company.models import Company
from company.serializers import CompanySerializer , LeadSerializer



class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['name','order','is_won','is_lost',]


class DealStageHistorySerializer(serializers.ModelSerializer):
    stage = StageSerializer(read_only=True)
    class Meta:
        model = DealStageHistory
        fields = ['deal','stage','entered_at','exited_at',]


class DealSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    stages = DealStageHistorySerializer(read_only=True,many=True)
    lead = LeadSerializer(read_only=True)

    company_id = serializers.IntegerField(write_only=True)
    assigned_to_id = serializers.CharField(write_only=True)

    class Meta:
        model = Deal
        fields = ['company', 'title', 'amount', 'status','stages',
                    'assigned_to', 'is_deleted','probability',
                    'created_at', 'updated_at', 'created_by',
                    'company_id','assigned_to_id',
                    'lead',]
        
        read_only_fields = ['created_at', 'updated_at', 'created_by',]


    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['company'] = Company.objects.get(
            id = validated_data.pop('company_id')
        )
        if 'assigned_to' in validated_data:
            validated_data['assigned_to'] = User.objects.get(
                id = validated_data.pop('assigned_to_id')
            )
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        if 'company_id' in validated_data:
            validated_data['company'] = Company.objects.get(
            id = validated_data.pop('company_id')
            )
        if 'assigned_to_id' in validated_data:
            validated_data['assigned_to'] = User.objects.get(
            id = validated_data.pop('assigned_to_id')
            )
        return super().update(instance, validated_data)
    



class NegotiationSerializer(serializers.ModelSerializer):

    deal = DealSerializer(read_only=True)
    negotiator = UserSerializer(read_only=True)

    deal_id = serializers.IntegerField(write_only=True)
    negotiator_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Negotiation
        fields = ['deal', 'negotiator', 'proposed_amount', 'discount_percent', 'title',
                     'goal', 'summary', 'description', 'result', 'start_time', 'end_time',
                       'is_deleted', 'created_at', 'updated_at', 'created_by',]
        read_only_fields = ['updated_at','created_at', 'created_by',]
        

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['deal'] = Deal.objects.get(
            id = validated_data.pop('deal_id')
        )
        if 'negotiator_id' in validated_data:
            validated_data['negotiator'] = User.objects.get(
                id = validated_data.pop('negotiator_id')
            )
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        if 'deal_id' in validated_data:
            validated_data['deal'] = Deal.objects.get(
                id = validated_data.pop('deal_id')
            )
        if 'negotiator_id' in validated_data:
            validated_data['negotiator'] = User.objects.get(
                id = validated_data.pop('negotiator_id')
            )       
        return super().update(instance, validated_data)
    



class SaleSerializer(serializers.ModelSerializer):
    deal = DealSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    saler = UserSerializer(read_only=True)

    company_id = serializers.IntegerField(write_only=True)
    saler_id = serializers.CharField(write_only=True)
    deal_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Sale
        fields = ['company','saler','amount','description',
                    'created_at','updated_at',
                    'company_id','created_by',
                    'saler_id','deal','deal_id',
                    ]
        read_only_fields = ['created_at', 'updated_at','created_by',]


    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['company'] = Company.objects.get(
            id = validated_data.pop('company_id')
        )
        validated_data['saler'] = User.objects.get(
            id = validated_data.pop('saler_id')
        )

        if 'deal_id' in validated_data:
            validated_data['deal'] = Deal.objects.get(
                id = validated_data.pop('deal_id')
            )
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        if 'company_id' in validated_data:
            validated_data['company'] = Company.objects.get(
            id = validated_data.pop('company_id')
        )
            
        if 'saler_id' in validated_data:
            validated_data['saler'] = User.objects.get(
            id = validated_data.pop('saler_id')
        )
            
        if 'deal_id' in validated_data:
            validated_data['deal'] = Deal.objects.get(
                id = validated_data.pop('deal_id')
            )
        return super().update(instance, validated_data)
    
