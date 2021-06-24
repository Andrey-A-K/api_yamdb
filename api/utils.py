from api_yamdb.settings import NOREPLY_YAMDB_EMAIL
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken


def email_is_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def generate_mail(to_email, code):
    subject = 'Код подтверждения'
    text_content = (f'''
        Код подтверждения для работы с API YaMDB.
        Внимание, храните его в тайне {code}
    ''')
    mail.send_mail(
        subject, text_content,
        NOREPLY_YAMDB_EMAIL, [to_email],
        fail_silently=False
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
