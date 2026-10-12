"""
Módulo de extração e processamento de features linguísticas e fonológicas.
"""

from src.features.canonicity import (
    classificar_canonicidade,
    calcular_taxa_canonicidade,
    EXEMPLOS_EDITAL,
)
from src.features.text_features import (
    extrair_metricas_superficiais,
    extrair_features_instancia,
)

__all__ = [
    "classificar_canonicidade",
    "calcular_taxa_canonicidade",
    "EXEMPLOS_EDITAL",
    "extrair_metricas_superficiais",
    "extrair_features_instancia",
]
