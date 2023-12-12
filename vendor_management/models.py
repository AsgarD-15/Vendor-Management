from django.db import models
from django.db.models import Count, Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from rest_framework.authtoken.models import Token

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def update_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed').count()
        on_time_deliveries = self.purchaseorder_set.filter(
            status='completed',
            delivery_date__lte=timezone.now()
        ).count()

        if completed_pos > 0:
            self.on_time_delivery_rate = (on_time_deliveries / completed_pos) * 100
        else:
            self.on_time_delivery_rate = 0

    def update_quality_rating_avg(self):
        completed_pos = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        avg_rating = completed_pos.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']

        if avg_rating:
            self.quality_rating_avg = avg_rating
        else:
            self.quality_rating_avg = 0

    def update_average_response_time(self):
        completed_pos = self.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
        response_times = completed_pos.annotate(
            response_time=models.F('acknowledgment_date') - models.F('issue_date')
        ).aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
        if response_times:
            self.average_response_time = response_times.total_seconds() / 60 
        else:
            self.average_response_time = 0

    def update_fulfillment_rate(self):
        total_pos = self.purchaseorder_set.count()
        successful_fulfillments = self.purchaseorder_set.filter(status='completed').count()

        if total_pos > 0:
            self.fulfillment_rate = (successful_fulfillments / total_pos) * 100
        else:
            self.fulfillment_rate = 0
    def needs_update(self):
        # print(self)
        threshold_time = timezone.now() - timezone.timedelta(hours=1)
        last_update_time = self.__dict__.get('_date_modified', None)
        return last_update_time and last_update_time < threshold_time

    def save_historical_performance(self):
        historical_performance = HistoricalPerformance(
            vendor=self,
            date=timezone.now(),
            on_time_delivery_rate=self.on_time_delivery_rate,
            quality_rating_avg=self.quality_rating_avg,
            average_response_time=self.average_response_time,
            fulfillment_rate=self.fulfillment_rate,
        )
        historical_performance.save()
        
    def update_performance_metrics(self):
        self.update_on_time_delivery_rate()
        self.update_quality_rating_avg()
        self.update_average_response_time()
        self.update_fulfillment_rate()
        self.save()
    
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.po_number} - {self.vendor.name}"
   
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"