# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext

import requests
from django.shortcuts import render
from django.shortcuts import render_to_response
from lxml import html as lhtml

from santinho.models import ESTADOS, Candidato, Cargo


def nome_do_estado(sigla):
    for estado in ESTADOS:
        if estado[0] == sigla:
            return estado[1]
    return ''


def obter_candidato(numero, estado, cargo, cargo_nome):
    if not "X" in numero and int(numero) > 0:
        return Candidato.obtem_do_numero(numero, estado, cargo)
    elif "X" in numero:
        return {
            "cargo": {"nome": cargo_nome, "codigo": cargo},
            "nome": "Voto Nulo",
            "primeiro_nome": "Voto",
            "segundo_nome": "Nulo",
            "numero_partido": numero[:2],
            "numero_sem_partido": numero[2:],
            "numero": numero,
            "partido": {"sigla": "NULO"}
        }
    return {
        "cargo": {"nome": cargo_nome, "codigo": cargo},
        "nome": "Voto em Branco",
        "primeiro_nome": "Voto em",
        "segundo_nome": "Branco",
        "numero_partido": numero[:2],
        "numero_sem_partido": numero[2:],
        "numero": numero,
        "partido": {"sigla": "BRANCO"}
    }


def criar(request, estado, presidente, governador, senador=None, deputado_federal=None, deputado_estadual=None):
    eh_segundo_turno = settings.EH_SEGUNDO_TURNO
    candidatos = [
        obter_candidato(presidente, 'BR', 1, "Presidente"),
        obter_candidato(governador, estado, 3, "Governador"),
    ]
    pre_gov = candidatos[:2]
    outros = []
    if senador:
        outros.append(obter_candidato(senador, estado, 5, "Senador"))
    if deputado_federal:
        outros.append(obter_candidato(deputado_federal, estado, 6, "Deputado Federal"))
    if deputado_estadual:
        cargo = 7
        cargo_nome = "Deputado Estadual"
        if estado == "DF":
            cargo = 8
            cargo_nome = "Deputado Distrital"
        outros.append(obter_candidato(deputado_estadual, estado, cargo, cargo_nome))
    return render_to_response('criar.html', locals(), context_instance=RequestContext(request))


def santinho_escolher_candidatos(request, estado):
    eh_segundo_turno = settings.EH_SEGUNDO_TURNO
    cargos = [
        {"nome": "Presidente", "candidatos": Candidato.obter_lista_por_cargo(1, 'BR', eh_segundo_turno), "nulo": "XX", "branco": "00"},
        {"nome": "Governador", "candidatos": Candidato.obter_lista_por_cargo(3, estado, eh_segundo_turno), "nulo": "XX", "branco": "00"},
    ]
    deputado_nome = "Deputado Estadual"
    deputado_slug = "deputado-estadual"
    deputado_cargo = 7
    if not eh_segundo_turno:
        cargos.append({"nome": "Senador", "candidatos": Candidato.obter_lista_por_cargo(5, estado), "nulo": "XXX", "branco": "000"})
        cargos.append({"nome": "Deputado Federal", "candidatos": Candidato.obter_lista_por_cargo(6, estado), "nulo": "XXXX", "branco": "0000"})
        if estado == "DF":
            deputado_cargo = 8
            deputado_slug = "deputado-distrital"
            deputado_nome = "Deputado Distrital"
        cargos.append({"nome": deputado_nome, "candidatos": Candidato.obter_lista_por_cargo(deputado_cargo, estado), "nulo": "XXXXX", "branco": "00000"})
    nome_estado = nome_do_estado(estado)
    if request.method == "POST":
        selecionados = {
            "presidente": request.POST.get("candidato_1", None),
            "governador": request.POST.get("candidato_3", None),
        }
        if eh_segundo_turno:
            selecionados["senador"] = request.POST.get("candidato_5", None)
            selecionados["deputado-federal"] = request.POST.get("candidato_6", None)
            selecionados[deputado_slug] = request.POST.get("candidato_{}".format(deputado_cargo), None)
    return render_to_response('escolher_candidatos.html', locals(), context_instance=RequestContext(request))


def resultado_escolher_candidatos(request, estado):
    cargos = [
        {"nome": "Presidente", "candidatos": Candidato.obter_lista_por_cargo(1, 'BR'), "nulo": "XX", "branco": "00"},
        {"nome": "Governador", "candidatos": Candidato.obter_lista_por_cargo(3, estado), "nulo": "XX", "branco": "00"},
        {"nome": "Senador", "candidatos": Candidato.obter_lista_por_cargo(5, estado), "nulo": "XXX", "branco": "000"},
        {"nome": "Deputado Federal", "candidatos": Candidato.obter_lista_por_cargo(6, estado), "nulo": "XXXX", "branco": "0000"}
    ]
    deputado_nome = "Deputado Estadual"
    deputado_slug = "deputado-estadual"
    deputado_cargo = 7
    if estado == "DF":
        deputado_cargo = 8
        deputado_slug = "deputado-distrital"
        deputado_nome = "Deputado Distrital"
    cargos.append({"nome": deputado_nome, "candidatos": Candidato.obter_lista_por_cargo(deputado_cargo, estado), "nulo": "XXXXX", "branco": "00000"})
    nome_estado = nome_do_estado(estado)
    if request.method == "POST":
        selecionados = {
            "presidente": request.POST.get("candidato_1", None),
            "governador": request.POST.get("candidato_3", None),
            "senador": request.POST.get("candidato_5", None),
            "deputado-federal": request.POST.get("candidato_6", None),
            deputado_slug: request.POST.get("candidato_{}".format(deputado_cargo), None)
        }
    eh_resultado = True
    return render_to_response('resultado_candidatos.html', locals(), context_instance=RequestContext(request))


def estados(request):
    estados = ESTADOS[1:]
    return render_to_response('estados.html', locals(), context_instance=RequestContext(request))


def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))


def resultado(request, estado, presidente, governador, senador, deputado_federal, deputado_estadual):
    candidatos = [
        obter_candidato(presidente, 'BR', 1, "Presidente"),
        obter_candidato(governador, estado, 3, "Governador"),
        obter_candidato(senador, estado, 5, "Senador"),
        obter_candidato(deputado_federal, estado, 6, "Deputado Federal")
    ]
    cargo = 7
    cargo_nome = "Deputado Estadual"
    if estado == "DF":
        cargo = 8
        cargo_nome = "Deputado Distrital"
    candidatos.append(obter_candidato(deputado_estadual, estado, cargo, cargo_nome))
    pre_gov = candidatos[:2]
    outros = candidatos[2:]
    eh_resultado = True
    return render_to_response('resultado.html', locals(), context_instance=RequestContext(request))
