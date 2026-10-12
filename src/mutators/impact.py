"""
Módulo para avaliação do impacto das mutações na complexidade textual.
Implementa o cálculo do Score Contínuo ponderado, Delta de Classe,
e verificação léxica contra o vocabulário didático do CAEd.
"""

from dataclasses import dataclass
import re
from typing import Callable, Optional, Set
import joblib
import pandas as pd

from src.config import BEST_MODEL_PATH, MAPA_ORDINAL
from src.features.text_features import extrair_features_instancia

_MODEL_CACHE = None
_VOCAB_CACHE: Optional[Set[str]] = None


@dataclass
class ResultadoImpacto:
    """Estrutura com os resultados quantitativos da mutação."""

    texto_original: str
    texto_mutado: str
    nome_operador: str
    nivel_original: str
    nivel_mutado: str
    score_original: float
    score_mutado: float
    delta_classe: int
    delta_score: float
    taxa_palavras_inventadas: float


def get_trained_model():
    """Retorna o modelo calibrado carregado do disco (com cache)."""
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        if not BEST_MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Artefato do modelo não encontrado em {BEST_MODEL_PATH}. "
                "Execute 'python -m src.models.train' para treinar e salvar o modelo."
            )
        _MODEL_CACHE = joblib.load(BEST_MODEL_PATH)
    return _MODEL_CACHE


def get_vocab_corpus() -> Set[str]:
    """Retorna o vocabulário de palavras do corpus CAEd para teste de palavras inventadas."""
    global _VOCAB_CACHE
    if _VOCAB_CACHE is None:
        try:
            from src.data.loader import carregar_dataset_caed

            df = carregar_dataset_caed()
            tokens = set()
            for t in df["texto"]:
                for w in re.findall(r"\b[a-zA-ZÀ-ÿ]+\b", t.lower()):
                    tokens.add(w)
            _VOCAB_CACHE = tokens
        except Exception:
            _VOCAB_CACHE = set()
    return _VOCAB_CACHE


def score_complexidade(features_df: pd.DataFrame, model=None) -> float:
    """
    Calcula o nível esperado contínuo entre 1.0 e 4.0 a partir das
    probabilidades calibradas do classificador.

    Fórmula:
        Score = sum( P(Nivel_k | x) * Ordem_k )
    """
    if model is None:
        model = get_trained_model()
    proba = model.predict_proba(features_df)[0]
    return float(sum(p * MAPA_ORDINAL[c] for p, c in zip(proba, model.classes_)))


def taxa_palavras_inventadas(
    original: str, mutado: str, vocab_corpus: Optional[Set[str]] = None
) -> float:
    """
    Mede a proporção de palavras introduzidas pela mutação que não constam no corpus.
    Evita alucinações morfológicas ou quebras lexicais.
    """
    if vocab_corpus is None:
        vocab_corpus = get_vocab_corpus()

    tokenizar = lambda s: re.findall(r"\b[a-zA-ZÀ-ÿ]+\b", s.lower())
    originais = set(tokenizar(original))
    novas = [w for w in tokenizar(mutado) if w not in originais]

    if not novas:
        return 0.0
    if not vocab_corpus:
        return 0.0

    inventadas = sum(w not in vocab_corpus for w in novas)
    return float(inventadas / len(novas))


def avaliar_impacto_mutacao(
    texto_original: str,
    funcao_mutadora: Callable,
    nome_operador: str,
    model=None,
    vocab_corpus: Optional[Set[str]] = None,
    **kwargs,
) -> ResultadoImpacto:
    """
    Executa a mutação textual, infere complexidade antes e depois, calcula os deltas
    e verifica a integridade léxica.

    Args:
        texto_original: String com o fragmento antes da mutação.
        funcao_mutadora: Função de mutação a ser invocada.
        nome_operador: Nome descritivo do operador.
        model: Pipeline preditivo scikit-learn (opcional, carrega do disco por padrão).
        vocab_corpus: Conjunto de vocabulário de validação (opcional).

    Returns:
        Instância de ResultadoImpacto com todas as métricas calculadas.
    """
    if model is None:
        model = get_trained_model()

    texto_mutado = funcao_mutadora(texto_original, **kwargs)

    feat_orig = extrair_features_instancia(texto_original)
    feat_mut = extrair_features_instancia(texto_mutado)

    nivel_orig = str(model.predict(feat_orig)[0])
    nivel_mut = str(model.predict(feat_mut)[0])

    sc_orig = score_complexidade(feat_orig, model=model)
    sc_mut = score_complexidade(feat_mut, model=model)

    delta_classe = MAPA_ORDINAL[nivel_mut] - MAPA_ORDINAL[nivel_orig]
    delta_score = sc_mut - sc_orig
    tx_inventada = taxa_palavras_inventadas(texto_original, texto_mutado, vocab_corpus=vocab_corpus)

    return ResultadoImpacto(
        texto_original=texto_original,
        texto_mutado=texto_mutado,
        nome_operador=nome_operador,
        nivel_original=nivel_orig,
        nivel_mutado=nivel_mut,
        score_original=sc_orig,
        score_mutado=sc_mut,
        delta_classe=delta_classe,
        delta_score=delta_score,
        taxa_palavras_inventadas=tx_inventada,
    )
