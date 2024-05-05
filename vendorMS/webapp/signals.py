from .models import PurchaseOrder, Performance
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models import Sum
from django.utils import timezone
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_save, sender=PurchaseOrder)
def update_metrics_completed_orders(sender, instance, **kwargs):
    try:
        sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        return

    # Update quality rating
    if (instance.quality_rating is not None and instance.status == 'completed'):
        vendor = instance.vendor
        new_quality_rating_avg = ((sender.objects.filter(vendor=instance.vendor, quality_rating__isnull=False).aggregate(Sum('quality_rating'))['quality_rating__sum']
                                   + instance.quality_rating)
                                  / sender.objects.filter(vendor=instance.vendor,
                                                          quality_rating__isnull=False).count()+1)
        vendor.quality_rating_avg = round(new_quality_rating_avg, 2)
        vendor.save()

    if ((sender.objects.get(id=instance.id).status != instance.status)
            and instance.status == 'completed'):
        number_of_total_po = sender.objects.filter(
            vendor=instance.vendor).count()
        vendor = instance.vendor

        # Update on-time delivery rate in Percentage
        prev_on_time_delivery = (
            vendor.on_time_delivery_rate * number_of_total_po)/100
        current_delivery = 1 if (sender.objects.get(
            id=instance.id).delivery_date >= instance.delivery_date) else 0
        vendor.on_time_delivery_rate = round(((prev_on_time_delivery + current_delivery)
                                              / number_of_total_po)*100, 2)

        # Update fulfillment rate in Percentage
        number_of_completed_po = sender.objects.filter(
            vendor=instance.vendor, status='completed').count()+1
        vendor.fulfillment_rate = round(
            (number_of_completed_po/number_of_total_po)*100, 2)

        vendor.save()
        # Update Delivery date as order is completed
        instance.delivery_date = timezone.now()


@receiver(pre_save, sender=PurchaseOrder)
def update_response_time(sender, instance, **kwargs):
    try:
        sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        return
    if ((sender.objects.get(id=instance.id).acknowledgment_date != instance.acknowledgment_date)
            and instance.acknowledgment_date is not None):
        current_response_time = (
            instance.acknowledgment_date - instance.issue_date).total_seconds() / (24 * 60 * 60)
        vendor = instance.vendor
        new_response_time = ((vendor.average_response_time
                              + current_response_time)
                             / (sender.objects.filter(vendor=instance.vendor,
                                                      acknowledgment_date__isnull=False).count() + 1))
        vendor.average_response_time = round(new_response_time, 2)
        vendor.save()
