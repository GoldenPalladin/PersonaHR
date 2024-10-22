# Generated by Django 3.1.2 on 2020-11-03 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leadSource', models.URLField(default='http://localhost', verbose_name='Respondent source url')),
                ('userType', models.CharField(choices=[('candidate', 'Candidate'), ('employer', 'Employer')], default='candidate', max_length=9)),
                ('userID', models.CharField(blank=True, max_length=20, verbose_name='Telegram user ID')),
                ('userFirstName', models.CharField(blank=True, max_length=20, verbose_name='Telegram user first name')),
                ('userLastName', models.CharField(blank=True, max_length=20, verbose_name='Telegram user last name')),
                ('userUserName', models.CharField(blank=True, max_length=20, verbose_name='Telegram user nickname')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
