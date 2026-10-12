"""
Módulo de configurações e constantes globais do projeto.
"""

from pathlib import Path
from typing import Dict, List

# Caminhos base do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT_DIR / "dataset_caed"
MODELS_DIR = ROOT_DIR / "models"
BEST_MODEL_PATH = MODELS_DIR / "best_model.joblib"

# Mapeamentos educacionais e ordinais
ORDEM_NIVEIS: List[str] = [
    "Ensino Fundamental I",
    "Ensino Fundamental II",
    "Ensino Médio",
    "Ensino Superior",
]

MAPA_ORDINAL: Dict[str, int] = {
    "Ensino Fundamental I": 1,
    "Ensino Fundamental II": 2,
    "Ensino Médio": 3,
    "Ensino Superior": 4,
}

MAPEAMENTO_PASTAS: Dict[str, tuple[str, int]] = {
    "1_Ensino_Fundamental_I": ("Ensino Fundamental I", 1),
    "2_Ensino_Fundamental_II": ("Ensino Fundamental II", 2),
    "3_Ensino_Medio": ("Ensino Médio", 3),
    "4_Ensino_Superior": ("Ensino Superior", 4),
}

# Features numéricas do modelo
FEATURES_NUMERICAS: List[str] = [
    "taxa_canonicidade",
    "tam_medio_palavra",
    "palavras_por_sentenca",
    "num_palavras",
    "num_caracteres",
]

# Semente pseudoaleatória global para reprodutibilidade
RANDOM_SEED: int = 42

# Modelo padrão do spaCy para Língua Portuguesa
SPACY_MODEL_NAME: str = "pt_core_news_sm"
