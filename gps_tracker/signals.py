from asgiref.sync import async_to_sync
from django.db.models import signals
from django.dispatch import receiver
from . import models
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


@receiver(signals.post_save, sender=models.GPSData)
def new_data_notification(sender, instance: models.GPSData, created: bool, **kwargs):
    if created:
        coordinates = {
            'latitude': str(instance.latitude),
            'longitude': str(instance.longitude),
        }
        async_to_sync(channel_layer.group_send)(
            'gps_data', {'type': 'send_coordinates', 'coordinates': coordinates}
        )
