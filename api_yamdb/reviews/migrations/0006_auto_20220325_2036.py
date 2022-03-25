# Generated by Django 3.0 on 2022-03-25 20:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220324_2141'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={},
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Оценка не может быть менее 1'), django.core.validators.MaxValueValidator(10, message='Оценка не может быть более 10')], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(blank=True, null=True, validators=[reviews.models.year_validator], verbose_name='Год выпуска'),
        ),
    ]
