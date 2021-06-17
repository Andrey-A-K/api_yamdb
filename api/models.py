from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


User = settings.AUTH_USER_MODEL

USER = 1
MODERATOR = 2
ADMIN = 3

ROLE_CHOICES = (
    ('USER', 'user'),
    ('MODERATOR', 'moderator'),
    ('ADMIN', 'admin')
)


class User(AbstractUser):
    email = models.EmailField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)

    def __str__(self):
        return self.username


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
