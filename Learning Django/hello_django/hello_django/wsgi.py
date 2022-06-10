## interface de porta de entrada do servidor web
## padrao para applicacoes web (servidores apachet etc)
## wsgi faz a interface com os servidores
## padrao criado pelo 'startproject'

"""
WSGI config for hello_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
## servidor leve para desenvolvimento:
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_django.settings')

application = get_wsgi_application()
