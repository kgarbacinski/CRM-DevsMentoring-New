# Generated by Django 4.0.3 on 2022-03-31 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Files_organizer', '0002_rename_subtopic_topic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='subtopic',
            new_name='topic',
        ),
    ]