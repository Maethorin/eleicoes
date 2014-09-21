# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from santinho.models import Cargo, Coligacao, Candidato, Partido

admin.site.register(Cargo)
admin.site.register(Partido)
admin.site.register(Coligacao)
admin.site.register(Candidato)
