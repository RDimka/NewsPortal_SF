import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'action_every_30_seconds': {
#         'task': 'tasks.action',
#         'schedule': 30,
#         'args': ("some_arg"),
#     },
# }

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'NewsPaper.tasks.printer',
        'schedule': 5,
        'args': (5,),
    },
}