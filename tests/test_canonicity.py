"""
Testes unitários para o algoritmo de canonicidade fonológica (sílabas exclusivamente CV).
"""

import pytest
from src.features.canonicity import (
    classificar_canonicidade,
    calcular_taxa_canonicidade,
    is_vogal,
    EXEMPLOS_EDITAL,
)


def test_exemplos_oficiais_edital():
    """Valida todos os exemplos fornecidos no Edital CAEd contra o gabarito."""
    for palavra, esperado in EXEMPLOS_EDITAL.items():
        is_canonica, padrao_cv, silabas = classificar_canonicidade(palavra)
        assert is_canonica == esperado, (
            f"Erro para '{palavra}': esperado {esperado}, obtido {is_canonica} (padrão {padrao_cv})"
        )


def test_palavras_canonicas():
    """Valida palavras estritamente formadas por sílabas Consoante-Vogal (CV)."""
    palavras = ["cabeça", "canela", "janela", "luta", "sopa", "pipoca", "bala", "sapato", "tatu"]
    for palavra in palavras:
        is_canonica, padrao_cv, silabas = classificar_canonicidade(palavra)
        assert is_canonica is True, f"'{palavra}' deveria ser canônica (padrão: {padrao_cv})"
        assert len(silabas) == len(palavra) // 2
        for s in silabas:
            assert len(s) == 2


def test_palavras_nao_canonicas():
    """Valida palavras não canônicas (V, CVC, CCV, VC, ditongos)."""
    palavras_nao_canonicas = [
        ("abajur", "V CVC"),
        ("lápis", "Coda em s"),
        ("cansado", "CVC"),
        ("asa", "V inicial"),
        ("alheio", "Encontro vocálico"),
        ("prato", "CCV"),
        ("brasil", "CCV e CVC"),
        ("flor", "CCVC"),
    ]
    for palavra, motivo in palavras_nao_canonicas:
        is_canonica, padrao_cv, silabas = classificar_canonicidade(palavra)
        assert is_canonica is False, f"'{palavra}' NÃO deveria ser canônica ({motivo}, padrão: {padrao_cv})"
        assert silabas == []


def test_is_vogal():
    """Testa a classificação de vogais e acentuações em português."""
    for v in ["a", "á", "à", "â", "ã", "e", "é", "ê", "i", "í", "o", "ó", "ô", "õ", "u", "ú", "y"]:
        assert is_vogal(v) is True
    for c in ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z", "ç"]:
        assert is_vogal(c) is False


def test_taxa_canonicidade_texto():
    """Testa o cálculo da proporção de palavras canônicas no texto."""
    # Texto 100% canônico:
    texto_puro = "Casa nova boca mole."
    assert calcular_taxa_canonicidade(texto_puro) == 1.0

    # Texto 0% canônico:
    texto_zero = "Transporte escolar difícil."
    assert calcular_taxa_canonicidade(texto_zero) == 0.0

    # Casos de borda:
    assert calcular_taxa_canonicidade("") == 0.0
    assert calcular_taxa_canonicidade("12345 !@#$%") == 0.0
