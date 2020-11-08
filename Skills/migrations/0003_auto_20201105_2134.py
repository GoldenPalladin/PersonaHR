# Generated by Django 3.1.2 on 2020-11-05 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Skills', '0002_auto_20201105_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skillGroup', models.CharField(max_length=100, verbose_name='Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='skill',
            name='group',
            field=models.ForeignKey(default=1,
                                    on_delete=django.db.models.deletion.CASCADE, related_name='group', to='Skills.skillgroup', verbose_name='Group'),
            preserve_default=False,
        ),
    ]