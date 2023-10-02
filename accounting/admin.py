from django.contrib import admin
from .models import PaymentCredentials, PackageSetting, Invoice
# Register your models here.

admin.site.register(PaymentCredentials)
admin.site.register(PackageSetting)
admin.site.register(Invoice)