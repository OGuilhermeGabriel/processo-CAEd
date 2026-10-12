"""
Operador 2: Troca de Gênero Gramatical Guiada pela Árvore Sintática do spaCy.
Restringe a flexão a substantivos biformes (seres animados) e propaga a concordância
exclusivamente para os dependentes sintáticos diretos.
"""

from typing import Dict, Optional
from spacy.tokens import Token

from src.utils.helpers import get_spacy_model, preservar_caixa, pluralizar

# Base de substantivos biformes (pessoas e animais)
_BIFORMES_BASE: Dict[str, str] = {
    "menino": "menina",
    "garoto": "garota",
    "aluno": "aluna",
    "amigo": "amiga",
    "filho": "filha",
    "irmão": "irmã",
    "tio": "tia",
    "primo": "prima",
    "avô": "avó",
    "pai": "mãe",
    "homem": "mulher",
    "rei": "rainha",
    "príncipe": "princesa",
    "cantor": "cantora",
    "jogador": "jogadora",
    "professor": "professora",
    "autor": "autora",
    "inventor": "inventora",
    "escritor": "escritora",
    "senhor": "senhora",
    "doutor": "doutora",
    "médico": "médica",
    "gato": "gata",
    "cachorro": "cachorra",
    "lobo": "loba",
}
SUBST_BIFORMES: Dict[str, str] = {**_BIFORMES_BASE, **{f: m for m, f in _BIFORMES_BASE.items()}}

# Tabela de determinantes, artigos e contrações
_DET_BASE: Dict[str, str] = {
    "o": "a",
    "os": "as",
    "um": "uma",
    "uns": "umas",
    "do": "da",
    "dos": "das",
    "no": "na",
    "nos": "nas",
    "ao": "à",
    "aos": "às",
    "pelo": "pela",
    "pelos": "pelas",
    "num": "numa",
    "nuns": "numas",
    "este": "esta",
    "estes": "estas",
    "esse": "essa",
    "esses": "essas",
    "aquele": "aquela",
    "aqueles": "aquelas",
    "deste": "desta",
    "desse": "dessa",
    "daquele": "daquela",
    "neste": "nesta",
    "nesse": "nessa",
    "naquele": "naquela",
    "meu": "minha",
    "meus": "minhas",
    "teu": "tua",
    "teus": "tuas",
    "seu": "sua",
    "seus": "suas",
    "nosso": "nossa",
    "nossos": "nossas",
    "outro": "outra",
    "outros": "outras",
    "todo": "toda",
    "todos": "todas",
    "algum": "alguma",
    "alguns": "algumas",
    "nenhum": "nenhuma",
}
DETERMINANTES: Dict[str, str] = {**_DET_BASE, **{f: m for m, f in _DET_BASE.items()}}

ADJ_INVARIAVEIS = {
    "melhor",
    "pior",
    "maior",
    "menor",
    "superior",
    "inferior",
    "anterior",
    "posterior",
    "interior",
    "exterior",
}

ADJ_IRREGULARES: Dict[str, str] = {
    "bom": "boa",
    "boa": "bom",
    "mau": "má",
    "má": "mau",
}


def flexionar_adjetivo(palavra: str) -> Optional[str]:
    """Inverte o gênero de adjetivos e particípios regulares ou irregulares."""
    w = palavra.lower()
    if w in ADJ_IRREGULARES:
        return ADJ_IRREGULARES[w]
    if w in ADJ_INVARIAVEIS or w.endswith(("ão", "ões")):
        return None

    regras = [
        ("oras", "ores"),
        ("ores", "oras"),
        ("ora", "or"),
        ("os", "as"),
        ("as", "os"),
        ("o", "a"),
        ("a", "o"),
        ("or", "ora"),
    ]
    for sufixo, troca in regras:
        if w.endswith(sufixo):
            return w[: -len(sufixo)] + troca
    return None


def flexionar_substantivo(token: Token) -> Optional[str]:
    """Retorna a forma no gênero oposto se o token for um substantivo biforme (singular ou plural)."""
    if token.pos_ != "NOUN":
        return None
    w = token.text.lower()
    if w in SUBST_BIFORMES:
        return SUBST_BIFORMES[w]

    for singular in (w[:-1], w[:-2], w[:-2] + "m"):
        if singular in SUBST_BIFORMES and pluralizar(singular) == w:
            return pluralizar(SUBST_BIFORMES[singular])
    return None


def mutador_troca_genero(texto: str) -> str:
    """
    Inverte o gênero gramatical de narrativas com rigor sintático:
    - Identifica substantivos biformes (pessoas e animais);
    - Navega pela árvore de dependências do spaCy;
    - Flexiona exclusivamente os determinantes, adjetivos diretos e predicativos do sujeito ligados ao alvo;
    - Deixa intactos substantivos inanimados (casa, imagem, ano, vidro) e preposições homógrafas.

    Args:
        texto: Texto a ser mutado.

    Returns:
        Texto com gênero gramatical invertido.
    """
    nlp = get_spacy_model()
    doc = nlp(texto)
    trocas = {}

    for token in doc:
        novo = flexionar_substantivo(token)
        if novo is None:
            continue
        trocas[token.i] = novo

        # (a) Dependentes diretos: artigos, possessivos, demonstrativos e adjetivos
        for filho in token.children:
            if filho.i in trocas:
                continue
            w = filho.text.lower()
            if w in DETERMINANTES:
                trocas[filho.i] = DETERMINANTES[w]
            elif filho.pos_ == "ADJ":
                adj = flexionar_adjetivo(filho.text)
                if adj:
                    trocas[filho.i] = adj

        # (b) Predicativo do sujeito ou particípio passivo vinculado ao sujeito
        cabeca = token.head
        if token.dep_.startswith("nsubj") and cabeca.i not in trocas:
            eh_participio = "Part" in cabeca.morph.get("VerbForm")
            if cabeca.pos_ == "ADJ" or (cabeca.pos_ in ("VERB", "AUX") and eh_participio):
                adj = flexionar_adjetivo(cabeca.text)
                if adj:
                    trocas[cabeca.i] = adj

    return "".join(
        preservar_caixa(t.text, trocas[t.i]) + t.whitespace_ if t.i in trocas else t.text_with_ws
        for t in doc
    )
