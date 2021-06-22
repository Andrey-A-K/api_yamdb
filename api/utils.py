from django.core import mail
from api_yamdb.settings import NOREPLY_YAMDB_EMAIL


def generate_mail(to_email, code):
    subject = 'Код подтверждения'
    to = to_email
    text_content = f'''Код подтверждения для работы с API YaMDB.\n
                        Внимание, храните его в тайне {code}'''
    mail.send_mail(
        subject, text_content,
        NOREPLY_YAMDB_EMAIL, [to],
        fail_silently=False
    )
