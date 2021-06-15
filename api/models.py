from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        (1, 'user'),
        (2, 'moderator'),
        (3, 'admin')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(
        verbose_name='Пользователь',
        max_length=50,
        unique=True
    )
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length=254)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, null=True, blank=True
    )

    def __str__(self):
        return self.username
