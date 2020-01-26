import re
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message
from .models import Room
import requests
import csv
import re
User = get_user_model()

# Main Class for the app that allow users interact with WS


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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


#   on Connect i send the last 50 messages

    def fetch_messages(self, data):
        #       messages = Message.last_50_messages(self,)
        messages = Message.last_50_messagesROOM(self, data['id_room'])
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

        # When bot is actives
        m = re.search(r'/stock=.*([^\s]+)', message_from)  # search REGEX
        if m is not None:
            stock_quote_name = m.group(0)[7:]
            csv_url = "https://stooq.com/q/l/?s=" + \
                stock_quote_name + "&f=sd2t2ohlcv&h&e=csv"
            quote = self.getQuoteFromCSV_url(csv_url)
            content_bot_message = stock_quote_name + " quote is $" + quote + " per share"
            bot_message = {'id': 'bot', 'author': 'bot',
                           'content': content_bot_message, 'timestamp': 'HORA'}
            Botcontent = {
                'command': 'new_message',
                'message': bot_message
            }
            self.send_chat_message(Botcontent)

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

    # Send the message
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # TWO TYPES OF COMMANDS
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Bot call the Quote API from CSV
    def getQuoteFromCSV_url(self, csv_url):
        with requests.Session() as s:
            download = s.get(csv_url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)  # get list
            index_Close = my_list[0].index('Close')  # get the index Close
            quoute_value = my_list[1][index_Close]
            print(csv_url)
            return quoute_value  # Str
