from django.contrib import admin

from main.models import Mercado, Ativo, Pedido

"""
Regitrar aqui faz com que a database seja 
acessivel pelo django admin (/admin) mas
não afeta se ela pode ser modificada ou não.
"""


admin.site.register(Mercado)
admin.site.register(Ativo)
admin.site.register(Pedido)

