A pasta [mainapp](mainapp) contém o aplicativo em sí e a pasta [stockproject](stockproject) contém o projeto inicial com as configurações do Celery e ASGI.
Estes serviços são necessários apenas para envio de e-mails e cotação atualizada em tempo real, mas o projeto pode ser inicializado e utilizado sem eles.
As cotações são buscadas pelo yahoo_fin (python) e funcionam normalmente sem o Celery.

O arquivo ["start_server"](start_server.sh) é um lembrete para iniciar os processos necessarios:
  - startserver
  - celery
  - celery-beat
