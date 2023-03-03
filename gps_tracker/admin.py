from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.GPSData)
class GPSDataAdmin(admin.ModelAdmin):
    list_display = ['id','date','latitude','longitude','altitude','speed','sattelites']