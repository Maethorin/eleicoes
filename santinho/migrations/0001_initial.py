# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=255)),
                ('numero', models.IntegerField()),
                ('estado', models.CharField(max_length=2, choices=[(b'BR', b'Brasil'), (b'AC', b'Acre')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.IntegerField()),
                ('nome', models.CharField(max_length=128)),
                ('ambito', models.CharField(max_length=1, choices=[(b'F', b'Federal'), (b'E', b'Estadual'), (b'M', b'Municipal')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Coligacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=255)),
                ('estado', models.CharField(max_length=2, choices=[(b'BR', b'Brasil'), (b'AC', b'Acre')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField()),
                ('sigla', models.CharField(max_length=10)),
                ('nome', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='coligacao',
            name='partidos',
            field=models.ManyToManyField(to='santinho.Partido'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidato',
            name='cargo',
            field=models.ForeignKey(to='santinho.Cargo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidato',
            name='partido',
            field=models.ForeignKey(to='santinho.Partido'),
            preserve_default=True,
        ),
    ]
