from django.db import models


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

    def __str__(self):
        return self.ticker



