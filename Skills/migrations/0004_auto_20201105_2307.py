# Generated by Django 3.1.2 on 2020-11-05 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Jobs', '0002_auto_20201103_1926'),
        ('Skills', '0003_auto_20201105_2134'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skills',
            new_name='Response',
        ),
    ]
