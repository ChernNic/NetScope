# Generated by Django 5.2 on 2025-04-06 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0005_remove_tag_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customfield',
            name='tags',
        ),
    ]
