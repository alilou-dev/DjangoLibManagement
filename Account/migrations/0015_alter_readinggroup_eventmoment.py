# Generated by Django 3.2.16 on 2023-01-17 11:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0014_auto_20230117_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readinggroup',
            name='eventMoment',
            field=models.TimeField(default=datetime.time(11, 50, 2, 948123)),
        ),
    ]
