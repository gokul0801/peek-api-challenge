# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_capacity', models.IntegerField(null=True)),
                ('bookable', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Boat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('capacity', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.IntegerField()),
                ('boat', models.ForeignKey(to='passport.Boat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timeslot_id', models.CharField(default=uuid.uuid4, unique=True, max_length=255)),
                ('start_time', models.PositiveIntegerField(unique=True)),
                ('duration', models.IntegerField()),
                ('availability', models.IntegerField(default=0)),
                ('customer_count', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='booking',
            name='timeslot',
            field=models.ForeignKey(to='passport.Timeslot'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='boat',
            field=models.ForeignKey(to='passport.Boat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='timeslot',
            field=models.ForeignKey(to='passport.Timeslot'),
            preserve_default=True,
        ),
    ]
