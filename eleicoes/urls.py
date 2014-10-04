# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'santinho.views.home', name='home'),
    url(r'^estados$', 'santinho.views.estados', name='estados'),
    url(r'^escolher/(?P<estado>[A-Z]{2})$', 'santinho.views.escolher_candidatos', name='escolher_candidatos'),
    url(r'^santinho/(?P<estado>[A-Z]{2})/(?P<presidente>(\d{2}|XX))/(?P<governador>(\d{2}|XX))/(?P<senador>(\d{3}|XXX))/(?P<deputado_federal>(\d{4}|XXXX))/(?P<deputado_estadual>(\d{5}|XXXXX))$', 'santinho.views.criar', name='criar_santinho'),
    url(r'^importar$', 'santinho.views.importar_de_csv', name='importar'),
    url(r'^codigos_fotos$', 'santinho.views.codigos_fotos', name='codigos_fotos'),
    url(r'^adicionar_fotos$', 'santinho.views.adiciona_fotos', name='adiciona_fotos'),
    url(r'^admin/', include(admin.site.urls)),
)
