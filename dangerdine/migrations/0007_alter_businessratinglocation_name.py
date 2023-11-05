# Generated by Django 4.2.7 on 2023-11-05 05:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dangerdine', '0006_alter_businessratinglocation_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessratinglocation',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator("^(?![\\s&\\\\'-])(?!.*[\\s#\\\\-]{2})[A-Za-z #\\\\0-9&'-]+(?<![\\s'-])\\Z"), django.core.validators.MinLengthValidator(2)], verbose_name='Name'),
        ),
    ]
