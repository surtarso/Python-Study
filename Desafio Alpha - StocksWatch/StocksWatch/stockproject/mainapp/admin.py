from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, Mercado, Alerta, Ativo, StockDetail, CarteiraAtivo

#forum DB
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

#alertas DB
admin.site.register(Mercado)
admin.site.register(Ativo)
admin.site.register(Alerta)
admin.site.register(StockDetail)

#carteira de ativos
admin.site.register(CarteiraAtivo)