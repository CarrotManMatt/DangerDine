# Generated by Django 4.2.7 on 2023-11-04 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dangerdine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
    ]
