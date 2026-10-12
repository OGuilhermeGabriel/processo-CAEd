"""
Módulo para extração de métricas estruturais, léxicas e sintáticas de fragmentos textuais.
"""

import re
import numpy as np
import pandas as pd

from src.features.canonicity import calcular_taxa_canonicidade


REGEX_PALAVRAS = re.compile(r"\b[a-zA-ZÀ-ÿ0-9_]+\b")
REGEX_SENTENCAS = re.compile(r"[^.!?]+[.!?]*")


def extrair_metricas_superficiais(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula as métricas estatísticas superficiais para um DataFrame com a coluna 'texto'.

    Métricas calculadas:
    - num_caracteres: Comprimento total do fragmento textual.
    - num_palavras: Quantidade de tokens alfanuméricos.
    - num_sentencas: Número de sentenças delimitadas por pontuação terminal.
    - palavras_por_sentenca: Densidade sintática média da oração.
    - tam_medio_palavra: Média de caracteres por palavra.

    Args:
        df: DataFrame contendo a coluna 'texto'.

    Returns:
        DataFrame com as novas colunas inseridas.
    """
    df = df.copy()

    df["num_caracteres"] = df["texto"].apply(len)

    df["palavras"] = df["texto"].apply(lambda t: REGEX_PALAVRAS.findall(t))
    df["num_palavras"] = df["palavras"].apply(len)

    df["sentencas"] = df["texto"].apply(
        lambda t: [s.strip() for s in REGEX_SENTENCAS.findall(t) if s.strip()]
    )
    df["num_sentencas"] = df["sentencas"].apply(lambda s: max(len(s), 1))

    df["palavras_por_sentenca"] = df["num_palavras"] / df["num_sentencas"]
    df["tam_medio_palavra"] = df["palavras"].apply(
        lambda p: float(np.mean([len(w) for w in p])) if len(p) > 0 else 0.0
    )

    return df.drop(columns=["palavras", "sentencas"])


def extrair_features_instancia(texto: str) -> pd.DataFrame:
    """
    Extrai as 5 features numéricas contínuas + a coluna de texto requeridas
    pelo pipeline preditivo (Linear SVM / ColumnTransformer) para uma única instância de texto.

    Features:
    - texto: String original bruta para o vetorizador TF-IDF.
    - taxa_canonicidade: Proporção de palavras puramente CV.
    - tam_medio_palavra: Média de caracteres por palavra.
    - palavras_por_sentenca: Média de palavras por sentença.
    - num_palavras: Quantidade total de palavras.
    - num_caracteres: Quantidade total de caracteres.

    Args:
        texto: String contendo o fragmento textual bruto.

    Returns:
        pd.DataFrame de 1 linha contendo as features prontas para o predict/predict_proba do modelo.
    """
    palavras = REGEX_PALAVRAS.findall(texto)
    num_palavras = max(len(palavras), 1)
    num_caracteres = len(texto)

    sentencas = [s.strip() for s in REGEX_SENTENCAS.findall(texto) if s.strip()]
    num_sentencas = max(len(sentencas), 1)

    return pd.DataFrame(
        [
            {
                "texto": texto,
                "taxa_canonicidade": calcular_taxa_canonicidade(texto),
                "tam_medio_palavra": float(np.mean([len(w) for w in palavras])) if palavras else 0.0,
                "palavras_por_sentenca": num_palavras / num_sentencas,
                "num_palavras": num_palavras,
                "num_caracteres": num_caracteres,
            }
        ]
    )
