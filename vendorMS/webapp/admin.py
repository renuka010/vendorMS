from django.contrib import admin
from .models import Vendor, PurchaseOrder, Performance

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(Performance)
