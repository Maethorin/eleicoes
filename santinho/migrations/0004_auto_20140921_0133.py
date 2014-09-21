# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('santinho', '0003_auto_20140921_0116'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='candidato',
            unique_together=set([('numero', 'estado', 'cargo')]),
        ),
    ]
