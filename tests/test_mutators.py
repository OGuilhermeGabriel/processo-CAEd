"""
Testes unitários e de integração para os operadores de mutação textual e cálculo de impacto.
"""

import pytest
from src.mutators.word_swap import mutador_troca_palavras
from src.mutators.gender_swap import mutador_troca_genero
from src.mutators.paraphrase import mutador_parafrase
from src.mutators.impact import (
    avaliar_impacto_mutacao,
    taxa_palavras_inventadas,
    ResultadoImpacto,
)


def test_mutador_word_swap_sinonimos():
    """Testa se o mutador de palavras substitui palavras por sinônimos mantendo a frase legível."""
    texto = "O homem encontrou um belo cão no caminho."
    mutado = mutador_troca_palavras(texto, modo="sinonimo", prob_troca=1.0, seed=42)
    assert isinstance(mutado, str)
    assert len(mutado) > 0


def test_mutador_word_swap_antonimos():
    """Testa se o mutador de palavras inverte o sentido com antônimos conhecidos."""
    texto = "O menino estava alegre e alto."
    mutado = mutador_troca_palavras(texto, modo="antonimo", prob_troca=1.0, seed=42)
    assert "triste" in mutado or "baixo" in mutado


def test_mutador_gender_swap():
    """Testa se a troca de gênero altera determinantes, substantivos e adjetivos coerentemente."""
    texto = "O aluno dedicado fez a prova."
    mutado = mutador_troca_genero(texto)
    assert "A aluna dedicada" in mutado or "aluna" in mutado


def test_mutador_paraphrase_tempo():
    """Testa a inversão sintática de adjuntos adverbiais temporais antepostos."""
    texto = "Há duas semanas atrás estava chovendo."
    mutado = mutador_parafrase(texto)
    assert mutado.startswith("Estava chovendo")
    assert "há duas semanas atrás" in mutado.lower()


def test_mutador_paraphrase_passiva():
    """Testa a conversão determinística de voz passiva para voz ativa com flexão do verbo irregular."""
    texto = "O texto foi lido pelo aluno."
    mutado = mutador_parafrase(texto)
    assert "O aluno leu o texto." in mutado


def test_taxa_palavras_inventadas():
    """Testa o cálculo da métrica de integridade léxica contra o corpus."""
    vocab = {"o", "menino", "leu", "o", "livro", "a", "menina"}
    original = "O menino leu o livro."

    # Nenhuma palavra nova
    assert taxa_palavras_inventadas(original, "O menino leu o livro.", vocab_corpus=vocab) == 0.0

    # Palavra nova existente no vocabulário
    assert taxa_palavras_inventadas(original, "A menina leu o livro.", vocab_corpus=vocab) == 0.0

    # Palavra inventada inexistente no vocabulário
    assert taxa_palavras_inventadas(original, "O menino leu o xptoqualquer.", vocab_corpus=vocab) == 1.0


def test_avaliar_impacto_mutacao_integracao():
    """Testa o pipeline completo de avaliação de impacto com o modelo preditivo."""
    texto = "O texto foi lido pelo aluno."
    res = avaliar_impacto_mutacao(
        texto_original=texto,
        funcao_mutadora=mutador_parafrase,
        nome_operador="Paráfrase",
    )
    assert isinstance(res, ResultadoImpacto)
    assert res.texto_original == texto
    assert res.texto_mutado != ""
    assert res.nivel_original in ["Ensino Fundamental I", "Ensino Fundamental II", "Ensino Médio", "Ensino Superior"]
    assert 1.0 <= res.score_original <= 4.0
    assert 1.0 <= res.score_mutado <= 4.0
    assert isinstance(res.delta_classe, int)
    assert isinstance(res.delta_score, float)
    assert 0.0 <= res.taxa_palavras_inventadas <= 1.0
