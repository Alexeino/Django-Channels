from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json

class TestConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data = json.dumps({ "status":"connected to django channel"}))

    def receive(self, text_data):
        print(text_data)

    def disconnect(self, close_code):
        # Called when the socket closes
        print("Dissconnected")
    
    def send_notification(self,event):
        print('send notification')
        data = json.loads(event.get('value'))
        self.send(text_data = json.dumps({
            'payload':data
        }))
        print('send notification')


class MyAsyncConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.room_name = "new_consumer"
        self.room_group_name = "new_consumer_group"

        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data = json.dumps({ "status":"connected to django channel with Async JSON Web Socket"}))
    async def receive(self, text_data):
        print(text_data)

    async def disconnect(self, close_code):
        # Called when the socket closes
        print("Dissconnected")

    async def send_notification(self,event):
        print('send notification')
        data = json.loads(event.get('value'))
        await self.send(text_data = json.dumps({
            'payload':data
        }))
        print('send notification')