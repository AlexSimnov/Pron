from config.celery import app

from django.core.mail import send_mail


@app.task
def send_successful_email_message(user_email, name):
    mes = f'{name} is successfully created.'
    send_mail(
        name,
        mes,
        'email@mail.ru',
        [user_email],
        fail_silently=False,
    )
