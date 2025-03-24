from django.contrib import admin

# Register your models here.
from .models import CustomUser, Jewelry, Order

admin.site.register(CustomUser)
admin.site.register(Jewelry)
admin.site.register(Order)
