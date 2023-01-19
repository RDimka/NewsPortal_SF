import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'spam_weekly': {
        'task': 'news_app.tasks.weekly_spam',
        'schedule': (hour=1, minute=0, day_of_week='monday'), #crontab(minute='*/1'),
    },
}

# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'NewsPaper.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }