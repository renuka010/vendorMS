from django.db import models


class Vendor(models.Model):
    """
    Vendor model to store vendor details

    name: Name of the vendor
    contact_details: Contact information of the vendor
    address: Physical address of the vendor
    vendor_code: - A unique identifier for the vendor.
    on_time_delivery_rate: Percentage of on-time deliveries
    quality_rating_avg: Average quality rating for purchase orders
    average_response_time: Average time taken to acknowldge purchase orders
    fulfillment_rate: Percentage of purchase orders fulfilled successfully"""

    name = models.CharField(max_length=255, blank=False)
    contact_details = models.TextField(blank=False)
    address = models.TextField(blank=False)
    vendor_code = models.CharField(max_length=100, unique=True, blank=False)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)


class PurchaseOrder(models.Model):
    """
    PurchaseOrder model to store purchase order details

    po_number: Purchase order number
    vendor: Foreign Key to the Vendor model
    order_date: Date when the order was placed
    delivery_date: Expected/actual delivery date of the order
    items: Details of items ordered
    quantity: Total quantity of items in the order
    status: Current status of the order
    quality_rating: Rating given to the vendor for this order
    issue_date: Timestamp when the order was issued to the vendor
    acknowledgment_date: Timestamp when the vendor acknowledged the order"""

    po_number = models.CharField(max_length=250, unique=True, blank=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=False)
    order_date = models.DateTimeField(blank=False)
    delivery_date = models.DateTimeField(blank=False)
    items = models.JSONField(blank=False)
    quantity = models.IntegerField(blank=False)
    status = models.CharField(choices=[
        ("pending", "order is pending"),
        ("completed", "order is completed"),
        ("canceled", "order is canceled")
    ], max_length=9, blank=False)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(blank=False)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


class Performance(models.Model):
    """
    Historical performance data for vendors

    vendor: Foreign Key to the Vendor model
    date: Date of the performance record
    on_time_delivery_rate: historical record of on-time delivery rate
    quality_rating_avg: historical record of average quality rating
    average_response_time: historical record of average response time
    fulfillment_rate: historical record of fulfillment rate
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
