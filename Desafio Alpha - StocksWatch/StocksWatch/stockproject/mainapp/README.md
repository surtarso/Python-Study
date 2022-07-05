Na pasta [templates](templates/mainapp) os templates foram separados por função dentro da aplicação para melhor modularidade.
Assim como também o "views.py" foi repartido e separado na pasta [views](views) de acordo com sua área de atuação.
O arquivo [tasks.py](tasks.py) contém as background tasks do celery que controlam os emails e a busca de cotações.
Em [routing.py](routing.py) o conteúdo foi tirado diretamente da documentação do Celery.

Os [formulários](forms.py) foram feitos em ModelForm fazendo assim o uso de [classes](models.py) e suas propriedades para manipulação da DB.

<h5>Admin Panel:</h5>
<img src="https://raw.githubusercontent.com/surtarso/Python-Projects/main/Desafio%20Alpha%20-%20StocksWatch/shots/admin_home.png" width=545 height=410>


<h5>Alertas na DB:</h5>
<img src="https://raw.githubusercontent.com/surtarso/Python-Projects/main/Desafio%20Alpha%20-%20StocksWatch/shots/admin_alerta.png" width=545 height=410>
