"""
Funções auxiliares para manipulação de strings, morfologia e modelo spaCy.
"""

from typing import Optional
import spacy
from spacy.language import Language

from src.config import SPACY_MODEL_NAME

_NLP_INSTANCE: Optional[Language] = None


def get_spacy_model() -> Language:
    """
    Retorna a instância compartilhada (singleton) do modelo spaCy pt_core_news_sm,
    evitando carregamentos redundantes e consumo desnecessário de memória.
    """
    global _NLP_INSTANCE
    if _NLP_INSTANCE is None:
        _NLP_INSTANCE = spacy.load(SPACY_MODEL_NAME)
    return _NLP_INSTANCE


def pluralizar(palavra: str) -> str:
    """
    Aplica regras morfológicas básicas de plural para substantivos e adjetivos em português.

    Regras:
    - Palavras terminadas em 'm' -> 'ns' (homem -> homens, jovem -> jovens)
    - Palavras terminadas em 'r', 'z', 's' -> '+es' (professor -> professores, rapaz -> rapazes)
    - Demais terminações vocálicas -> '+s' (menino -> meninos)
    """
    if palavra.endswith("m"):
        return palavra[:-1] + "ns"
    if palavra.endswith(("r", "z", "s")):
        return palavra + "es"
    return palavra + "s"


def preservar_caixa(original: str, nova: str) -> str:
    """
    Preserva a capitalização da palavra original ao aplicar a forma substituta:
    - Se a original for toda maiúscula (ex.: 'MENINO') -> 'MENINA'
    - Se a original começar com maiúscula (ex.: 'Menino') -> 'Menina'
    - Se for minúscula (ex.: 'menino') -> 'menina'
    """
    if len(original) > 1 and original.isupper():
        return nova.upper()
    if original and original[0].isupper():
        return nova[0].upper() + nova[1:]
    return nova
