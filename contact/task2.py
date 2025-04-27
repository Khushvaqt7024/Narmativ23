from django.utils import timezone
from celery import shared_task

@shared_task
def print_time():
    print(f'{timezone.now()} hozirgi vaqt!')