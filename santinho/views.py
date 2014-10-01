# -*- coding: utf-8 -*-
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


def codigos_fotos(request):
    for estado in ESTADOS:
        for cargo in range(1, 9):
            if estado[0] == 'BR' and cargo > 2:
                continue
            if estado[0] != 'BR' and cargo <= 2:
                continue
            if estado[0] == "DF" and cargo == 7:
                continue
            if estado[0] != "DF" and cargo == 8:
                continue
            url_imagem = "http://divulgacand2014.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/{}/candidatos/cargo/{}".format(estado[0], cargo)
            conteudo_imagem = requests.get(url_imagem).content.decode('ISO-8859-1')
            pagina = lhtml.fromstring(conteudo_imagem)
            lista_candidatos = pagina.cssselect('.row-link-cand')
            for linha in lista_candidatos:
                numero_canditado = int(linha.cssselect('td')[2].text)
                candidato = Candidato.obtem_do_numero(numero_canditado, estado[0], cargo)
                if candidato and not candidato.codigo_foto:
                    candidato.codigo_foto = linha.attrib['id']
                    candidato.save()
    return render(request, "importar.html", locals())


def importar_de_csv(request):
    urls = []
    for estado in ESTADOS:
        for cargo in range(1, 9):
            if estado[0] == 'BR' and cargo > 2:
                continue
            if estado[0] != 'BR' and cargo <= 2:
                continue
            if estado[0] == "DF" and cargo == 7:
                continue
            if estado[0] != "DF" and cargo == 8:
                continue
            url = "http://divulgacand2014.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/{}/candidatos/cargo/{}/downloadCSV".format(estado[0], cargo)
            csv = requests.get(url).content.decode('ISO-8859-1')
            linhas = csv.split("\n")[1:]
            candidatos = 0
            for linha in linhas:
                if not linha:
                    continue
                if linha.split(";")[5] != "Deferido":
                    continue
                Candidato.obtem_a_partir_de_linha_do_csv(linha, cargo, estado[0])
                candidatos += 1
            urls.append(u"{} em {}: {} candidatos processados".format(Cargo.objects.get(id=cargo).nome, estado[0], candidatos))
    return render(request, "importar.html", locals())


def criar(request, estado, presidente, governador, senador, deputado_federal, deputado_estadual):
    candidatos = [
        Candidato.obtem_do_numero(presidente, 'BR', 1),
        Candidato.obtem_do_numero(governador, estado, 3),
        Candidato.obtem_do_numero(senador, estado, 5),
        Candidato.obtem_do_numero(deputado_federal, estado, 6)
    ]
    cargo = 7
    if estado == "DF":
        cargo = 8
    candidatos.append(Candidato.obtem_do_numero(deputado_estadual, estado, cargo))
    pre_gov = candidatos[:2]
    outros = candidatos[2:]
    return render_to_response('criar.html', locals(), context_instance=RequestContext(request))


def escolher_candidatos(request, estado):
    cargos = [
        {"nome": "Presidente", "candidatos": Candidato.obter_lista_por_cargo(1, 'BR')},
        {"nome": "Governador", "candidatos": Candidato.obter_lista_por_cargo(3, estado)},
        {"nome": "Senador", "candidatos": Candidato.obter_lista_por_cargo(5, estado)},
        {"nome": "Deputado Federal", "candidatos": Candidato.obter_lista_por_cargo(6, estado)},
    ]
    cargo_nome = "Deputado Estadual"
    cargo_slug = "deputado-estadual"
    cargo = 7
    if estado == "DF":
        cargo = 8
        cargo_slug = "deputado-distrital"
        cargo_nome = "Deputado Distrital"
    cargos.append({"nome": cargo_nome, "candidatos": Candidato.obter_lista_por_cargo(cargo, estado)})
    nome_estado = nome_do_estado(estado)
    if request.method == "POST":
        selecionados = {
            "presidente": request.POST.get("candidato_1", None),
            "governador": request.POST.get("candidato_3", None),
            "senador": request.POST.get("candidato_5", None),
            "deputado-federal": request.POST.get("candidato_6", None),
            cargo_slug: request.POST.get("candidato_{}".format(cargo), None),
        }
    return render_to_response('escolher_candidatos.html', locals())


def estados(request):
    estados = ESTADOS[1:]
    return render_to_response('estados.html', locals())


def home(request):
    return render_to_response('home.html')