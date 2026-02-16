from .models import Lead , Company
from sale.models import Deal 
from django.db import transaction
from django.utils import timezone

class LeadService:

    def convert_lead(self,lead_id):
        with transaction.atomic():
            lead = Lead.objects.get(
                id = lead_id
            )
            lead.is_converted = True
            lead.converted_at = timezone.now()
            lead.save()

            company = Company.objects.create(
                name = lead.company_name,
                phone_number = lead.phone,
                email = lead.email,  
            )

            deal = Deal.objects.create(
                company=company,
                assigned_to=lead.assigned_to
            )

        return deal




