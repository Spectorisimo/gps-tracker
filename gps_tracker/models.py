from django.db import models

# Create your models here.
class GPSData(models.Model):
    date = models.DateTimeField()
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    altitude = models.IntegerField()
    sattelites = models.IntegerField()
    speed = models.IntegerField()
    def __str__(self):
        return f"Запись {self.id}"


