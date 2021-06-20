# Generated by Django 3.0.5 on 2021-06-20 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20210620_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_titles', to='api.Categories', verbose_name='выберите категорию'),
        ),
        migrations.AlterField(
            model_name='titles',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='genre_titles', to='api.Genres', verbose_name='выберите жанр'),
        ),
    ]
