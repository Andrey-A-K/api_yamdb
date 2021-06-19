from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

User = settings.AUTH_USER_MODEL

USER = 1
MODERATOR = 2
ADMIN = 3

ROLE_CHOICES = (
    ('USER', 'user'),
    ('MODERATOR', 'moderator'),
    ('ADMIN', 'admin')
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, email, password)
        # user.is_superuser = True
        # user.is_staff = True
        user.role = 1
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)
    # first_name = models.CharField(max_length=250)
    # last_name = models.CharField(max_length=250)
    password = models.CharField(max_length=128, blank=True, null=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)

    def is_staff(self):
        return self.is_admin

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

'''
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
'''


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.slug}'


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.slug}'


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField(auto_now_add=True, blank=True, null=True)
    description = models.TextField()
    genre = models.ManyToManyField(Genres,
                                   blank=True,
                                   related_name='genre_titles',)
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='category_titles',)

    def __str__(self):
        return f'{self.pk} - {self.name[:20]} - {self.category}'


class Reviews(models.Model):
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name="reviews"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()

    score = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 11)]
    )

    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ['author', 'title']


class Comment(models.Model):
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )


