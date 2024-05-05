from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from webapp.models import Vendor, Performance

# Update Performance Table every Sunday at 12:00 AM
# Ensure Performance Table is updated with latest data from the Vendor Table
# for Historical Performance Tracking


def update_performance():
    for vendor in Vendor.objects.all():
        Performance.objects.create(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=vendor.on_time_delivery_rate,
            quality_rating_avg=vendor.quality_rating_avg,
            average_response_time=vendor.average_response_time,
            fulfillment_rate=vendor.fulfillment_rate,
        )


scheduler = BackgroundScheduler()
scheduler.add_job(update_performance, 'cron',
                  day_of_week='sun', hour=0, minute=0)
scheduler.start()
