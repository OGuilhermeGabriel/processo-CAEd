"""
Módulo para cálculo de métricas de avaliação e diagnóstico de modelos preditivos.
"""

from typing import Dict, List, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

from src.config import ORDEM_NIVEIS


def calcular_metricas_classificacao(
    y_true: List[str] | np.ndarray, y_pred: List[str] | np.ndarray
) -> Dict[str, float]:
    """
    Calcula as principais métricas de desempenho: Acurácia e F1-Score (macro e ponderado).

    Args:
        y_true: Rótulos reais da partição de teste.
        y_pred: Rótulos preditos pelo modelo.

    Returns:
        Dicionário com 'acuracia', 'f1_macro' e 'f1_weighted'.
    """
    return {
        "acuracia": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted")),
    }


def gerar_matriz_confusao(
    y_true: List[str] | np.ndarray,
    y_pred: List[str] | np.ndarray,
    labels: Optional[List[str]] = None,
) -> np.ndarray:
    """
    Gera a matriz de confusão estruturada de acordo com os níveis educacionais ordenados.

    Args:
        y_true: Rótulos reais.
        y_pred: Rótulos previstos.
        labels: Ordem explícita das classes. Se None, utiliza ORDEM_NIVEIS.

    Returns:
        Matriz numpy (n_classes x n_classes).
    """
    if labels is None:
        labels = ORDEM_NIVEIS
    return confusion_matrix(y_true, y_pred, labels=labels)


def gerar_relatorio_classificacao(
    y_true: List[str] | np.ndarray,
    y_pred: List[str] | np.ndarray,
    labels: Optional[List[str]] = None,
) -> str:
    """
    Gera o relatório textual do scikit-learn com precision, recall e f1-score por classe.
    """
    if labels is None:
        labels = ORDEM_NIVEIS
    return classification_report(y_true, y_pred, target_names=labels, digits=4)
