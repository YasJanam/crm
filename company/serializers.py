from rest_framework import serializers
from .models import *
from accounts.serializers import UserSerializer



class CompanySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id','name','abbreviation','phone','is_deleted',
                  'industry','email','address','description',
                  'type',
                  'created_at','updated_at','created_by',]
        read_only_fields = ['created_at', 'updated_at','created_by']
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    


class CompanyContactSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CompanyContact
        fields = ['id','name','phone','email', 'company', 'role',
                   'created_at', 'updated_at',
                     'created_by',  'is_active','is_deleted',
                     'company_id',]
        read_only_fields = ['created_at', 'updated_at','created_by']
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['company'] = Company.objects.get(id=validated_data.pop('company_id'))
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        if 'company_id' in validated_data:
            validated_data['company'] = Company.objects.get(id=validated_data.pop('company_id'))
        return super().update(instance, validated_data)
    



class LeadSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.CharField(write_only=True)
    class Meta:
        model = Lead
        fields = ['name','phone','email',
                    'assigned_to','company_name',
                    'status','description','is_deleted',
                    'created_at','updated_at','created_by',
                    'is_converted','converted_at',
                    'source',
                    'company_id','assigned_to_id',]
        read_only_fields = ['created_at', 'updated_at','created_by','converted_at',]
        
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        if 'assigned_to_id' in validated_data:
            validated_data['assigned_to'] = User.objects.get(
                id = validated_data['assigned_to_id']
            )
        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        if 'assigned_to_id' in validated_data:
            validated_data['assigned_to'] = User.objects.get(
            id = validated_data['assigned_to_id']
            )
        return super().update(instance, validated_data)