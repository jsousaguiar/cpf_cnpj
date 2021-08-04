import re
from enum import Enum


_DIVISOR = 11

_CPF_WEIGHTS = ((10, 9, 8, 7, 6, 5, 4, 3, 2), (11, 10, 9, 8, 7, 6, 5, 4, 3, 2))
_CNPJ_WEIGHTS = (
    (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2),
    (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2),
)


def _calcula_primeiro_digito(number):
    """Esta função caulcula o primeiro dígito de verificação
    de um CPF ou CNPJ.
    :param number: cpf (length 9) or cnpf (length 12)
        string para verificar o primeir dígito. Somente números.
    :type number: string
    :returns: string -- o primeiro dígito
    """

    sum = 0
    if len(number) == 9:
        weights = _CPF_WEIGHTS[0]
    else:
        weights = _CNPJ_WEIGHTS[0]

    for i in range(len(number)):
        sum = sum + int(number[i]) * weights[i]
    rest_division = sum % _DIVISOR
    if rest_division < 2:
        return "0"
    return str(11 - rest_division)


def _calcula_segundo_digito(number):
    """Esta função caulcula o segundo dígito de verificação
    de um CPF ou CNPJ.
    **Esta função deve ser chamada antes da que verifica o primeiro dígito.**
    :param number: cpf (length 10) or cnpj
        (length 13) contando com o primeiro dígito. Apenas números.
    :type number: string
    :returns: string -- o segundo dígito
    """

    sum = 0
    if len(number) == 10:
        weights = _CPF_WEIGHTS[1]
    else:
        weights = _CNPJ_WEIGHTS[1]

    for i in range(len(number)):
        sum = sum + int(number[i]) * weights[i]
    rest_division = sum % _DIVISOR
    if rest_division < 2:
        return "0"
    return str(11 - rest_division)


def _limpa_pontuacao(document):
    """Remove todos os caracteres não numéricos."""
    return re.sub(r"\D", "", str(document))


def valida_cpf(cpf_number):
    """Esta função valida um número de CPF.
    Esta função usa os pacotes de cálculo para calcular os dígitos e
    então validar o número.
    :param cpf_number: um número de CPF a ser validado.  Somente números.
    :type cpf_number: string
    :return: Bool -- True para um número válido, False se inválido.
    """

    cpf_str = str(cpf_number)

    _cpf = _limpa_pontuacao(cpf_str)

    if len(_cpf) > 11:
        return False

    _cpf = _cpf.rjust(11, "0")
    # outra opção:
    # _cpf = f"{_cpf:>011}"

    if len(set(_cpf)) == 1:
        return False

    first_part = _cpf[:9]
    second_part = _cpf[:10]
    first_digit = _cpf[9]
    second_digit = _cpf[10]

    if first_digit == _calcula_primeiro_digito(
        first_part
    ) and second_digit == _calcula_segundo_digito(second_part):
        return True

    return False


def valida_cnpj(cnpj_number):
    """Esta função valida um número de CNPJ.
    Esta função usa os pacotes de cálculo para calcular os dígitos e
    então validar o número.
    :param cnpj_number: um número de CNPJ a ser validado.  Somente números.
    :type cnpj_number: string
    :return: Bool -- True para um número válido, False se inválido.
    """

    cnpj_str = str(cnpj_number)

    _cnpj = _limpa_pontuacao(cnpj_str)

    if len(_cnpj) > 14:
        return False

    _cnpj = _cnpj.rjust(14, "0")
    # outra opção:
    # _cnpj = f"{_cnpj:>014}"

    if len(set(_cnpj)) == 1:
        return False

    first_part = _cnpj[:12]
    second_part = _cnpj[:13]
    first_digit = _cnpj[12]
    second_digit = _cnpj[13]

    if first_digit == _calcula_primeiro_digito(
        first_part
    ) and second_digit == _calcula_segundo_digito(second_part):
        return True

    return False


# Cria uma classe para o tipo de documento identificado


class TipoDocumento(Enum):
    CPF = 1
    CNPJ = 2
    INVALIDO = 3


"""Completa os dígitos faltantes e insere os separadores para formatar o CPF"""


def cpf_com_pontuacao(cpf):
    cpf = str(cpf)
    cpf = cpf.rjust(11, "0")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


"""Completa os dígitos faltantes e insere os separadores para formatar o CNPJ"""


def cnpj_com_pontuacao(cnpj):
    cnpj = str(cnpj)
    cnpj = cnpj.rjust(14, "0")
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


# Identifica o tipo de documento
def valida_cpf_cnpj(num_doc):
    if valida_cpf(num_doc):
        return TipoDocumento.CPF
    if valida_cnpj(num_doc):
        return TipoDocumento.CNPJ
    return TipoDocumento.INVALIDO


# Formata de acordo com o tipo de documento
def formatar_cpf_cnpj(num_doc):
    tipo_doc = valida_cpf_cnpj(num_doc)
    if tipo_doc == TipoDocumento.CPF:
        return cpf_com_pontuacao(num_doc)
    if tipo_doc == TipoDocumento.CNPJ:
        return cnpj_com_pontuacao(num_doc)
    return num_doc


# Identifica o tipo de documento correspondente ao número fornecido
def tipo_documento(num_doc):
    tipo_doc = valida_cpf_cnpj(num_doc)
    if tipo_doc == TipoDocumento.CPF:
        return "CPF"
    if tipo_doc == TipoDocumento.CNPJ:
        return "CNPJ"
    return "CPF/CNPJ"


# Identifica o tipo de pessoa correspondente ao documento fornecido
def tipo_pessoa(num_doc):
    tipo_doc = valida_cpf_cnpj(num_doc)
    if tipo_doc == TipoDocumento.CPF:
        return "pessoa física"
    if tipo_doc == TipoDocumento.CNPJ:
        return "pessoa jurídica"
    return "pessoa"
