# Generated by Django 5.2 on 2025-04-12 10:53

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainee',
            name='fixed_session_days',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('MO', 'Monday'), ('TU', 'Tuesday'), ('WE', 'Wednesday'), ('TH', 'Thursday'), ('FR', 'Friday'), ('SA', 'Saturday'), ('SU', 'Sunday')], max_length=20),
        ),
    ]
