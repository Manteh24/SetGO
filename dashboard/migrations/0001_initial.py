# Generated by Django 5.2 on 2025-04-12 12:25

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_remove_trainee_fixed_session_days_fixedsession'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerDashboard',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.trainer',),
        ),
    ]
