# Generated by Django 3.0.5 on 2021-06-18 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210618_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='titles',
            name='description',
        ),
    ]
