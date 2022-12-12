from lessons.services.webinar import create_new_webinar
from terenoi.celery import app


@app.task
def create_webinar_and_users_celery(webinar_pk):
    create_new_webinar(webinar_pk)
