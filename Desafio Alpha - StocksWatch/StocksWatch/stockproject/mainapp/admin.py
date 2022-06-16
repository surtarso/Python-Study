from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, Mercado, Alerta

#forum DB
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

#alertas DB
admin.site.register(Mercado)
admin.site.register(Alerta)
