import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from core.models import Profile
from .models import Chat
from urllib.parse import parse_qsl




class ChatConsumer(WebsocketConsumer):

    def connect(self):
        query_params = dict(parse_qsl(self.scope['query_string'].decode('utf-8')))
        group = query_params['group']
        if Profile.objects.filter(uid=group).exists():
            self.room_group_name = str(group).replace('-', '')

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        chat_group_id = text_data_json['chat_group_id']
        sender = text_data_json['sender']        

        if not Profile.objects.filter(uid=chat_group_id).exists():
            return

        if sender != 'user' and sender != 'manager':
            return    

        new_chat_msg =  Chat.objects.create(
            profile = Profile.objects.get(uid=chat_group_id),
            sender = sender,
            message = message,
        )


        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'chat_group_id' : chat_group_id,
                'sender' : sender,
            }
        )

    def chat_message(self, event):
        message = event['message']
        chat_group_id = event['chat_group_id']
        sender = event['sender']

        if not Profile.objects.filter(uid=chat_group_id).exists():
            return
        if sender != 'user' and sender != 'manager':
            return

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'chat_group_id' : chat_group_id,
            'sender' : sender,
        }))
