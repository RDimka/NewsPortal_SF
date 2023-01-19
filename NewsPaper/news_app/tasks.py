from celery import shared_task
import datetime
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper import settings
from news_app.models import Post, Category
from news_app.signals import send_email_notif


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def notify_at_new_post_added(post_pk):
    #обьект статьи
    post = Post.objects.get(id=post_pk)

    #получаем категории добавленной статьи
    categories = post.category.all()

    #наполняем список подписчиков категорий добавленной статьи
    subscribers = []
    for category in categories:
        subscribers += category.subscribers.all()

    subscribers_email_list = []
    for subscr in subscribers:
        subscribers_email_list.append(subscr.email)

    send_email_notif(post.preview(), post.pk, post.title, subscribers_email_list)

@shared_task
def weekly_spam():
    # #Your job processing logic here...
    # print('hello from job')

    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_time_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()