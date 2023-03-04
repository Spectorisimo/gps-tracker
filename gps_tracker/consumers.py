import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GPSDataConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        await self.channel_layer.group_add('gps_data', self.channel_name)
        await self.accept()

    async def websocket_receive(self, event):
        pass

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('gps_data', self.channel_name)

    async def send_coordinates(self, event):
        coordinates = event['coordinates']
        await self.send(text_data=json.dumps(coordinates))
