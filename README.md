# Sistema de Classificação de Complexidade e Mutação Textual

> **Processo Seletivo CAEd — Edital 024-2026**  
> **Candidato:** Guilherme Gabriel Saldanha Pereira
> **Data:** Outubro / 2026  

---

## Sumário Executivo / Relatório Técnico

Este documento constitui o **Relatório Técnico Geral** e a documentação completa da solução desenvolvida para o processo seletivo do **CAEd (Centro de Políticas Públicas e Avaliação da Educação)**. O projeto contempla um classificador de complexidade textual em 4 níveis educacionais, algoritmos heurísticos de mutação textual e uma aplicação web construída com **FastAPI**.

---

## 1. Introdução e Contextualização do Problema

A avaliação da capacidade leitora e decodificação em crianças exige narrativas curtas calibradas pedagogicamente para diferentes níveis de dificuldade. À medida que as avaliações de fluência se expandem nacionalmente, surge a necessidade de automatizar tanto a mensuração da complexidade dos textos quanto a geração de novas variantes textuais inéditas que preservem ou modulem essa complexidade.

### Objetivos do Projeto:
1. **Classificação em 4 Níveis Educacionais**:
   - Ensino Fundamental I (EF1)
   - Ensino Fundamental II (EF2)
   - Ensino Médio (EM)
   - Ensino Superior (ES)
2. **Implementação de Algoritmo Fonológico de Canonicidade**:
   - Identificação de palavras canônicas (compostas estritamente por sílabas do tipo Consoante + Vogal - `CV`).
3. **Mecanismo de Mutação Textual**:
   - Troca de palavras (sinônimos / antônimos);
   - Troca de gênero gramatical;
   - Paráfrase e reestruturação sintática.
4. **Análise de Impacto das Mutações**:
   - Aferição da alteração de complexidade decorrente das mutações.
5. **Aplicação Web Interativa**:
   - Interface simples e intuitiva servida com FastAPI.

---

## 2. Metodologia Científica e Desenvolvimento Empírico

A abordagem do projeto é orientada a dados e validação empírica progressiva:

```text
[Análise Exploratória] ➔ [Canonicidade Silábica] ➔ [Modelagem & Comparação] ➔ [Heurísticas de Mutação] ➔ [Modularização & API]
```

- **Ambiente de Experimentação**: Todas as etapas preliminares de mineração de dados, extração de features, treinamento de modelos e testes qualitativos de mutação foram conduzidas no Jupyter Notebook (`notebooks/experimentos.ipynb`).
- **Engenharia de Software**: O código validado foi refatorado em pacotes modulares em `src/`, com testes unitários em `tests/` e API em `app/`.

---

## 3. Análise Exploratória e Pré-processamento dos Dados (EDA)

*(Esta seção será preenchida durante a execução da Fase 1 no Notebook)*

- **Descrição da Base de Dados**:
  - Amostras de materiais didáticos do MEC divididos em 4 pastas (`dataset_caed/`).
- **Estatísticas Descritivas**:
  - Distribuição do número de textos por classe.
  - Distribuição do tamanho dos textos (número de palavras, caracteres e sentenças).
  - Análise de vocabulário e dispersão lexical.

---

## 4. Algoritmo de Canonicidade de Palavras

*(Esta seção detalhará a fundamentação e a implementação da canonicidade silábica)*

### 4.1 Conceito Fonológico
Uma palavra é considerada **canônica** quando sua estrutura silábica é formada exclusivamente por sílabas abertas simples do tipo **Consoante + Vogal (CV)**. Exceções com sílabas do tipo V, CVC, CCV, CVV tornam a palavra **não canônica**.

- **Exemplos Canônicos**: *ca-be-ça*, *ca-ne-la*, *ja-ne-la*, *lu-ta*, *so-pa*.
- **Exemplos Não Canônicos**: *a-ba-jur* (V-CV-CVC), *lá-pis* (CV-CVC), *can-sa-do* (CVC-CV-CV), *a-sa* (V-CV).

