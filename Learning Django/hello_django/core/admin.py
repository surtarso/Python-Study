## interface adminstrativa automatica

from django.contrib import admin
from core.models import Pessoa
# Register your models here.

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade')
    list_filter = ('nome')

admin.site.register(Pessoa)