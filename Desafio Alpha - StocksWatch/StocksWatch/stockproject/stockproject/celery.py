from __future__ import absolute_import, unicode_literals
import os
#celery
from celery import Celery
from django.conf import settings

# "stockproject" = nome do projeto atual.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockproject.settings')

app = Celery('stockproject')
# desliga o horario padrao do celerry (UTC)
app.conf.enable_utc = False
# muda para o horario local
app.conf.update(timezone = 'America/Sao_Paulo')

app.config_from_object(settings, namespace='CELERY')

# celery-beat settings:
app.conf.beat_schedule = {
    # 'every-10-seconds' : {
    #     'task' : 'mainapp.tasks.update_stock',
    #     'schedule' : 10,
    #     'args' : (['ITSA4', 'CIEL3'],)
    # },
    ### IS THIS WHERE I WILL ADD THE EMAILS???
}

app.autodiscover_tasks()


@app.task(bind = True)
def debug_task(self):
    print(f'Request: {self.request!r}')