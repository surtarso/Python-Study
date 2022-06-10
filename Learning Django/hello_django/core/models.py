## onde define o modelo de dados
## faz abstracao dos objetos de banco para python
## transforma o banco em classes

from django.db import models

# Create your models here.

class Pessoa(models.Model):
    name = models.CharField(max_length=200)
    idade = models.IntegerField()

###-------
## pessoa = Pessoa.objects.get(nome='Rafael')
# é o mesmo que:
## SELECT * FROM pessoa WHERE nome = 'Rafael';
###-------
