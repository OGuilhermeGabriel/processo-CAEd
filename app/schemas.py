"""
Esquemas de dados (Pydantic models) para validação de entrada e serialização de saída da API REST.
"""

from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class TipoOperador(str, Enum):
    """Operadores de mutação textual suportados pelo sistema."""

    TROCA_PALAVRAS = "troca_palavras"
    TROCA_GENERO = "troca_genero"
    PARAFRASE = "parafrase"


class ModoTrocaPalavras(str, Enum):
    """Modos de substituição para o operador de troca de palavras."""

    SINONIMO = "sinonimo"
    ANTONIMO = "antonimo"


# ==============================================================================
# Modelos de Métricas Auxiliares
# ==============================================================================


class MetricasLinguisticas(BaseModel):
    """Métricas linguísticas e fonológicas extraídas do fragmento textual."""

    taxa_canonicidade: float = Field(
        ...,
        description="Proporção de palavras estritamente formadas por sílabas CV",
        ge=0.0,
        le=1.0,
    )
    tam_medio_palavra: float = Field(
        ...,
        description="Média de caracteres por palavra",
        ge=0.0,
    )
    palavras_por_sentenca: float = Field(
        ...,
        description="Densidade sintática (palavras por oração)",
        ge=0.0,
    )
    num_palavras: int = Field(
        ...,
        description="Contagem total de tokens de palavras",
        ge=0,
    )
    num_caracteres: int = Field(
        ...,
        description="Contagem total de caracteres",
        ge=0,
    )


# ==============================================================================
# Requisições (Input Schemas)
# ==============================================================================


class PredictRequest(BaseModel):
    """Payload de entrada para classificação de nível de leitura."""

    texto: str = Field(
        ...,
        min_length=3,
        description="Texto em língua portuguesa a ser avaliado",
        examples=["O menino leu o livro com muita atenção na sala de aula."],
    )


class MutateRequest(BaseModel):
    """Payload de entrada para geração de texto mutado."""

    texto: str = Field(
        ...,
        min_length=3,
        description="Texto original a ser transformado",
        examples=["O aluno dedicado leu o texto com bastante calma."],
    )
    operador: TipoOperador = Field(
        default=TipoOperador.TROCA_PALAVRAS,
        description="Operador de mutação a ser aplicado",
    )
    modo_palavras: ModoTrocaPalavras = Field(
        default=ModoTrocaPalavras.SINONIMO,
        description="Substituir por sinônimos ou antônimos (apenas para operador troca_palavras)",
    )
    prob_troca: float = Field(
        default=0.35,
        ge=0.0,
        le=1.0,
        description="Probabilidade de substituição de tokens elegíveis",
    )
    seed: Optional[int] = Field(
        default=42,
        description="Semente para garantia de determinismo e reprodutibilidade",
    )


class AnalyzeImpactRequest(BaseModel):
    """Payload de entrada para análise comparativa de impacto na complexidade."""

    texto: str = Field(
        ...,
        min_length=3,
        description="Texto original para mensuração comparativa",
        examples=["O texto foi lido pela professora na aula."],
    )
    operador: TipoOperador = Field(
        default=TipoOperador.PARAFRASE,
        description="Operador de mutação a ser testado",
    )
    modo_palavras: ModoTrocaPalavras = Field(
        default=ModoTrocaPalavras.SINONIMO,
        description="Substituir por sinônimos ou antônimos (se aplicável)",
    )
    prob_troca: float = Field(
        default=0.35,
        ge=0.0,
        le=1.0,
        description="Probabilidade de substituição de palavras elegíveis",
    )
    seed: Optional[int] = Field(
        default=42,
        description="Semente pseudoaleatória",
    )


# ==============================================================================
# Respostas (Output Schemas)
# ==============================================================================


class PredictResponse(BaseModel):
    """Payload de retorno da inferência preditiva."""

    texto: str = Field(..., description="Texto avaliado")
    nivel_previsto: str = Field(
        ...,
        description="Nível educacional mais provável previsto pelo modelo",
    )
    score_continuo: float = Field(
        ...,
        description="Nível contínuo ponderado entre 1.0 e 4.0 baseado nas probabilidades",
        ge=1.0,
        le=4.0,
    )
    probabilidades: Dict[str, float] = Field(
        ...,
        description="Distribuição calibrada de probabilidades por nível educacional",
    )
    metricas: MetricasLinguisticas = Field(
        ...,
        description="Métricas estruturais e fonológicas calculadas",
    )


class MutateResponse(BaseModel):
    """Payload de retorno da aplicação de mutação."""

    texto_original: str = Field(..., description="Texto de entrada")
    texto_mutado: str = Field(..., description="Texto gerado pela mutação")
    operador: TipoOperador = Field(..., description="Operador aplicado")
    parametros_usados: Dict[str, Any] = Field(
        default_factory=dict,
        description="Hiperparâmetros utilizados na mutação",
    )


class AnalyzeImpactResponse(BaseModel):
    """Payload de retorno da avaliação comparativa de impacto."""

    texto_original: str = Field(..., description="Texto de partida")
    texto_mutado: str = Field(..., description="Texto resultante da mutação")
    operador: TipoOperador = Field(..., description="Operador avaliado")
    nivel_original: str = Field(..., description="Nível previsto do texto original")
    nivel_mutado: str = Field(..., description="Nível previsto do texto mutado")
    score_original: float = Field(..., description="Score contínuo [1.0 - 4.0] original")
    score_mutado: float = Field(..., description="Score contínuo [1.0 - 4.0] mutado")
    delta_classe: int = Field(
        ...,
        description="Variação discreta de nível educacional (mutado - original)",
    )
    delta_score: float = Field(
        ...,
        description="Variação contínua de complexidade (mutado - original)",
    )
    taxa_palavras_inventadas: float = Field(
        ...,
        description="Proporção de palavras inéditas que não constam no corpus CAEd",
        ge=0.0,
        le=1.0,
    )
    impacto_status: str = Field(
        ...,
        description="Interpretação textual do impacto (Preservada, Aumentou ou Diminuiu)",
    )
    metricas_original: MetricasLinguisticas = Field(
        ...,
        description="Métricas do texto original",
    )
    metricas_mutado: MetricasLinguisticas = Field(
        ...,
        description="Métricas do texto mutado",
    )


class HealthResponse(BaseModel):
    """Status operacional do serviço e do modelo preditivo."""

    status: str = Field(default="ok", description="Status da API")
    modelo_carregado: bool = Field(
        ...,
        description="Indica se o artefato best_model.joblib está pronto em memória",
    )
    versao: str = Field(default="1.0.0", description="Versão da aplicação")
