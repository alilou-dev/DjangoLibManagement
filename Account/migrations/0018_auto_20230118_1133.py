# Generated by Django 3.2.16 on 2023-01-18 11:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0017_auto_20230118_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readinggroup',
            name='eventMoment',
            field=models.TimeField(default=datetime.time(11, 33, 41, 207818)),
        ),
        migrations.AlterField(
            model_name='readinggroup',
            name='img',
            field=models.FileField(upload_to='./media/'),
        ),
    ]
