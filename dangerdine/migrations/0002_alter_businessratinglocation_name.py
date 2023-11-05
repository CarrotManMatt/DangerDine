# Generated by Django 4.2.7 on 2023-11-05 03:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dangerdine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessratinglocation',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator("^(?![\\s'-])(?!.*[\\s'-]{2})[A-Za-z '-#]+(?<![\\s'-])\\Z"), django.core.validators.MinLengthValidator(2)], verbose_name='Name'),
        ),
    ]