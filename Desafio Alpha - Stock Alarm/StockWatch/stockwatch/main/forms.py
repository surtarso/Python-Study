from django import forms
from yahoo_fin.stock_info import *
from stockwatch.settings import DEBUG


##--------------------------------------------FORMULARIO PARA ALERTAS:
class AlertForm(forms.Form):

    if DEBUG: #harcoded:
        tickers = [('ABEV3', 'ABEV3'), ('AZUL4', 'AZUL4'), ('B3SA3', 'B3SA3'), ('BBAS3', 'BBAS3'), ('BBDC3', 'BBDC3'), ('BBDC4', 'BBDC4'), ('BBSE3', 'BBSE3'), ('BEEF3', 'BEEF3'), ('BPAC11', 'BPAC11'), ('BRAP4', 'BRAP4'), ('BRDT3', 'BRDT3'), ('BRFS3', 'BRFS3'), ('BRKM5', 'BRKM5'), ('BRML3', 'BRML3'), ('BTOW3', 'BTOW3'), ('CCRO3', 'CCRO3'), ('CIEL3', 'CIEL3'), ('CMIG4', 'CMIG4'), ('COGN3', 'COGN3'), ('CPFE3', 'CPFE3'), ('CRFB3', 'CRFB3'), ('CSAN3', 'CSAN3'), ('CSNA3', 'CSNA3'), ('CVCB3', 'CVCB3'), ('CYRE3', 'CYRE3'), ('ECOR3', 'ECOR3'), ('EGIE3', 'EGIE3'), ('ELET3', 'ELET3'), ('ELET6', 'ELET6'), ('EMBR3', 'EMBR3'), ('ENBR3', 'ENBR3'), ('ENGI11', 'ENGI11'), ('EQTL3', 'EQTL3'), ('FLRY3', 'FLRY3'), ('GGBR4', 'GGBR4'), ('GNDI3', 'GNDI3'), ('GOAU4', 'GOAU4'), ('GOLL4', 'GOLL4'), ('HAPV3', 'HAPV3'), ('HGTX3', 'HGTX3'), ('HYPE3', 'HYPE3'), ('IGTA3', 'IGTA3'), ('IRBR3', 'IRBR3'), ('ITSA4', 'ITSA4'), ('ITUB4', 'ITUB4'), ('JBSS3', 'JBSS3'), ('KLBN11', 'KLBN11'), ('LAME4', 'LAME4'), ('LREN3', 'LREN3'), ('MGLU3', 'MGLU3'), ('MRFG3', 'MRFG3'), ('MRVE3', 'MRVE3'), ('MULT3', 'MULT3'), ('NTCO3', 'NTCO3'), ('PCAR3', 'PCAR3'), ('PETR3', 'PETR3'), ('PETR4', 'PETR4'), ('QUAL3', 'QUAL3'), ('RADL3', 'RADL3'), ('RAIL3', 'RAIL3'), ('RENT3', 'RENT3'), ('SANB11', 'SANB11'), ('SBSP3', 'SBSP3'), ('SULA11', 'SULA11'), ('SUZB3', 'SUZB3'), ('TAEE11', 'TAEE11'), ('TIMP3', 'TIMP3'), ('TOTS3', 'TOTS3'), ('UGPA3', 'UGPA3'), ('USIM5', 'USIM5'), ('VALE3', 'VALE3'), ('VIVT4', 'VIVT4'), ('VVAR3', 'VVAR3'), ('WEGE3', 'WEGE3'), ('YDUQ3', 'YDUQ3')]
    else: #dynamic:
        t1 = tickers_ibovespa()
        t2 = t1
        tickers = list(zip(t1,t2))
    
    PERIODO = [(1,'1m'),(2,'2m'),(5,'5m'),(15,'15m'),(30,'30m'),(60,'1h'),(120,'2h')]

    email = forms.EmailField()
    ativo = forms.ChoiceField(label="Ativo", choices=tickers)
    precocompra = forms.DecimalField(label="Preço de Compra", max_digits=6, decimal_places=2)
    precovenda = forms.DecimalField(label="Preço de Venda", max_digits=6, decimal_places=2)
    periodo = forms.ChoiceField(label="Periodo entre checagens", choices=PERIODO)
    duracao = forms.DateField(label="Duração da operação", widget=forms.SelectDateWidget)
    checkbox = forms.BooleanField(label="Entendo que receberei e-mails periodicos")