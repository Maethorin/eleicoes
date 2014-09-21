# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('santinho', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='codigo',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='partido',
            name='numero',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='partido',
            name='sigla',
            field=models.CharField(unique=True, max_length=10),
        ),
    ]
