# Generated by Django 3.2.16 on 2023-01-15 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0007_auto_20230115_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='readinggroup',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
    ]
