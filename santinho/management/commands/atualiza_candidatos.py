# -*- coding: utf-8 -*-

import requests
from django.core.management.base import BaseCommand, CommandError
from lxml import html as lhtml

from santinho.models import ESTADOS, Candidato, Cargo


class Command(BaseCommand):
    def handle(self, *args, **options):
        if args[0] == "fotos":
            if "adiciona" in args:
                self.adiciona_fotos()
            else:
                self.grava_fotos_todos()
        if args[0] == "candidatos":
            resultado = "resultado" in args
            self.importar_candidatos(resultado)

    def adiciona_fotos(self):
        self.stdout.write(u"INICIANDO")
        candidatos_sem_foto = Candidato.objects.filter(codigo_foto=None).order_by("estado")
        estado = ""
        lista_candidatos = []
        todos_atualizados = True
        for candidato in candidatos_sem_foto:
            if estado != candidato.estado:
                estado = candidato.estado
                url_imagem = "http://divulgacand2014.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/{}/candidatos/cargo/{}".format(candidato.estado, candidato.cargo_id)
                self.stdout.write(u"OBTENDO PÁGINA: {}".format(url_imagem))
                conteudo_imagem = requests.get(url_imagem).content.decode('ISO-8859-1')
                pagina = lhtml.fromstring(conteudo_imagem)
                lista_candidatos = pagina.cssselect('.row-link-cand')
            atualizado = False
            self.stdout.write(u"VERFICANDO {}".format(candidato))
            for linha in lista_candidatos:
                numero_canditado = int(linha.cssselect('td')[2].text)
                if candidato.numero == numero_canditado:
                    atualizado = True
                    candidato.codigo_foto = linha.attrib['id']
                    candidato.save()
                    self.stdout.write(u"ATUALIZADO {}".format(candidato))
                    break
            if not atualizado and todos_atualizados:
                todos_atualizados = False
            self.stdout.write(u"{} - {} - {} - {} - {}".format(atualizado, estado, candidato.cargo_id, candidato.numero, candidato.nome))
        if not todos_atualizados:
            self.stdout.write(u"RODE NOVAMENTE, POIS NEM TODOS FORAM ATUALIZADOS")
        self.stdout.write(u"FINALIZADO")

    def importar_candidatos(self, resultado):
        self.stdout.write(u"INICIANDO")
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
                self.stdout.write(u"OBTENDO CSV: {}".format(url))
                csv = requests.get(url).content.decode('ISO-8859-1')
                linhas = csv.split("\n")[1:]
                candidatos = 0
                indice_deferido = (6 if resultado else 5)
                for linha in linhas:
                    if not linha:
                        continue
                    if "Deferido" in linha.split(";")[indice_deferido]:
                        Candidato.obtem_a_partir_de_linha_do_csv(linha, cargo, estado[0], printer=self.stdout.write, resultado=resultado)
                        candidatos += 1
                self.stdout.write(u"{} EM {}: {} CANDIDATOS PROCESSADOS".format(Cargo.objects.get(id=cargo).nome, estado[0], candidatos))

    def grava_fotos_todos(self):
        self.stdout.write(u"INICIANDO")
        for estado in ESTADOS:
            self.stdout.write(u"ESTADO: {}".format(estado[1]))
            for cargo in range(1, 9):
                if estado[0] == 'BR' and cargo > 2:
                    continue
                if estado[0] != 'BR' and cargo <= 2:
                    continue
                if estado[0] == "DF" and cargo == 7:
                    continue
                if estado[0] != "DF" and cargo == 8:
                    continue
                cargo_nome = Cargo.objects.get(id=cargo).nome
                self.stdout.write(u"CARGO: {}".format(cargo_nome))
                url_lista_candidatos = "http://divulgacand2014.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/{}/candidatos/cargo/{}".format(estado[0], cargo)
                self.stdout.write(u"OBTENDO PÁGINA: {}".format(url_lista_candidatos))
                conteudo_imagem = requests.get(url_lista_candidatos).content.decode('ISO-8859-1')
                pagina = lhtml.fromstring(conteudo_imagem)
                lista_candidatos = pagina.cssselect('.row-link-cand')
                quantidade_candidatos = len(lista_candidatos)
                encontrados = 0
                atualizados = 0
                for linha in lista_candidatos:
                    numero_canditado = int(linha.cssselect('td')[2].text)
                    # self.stdout.write(u"BUSCANDO CANDIDATO NO ESTADO {} DO CARGO {} COM O NÚMERO {}".format(estado[0], cargo, numero_canditado))
                    candidato = Candidato.obtem_do_numero(numero_canditado, estado[0], cargo)
                    if candidato:
                        encontrados += 1
                        # self.stdout.write(u"ENCONTRADO {} \r".format(candidato))
                    if candidato and not candidato.codigo_foto:
                        atualizados += 1
                        self.stdout.write(u"ATUALIZANDO FOTO DO CANDIDATO {}".format(candidato))
                        candidato.codigo_foto = linha.attrib['id']
                        candidato.save()
                self.stdout.write(u"FINALIZADO: TOTAL NA PÁGINA: {}; ENCONTRADOS: {}; ATUALIZADOS: {}".format(quantidade_candidatos, encontrados, atualizados))
