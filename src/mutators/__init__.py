"""
Módulo contendo os operadores de mutação textual e cálculo de impacto na complexidade.
"""

from src.mutators.word_swap import mutador_troca_palavras
from src.mutators.gender_swap import mutador_troca_genero
from src.mutators.paraphrase import mutador_parafrase
from src.mutators.impact import (
    score_complexidade,
    taxa_palavras_inventadas,
    avaliar_impacto_mutacao,
    ResultadoImpacto,
)

__all__ = [
    "mutador_troca_palavras",
    "mutador_troca_genero",
    "mutador_parafrase",
    "score_complexidade",
    "taxa_palavras_inventadas",
    "avaliar_impacto_mutacao",
    "ResultadoImpacto",
]
