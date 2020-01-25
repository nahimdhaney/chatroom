from django.contrib import admin


from chat.models import Room

from chat.models import Message

admin.site.register(Room)
admin.site.register(Message)
