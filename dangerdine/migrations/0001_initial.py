# Generated by Django 4.2.7 on 2023-11-04 19:26

from django.db import migrations, models

import dangerdine.models.managers
import dangerdine.models.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'max_length': 'The Email Address must be at most 255 digits.', 'unique': 'A user with that Email Address already exists.'}, max_length=255, unique=True, validators=[dangerdine.models.validators.HTML5EmailValidator(), dangerdine.models.validators.FreeEmailValidator(), dangerdine.models.validators.ConfusableEmailValidator(), dangerdine.models.validators.PreexistingEmailTLDValidator(), dangerdine.models.validators.ExampleEmailValidator()], verbose_name='Email Address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Is Admin?')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Is Active?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
            },
            managers=[
                ('objects', dangerdine.models.managers.UserManager()),
            ],
        ),
    ]