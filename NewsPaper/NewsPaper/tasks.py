from celery import shared_task
import time

@sha red_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)