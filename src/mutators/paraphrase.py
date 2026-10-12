"""
Operador 3: Paráfrase e Reestruturação Sintática de Orações.
Aplica transformações determinísticas preservando coerência e significado:
1. Inversão de adjuntos adverbiais temporais antepostos.
2. Conversão de voz passiva analítica para voz ativa com flexão verbal correta.
3. Inversão de aposto identificador com núcleo próprio.
"""

import re
from typing import Dict, Optional, Tuple

from src.utils.helpers import get_spacy_model

ARTIGO_AGENTE: Dict[str, str] = {
    "pelo": "O",
    "pela": "A",
    "pelos": "Os",
    "pelas": "As",
}

PARTICIPIOS_IRREGULARES: Dict[str, Tuple[str, str]] = {
    "lido": ("leu", "leram"),
    "escrito": ("escreveu", "escreveram"),
    "feito": ("fez", "fizeram"),
    "visto": ("viu", "viram"),
    "dito": ("disse", "disseram"),
    "aberto": ("abriu", "abriram"),
    "descoberto": ("descobriu", "descobriram"),
    "posto": ("pôs", "puseram"),
    "vendido": ("vendeu", "venderam"),
    "recebido": ("recebeu", "receberam"),
    "escolhido": ("escolheu", "escolheram"),
    "conhecido": ("conheceu", "conheceram"),
    "construído": ("construiu", "construíram"),
    "destruído": ("destruiu", "destruíram"),
}

REGEX_TEMPO = re.compile(
    r"^(Há\s+.+?\s+atrás|Na época[^,]+|Durante [^,]+|Antigamente)[,\s]+(.+?)([.!?]?)$",
    flags=re.IGNORECASE,
)

REGEX_PASSIVA = re.compile(
    r"^(?P<paciente>.+?)\s+(?:foi|foram)\s+(?P<part>[a-zA-ZÀ-ÿ]+?(?:d|t)[oa]s?)\s+"
    r"(?P<prep>pel[oa]s?)\s+(?P<agente>.+?)(?P<fim>[.!?]?)$",
    flags=re.IGNORECASE,
)


def _minuscula_inicial(s: str) -> str:
    """Converte apenas o primeiro caractere da string para minúsculo."""
    return s[0].lower() + s[1:] if s else s


def _participio_para_ativo(participio: str, plural: bool) -> Optional[str]:
    """
    Converte um particípio passado (regular ou irregular) para a terceira pessoa
    do singular ou plural do pretérito perfeito do indicativo.
    """
    base = re.sub(r"(a|os|as)$", "o", participio.lower())
    if base in PARTICIPIOS_IRREGULARES:
        return PARTICIPIOS_IRREGULARES[base][1 if plural else 0]
    if base.endswith("ado"):
        return base[:-3] + ("aram" if plural else "ou")
    return None


def _inverter_aposto(sent) -> Optional[str]:
    """
    Identifica estruturas como 'O cantor Roberto Carlos fez...' e inverte
    para 'Roberto Carlos, o cantor, fez...'.
    """
    toks = list(sent)
    if (
        len(toks) < 4
        or toks[0].pos_ != "DET"
        or toks[1].pos_ != "NOUN"
        or toks[2].pos_ != "PROPN"
    ):
        return None

    j = 2
    while j < len(toks) and toks[j].pos_ == "PROPN":
        j += 1

    if j >= len(toks) or toks[j].is_punct or toks[j].pos_ == "ADP":
        return None

    return f"{sent[2:j].text}, {_minuscula_inicial(sent[0:2].text)}, {sent[j:].text}"


def _parafrasear_sentenca(sent) -> str:
    """Aplica as transformações heurísticas sobre uma sentença do spaCy."""
    s = sent.text.strip()

    # 1. Inversão de adjunto temporal anteposto
    m_tempo = REGEX_TEMPO.match(s)
    if m_tempo:
        adjunto, principal, fim = m_tempo.group(1), m_tempo.group(2), m_tempo.group(3) or "."
        return f"{principal[0].upper() + principal[1:]} {_minuscula_inicial(adjunto)}{fim}"

    # 2. Conversão de voz passiva analítica para ativa
    m_passiva = REGEX_PASSIVA.match(s)
    if m_passiva:
        prep = m_passiva.group("prep").lower()
        verbo = _participio_para_ativo(m_passiva.group("part"), plural=prep.endswith("s"))
        if verbo:
            agente = m_passiva.group("agente")
            paciente = _minuscula_inicial(m_passiva.group("paciente"))
            fim = m_passiva.group("fim") or "."
            return f"{ARTIGO_AGENTE[prep]} {agente} {verbo} {paciente}{fim}"

    # 3. Inversão de aposto
    aposto = _inverter_aposto(sent)
    if aposto:
        return aposto

    return s


def mutador_parafrase(texto: str) -> str:
    """
    Operador 3: Reestrutura sintaticamente orações no texto respeitando
    parágrafos e fluxo discursivo.

    Args:
        texto: Texto original em português.

    Returns:
        Texto com transformações de paráfrase aplicadas.
    """
    nlp = get_spacy_model()
    linhas = []
    for linha in texto.split("\n"):
        if not linha.strip():
            linhas.append(linha)
            continue
        sentencas = list(nlp(linha).sents)
        linhas.append(" ".join(_parafrasear_sentenca(s) for s in sentencas))
    return "\n".join(linhas)
