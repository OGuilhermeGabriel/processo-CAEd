"""
Script para treinamento, calibração e exportação do modelo campeão de classificação de complexidade textual.
Pipeline:
- Pré-processamento: ColumnTransformer com TF-IDF (1-2 gramas) para 'texto' e StandardScaler para métricas numéricas.
- Classificador: CalibratedClassifierCV com LinearSVC (5-fold cross-validation para probabilidades calibradas).
"""

from pathlib import Path
from typing import Tuple
import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

from src.config import BEST_MODEL_PATH, FEATURES_NUMERICAS, MODELS_DIR, RANDOM_SEED
from src.data.loader import carregar_dataset_caed
from src.features.canonicity import calcular_taxa_canonicidade
from src.features.text_features import extrair_metricas_superficiais
from src.models.evaluate import (
    calcular_metricas_classificacao,
    gerar_relatorio_classificacao,
)


def construir_pipeline_modelo() -> Pipeline:
    """
    Constrói a arquitetura do pipeline scikit-learn campeão:
    - Ramo textual: TfidfVectorizer(max_features=2500, min_df=3, max_df=0.85, ngram_range=(1, 2))
    - Ramo numérico: StandardScaler() aplicado às 5 features estruturais/canonicidade
    - Estimador: CalibratedClassifierCV(LinearSVC(max_iter=2000, random_state=42), cv=5)
    """
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=2500,
                    min_df=3,
                    max_df=0.85,
                    ngram_range=(1, 2),
                ),
                "texto",
            ),
            ("scaler", StandardScaler(), FEATURES_NUMERICAS),
        ]
    )

    clf = CalibratedClassifierCV(
        estimator=LinearSVC(max_iter=2000, random_state=RANDOM_SEED),
        cv=5,
    )

    return Pipeline([("prep", preprocessor), ("clf", clf)])


def preparar_dados_completos() -> pd.DataFrame:
    """
    Carrega o dataset e extrai as features numéricas e de canonicidade necessárias para o treino.
    """
    df = carregar_dataset_caed()
    df = extrair_metricas_superficiais(df)
    df["taxa_canonicidade"] = df["texto"].apply(calcular_taxa_canonicidade)
    return df


def treinar_e_salvar_modelo(
    caminho_saida: Path = BEST_MODEL_PATH,
) -> Tuple[Pipeline, dict]:
    """
    Executa o ciclo completo de treinamento:
    1. Carregamento e engenharia de features dos dados.
    2. Split estratificado 80/20.
    3. Treinamento e calibração de probabilidades com validação cruzada interna de 5 folds.
    4. Avaliação e exibição de métricas na partição de teste.
    5. Serialização do artefato joblib no caminho indicado.

    Args:
        caminho_saida: Caminho para gravação do arquivo .joblib.

    Returns:
        Tupla contendo (pipeline_treinado, dicionario_metricas).
    """
    print("1/4 Carregando dataset e extraindo features completas...")
    df = preparar_dados_completos()

    X = df[["texto"] + FEATURES_NUMERICAS]
    y = df["nivel"]

    print("2/4 Dividindo em partições de Treino (80%) e Teste (20%) estratificadas...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_SEED,
    )

    print("3/4 Treinando e calibrando o pipeline LinearSVC...")
    pipeline = construir_pipeline_modelo()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    metricas = calcular_metricas_classificacao(y_test, y_pred)

    print("\n--- AVALIAÇÃO DO MODELO CAMPEÃO NO CONJUNTO DE TESTE ---")
    print(f"Acurácia : {metricas['acuracia']:.2%}")
    print(f"F1-Macro : {metricas['f1_macro']:.4f}")
    print("\nRelatório Detalhado por Nível:")
    print(gerar_relatorio_classificacao(y_test, y_pred))

    print(f"4/4 Exportando modelo treinado para: {caminho_saida}")
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, caminho_saida)
    print("✓ Modelo salvo com sucesso!\n")

    return pipeline, metricas


if __name__ == "__main__":
    treinar_e_salvar_modelo()
