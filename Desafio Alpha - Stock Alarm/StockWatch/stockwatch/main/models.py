from datetime import date
from time import sleep
from django.db import models
import yfinance as yf


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
        return str(self.criado) #ordema por criacao na database


    def iniciaOperacao(pedido):
        today = date.today()  #data inicio da operacao
        end_day = pedido.duracao  #data final da operacao
        periodo = int(pedido.periodo) * 60  #tempo entre precos
        ticker = yf.Ticker(pedido.ativo+".SA")  #ticker escolhido

        while today != end_day: 
            #pega preço atual do ticker
            cotacao = round(ticker.info['regularMarketPrice'], 2)

            #PLACEHOLDER: adicionar sistema de email
            if cotacao >= pedido.precovenda:
                print("\nPreço de VENDA atingido---> enviado para:")
            elif cotacao <= pedido.precocompra:
                print("\nPreço de COMPRA atingido---> enviado para:")
            else:
                pass

            sleep(int(periodo))

        print("este deveria ser um email avisando q o processo acabou")
    



