# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'santinho.views.home', name='home'),
    url(r'^estados$', 'santinho.views.estados', name='estados'),
    url(r'^santinho/(?P<estado>[A-Z]{2})/(?P<presidente>(\d{2}|XX))/(?P<governador>(\d{2}|XX))/(?P<senador>(\d{3}|XXX))/(?P<deputado_federal>(\d{4}|XXXX))/(?P<deputado_estadual>(\d{5}|XXXXX))$', 'santinho.views.criar', name='santinho_criar'),
    url(r'^santinho/escolher/(?P<estado>[A-Z]{2})$', 'santinho.views.santinho_escolher_candidatos', name='santinho_escolher_candidatos'),
    url(r'^santinho/2-turno/(?P<estado>[A-Z]{2})/(?P<presidente>(\d{2}|XX))$', 'santinho.views.criar', name='santinho_criar_2_turno'),
    url(r'^santinho/2-turno/(?P<estado>[A-Z]{2})/(?P<presidente>(\d{2}|XX))/(?P<governador>(\d{2}|XX))$', 'santinho.views.criar', name='santinho_criar_2_turno'),
    url(r'^resultado/escolher/(?P<estado>[A-Z]{2})$', 'santinho.views.resultado_escolher_candidatos', name='resultado_escolher_candidatos'),
    url(r'^resultado/(?P<estado>[A-Z]{2})/(?P<presidente>(\d{2}|XX))/(?P<governador>(\d{2}|XX))/(?P<senador>(\d{3}|XXX))/(?P<deputado_federal>(\d{4}|XXXX))/(?P<deputado_estadual>(\d{5}|XXXXX))$', 'santinho.views.resultado', name='resultado_criar'),
    url(r'^admin/', include(admin.site.urls)),
)
