# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('santinho', '0004_auto_20140921_0133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidato',
            options={'ordering': ('nome',)},
        ),
        migrations.AddField(
            model_name='candidato',
            name='situacao',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Deferido'), (b'E', b'Eleito'), (b'S', b'Segundo Turno'), (b'N', 'N\xe3o Eleito')]),
            preserve_default=True,
        ),
    ]
