# Generated by Django 5.1.5 on 2025-03-25 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_delete_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
