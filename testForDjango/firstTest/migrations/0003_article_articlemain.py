# Generated by Django 2.2.7 on 2019-12-06 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstTest', '0002_reporter_reporterkind'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='articleMain',
            field=models.CharField(default='body', max_length=3000, verbose_name='article body'),
        ),
    ]