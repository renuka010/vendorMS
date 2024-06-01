from django.urls import path, include
from .views.vendor_views import VendorViewSet
from .views.purchase_order_views import PurchaseOrderViewSet
from .views.performance_views import vendor_performance
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('vendors/<int:vendor_id>/performances',
         vendor_performance, name='vendor_performance'),
]
