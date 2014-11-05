# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passport', '0002_auto_20141104_0518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='timeslot_id',
        ),
    ]
