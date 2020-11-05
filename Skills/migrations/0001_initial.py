# Generated by Django 3.1.2 on 2020-11-05 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Jobs', '0002_auto_20201103_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skillName', models.CharField(max_length=100, verbose_name='Skill')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skillLevel', models.IntegerField(choices=[(1, 'Do not have this skill'), (2, 'Actively learning'), (3, 'Using from time to time'), (4, 'Using every day'), (5, 'Expert')], default=1, verbose_name='What is your level in this skill?')),
                ('skillApplication', models.IntegerField(choices=[(1, 'Do not want'), (2, "I don't care"), (3, "I'd like to")], default=2, verbose_name='Would you like to use this skill in your job?')),
                ('skillGrowth', models.IntegerField(choices=[(1, 'Do not want'), (2, "I don't care"), (3, "I'd like to")], default=2, verbose_name='Would you like to learn more on this skill?')),
                ('cv', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Jobs.cv', verbose_name='Link to candidate CV')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Jobs.position', verbose_name='Link to position')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill', to='Skills.skill', verbose_name='Skill')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
