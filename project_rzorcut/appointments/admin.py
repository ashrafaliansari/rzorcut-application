from django.contrib import admin
from .models import Store,Appointment,EmailOTP
# Register your models here.
admin.site.register(Store)
admin.site.register(Appointment)
admin.site.register(EmailOTP)