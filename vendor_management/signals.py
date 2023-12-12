
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Vendor,PurchaseOrder,HistoricalPerformance
from django.conf import settings
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None,created=False, **kwargs):
    if created and not Token.objects.filter(user=instance).exists():
        Token.objects.create(user=instance)

@receiver(post_save, sender=Vendor)
def save_historical_performance(sender, instance, **kwargs):
    instance.save_historical_performance()

@receiver(post_delete, sender=Vendor)
def delete_historical_performance(sender, instance, **kwargs):
    HistoricalPerformance.objects.filter(vendor=instance).delete()
      
@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    vendor = instance.vendor
    vendor.update_performance_metrics()