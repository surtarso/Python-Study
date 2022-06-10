from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Evento(models.Model):  # tabela chama 'core_eventos'
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True)
    # se o usuario for excluido, exclui todos seus eventos.
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #     ## manda a tabela se chamar 'evento'
    #     db_table = 'evento'
