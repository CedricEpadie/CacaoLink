# Generated by Django 5.1.5 on 2025-01-30 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='was_read',
            field=models.BooleanField(default=False),
        ),
    ]
