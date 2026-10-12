"""
Funções para carregamento e parsing estruturado do dataset_caed.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

from src.config import DATASET_DIR, MAPEAMENTO_PASTAS


def carregar_corpus_caed(caminho_base: Optional[Path] = None) -> pd.DataFrame:
    """
    Percorre as pastas do dataset_caed e consolida todos os arquivos .txt em um DataFrame pandas.

    Args:
        caminho_base: Caminho customizado para o diretório dataset_caed (opcional).

    Returns:
        pd.DataFrame com colunas: ['arquivo', 'nivel', 'nivel_ord', 'pasta', 'texto'].
    """
    caminho = Path(caminho_base) if caminho_base is not None else DATASET_DIR
    if not caminho.exists():
        raise FileNotFoundError(f"Diretório do dataset não encontrado em: {caminho}")

    dados = []
    for pasta, (nome_nivel, ordem) in MAPEAMENTO_PASTAS.items():
        diretorio_pasta = caminho / pasta
        if not diretorio_pasta.exists():
            continue

        for arq in sorted(diretorio_pasta.glob("*.txt")):
            try:
                texto = arq.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                texto = arq.read_text(encoding="latin-1")

            texto_limpo = texto.strip()
            if not texto_limpo:
                continue

            dados.append({
                "arquivo": arq.name,
                "nivel": nome_nivel,
                "nivel_ord": ordem,
                "pasta": pasta,
                "texto": texto_limpo,
            })

    df = pd.DataFrame(dados)
    return df


carregar_dataset_caed = carregar_corpus_caed
