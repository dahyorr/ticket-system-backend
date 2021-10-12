# Generated by Django 3.1.7 on 2021-10-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0002_user_is_authorized'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that username already exists.'}, max_length=255, unique=True, verbose_name='Email Address'),
        ),
    ]
