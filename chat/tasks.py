# chat/tasks.py

# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
import csv
import json


@shared_task
def robotCall(m, room_group_name):
    stock_quote_name = m
    csv_url = "https://stooq.com/q/l/?s=" + \
        stock_quote_name + "&f=sd2t2ohlcv&h&e=csv"
    quote = getQuoteFromCSV_url(csv_url)
    content_bot_message = stock_quote_name + " quote is $" + quote + " per share"
    bot_message = {'id': 'bot', 'author': 'bot',
                   'content': content_bot_message, 'timestamp': 'now'}
    Botcontent = {
        'command': 'new_message',
        'message': bot_message
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'task_message',
            'message': Botcontent
        })
    return Botcontent


def getQuoteFromCSV_url(csv_url):
    with requests.Session() as s:
        download = s.get(csv_url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)  # get list
        index_Close = my_list[0].index('Close')  # get the index Close
        quoute_value = my_list[1][index_Close]
        print(csv_url)
        return quoute_value  # Str
