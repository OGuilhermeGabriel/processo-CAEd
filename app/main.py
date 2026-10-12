"""
Aplicação principal FastAPI para servir o modelo preditivo de complexidade textual
e os operadores de mutação do Processo Seletivo CAEd.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict
import joblib
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.schemas import (
    AnalyzeImpactRequest,
    AnalyzeImpactResponse,
    HealthResponse,
    MetricasLinguisticas,
    ModoTrocaPalavras,
    MutateRequest,
    MutateResponse,
    PredictRequest,
    PredictResponse,
    TipoOperador,
)
from src.config import BEST_MODEL_PATH, MAPA_ORDINAL
from src.features.text_features import extrair_features_instancia
from src.mutators.gender_swap import mutador_troca_genero
from src.mutators.impact import get_vocab_corpus, score_complexidade, taxa_palavras_inventadas
from src.mutators.paraphrase import mutador_parafrase
from src.mutators.word_swap import mutador_troca_palavras

# Diretórios base da aplicação web
APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
TEMPLATES_DIR = APP_DIR / "templates"

# Garantir existência dos diretórios de interface
STATIC_DIR.mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "css").mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "js").mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# Cache do modelo carregado em memória
app_state: Dict[str, Any] = {
    "model": None,
    "vocab_corpus": None,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida da API:
    Carrega o modelo campeão e o vocabulário de validação na memória ao iniciar,
    garantindo inferências instantâneas sem overhead de I/O em disco.
    """
    print("🚀 [FastAPI] Inicializando servidor e carregando artefatos...")
    if not BEST_MODEL_PATH.exists():
        print(f"⚠️ [FastAPI] Modelo não encontrado em {BEST_MODEL_PATH}!")
    else:
        app_state["model"] = joblib.load(BEST_MODEL_PATH)
        print(f"✓ [FastAPI] Modelo carregado com sucesso de: {BEST_MODEL_PATH}")

    # Pré-carrega o vocabulário léxico do corpus CAEd em background
    app_state["vocab_corpus"] = get_vocab_corpus()
    print(f"✓ [FastAPI] Vocabulário carregado com {len(app_state['vocab_corpus'])} termos únicos.")

    yield

    print("🛑 [FastAPI] Encerrando servidor e liberando recursos.")
    app_state["model"] = None
    app_state["vocab_corpus"] = None


# Instanciação da aplicação FastAPI
app = FastAPI(
    title="API de Predição de Complexidade Textual e Mutações — CAEd",
    description=(
        "API RESTful para inferência de nível de leitura (Ensino Fundamental I e II, "
        "Ensino Médio e Superior), extração de canonicidade fonológica (sílabas CV) "
        "e avaliação experimental do impacto de operadores de mutação textual."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Configuração de CORS (permite integração fluida com frontends modernos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montagem de arquivos estáticos e templates Jinja2
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _get_model():
    """Recupera a instância do modelo em memória ou levanta exceção amigável."""
    model = app_state.get("model")
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "O modelo preditivo ainda não está carregado ou não foi encontrado em disco. "
                "Execute 'python -m src.models.train' para treiná-lo e salvá-lo."
            ),
        )
    return model


def _extrair_metricas_pydantic(df_feat) -> MetricasLinguisticas:
    """Converte o DataFrame de features em um objeto Pydantic validado."""
    row = df_feat.iloc[0]
    return MetricasLinguisticas(
        taxa_canonicidade=float(row["taxa_canonicidade"]),
        tam_medio_palavra=float(row["tam_medio_palavra"]),
        palavras_por_sentenca=float(row["palavras_por_sentenca"]),
        num_palavras=int(row["num_palavras"]),
        num_caracteres=int(row["num_caracteres"]),
    )


# ==============================================================================
# Rotas da API REST
# ==============================================================================


@app.get("/", response_class=HTMLResponse, summary="Página inicial (Dashboard Web)")
async def index(request: Request):
    """Renderiza a interface web interativa do projeto."""
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse(
            "<h2>Interface Web em construção (Etapa 3). Acesse a documentação interativa da API em <a href='/docs'>/docs</a>.</h2>"
        )
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health", response_model=HealthResponse, summary="Diagnóstico de saúde da aplicação")
async def health_check():
    """Retorna o status operacional da API e a disponibilidade do modelo em memória."""
    return HealthResponse(
        status="ok",
        modelo_carregado=(app_state.get("model") is not None),
        versao="1.0.0",
    )


@app.post(
    "/predict",
    response_model=PredictResponse,
    summary="Predição de nível de leitura e métricas linguísticas",
)
async def predict_complexidade(payload: PredictRequest):
    """
    Classifica o nível educacional mais provável para o fragmento textual,
    calcula o score contínuo ponderado [1.0 - 4.0], a distribuição de probabilidades
    calibradas e todas as métricas fonológicas (taxa de canonicidade) e estruturais.
    """
    model = _get_model()

    feat_df = extrair_features_instancia(payload.texto)
    nivel_previsto = str(model.predict(feat_df)[0])
    score = score_complexidade(feat_df, model=model)

    probabilidades = {
        classe: float(p)
        for classe, p in zip(model.classes_, model.predict_proba(feat_df)[0])
    }

    metricas = _extrair_metricas_pydantic(feat_df)

    return PredictResponse(
        texto=payload.texto,
        nivel_previsto=nivel_previsto,
        score_continuo=round(score, 4),
        probabilidades=probabilidades,
        metricas=metricas,
    )


@app.post(
    "/mutate",
    response_model=MutateResponse,
    summary="Geração de mutação textual via operadores linguísticos",
)
async def aplicar_mutacao(payload: MutateRequest):
    """
    Aplica um dos três operadores de mutação textual sobre o texto fornecido:
    - troca_palavras (sinônimos ou antônimos via NLTK WordNet)
    - troca_genero (inversão morfológica com spaCy)
    - parafrase (reestruturação sintática e conversão de voz passiva)
    """
    texto = payload.texto
    operador = payload.operador
    params_usados: Dict[str, Any] = {}

    if operador == TipoOperador.TROCA_PALAVRAS:
        modo = payload.modo_palavras.value
        prob = payload.prob_troca
        seed = payload.seed or 42
        params_usados = {"modo": modo, "prob_troca": prob, "seed": seed}
        texto_mutado = mutador_troca_palavras(
            texto,
            modo=modo,
            prob_troca=prob,
            seed=seed,
        )
    elif operador == TipoOperador.TROCA_GENERO:
        params_usados = {"operador": "flexao_genero"}
        texto_mutado = mutador_troca_genero(texto)
    elif operador == TipoOperador.PARAFRASE:
        params_usados = {"operador": "reestruturacao_sintatica"}
        texto_mutado = mutador_parafrase(texto)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operador '{operador}' não suportado.",
        )

    return MutateResponse(
        texto_original=texto,
        texto_mutado=texto_mutado,
        operador=operador,
        parametros_usados=params_usados,
    )


