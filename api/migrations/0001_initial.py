# Generated by Django 3.0.5 on 2021-06-15 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Titles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('year', models.DateTimeField(auto_now_add=True,
                 verbose_name='Дата')),
                ('description', models.TextField()),
                ('category', models.ForeignKey(blank=True,
                 help_text='Выберите категорию из списка', null=True,
                 on_delete=django.db.models.deletion.SET_NULL,
                 related_name='category', to='api.Categories',
                 verbose_name='категория')),
                ('genre', models.ForeignKey(blank=True,
                 help_text='Выберите жанр из списка', null=True,
                 on_delete=django.db.models.deletion.SET_NULL,
                 related_name='genre', to='api.Genres', verbose_name='жанр')),
            ],
        ),
    ]
