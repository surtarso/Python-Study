from django.contrib import admin

from main.models import Ativo, Mercado

# Register your models here.

admin.site.register(Mercado)
admin.site.register(Ativo)

