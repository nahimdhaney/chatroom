import re
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message
from .models import Room
import re
from . import tasks
User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name.strip()
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # Send message to room group LOGIN
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': 'new login'
            }
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # receiving message from in commands and exec

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    def task_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

#   on Connect i send the last 50 messages

    def fetch_messages(self, data):
        #       messages = Message.last_50_messages(self,)
        messages = reversed(
            Message.last_50_messagesROOM(self, data['id_room']))
#        import pdb
#        pdb.set_trace()

        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    # New Message from user
    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        roomObj = Room.objects.get(pk=data['id_room'])
        message_from = data['message']
#       roomObj = Room.objects.get(id=1)
        message = Message.objects.create(
            author=author_user,
            content=message_from,
            room=roomObj
        )

        # Regex check to send to bot
        for key in self.api_request:
            # search REGEX
            m = re.search(r'^/' + key + '=.*([^\s]+)', message_from)
            if m is not None:
                self.api_request[key](self, m)

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    # Converte message to Json

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }
    # Convert a lot of messages to json

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    # Call Quote Request
    def quote_request(self, m):
        # executing robotCall
        tasks.robotCall.delay(m.group(0)[7:], self.room_group_name)

    # Send the message

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # TWO TYPES OF COMMANDS to call
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    # API REQUESTS
    api_request = {
        'stock': quote_request,
    }

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
