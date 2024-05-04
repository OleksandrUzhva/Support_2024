import time

from config import celery_app


@celery_app.task
def send_email():
    print("Send email...")
    time.sleep(3)
    print("Success")
