from django.contrib import admin
from .models import CustomUser, Report
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Report)