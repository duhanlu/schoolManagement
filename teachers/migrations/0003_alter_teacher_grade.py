# Generated by Django 5.1.2 on 2024-11-19 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0001_initial'),
        ('teachers', '0002_alter_teacher_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='grade',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='grades.grade', verbose_name='manage class'),
        ),
    ]
