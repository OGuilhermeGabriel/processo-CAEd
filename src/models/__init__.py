"""
Módulo para modelagem preditiva, treinamento e avaliação de modelos de Machine Learning.
"""

from src.models.evaluate import (
    calcular_metricas_classificacao,
    gerar_matriz_confusao,
    gerar_relatorio_classificacao,
)

__all__ = [
    "calcular_metricas_classificacao",
    "gerar_matriz_confusao",
    "gerar_relatorio_classificacao",
]
