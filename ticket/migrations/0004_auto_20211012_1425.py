# Generated by Django 3.1.7 on 2021-10-12 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_auto_20211012_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.IntegerField(choices=[(1, 'Open'), (2, 'Closed')], default=1, max_length=10),
        ),
    ]
