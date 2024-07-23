# CHATROOM CHALLENGE

This Django Project use redis and celery to manage chat-rooms.

with /stock='quote' you'll call a bot and he is going to send a message to the room.

## To run the backend, run:

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

if you have problem with requirements:

```
pip install django
pip install channels
pip install channels_redis
pip install django-nose
pip install celery

```

how to use:

```
1. Install redit: https://redis.io/ run in the standard port
2.1) Windows - https://redislabs.com/blog/redis-on-windows-10/
2.2) docker - https://hub.docker.com/_/redis/
3. Make sure you have an instance of redis running.
4. Make sure you have celery Working correctly.
5. Login with users user1 and user2 with the password 'admin' to test
6. go to http://127.0.0.1:8000/chat/ log in and try.
7. enjoy.
```

IMPORTANT - how to run celery and tests

```
celery : celery -A chatroom worker -l info -P eventlet
tests: nosetests

```

use the bot

```
with the command **/stock='quote'** you will call a bot and it will send a message to the room.

example:

/stock=aapl.us
```

Please note this is a **demo project**

if you require any further information please contact me :
Nahim Terrazas
SC - Bolivia
