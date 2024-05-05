from rest_framework import serializers
from .models import Vendor, PurchaseOrder, Performance


class VendorSerializer(serializers.ModelSerializer):
    """
    Serializer for Vendor model"""
    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ('on_time_delivery_rate',
                            'quality_rating_avg',
                            'average_response_time',
                            'fulfillment_rate',)


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for PurchaseOrder model"""
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ('acknowledgment_date',)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be more than 0.")
        return value

    def validate_status(self, value):
        if self.instance and self.instance.status == 'completed' and self.instance.status != value:
            raise serializers.ValidationError(
                "You cannot change the status of a completed purchase order.")
        return value


class PerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Performance model"""
    class Meta:
        model = Performance
        fields = '__all__'
