
from rest_framework import serializers
from .models import Interaction 

from django.contrib.auth.models import User
from accounts.serializers import UserSerializer
from company.serializers import CompanySerializer


class InteractionSerializer(serializers.ModelSerializer):
    saler = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    saler_username = serializers.CharField(write_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Interaction
        fields = ['saler', 'company', 'type', 'title', 'objective',
                   'note', 'start_date', 'end_time', 'score',
                   'is_deleted', 'created_at', 'updated_at',
                    'created_by',
                    'saler_username','company_id',]
        
        read_only_fields = ['created_at', 'updated_at','created_by',]
