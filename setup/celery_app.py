from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from setup import settings

# Define a configuração de ambiente do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")

# Cria a aplicação Celery
app = Celery("setup")

# Configura Celery para usar as configurações do Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Descobre e carrega tarefas dos apps instalados automaticamente
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
