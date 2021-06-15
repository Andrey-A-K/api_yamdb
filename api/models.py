from django.db import models
from django.contrib.auth.models import AbstractUser


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


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateTimeField('Дата',
                                auto_now_add=True)
    # rating = models.ForeignKey(Reviews,
    #                            on_delete=models.SET_NULL)
    description = models.TextField()
    genre = models.ForeignKey(Genres,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              verbose_name='жанр',
                              related_name='genre',
                              help_text='Выберите жанр из списка')
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 verbose_name='категория',
                                 related_name='category',
                                 help_text='Выберите категорию из списка')


class Reviews(models.Model):
    titles = models.ForeignKey(
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
        unique_together = ['author', 'titles']


class Comment(models.Model):
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
