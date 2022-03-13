from django.core.mail import send_mail

from education_services import settings
from education_services.celery import app


@app.task
def send_email_to_user_result_answers(data):
    quantity_correct_answers = data.get("result_answers").get("correct")
    quantity_wrong_answers = data.get("result_answers").get("wrong")
    topic = data.get("topic")
    email = data.get("user_email")
    subject = f'Вы прошли тест на тему {topic}!'
    message = f'Результат тестирования:\n' \
              f'Правильных ответов: {quantity_correct_answers};\n' \
              f'Неправильных ответов: {quantity_wrong_answers}.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=True)
