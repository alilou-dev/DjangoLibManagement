# Generated by Django 3.2.16 on 2023-01-14 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Account', '0004_book_editor'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembersGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ReadingGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('img', models.ImageField(upload_to='images/')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='Account.book')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.AddField(
            model_name='membersgroup',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Account.readinggroup'),
        ),
        migrations.AddField(
            model_name='membersgroup',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='readinggroup',
            constraint=models.UniqueConstraint(fields=('created_by', 'book'), name='unique_OwnerGroup_targetBook_combination'),
        ),
        migrations.AddConstraint(
            model_name='membersgroup',
            constraint=models.UniqueConstraint(fields=('member', 'group'), name='unique_member_group_combination'),
        ),
    ]