@app.post(
    "/analyze-impact",
    response_model=AnalyzeImpactResponse,
    summary="Avaliação comparativa de impacto na complexidade e integridade léxica",
)
async def analisar_impacto(payload: AnalyzeImpactRequest):
    """
    Executa o ciclo completo de experimentação:
    1. Aplica a mutação solicitada no texto.
    2. Extrai métricas de ambas as versões (original e mutada).
    3. Infere o nível educacional e calcula o Score Contínuo ponderado de ambas.
    4. Computa os deltas de classe e de score contínuo.
    5. Mede a taxa de palavras inéditas fora do vocabulário do corpus CAEd.
    """
    model = _get_model()
    texto_original = payload.texto
    operador = payload.operador

    # 1. Executa a mutação
    if operador == TipoOperador.TROCA_PALAVRAS:
        texto_mutado = mutador_troca_palavras(
            texto_original,
            modo=payload.modo_palavras.value,
            prob_troca=payload.prob_troca,
            seed=payload.seed or 42,
        )
    elif operador == TipoOperador.TROCA_GENERO:
        texto_mutado = mutador_troca_genero(texto_original)
    elif operador == TipoOperador.PARAFRASE:
        texto_mutado = mutador_parafrase(texto_original)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Operador '{operador}' não suportado.",
        )

    # 2. Extrai features e calcula predições para ambas as versões
    feat_orig = extrair_features_instancia(texto_original)
    feat_mut = extrair_features_instancia(texto_mutado)

    nivel_orig = str(model.predict(feat_orig)[0])
    nivel_mut = str(model.predict(feat_mut)[0])

    sc_orig = score_complexidade(feat_orig, model=model)
    sc_mut = score_complexidade(feat_mut, model=model)

    delta_classe = MAPA_ORDINAL[nivel_mut] - MAPA_ORDINAL[nivel_orig]
    delta_score = sc_mut - sc_orig

    # 3. Taxa de palavras fora do vocabulário
    tx_inventada = taxa_palavras_inventadas(
        texto_original,
        texto_mutado,
        vocab_corpus=app_state.get("vocab_corpus"),
    )

    # 4. Status descritivo do impacto
    if delta_classe == 0:
        impacto_status = "Preservada (Δ = 0)"
    elif delta_classe > 0:
        impacto_status = f"Aumentou complexidade (+{delta_classe})"
    else:
        impacto_status = f"Diminuiu complexidade ({delta_classe})"

    return AnalyzeImpactResponse(
        texto_original=texto_original,
        texto_mutado=texto_mutado,
        operador=operador,
        nivel_original=nivel_orig,
        nivel_mutado=nivel_mut,
        score_original=round(sc_orig, 4),
        score_mutado=round(sc_mut, 4),
        delta_classe=delta_classe,
        delta_score=round(delta_score, 4),
        taxa_palavras_inventadas=round(tx_inventada, 4),
        impacto_status=impacto_status,
        metricas_original=_extrair_metricas_pydantic(feat_orig),
        metricas_mutado=_extrair_metricas_pydantic(feat_mut),
    )
