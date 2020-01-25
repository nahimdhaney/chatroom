from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


# room Model
class Room(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name
# Message Model


class Message(models.Model):
    room = models.ForeignKey('chat.Room', models.CASCADE)
    author = models.ForeignKey(
        User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_50_messages(self):
        return Message.objects.order_by('timestamp').all()[:50]

    def last_50_messagesROOM(self, room):
        return Message.objects.order_by('timestamp').all()[:50]
