# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_number', models.CharField(max_length=30, null=True, blank=True)),
                ('booked', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'RoomNumber',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_type', models.CharField(max_length=300, null=True, blank=True)),
                ('room_description', models.CharField(max_length=1500, null=True, blank=True)),
                ('room_image', models.ImageField(null=True, upload_to=b'room_type', blank=True)),
                ('room_price_1', models.FloatField(default=0, max_length=50)),
                ('room_service1', models.CharField(max_length=500, null=True, blank=True)),
                ('room_service2', models.CharField(max_length=500, null=True, blank=True)),
                ('room_service3', models.CharField(max_length=500, null=True, blank=True)),
                ('room_service4', models.CharField(max_length=500, null=True, blank=True)),
                ('room_service_others', models.CharField(max_length=1500, null=True, blank=True)),
                ('days_of_week', models.CharField(max_length=200, null=True, blank=True)),
                ('room_count', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'RoomType',
            },
        ),
        migrations.AddField(
            model_name='roomnumber',
            name='room_type',
            field=models.ForeignKey(blank=True, to='backend.RoomType', null=True),
        ),
    ]
