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


def adiciona_fotos(request):
    candidatos_sem_foto = Candidato.objects.filter(codigo_foto=None).order_by("estado")
    estado = ""
    lista_candidatos = []
    for candidato in candidatos_sem_foto:
        if estado != candidato.estado:
            estado = candidato.estado
            url_imagem = "http://divulgacand2014.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/{}/candidatos/cargo/{}".format(candidato.estado, candidato.cargo_id)
            conteudo_imagem = requests.get(url_imagem).content.decode('ISO-8859-1')
            pagina = lhtml.fromstring(conteudo_imagem)
            lista_candidatos = pagina.cssselect('.row-link-cand')
        atualizado = False
        for linha in lista_candidatos:
            numero_canditado = int(linha.cssselect('td')[2].text)
            if candidato.numero == numero_canditado:
                atualizado = True
                candidato.codigo_foto = linha.attrib['id']
                candidato.save()
                break
        print u"{} - {} - {} - {} - {}".format(atualizado, estado, candidato.cargo_id, candidato.numero, candidato.nome)
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
                if "Deferido" in linha.split(";")[5]:
                    Candidato.obtem_a_partir_de_linha_do_csv(linha, cargo, estado[0])
                    candidatos += 1
            urls.append(u"{} em {}: {} candidatos processados".format(Cargo.objects.get(id=cargo).nome, estado[0], candidatos))
    return render(request, "importar.html", locals())


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


def criar(request, estado, presidente, governador, senador, deputado_federal, deputado_estadual):
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
    return render_to_response('criar.html', locals(), context_instance=RequestContext(request))


def escolher_candidatos(request, estado):
    cargos = [
        {"nome": "Presidente", "candidatos": Candidato.obter_lista_por_cargo(1, 'BR'), "nulo": "XX", "branco": "00"},
        {"nome": "Governador", "candidatos": Candidato.obter_lista_por_cargo(3, estado), "nulo": "XX", "branco": "00"},
        {"nome": "Senador", "candidatos": Candidato.obter_lista_por_cargo(5, estado), "nulo": "XXX", "branco": "000"},
        {"nome": "Deputado Federal", "candidatos": Candidato.obter_lista_por_cargo(6, estado), "nulo": "XXXX", "branco": "0000"},
    ]
    cargo_nome = "Deputado Estadual"
    cargo_slug = "deputado-estadual"
    cargo = 7
    if estado == "DF":
        cargo = 8
        cargo_slug = "deputado-distrital"
        cargo_nome = "Deputado Distrital"
    cargos.append({"nome": cargo_nome, "candidatos": Candidato.obter_lista_por_cargo(cargo, estado), "nulo": "XXXXX", "branco": "00000"})
    nome_estado = nome_do_estado(estado)
    if request.method == "POST":
        selecionados = {
            "presidente": request.POST.get("candidato_1", None),
            "governador": request.POST.get("candidato_3", None),
            "senador": request.POST.get("candidato_5", None),
            "deputado-federal": request.POST.get("candidato_6", None),
            cargo_slug: request.POST.get("candidato_{}".format(cargo), None),
        }
    return render_to_response('escolher_candidatos.html', locals(), context_instance=RequestContext(request))


def estados(request):
    estados = ESTADOS[1:]
    return render_to_response('estados.html', locals(), context_instance=RequestContext(request))


def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))