from datetime import date
from time import sleep
from django.db import models
import yfinance as yf
from django.core.mail import send_mail


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

        msg_venda = ("{} - preço de VENDA R${} foi atingido.").format(pedido.ativo, pedido.precovenda)
        msg_compra = ("{} - preço de COMPRA R${} foi atingido.").format(pedido.ativo, pedido.precocompra)
        msg_fim = ('Sua operação com {} terminou!').format(pedido.ativo)

        while today != end_day: 
            #pega preço atual do ticker
            cotacao = round(ticker.info['regularMarketPrice'], 2)

            if cotacao >= pedido.precovenda:
                send_mail('StockWatch Alerta!', msg_venda,'admin@stockwatch.com',
                            [pedido.email], fail_silently=False,)

            elif cotacao <= pedido.precocompra:
                send_mail('StockWatch Alerta!', msg_compra,'admin@stockwatch.com',
                            [pedido.email], fail_silently=False,)
            else:
                pass

            sleep(int(periodo))

        send_mail('StockWatch Alerta!', msg_fim,'admin@stockwatch.com',
                    [pedido.email], fail_silently=False,)
    



