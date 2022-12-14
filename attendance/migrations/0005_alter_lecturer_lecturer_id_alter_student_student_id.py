# Generated by Django 4.1.2 on 2022-10-19 02:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_remove_class_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='lecturer_id',
            field=models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(20000001), django.core.validators.MaxValueValidator(30000000)]),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1000000), django.core.validators.MaxValueValidator(20000000)]),
        ),
    ]
