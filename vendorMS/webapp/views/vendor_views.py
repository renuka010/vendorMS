from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from ..models import Vendor
from ..serializers import VendorSerializer
from django.shortcuts import get_object_or_404


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = get_object_or_404(Vendor, pk=pk)
        performance_data = Vendor.objects.filter(pk=pk).values(
            'on_time_delivery_rate', 
            'quality_rating_avg', 
            'average_response_time', 
            'fulfillment_rate'
        )
        return Response(performance_data[0])