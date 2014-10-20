# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def selecionando(context, cargo, numero):
    if "selecionados" in context:
        if context["selecionados"][cargo] == unicode(numero):
            return 'selected="selected"'
    return ''


@register.simple_tag(takes_context=True)
def define_valor_js(context, cargo):
    if "selecionados" in context:
        return context["selecionados"].get(cargo, 'null')
    return 'null'

@register.simple_tag
def css_situacao(situacao):
    if situacao == "E":
        return "success"
    if situacao == "N":
        return "danger"
    if situacao == "T":
        return "warning"
    return "default"
