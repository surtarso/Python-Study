from django import forms

class AlertForm(forms.Form):
    name = forms.CharField(label="Nome", max_length=200)
    email = forms.EmailInput()
    ticker = forms.CharField(label="Ativo", max_length=200)
    precocompra = forms.CharField(label="Compra", max_length=200)
    precovenda = forms.CharField(label="Venda", max_length=200)
    periodo = forms.DurationField(label="Periodo")
    limite = forms.DateField(label="Duração")
    check = forms.BooleanField(label="Aceita")