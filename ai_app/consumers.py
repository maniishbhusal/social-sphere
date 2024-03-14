from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
import json
from asgiref.sync import async_to_sync


class ChatConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("connected", event)
        self.send({
            "type": "websocket.accept"
        })

        # Add the consumer to the "chat_group" group
        async_to_sync(self.channel_layer.group_add)(
            "chat_group", self.channel_name)

    def websocket_receive(self, event):
        print("receive", event)
        print(event['text'])
        self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    def chat_message(self, event):
        data = event['text']
        self.send({
            "type": "websocket.send",
            "text": data
        })

    def websocket_disconnect(self, event):
        print("disconnected", event)
        raise StopConsumer()
