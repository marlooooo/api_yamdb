# Generated by Django 3.0 on 2022-03-15 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, 'User'), (1, 'Moderator'), (2, 'Admin')], default=1),
        ),
    ]