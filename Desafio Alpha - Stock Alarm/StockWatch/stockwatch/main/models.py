from datetime import date
from time import sleep
from django.db import models
from yahoo_fin.stock_info import *


##-----------------------------------------------------MERCADO:
class Mercado(models.Model):
    # um mercado tem varios ativos (one to many)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


##-----------------------------------------------------TICKERS:
class Ativo(models.Model):
    # varios ativos pertencem a um mercado (many to one)
    mercado = models.ForeignKey(Mercado, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=30)

    class Meta:
        # ordena por ordem alfabetica
        ordering = ['ticker']
    
    def __str__(self):
        return self.ticker

class Pedido(models.Model):
    email = models.EmailField()
    mercado = models.CharField(max_length=20)
    ativo = models.CharField(max_length=20)
    precocompra = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    precovenda = models.DecimalField(max_digits=6, decimal_places=2, default=0.01)
    periodo = models.IntegerField(default=15)
    duracao = models.DateField(default=date.today)
    checkbox = models.BooleanField(default=False)
    modificado = models.DateTimeField(auto_now=True) # snapshot every time
    criado = models.DateTimeField(auto_now_add=True) # snapshot once

    def __str__(self):
        return str(self.criado)

    def iniciaOperacao(pedido):
        print(pedido.email)
        print(pedido.mercado)
        print(pedido.ativo)
        print(pedido.precocompra)
        print(pedido.precovenda)
        print(pedido.periodo)
        print(pedido.duracao)  ## transformar em int!! (days from today)
        ## untested!!
        # dias = date.today - pedido.duracao
        # cotacoes = []
        # i = 0
        # while i != dias:
        #     #pega preço atual do ticker
        #     cotacao = "" ## GET TICKER PRICE!!!
        #     print(cotacao)
        #     #insere preço no inicio da tabela
        #     cotacoes.insert(0, cotacao)

        # #PLACEHOLDER: adicionar sistema de email
        # if cotacao >= float(pedido.precovenda):
        #     print("\nPreço de VENDA atingido---> enviado para:")
        # elif cotacao <= float(pedido.precocompra):
        #     print("\nPreço de COMPRA atingido---> enviado para:")
        # else:
        #     pass
        # sleep(int(pedido.periodo))
        # i += 1

    



