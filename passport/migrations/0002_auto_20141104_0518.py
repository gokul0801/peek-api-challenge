# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='timeslot_id',
            field=models.CharField(unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
