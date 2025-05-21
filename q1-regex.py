"""
Expressões regulares simples
============================

Complete o atributo regex = r"..." no retorno de cada função com
a expressão regular correta que aceita todos os exemplos da seção "aceita" e
recusa todos os exemplos da seção "recusa".

Se a expressão contiver size caracteres ou menos, a questão será considerada
100% correta. Se a questão contiver entre size e max_size, será considerada 70%
correta. Se for maior que isso, será considerada incorreta, idependente de acertar
ou não os exemplos.

Você pode testar essa questão usando o pytest ou executando este arquivo
diretamente.
"""

from lox.aux import check_re


# Classe de exemplo já respondida. Observe que existe uma lista de exemplos
# que a regex deve aceitar, seguida por uma lista em branco e uma lista de
# exemplos que a regex deve recusar
@check_re(size=4, max_size=6, skip=True)
def exemplos_de_números():
    """
    aceita:
        1
        42
        10
        20
        007

    recusa:
        1.2
        .1
    """
    return r"\d+"


#
# A partir daqui é com você!
#
@check_re(size=17, max_size=32)
def nome_minúsculo_com_a_notação_de_ponto_pt0_75():
    return r"^[a-z]+(\.[a-z]+)*$"

@check_re(size=9, max_size=20)
def nome_de_variável_simples_começando_com_letra_minúscula_pt0_75():
    return r"^[a-z][_a-zA-Z0-9]*$"

@check_re(size=11, max_size=16)
def número_hexadecimal_positivo_com_letras_maiúsculas_pt0_75():
    return r"^0x[A-F0-9]+$"

@check_re(size=19, max_size=32)
def número_inteiro_com_underscores_opcionais_pt0_75():
    return r"^[1-9]\d*(?:_\d+)*$"

@check_re(size=23, max_size=45)
def número_inteiro_com_underscores_obrigatórios_separando_milhares_pt1_00():
    return r"^\d{1,3}(?:_\d{3})*$"

@check_re(size=33, max_size=64)
def número_com_parte_decimal_opcional_e_notação_científica_pt1_00():
    return r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$"