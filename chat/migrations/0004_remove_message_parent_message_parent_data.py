# Generated by Django 5.2.3 on 2025-06-30 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='parent',
        ),
        migrations.AddField(
            model_name='message',
            name='parent_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
