# Generated by Django 2.2.7 on 2019-12-16 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstTest', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
