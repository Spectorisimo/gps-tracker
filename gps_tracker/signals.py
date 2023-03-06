from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .models import GPSData

channel_layer = get_channel_layer()

@receiver(post_save, sender=GPSData)
def new_data_notification(sender, instance, created, **kwargs):
    if created:
        coordinates = {
            'latitude': str(instance.latitude),
            'longitude': str(instance.longitude),
        }
        async_to_sync(channel_layer.group_send)(
            'gps_data', {'type': 'send_coordinates', 'coordinates': coordinates}
        )
