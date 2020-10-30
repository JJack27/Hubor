from channels.generic.websocket import WebsocketConsumer
import json

class NotificationConsumer(WebsocketConsumer):
    
    # Override
    def connect(self):
        print("Connecting")
        self.accept()

    # Override
    def disconnect(self):
        self.close()

    def receive(self, text_data):
        print(text_data)
        text_message_json = json.loads(text_data)
        message = text_message_json['message'] + ", Response from the server"
        print(message)
        self.send(text_data=json.dumps({
            'message': message
        }))