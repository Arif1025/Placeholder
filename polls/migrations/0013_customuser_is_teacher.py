# Generated by Django 5.1.5 on 2025-03-25 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_poll_class_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
