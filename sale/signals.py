from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction

"""
@receiver(post_save, sender=Deal)
def create_deal_stages(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic:
            dealstages = []
            stages = Stage.objects.all()
            for stage in stages:
                dealstages.append(
                    DealStage(
                        stage=stage,
                        deal = sender
                    )
                )
            DealStage.objects.bulk_create(dealstages)
"""