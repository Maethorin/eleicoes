# -*- coding: utf-8 -*-

from django.db import models

ESTADOS = (
    ('BR', 'Brasil'),
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', u'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', u'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', u'Espírito Santo'),
    ('GO', 'Goias'),
    ('MA', u'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'MInas Gerais'),
    ('PA', u'Pará'),
    ('PB', u'Paraíba'),
    ('PR', u'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', u'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', u'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', u'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)

AMBITOS = (('F', 'Federal'), ('E', 'Estadual'), ('M', 'Municipal'))


class Cargo(models.Model):
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=128)
    ambito = models.CharField(max_length=1, choices=AMBITOS)

    class Meta:
        ordering = ("codigo", )

    def __unicode__(self):
        return self.nome

    @classmethod
    def obter_por_codigo(cls, codigo):
        return cls.objects.get(codigo=codigo)


class Partido(models.Model):
    numero = models.IntegerField(unique=True)
    sigla = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=255)

    class Meta:
        ordering = ("numero", )

    def __unicode__(self):
        return u"{} - {}".format(self.numero, self.sigla)

    @classmethod
    def obter_por_sigla(cls, sigla):
        return cls.objects.get(sigla=sigla)


class Coligacao(models.Model):
    nome = models.CharField(max_length=255)
    estado = models.CharField(max_length=2, choices=ESTADOS)
    partidos = models.ManyToManyField(Partido)

    def __unicode__(self):
        return self.nome


class SituacaoDeCandidato(object):
    deferido = "D"
    eleito = "E"
    suplente = "S"
    segundo_turno = "T"
    nao_eleito = "N"

    @classmethod
    def obter_situacao(cls, situacao):
        if situacao.lower() == u"suplente":
            return cls.suplente
        if situacao.lower() == u"não eleito":
            return cls.nao_eleito
        if situacao.lower() == u"2º turno":
            return cls.segundo_turno
        if situacao.lower() in [u"eleito por qp", u"eleito por média", u"eleito"]:
            return cls.eleito
        return cls.deferido


class Candidato(models.Model):
    SITUACOES = (
        (SituacaoDeCandidato.deferido, "Deferido"),
        (SituacaoDeCandidato.eleito, "Eleito"),
        (SituacaoDeCandidato.suplente, "Suplente"),
        (SituacaoDeCandidato.segundo_turno, "Segundo Turno"),
        (SituacaoDeCandidato.nao_eleito, u"Não Eleito"))

    nome = models.CharField(max_length=255)
    numero = models.IntegerField()
    codigo_foto = models.CharField(max_length=15, null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS)
    cargo = models.ForeignKey(Cargo)
    partido = models.ForeignKey(Partido)
    situacao = models.CharField(max_length=1, choices=SITUACOES, default="D")

    class Meta:
        ordering = ("nome", )
        unique_together = (("numero", "estado", "cargo"),)

    def __unicode__(self):
        return u"{} - {} - {} - {}".format(self.estado, self.numero, self.partido.sigla, self.nome)

    @classmethod
    def obter_lista_por_cargo(cls, cargo, estado, eh_segundo_turno=False):
        if eh_segundo_turno:
            return cls.objects.prefetch_related('partido').filter(cargo=cargo, estado=estado, situacao=SituacaoDeCandidato.segundo_turno)
        return cls.objects.prefetch_related('partido').filter(cargo=cargo, estado=estado)

    @classmethod
    def obtem_do_numero(cls, numero, estado, cargo):
        try:
            return cls.objects.get(numero=numero, estado=estado, cargo_id=cargo)
        except cls.DoesNotExist:
            return None

    @classmethod
    def obtem_a_partir_de_linha_do_csv(cls, linha, cargo, estado, printer=None, resultado=False):
        campos = linha.split(";")
        soma = (1 if resultado else 0)
        nome = campos[1 + soma]
        numero = campos[3 + soma]
        partido_sigla = campos[4 + soma]
        partido = Partido.obter_por_sigla(partido_sigla)
        cargo = Cargo.objects.get(id=cargo)
        candidato, criado = cls.objects.get_or_create(numero=numero, estado=estado, cargo=cargo, partido=partido)
        atualizado = False
        if candidato.nome != nome:
            atualizado = True
            candidato.nome = nome
        if resultado:
            situacao = SituacaoDeCandidato.obter_situacao(campos[0])
            if candidato.situacao != situacao:
                atualizado = True
                candidato.situacao = situacao
        if printer:
            printer(u"{} - {} - {} - {} - {}".format(("CRIADO" if criado else ("ATUALIZADO" if atualizado else u"SEM ALTERAÇÃO")), estado, cargo.id, numero, nome))
        if atualizado:
            candidato.save()

    @property
    def primeiro_nome(self):
        return " ".join(self.nome.split(" ")[0:-1])

    @property
    def segundo_nome(self):
        return " ".join(self.nome.split(" ")[-1])

    @property
    def numero_lista(self):
        return str(self.numero)

    @property
    def numero_partido(self):
        return self.numero_lista[:2]

    @property
    def numero_sem_partido(self):
        return self.numero_lista[2:]

    @property
    def url_de_imagem(self):
        return "http://divulgacand2014.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/{}/foto/{}.jpg".format(self.estado, self.estado_codigo, self.codigo_foto)