# Generated by Django 4.1.2 on 2022-10-19 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_alter_lecturer_lecturer_id_alter_student_student_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semester',
            old_name='semester',
            new_name='name',
        ),
    ]
