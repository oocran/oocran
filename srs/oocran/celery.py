from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oocran.settings')

app = Celery('oocran',
             broker='amqp://oocran:oocran@localhost/oocran',
             backend='rpc://')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'scheduler_ns': {
        'task': 'pools.tasks.ns',
        'schedule': 60.0,
    },
    'scheduler_nvf': {
        'task': 'pools.tasks.nvf',
        'schedule': 60.0,
    },
}

app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


