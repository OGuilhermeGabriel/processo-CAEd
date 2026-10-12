/**
 * CAEd — Script Frontend da Aplicação Web
 * Gerencia chamadas à API REST, eventos do DOM e renderização dinâmica.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Referências aos elementos do DOM
    const apiStatusDot = document.getElementById("api-status-dot");
    const apiStatusText = document.getElementById("api-status-text");
    const inputText = document.getElementById("input-text");
    const charCounter = document.getElementById("char-counter");
    const btnClearText = document.getElementById("btn-clear-text");
    const btnPredict = document.getElementById("btn-predict");

    // Presets
    const presetBtns = {
        ef1: document.getElementById("btn-preset-ef1"),
        ef2: document.getElementById("btn-preset-ef2"),
        em: document.getElementById("btn-preset-em"),
        sup: document.getElementById("btn-preset-sup"),
    };

    const PRESETS = {
        ef1: "A bala de canela sumiu da panela. O menino comeu a pipoca e tomou a sopa na casa da vovó.",
        ef2: "Durante a tarde chuvosa, os alunos estudaram os mistérios do sistema solar e fizeram experiências fascinantes no laboratório de ciências.",
        em: "A revolução científica moderna rompeu com as concepções teleológicas tradicionais, consolidando métodos empíricos e matemáticos rigorosos para investigar as leis fundamentais da física.",
        sup: "A ontologia contemporânea problematiza a dicotomia epistemológica entre sujeito cognoscente e objeto apreendido, desconstruindo paradigmas hermenêuticos hegemônicos na tradição metafísica ocidental.",
    };

    // Seção de Resultados de Predição
    const sectionPredictResults = document.getElementById("section-predict-results");
    const predLevelBadge = document.getElementById("pred-level-badge");
    const predScoreValue = document.getElementById("pred-score-value");
    const predScoreBar = document.getElementById("pred-score-bar");
    const predCanonicityValue = document.getElementById("pred-canonicity-value");
    const probBarsContainer = document.getElementById("prob-bars-container");
    const metricWordsPerSent = document.getElementById("metric-words-per-sent");
    const metricAvgWordLen = document.getElementById("metric-avg-word-len");
    const metricTotalWords = document.getElementById("metric-total-words");
    const metricTotalChars = document.getElementById("metric-total-chars");

    // Operadores e Configurações
    const operatorOptions = document.querySelectorAll(".operator-option");
    const wordSwapConfigs = document.getElementById("word-swap-configs");
    const selectWordMode = document.getElementById("select-word-mode");
    const inputProbSwap = document.getElementById("input-prob-swap");
    const probSwapVal = document.getElementById("prob-swap-val");
    const btnApplyMutation = document.getElementById("btn-apply-mutation");
    const btnAnalyzeImpact = document.getElementById("btn-analyze-impact");

    // Seção de Comparativo
    const sectionComparison = document.getElementById("section-comparison");
    const badgeImpactStatus = document.getElementById("badge-impact-status");
    const displayOrigText = document.getElementById("display-orig-text");
    const displayMutText = document.getElementById("display-mut-text");
    const paneOrigLevel = document.getElementById("pane-orig-level");
    const paneMutLevel = document.getElementById("pane-mut-level");
    const paneOrigScore = document.getElementById("pane-orig-score");
    const paneMutScore = document.getElementById("pane-mut-score");
    const paneOrigCv = document.getElementById("pane-orig-cv");
    const paneMutCv = document.getElementById("pane-mut-cv");
    const deltaClassVal = document.getElementById("delta-class-val");
    const deltaScoreVal = document.getElementById("delta-score-val");
    const outOfVocabVal = document.getElementById("out-of-vocab-val");

    // Cores e Estilos por Nível
    const LEVEL_CONFIG = {
        "Ensino Fundamental I": { class: "level-ef1", color: "var(--color-ef1)", order: 1 },
        "Ensino Fundamental II": { class: "level-ef2", color: "var(--color-ef2)", order: 2 },
        "Ensino Médio": { class: "level-em", color: "var(--color-em)", order: 3 },
        "Ensino Superior": { class: "level-sup", color: "var(--color-sup)", order: 4 },
    };

    // =========================================================================
    // 1. Diagnóstico de Saúde da API
    // =========================================================================
    async function checkApiHealth() {
        try {
            const res = await fetch("/health");
            if (res.ok) {
                const data = await res.json();
                if (data.modelo_carregado) {
                    apiStatusDot.className = "status-dot status-online";
                    apiStatusText.textContent = "API Online (Modelo pronto)";
                } else {
                    apiStatusDot.className = "status-dot status-offline";
                    apiStatusText.textContent = "API Online (Modelo não treinado)";
                }
            } else {
                throw new Error();
            }
        } catch {
            apiStatusDot.className = "status-dot status-offline";
            apiStatusText.textContent = "API Offline";
        }
    }
    checkApiHealth();

    // =========================================================================
    // 2. Contadores e Presets
    // =========================================================================
    function updateCharCount() {
        const text = inputText.value;
        const chars = text.length;
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        charCounter.textContent = `${chars} caracteres • ${words} palavras`;
    }

    inputText.addEventListener("input", updateCharCount);

    btnClearText.addEventListener("click", () => {
        inputText.value = "";
        updateCharCount();
        sectionPredictResults.style.display = "none";
        sectionComparison.style.display = "none";
    });

    Object.entries(presetBtns).forEach(([key, btn]) => {
        if (btn) {
            btn.addEventListener("click", () => {
                inputText.value = PRESETS[key];
                updateCharCount();
                btnPredict.click();
            });
        }
    });

    // =========================================================================
    // 3. Controle dos Operadores de Mutação
    // =========================================================================
    operatorOptions.forEach(opt => {
        opt.addEventListener("click", () => {
            operatorOptions.forEach(o => o.classList.remove("active"));
            opt.classList.add("active");
            const radio = opt.querySelector("input[type='radio']");
            radio.checked = true;

            const selectedOp = radio.value;
            if (selectedOp === "troca_palavras") {
                wordSwapConfigs.style.display = "block";
            } else {
                wordSwapConfigs.style.display = "none";
            }
        });
    });

    inputProbSwap.addEventListener("input", (e) => {
        const pct = Math.round(parseFloat(e.target.value) * 100);
        probSwapVal.textContent = `${pct}%`;
    });

    function getSelectedOperator() {
        const checked = document.querySelector("input[name='operator_choice']:checked");
        return checked ? checked.value : "troca_palavras";
    }

    // =========================================================================
    // 4. Executar Predição de Complexidade
    // =========================================================================
    btnPredict.addEventListener("click", async () => {
        const text = inputText.value.trim();
        if (text.length < 3) {
            alert("Por favor, digite ou cole um texto com pelo menos 3 caracteres.");
            inputText.focus();
            return;
        }

        const originalBtnHtml = btnPredict.innerHTML;
        btnPredict.innerHTML = '<span class="spinner"></span> Analisando...';
        btnPredict.disabled = true;

        try {
            const res = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ texto: text }),
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Erro ao consultar a API.");
            }

            const data = await res.json();
            renderPredictionResults(data);
        } catch (err) {
            alert(`Falha na predição: ${err.message}`);
        } finally {
            btnPredict.innerHTML = originalBtnHtml;
            btnPredict.disabled = false;
        }
    });

    function renderPredictionResults(data) {
        sectionPredictResults.style.display = "block";

        // 1. Badge de Nível
        const levelConf = LEVEL_CONFIG[data.nivel_previsto] || { class: "level-ef1", color: "var(--color-primary)" };
        predLevelBadge.className = `level-badge ${levelConf.class}`;
        predLevelBadge.textContent = data.nivel_previsto;

        // 2. Score Contínuo
        predScoreValue.textContent = data.score_continuo.toFixed(2);
        const scorePct = Math.max(0, Math.min(100, ((data.score_continuo - 1.0) / 3.0) * 100));
        predScoreBar.style.width = `${scorePct}%`;

        // 3. Canonicidade Fonológica
        predCanonicityValue.textContent = `${(data.metricas.taxa_canonicidade * 100).toFixed(1)}%`;

        // 4. Métricas estruturais
        metricWordsPerSent.textContent = data.metricas.palavras_por_sentenca.toFixed(1);
        metricAvgWordLen.textContent = `${data.metricas.tam_medio_palavra.toFixed(1)} carac.`;
        metricTotalWords.textContent = data.metricas.num_palavras;
        metricTotalChars.textContent = data.metricas.num_caracteres;

        // 5. Barras de Probabilidades
        probBarsContainer.innerHTML = "";
        const orderedLevels = [
            "Ensino Fundamental I",
            "Ensino Fundamental II",
            "Ensino Médio",
            "Ensino Superior",
        ];

        orderedLevels.forEach(lvl => {
            const prob = data.probabilidades[lvl] || 0.0;
            const pct = (prob * 100).toFixed(1);
            const conf = LEVEL_CONFIG[lvl];

            const row = document.createElement("div");
            row.className = "prob-row";
            row.innerHTML = `
                <div class="prob-label-row">
                    <span style="color: ${conf.color}">${lvl}</span>
                    <span>${pct}%</span>
                </div>
                <div class="prob-track">
                    <div class="prob-fill" style="width: ${pct}%; background-color: ${conf.color}"></div>
                </div>
            `;
            probBarsContainer.appendChild(row);
        });

        sectionPredictResults.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // =========================================================================
    // 5. Executar Apenas Mutação
    // =========================================================================
    btnApplyMutation.addEventListener("click", async () => {
        const text = inputText.value.trim();
        if (text.length < 3) {
            alert("Insira um texto válido para mutar.");
            return;
        }

        const originalBtnHtml = btnApplyMutation.innerHTML;
        btnApplyMutation.innerHTML = '<span class="spinner"></span> Mutando...';
        btnApplyMutation.disabled = true;

        try {
            const operator = getSelectedOperator();
            const payload = {
                texto: text,
                operador: operator,
                modo_palavras: selectWordMode.value,
                prob_troca: parseFloat(inputProbSwap.value),
            };

            const res = await fetch("/mutate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!res.ok) throw new Error("Erro ao gerar mutação.");
            const data = await res.json();

            sectionComparison.style.display = "block";
            badgeImpactStatus.textContent = "Mutação Gerada";
            badgeImpactStatus.className = "impact-badge impact-preserved";

            displayOrigText.textContent = data.texto_original;
            displayMutText.textContent = data.texto_mutado;
            paneOrigLevel.textContent = "Original";
            paneMutLevel.textContent = `Mutado (${data.operador})`;
            paneOrigScore.textContent = "";
            paneMutScore.textContent = "";
            paneOrigCv.textContent = "";
            paneMutCv.textContent = "";

            document.getElementById("impact-results-panel").style.display = "none";
            sectionComparison.scrollIntoView({ behavior: "smooth", block: "start" });
        } catch (err) {
            alert(`Erro: ${err.message}`);
        } finally {
            btnApplyMutation.innerHTML = originalBtnHtml;
            btnApplyMutation.disabled = false;
        }
    });

    // =========================================================================
    // 6. Avaliar Impacto Completo na Complexidade
    // =========================================================================
    btnAnalyzeImpact.addEventListener("click", async () => {
        const text = inputText.value.trim();
        if (text.length < 3) {
            alert("Insira um texto válido para avaliar o impacto.");
            return;
        }

        const originalBtnHtml = btnAnalyzeImpact.innerHTML;
        btnAnalyzeImpact.innerHTML = '<span class="spinner"></span> Avaliando impacto...';
        btnAnalyzeImpact.disabled = true;

        try {
            const operator = getSelectedOperator();
            const payload = {
                texto: text,
                operador: operator,
                modo_palavras: selectWordMode.value,
                prob_troca: parseFloat(inputProbSwap.value),
            };

            const res = await fetch("/analyze-impact", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Erro ao analisar impacto.");
            }

            const data = await res.json();
            renderImpactResults(data);
        } catch (err) {
            alert(`Falha na avaliação de impacto: ${err.message}`);
        } finally {
            btnAnalyzeImpact.innerHTML = originalBtnHtml;
            btnAnalyzeImpact.disabled = false;
        }
    });

    function renderImpactResults(data) {
        sectionComparison.style.display = "block";
        document.getElementById("impact-results-panel").style.display = "grid";

        // Badges e Textos
        displayOrigText.textContent = data.texto_original;
        displayMutText.textContent = data.texto_mutado;

        paneOrigLevel.textContent = data.nivel_original;
        paneMutLevel.textContent = data.nivel_mutado;

        paneOrigScore.textContent = `Score: ${data.score_original.toFixed(3)}`;
        paneMutScore.textContent = `Score: ${data.score_mutado.toFixed(3)}`;

        paneOrigCv.textContent = `CV: ${(data.metricas_original.taxa_canonicidade * 100).toFixed(1)}%`;
        paneMutCv.textContent = `CV: ${(data.metricas_mutado.taxa_canonicidade * 100).toFixed(1)}%`;

        // Status do impacto
        badgeImpactStatus.textContent = data.impacto_status;
        if (data.delta_classe === 0) {
            badgeImpactStatus.className = "impact-badge impact-preserved";
            deltaClassVal.className = "impact-metric-num delta-neutral";
            deltaClassVal.textContent = "Δ = 0 (Preservada)";
        } else if (data.delta_classe > 0) {
            badgeImpactStatus.className = "impact-badge impact-increased";
            deltaClassVal.className = "impact-metric-num delta-pos";
            deltaClassVal.textContent = `+${data.delta_classe} (Aumentou)`;
        } else {
            badgeImpactStatus.className = "impact-badge impact-decreased";
            deltaClassVal.className = "impact-metric-num delta-neg";
            deltaClassVal.textContent = `${data.delta_classe} (Diminuiu)`;
        }

        // Delta de Score Contínuo
        const deltaScoreSign = data.delta_score >= 0 ? `+${data.delta_score.toFixed(4)}` : data.delta_score.toFixed(4);
        deltaScoreVal.textContent = deltaScoreSign;
        if (data.delta_score > 0.05) {
            deltaScoreVal.className = "impact-metric-num delta-pos";
        } else if (data.delta_score < -0.05) {
            deltaScoreVal.className = "impact-metric-num delta-neg";
        } else {
            deltaScoreVal.className = "impact-metric-num delta-neutral";
        }

        // Palavras Fora do Vocabulário
        outOfVocabVal.textContent = `${(data.taxa_palavras_inventadas * 100).toFixed(1)}%`;
        if (data.taxa_palavras_inventadas > 0.1) {
            outOfVocabVal.style.color = "var(--color-danger)";
        } else {
            outOfVocabVal.style.color = "var(--color-text-primary)";
        }

        sectionComparison.scrollIntoView({ behavior: "smooth", block: "start" });
    }
});
