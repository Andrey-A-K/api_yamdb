from api_yamdb.settings import NOREPLY_YAMDB_EMAIL
from django.core import mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


def generate_mail(to_email, code):
    subject = 'Код подтверждения'
    text_content = f'''
        Код подтверждения для работы с API YaMDB.
        Внимание, храните его в тайне {code}
    '''
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


def validate(self, data):
    user = get_object_or_404(
        User, confirmation_code=data['confirmation_code'],
        email=data['email']
    )
    return get_tokens_for_user(user)