### 4.2 Heurística e Implementação
- Algoritmo determinístico de separação silábica e rotulagem segmental (`C` vs `V`).
- Validação com casos de borda do português (dígrafos, encontros consonantais, semivogais).

---

## 5. Engenharia de Features e Modelagem Preditiva

*(Esta seção apresentará a tabela comparativa de modelos testados e as métricas obtidas)*

### 5.1 Features Extraídas
- Taxa de canonicidade no texto ($\frac{\text{palavras canônicas}}{\text{total de palavras}}$);
- Métricas de legibilidade (índice Flesch-Kincaid adaptado ao português);
- Médias estruturais (tamanho médio de sentença, sílabas por palavra);
- Features léxicas e semânticas (TF-IDF / N-grams).

### 5.2 Modelos Avaliados e Comparação de Métricas
| Modelo | Acurácia | F1-Macro | Precisão | Revocação | Observações |
| :--- | :---: | :---: | :---: | :---: | :--- |
| *Baseline (TF-IDF + Reg. Logística)* | - | - | - | - | Em experimentação |
| *Random Forest (Features Linguísticas)* | - | - | - | - | Em experimentação |
| *LightGBM / XGBoost* | - | - | - | - | Em experimentação |
| *Ensemble / Híbrido* | - | - | - | - | Em experimentação |

### 5.3 Matriz de Confusão e Modelo Escolhido
*(Discussão sobre o modelo campeão e análise de erros entre classes limítrofes, ex: EF2 vs Ensino Médio)*.

---

## 6. Heurísticas dos Operadores de Mutação Textual

*(Esta seção documentará as estratégias de Processamento de Linguagem Natural adotadas)*

### 6.1 Troca de Palavras (Sinônimos e Antônimos)
- Utilização da **WordNet (OpenWN-PT)** via NLTK para identificação de sinônimos/antônimos coerentes.

### 6.2 Troca de Gênero Gramatical
- Análise morfossintática via **spaCy** (`pt_core_news_sm`/`lg`).
- Detecção e concordância entre determinantes, substantivos e adjetivos.

### 6.3 Paráfrase e Reestruturação Sintática
- Regras sintáticas baseadas em árvores de dependência (inversão de adjuntos, conversão ativa/passiva).

---

## 7. Análise de Impacto das Mutações

- Metodologia de medição da variação da complexidade $\Delta(\text{complexidade})$.
- Exemplos de textos antes e depois da mutação e comportamento da predição.

---

## 8. Arquitetura da Aplicação Web

- **Backend**: API construída em **FastAPI** com documentação Swagger interativa (`/docs`).
- **Frontend**: Interface limpa e responsiva (HTML5/CSS3/Vanilla JS) para teste em tempo real das predições e mutações.

---

## 9. Instruções de Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior
- Git

### 1. Clonar o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd "Processo Seletivo CAEd"
```

### 2. Criar e ativar o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# ou: venv\Scripts\activate  # No Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

### 4. Executar os Experimentos (Notebook)
```bash
jupyter notebook notebooks/experimentos.ipynb
```

### 5. Executar a Aplicação Web
```bash
uvicorn app.main:app --reload --port 8000
```
Acesse no navegador: `http://localhost:8000`

---

## 10. Discussão de Resultados, Limitações e Trabalhos Futuros

- Principais desafios enfrentados no processamento da língua portuguesa.
- Limitações das abordagens baseadas em regras e possibilidades de melhoria (ex: fine-tuning de LLMs menores, expansão do léxico de canonicidade).

---

## 11. Referências

- NLTK: Natural Language Toolkit ([https://www.nltk.org/](https://www.nltk.org/))
- OpenWordNet-PT: ([https://github.com/arademaker/wordnet-pt](https://github.com/arademaker/wordnet-pt))
- spaCy: Industrial-Strength Natural Language Processing ([https://spacy.io/](https://spacy.io/))
- CAEd - Avaliação e Medidas Educacionais
