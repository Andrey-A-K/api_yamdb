from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
