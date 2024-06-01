from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Vendor, Performance
from ..serializers import PerformanceSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    # Retrieve the Vendor instance
    vendor = get_object_or_404(Vendor, id=vendor_id)

    # Retrieve all Performance instances associated with this Vendor
    performances = Performance.objects.filter(vendor=vendor)

    # Serialize the performances
    performance_serializer = PerformanceSerializer(performances, many=True)

    return Response(performance_serializer.data)
