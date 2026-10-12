"""
Algoritmo determinístico de classificação e cálculo de canonicidade de palavras (padrão CV).
"""

import re
from typing import Dict, List, Tuple

# Conjunto de grafemas vocálicos válidos para a língua portuguesa (incluindo acentuados e y)
VOGAIS_PT = set("aáàâãeéêiíoóôõuúy")

# Dicionário oficial de testes e gabarito estipulados no Edital CAEd
EXEMPLOS_EDITAL: Dict[str, bool] = {
    "cabeça": True,
    "canela": True,
    "janela": True,
    "luta": True,
    "sopa": True,
    "abajur": False,
    "lápis": False,
    "cansado": False,
    "asa": False,
    "alheio": False,
}


def is_vogal(char: str) -> bool:
    """Verifica se o caractere é uma vogal em português."""
    return char.lower() in VOGAIS_PT


def classificar_canonicidade(palavra: str) -> Tuple[bool, str, List[str]]:
    """
    Classifica se uma palavra é estritamente canônica segundo o padrão silábico Consoante-Vogal (CV).

    Regras:
    1. Apenas caracteres alfabéticos (a-z, incluindo acentos e cedilha) são avaliados.
    2. A palavra deve ter tamanho par.
    3. Cada par precisa ser rigorosamente formado por uma Consoante seguida de uma Vogal (CV).
       Qualquer encontro consonantal (CC), dígrafo ortográfico, hiato/ditongo (VV)
       ou coda consonantal (CVC) descaracteriza a palavra como canônica.

    Args:
        palavra: Vocábulo a ser avaliado.

    Returns:
        Tupla contendo:
        - is_canonica (bool): True se for puramente formada por sílabas CV.
        - padrao_cv (str): Sequência de 'C' e 'V' representando os grafemas.
        - silabas (list[str]): Lista de sílabas segmentadas de 2 em 2 se canônica, senão vazia.
    """
    palavra_limpa = re.sub(r"[^a-záàâãéêíóôõúç]", "", palavra.lower())
    if not palavra_limpa:
        return False, "", []

    padrao_cv = "".join("V" if is_vogal(c) else "C" for c in palavra_limpa)

    if len(padrao_cv) % 2 != 0:
        return False, padrao_cv, []

    padrao_esperado = "CV" * (len(padrao_cv) // 2)
    is_canonica = (padrao_cv == padrao_esperado)

    silabas = [palavra_limpa[i : i + 2] for i in range(0, len(palavra_limpa), 2)] if is_canonica else []
    return is_canonica, padrao_cv, silabas


def calcular_taxa_canonicidade(texto: str) -> float:
    """
    Calcula a proporção de palavras estritamente canônicas em um texto.

    Args:
        texto: Conteúdo textual completo.

    Returns:
        Taxa entre 0.0 e 1.0 (float).
    """
    palavras = re.findall(r"\b[a-zA-ZÀ-ÿ]+\b", texto)
    if not palavras:
        return 0.0

    qtd_canonicas = sum(1 for p in palavras if classificar_canonicidade(p)[0])
    return qtd_canonicas / len(palavras)
