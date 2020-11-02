from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    
    # Override
    async def connect(self):
        # use self.scope["user"] to get reqeust user's information
        # i.e. print(self.scope['user'])
        # i.e. self.scope['url_route']['kwargs'] to get kwargs in request
        # i.e. self.scope['url_route']['kwargs']['room_number']

        # hardcoded for testing
        self.group = str(self.scope['url_route']['kwargs']['room_number'])
        # Add channel_name to the group
        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )

        await self.accept()

    # Override
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group,
            self.channel_name
        )

    async def receive(self, text_data):
        # Parsing incomming text_data
        text_message_json = json.loads(text_data)
        data = text_message_json['data'] + ", Response from the server"
        
        # send message to the room group
        await self.channel_layer.group_send(
            self.group,
            {
                'type': 'notification_message',
                'data': data
            }
        )
    
    async def notification_message(self, event):
        message = event['data']
        await self.send(text_data=json.dumps({
            'data':message
        }))
