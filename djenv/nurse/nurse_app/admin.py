from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(reg_tbl)
admin.site.register(Nurse)
admin.site.register(Patient)
admin.site.register(ServiceRequest)
