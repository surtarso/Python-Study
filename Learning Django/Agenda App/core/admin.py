from django.contrib import admin
from core.models import Evento

# Register your models here.

#classe para representar os eventos de admin


class EventoAdmin(admin.ModelAdmin):
    #lista eventos por nome/data
    list_display = ('id', 'titulo', 'data_evento', 'data_criacao')
    list_filter = ('usuario', 'data_evento',)   ## add filtro lateral


#registra models.py[Eventos] e self EventoAdmin
admin.site.register(Evento, EventoAdmin)
