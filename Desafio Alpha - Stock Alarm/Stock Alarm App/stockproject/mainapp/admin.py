from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message  #, AlarmIbovespa

#working
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

# #WIP
# admin.site.register(AlarmIbovespa)