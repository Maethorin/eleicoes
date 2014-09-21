# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('santinho', '0002_auto_20140919_1614'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidato',
            options={'ordering': ('numero',)},
        ),
        migrations.AlterModelOptions(
            name='cargo',
            options={'ordering': ('codigo',)},
        ),
        migrations.AlterModelOptions(
            name='partido',
            options={'ordering': ('numero',)},
        ),
        migrations.AddField(
            model_name='candidato',
            name='codigo_foto',
            field=models.CharField(max_length=15, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='candidato',
            name='estado',
            field=models.CharField(max_length=2, choices=[(b'BR', b'Brasil'), (b'AC', b'Acre'), (b'AL', b'Alagoas'), (b'AP', 'Amap\xe1'), (b'AM', b'Amazonas'), (b'BA', b'Bahia'), (b'CE', 'Cear\xe1'), (b'DF', b'Distrito Federal'), (b'ES', 'Esp\xedrito Santo'), (b'GO', b'Goias'), (b'MA', 'Maranh\xe3o'), (b'MT', b'Mato Grosso'), (b'MS', b'Mato Grosso do Sul'), (b'MG', b'MInas Gerais'), (b'PA', 'Par\xe1'), (b'PB', 'Para\xedba'), (b'PR', 'Paran\xe1'), (b'PE', b'Pernambuco'), (b'PI', 'Piau\xed'), (b'RJ', b'Rio de Janeiro'), (b'RN', b'Rio Grande do Norte'), (b'RS', b'Rio Grande do Sul'), (b'RO', 'Rond\xf4nia'), (b'RR', b'Roraima'), (b'SC', b'Santa Catarina'), (b'SP', 'S\xe3o Paulo'), (b'SE', b'Sergipe'), (b'TO', b'Tocantins')]),
        ),
        migrations.AlterField(
            model_name='coligacao',
            name='estado',
            field=models.CharField(max_length=2, choices=[(b'BR', b'Brasil'), (b'AC', b'Acre'), (b'AL', b'Alagoas'), (b'AP', 'Amap\xe1'), (b'AM', b'Amazonas'), (b'BA', b'Bahia'), (b'CE', 'Cear\xe1'), (b'DF', b'Distrito Federal'), (b'ES', 'Esp\xedrito Santo'), (b'GO', b'Goias'), (b'MA', 'Maranh\xe3o'), (b'MT', b'Mato Grosso'), (b'MS', b'Mato Grosso do Sul'), (b'MG', b'MInas Gerais'), (b'PA', 'Par\xe1'), (b'PB', 'Para\xedba'), (b'PR', 'Paran\xe1'), (b'PE', b'Pernambuco'), (b'PI', 'Piau\xed'), (b'RJ', b'Rio de Janeiro'), (b'RN', b'Rio Grande do Norte'), (b'RS', b'Rio Grande do Sul'), (b'RO', 'Rond\xf4nia'), (b'RR', b'Roraima'), (b'SC', b'Santa Catarina'), (b'SP', 'S\xe3o Paulo'), (b'SE', b'Sergipe'), (b'TO', b'Tocantins')]),
        ),
    ]
