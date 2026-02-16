from .models import Lead , Company
from sale.models import Deal 
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class ConvertLeadService:
   
    @classmethod
    def _get_or_create_company(cls,data,lead):

        if 'company_id' in data:
            try:
                return Company.objects.get(id=data["company_id"])
            except Company.DoesNotExist:
                raise ValidationError({"selected company not found"})
            
        elif 'company' in data:
            company_data = data['company']
            return Company.objects.create(
                name = company_data.get('name',lead.company_name or "new company"),
                phone = company_data.get('phone',lead.phone),
                email = company_data.get('email',lead.email),
                industry = company_data.get('industry'),
                address = company_data.get('address'),
                abbreviation = company_data.get('abbreviation'),
            )
        
        
        return Company.objects.create(
            name = lead.company_name or f"{lead.name} Company",
            phone = lead.phone,
            email = lead.email
        )
    
    @classmethod
    def _assign_user(cls,data,lead):
        if 'user_id' in data:
            userid = data['user_id']
            try:
                return User.objects.get(id=userid)
            except User.DoesNotExist:
                return lead.assigned_to
        return lead.assigned_to
        

    @classmethod
    def main(cls,data,lead_id):
        with transaction.atomic():
           
            lead = Lead.objects.get(id=lead_id)
            lead.is_converted = True
            lead.converted_at = timezone.now()
            lead.save()
            
            company = cls._get_or_create_company(data,lead)
            assigned_to = cls._assign_user(data,lead)

            _deal = data.get('deal',{})
            deal =  Deal.objects.create(
                    company = company,
                    title = _deal.get('title',f"{lead.name} deal"),
                    amount = _deal.get('amount'),
                    assigned_to = assigned_to
                )
            return deal , lead , company
            
      
            
            

