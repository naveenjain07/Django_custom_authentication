# Generated by Django 2.2.4 on 2019-08-13 12:17

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator])),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('name', models.CharField(max_length=30)),
                ('mobile', models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(5)])),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('dob', models.DateField(default=datetime.date.today)),
                ('roleid', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('roleid', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=15)),
            ],
        ),
    ]
