# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tracking_number', models.CharField(max_length=30, null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('checK_in', models.CharField(max_length=30, null=True, blank=True)),
                ('checK_out', models.CharField(max_length=30, null=True, blank=True)),
                ('checked_out', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'New', max_length=30)),
                ('ref_num', models.CharField(max_length=30, null=True, blank=True)),
                ('days', models.CharField(max_length=30, null=True, blank=True)),
                ('paid', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('room_type', models.CharField(max_length=30, null=True, blank=True)),
                ('room_id', models.CharField(max_length=30, null=True, blank=True)),
                ('amount_paid', models.IntegerField(null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('new_booking', models.BooleanField(default=True)),
                ('room_number', models.CharField(max_length=30, null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Bookings',
            },
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password2', models.CharField(max_length=50, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
                ('created_on', models.DateTimeField(null=True, blank=True)),
                ('edited_on', models.DateTimeField(null=True, blank=True)),
                ('deleted_on', models.DateTimeField(null=True, blank=True)),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('booking', models.ForeignKey(blank=True, to='general.Bookings', null=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name_plural': 'Useraccount',
            },
        ),
    ]
