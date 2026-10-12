"""
Operador 1: Troca de Palavras de Conteúdo por Sinônimos ou Antônimos.
Utiliza OpenWordNet-PT (NLTK) filtrado por classe gramatical e dicionário de apoio para antônimos.
"""

import random
from typing import Dict, List, Optional, Set
from nltk.corpus import wordnet as wn

from src.utils.helpers import get_spacy_model, preservar_caixa, pluralizar

# Mapeamento do dicionário de apoio para antônimos universais e frequentes
ANTONIMOS_PT: Dict[str, str] = {
    "alegre": "triste",
    "triste": "alegre",
    "feliz": "infeliz",
    "infeliz": "feliz",
    "grande": "pequeno",
    "pequeno": "grande",
    "bom": "mau",
    "mau": "bom",
    "bonito": "feio",
    "feio": "bonito",
    "claro": "escuro",
    "escuro": "claro",
    "alto": "baixo",
    "baixo": "alto",
    "fácil": "difícil",
    "difícil": "fácil",
    "rápido": "lento",
    "lento": "rápido",
    "novo": "velho",
    "velho": "novo",
    "forte": "fraco",
    "fraco": "forte",
    "cheio": "vazio",
    "vazio": "cheio",
    "aberto": "fechado",
    "fechado": "aberto",
    "correto": "errado",
    "errado": "correto",
    "começo": "fim",
    "fim": "começo",
    "início": "fim",
    "final": "início",
    "subir": "descer",
    "descer": "subir",
    "entrar": "sair",
    "sair": "entrar",
    "ganhar": "perder",
    "perder": "ganhar",
    "comprar": "vender",
    "vender": "comprar",
}

# Mapeamento entre tags POS do spaCy e synset POS do WordNet
POS_WORDNET = {
    "NOUN": {"n"},
    "ADJ": {"a", "s"},
    "VERB": {"v"},
}


def obter_sinonimos_wordnet(lema: str, pos_spacy: str) -> List[str]:
    """
    Consulta a WordNet em busca de sinônimos em português restritos estritamente
    à mesma classe gramatical (POS) do token original.
    Usa ordenação determinística ('sorted') para garantir 100% de reprodutibilidade com seed.
    """
    pos_validos = POS_WORDNET.get(pos_spacy, set())
    sinonimos = set()

    for syn in wn.synsets(lema, lang="por"):
        if syn.pos() not in pos_validos:
            continue
        for lemma in syn.lemmas("por"):
            nome = lemma.name().replace("_", " ").lower()
            if nome != lema.lower() and " " not in nome:
                sinonimos.add(nome)

    return sorted(sinonimos)


def genero_aparente(palavra: str) -> Optional[str]:
    """Heurística morfológica de terminação para manter consistência de gênero em substantivos."""
    w = palavra.lower()
    if w.endswith(("a", "ade", "ção", "são", "gem")):
        return "Fem"
    if w.endswith(("o", "or", "ão")):
        return "Masc"
    return None


def concordar_adjetivo(adj: str, morph) -> str:
    """Ajusta gênero e número de um adjetivo substituto conforme os traços do adjetivo original."""
    if morph.get("Gender") == ["Fem"] and adj.endswith("o"):
        adj = adj[:-1] + "a"
    if morph.get("Number") == ["Plur"]:
        adj = pluralizar(adj)
    return adj


def mutador_troca_palavras(
    texto: str,
    modo: str = "sinonimo",
    prob_troca: float = 0.35,
    seed: int = 42,
    vocab_permitido: Optional[Set[str]] = None,
) -> str:
    """
    Substitui palavras de conteúdo (substantivos, adjetivos, verbos) por sinônimos ou antônimos.

    Garantias do operador:
    - Preservação da classe gramatical (POS tag).
    - Concordância básica de adjetivos.
    - Determinismo e reprodutibilidade com semente local (random.Random).
    - Preservação da caixa alta/baixa do texto original.
    - Suporte a vocabulário restrito para controle de complexidade.

    Args:
        texto: Texto a ser mutado.
        modo: 'sinonimo' para sinônimos ou 'antonimo' para antônimos.
        prob_troca: Probabilidade de um token elegível ser alterado (padrão 0.35).
        seed: Semente para reprodutibilidade estrita.
        vocab_permitido: Conjunto opcional de palavras permitidas para evitar termos excessivamente raros.

    Returns:
        Texto mutado.
    """
    nlp = get_spacy_model()
    rng = random.Random(seed)
    doc = nlp(texto)
    saida = []

    for token in doc:
        substituto = None
        elegivel = (
            token.pos_ in ("NOUN", "ADJ", "VERB")
            and len(token.text) > 3
            and not (token.ent_type_ and token.text.istitle())
        )

        if elegivel and rng.random() < prob_troca:
            morph = token.morph
            # Verbos: WordNet retorna infinitivos; restringimos a verbos já no infinitivo
            if token.pos_ == "VERB" and morph.get("VerbForm") != ["Inf"]:
                elegivel = False
            # Substantivos: evitar plurais sem flexão adequada
            if token.pos_ == "NOUN" and morph.get("Number") == ["Plur"]:
                elegivel = False

            if elegivel:
                lema = token.lemma_.lower() if token.pos_ == "ADJ" else token.text.lower()
                if modo == "sinonimo":
                    candidatos = obter_sinonimos_wordnet(lema, token.pos_)
                    if token.pos_ == "NOUN":
                        g = genero_aparente(token.text.lower())
                        candidatos = [c for c in candidatos if genero_aparente(c) == g]
                    if vocab_permitido is not None:
                        candidatos = [c for c in candidatos if c in vocab_permitido]
                    if candidatos:
                        substituto = rng.choice(candidatos)
                else:
                    substituto = ANTONIMOS_PT.get(lema)

                if substituto and token.pos_ == "ADJ":
                    substituto = concordar_adjetivo(substituto, morph)

        if substituto:
            saida.append(preservar_caixa(token.text, substituto) + token.whitespace_)
        else:
            saida.append(token.text_with_ws)

    return "".join(saida)
