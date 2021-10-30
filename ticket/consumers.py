import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class TicketConsumer(WebsocketConsumer):
    def connect(self):
        group_name = str(self.scope["user"].id)
        async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def send_notification(self, event):
        self.send(text_data=json.dumps(event["text"]))
