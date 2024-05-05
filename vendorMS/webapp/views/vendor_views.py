from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication

from ..models import Vendor
from ..serializers import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
