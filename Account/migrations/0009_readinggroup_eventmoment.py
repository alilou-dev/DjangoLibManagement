# Generated by Django 3.2.16 on 2023-01-15 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0008_readinggroup_is_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='readinggroup',
            name='eventMoment',
            field=models.TimeField(default=datetime.time(17, 9, 17, 427585)),
        ),
    ]
