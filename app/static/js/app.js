/**
 * CAEd — Script Frontend da Aplicação Web
 * Gerencia chamadas à API REST, eventos do DOM e renderização dinâmica.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Referências aos elementos do DOM
    const inputText = document.getElementById("input-text");
    const charCounter = document.getElementById("char-counter");
    const btnClearText = document.getElementById("btn-clear-text");
    const btnPredict = document.getElementById("btn-predict");
    const shortTextWarning = document.getElementById("short-text-warning");
    const warningWordCount = document.getElementById("warning-word-count");
    const noticeUnchangedContainer = document.getElementById("notice-unchanged-container");

    // Presets
    const presetBtns = {
        ef1: document.getElementById("btn-preset-ef1"),
        ef2: document.getElementById("btn-preset-ef2"),
        em: document.getElementById("btn-preset-em"),
        sup: document.getElementById("btn-preset-sup"),
    };

    const PRESETS = {
        "ef1": "Quando era criança, o jogador era um desses meninos que adoram esportes e só vão para a escola por causa das aulas de Educação Física. Além do tênis, ele gostava de jogar futebol e basquete. De vez em quando, sobrava um tempo para pegar ondas nas praias de Santa Catarina. Em 15 de novembro de 1999, depois de uma seqüência de bons resultados, ele alcançou o terceiro lugar no ranking da ATP (Associação de Tenistas Profissionais). Mas sua grande vitória aconteceu mesmo em 11 de junho de 2000. Guga derrotou o primeiro do mundo, o sueco Magnus Norman, no torneio de Roland Garros, vencendo o torneio pela segunda vez. Pela primeira vez na história, um brasileiro conseguiu ser o número 1 do tênis mundial! Você sabe qual é o lugar mais seguro para guardar o seu dinheiro??? Não pense que é enterrado no quintal ou em baixo do colchão...Hoje o lugar mais seguro para guardar o dinheiro é no banco! E para entendermos como ele funciona hoje, temos que saber como ele nasceu...\nLá no final da Idade Média, os comerciantes montavam feiras próximas das estradas e recebiam muitos viajantes e comerciantes, conhecidos como mercadores. Esses mercadores compravam especiarias que vinham do Oriente. Certo dia, um mercador, observou o seu baú e percebeu que estava cheio de moedas! Ele estava ficando rico só com o trabalho de comprar e vender mercadorias! Não demorou muito e outras pessoas começaram a fazer o mesmo, então ele teve uma grande idéia! Já que na Idade Média o modelo de organização era o feudalismo, não tinha um governo central, ele passou a emprestar dinheiro a seus novos concorrentes (financiamento) e se tornou um “banqueiro” (porque ficava sentado atrás de uma banca). Com o passar dos anos, foram surgindo outros banqueiros... os historiadores relatam que em 1478 existiam aproximadamente 80 casas bancárias nos principados italianos. Esse crescimento do mercado bancário fez surgir o mercado financeiro, no qual nós todos estamos envolvidos!",
        "ef2": "Estudo de DNA liga essa epidemia bacteriana ao colapso da civilização após a chegada dos espanhóis. Estudos e pesquisas. Quando as forças espanholas chegaram ao México, em 1519, a população nativa girava em torno de 25 milhões de pessoas. Um século depois, esse número foi reduzido para um milhão. Tudo isso devido a doenças pestilentas que chegaram junto com os colonizadores europeus. Muitos estudos sugeriram que o sarampo, a varíola, o tifo e uma febre hemorrágica seriam os causadores do colapso da civilização asteca, mas nunca apresentaram evidências sólidas que comprovassem tais hipóteses. Agora, cientistas afirmam ter recuperado amostras de DNA que estariam infectadas por um tipo mortal de salmonella, a Salmonella Paratyphi C. Essa bactéria seria a verdadeira culpada pelo surto cocolizti (febre hemorrágica viral) que dizimou 80% dos habitantes nativos do México entre 1545 e 1550. O resultado da pesquisa foi publicado neste mês pela Nature. Para ter acesso às amostras, os pesquisadores desenterraram cerca de 30 corpos de nativos em um cemitério de Oaxaca, no sul do México. Após extrair e sequenciar o DNA dos dentes, a equipe comparou os genes com mais de 2.700 genomas bacterianos modernos. E os testes comprovaram que havia indícios de infecção por salmonella. Esse tipo de bactéria é bem raro hoje, mas ainda pode ser encontrado em países pobres. Pode ser transmitida por meio das fezes e febre entérica (febre alta, dores de cabeça, sangramentos, dores musculares, manchas na pele, entre outros sintomas). Quando não tratada, pode matar de 10 a 15% dos infectados. “Nosso estudo propõe que a salmonella contribuiu para o declínio populacional durante o surto de cocoliztli no México”, concluíram os pesquisadores alemães do Instituto Max Planck à Nature. Para dar suporte às novas evidências, outra pesquisa conduzida na Universidade de Warwick, no Reino Unido, encontrou vestígios da S. Paratyphi C na Europa cerca de 300 anos antes da devastação que ocorreu no México. O genoma bacteriano foi retirado de uma mulher enterrada na Noruega por volta de 1.200. Isso significa que a doença já estaria circulando pelo continente europeu muito antes de ser levada para o México e seria um ponto de partida para novos mapeamentos da doença. “Realmente, gostaríamos de estudar as duas cepas juntas para obter mais resultados”, acrescentou o pesquisador Hendrick Poinar.",
        "em": "Os moradores do morro se mudaram para o Morro do Borel, no bairro da Tijuca, originando a atual favela do Morro do Borel. Foi inaugurado o prédio do Bar Amarelinho, na Cinelândia, projetado por Mário Vedred. O prédio foi construído no local do antigo Convento da Ajuda. Na época de sua inauguração, o Bar Amarelinho se chamava Café Rivera, nome que mudou para Amarelinho em decorrência da cor do edifício no qual se localizava. Em 1922, ocorreu a Revolta do Forte de Copacabana. O forte se rebelou contra o governo, que era dominado pelas oligarquias cafeeiras. Ao contrário do esperado, as demais unidades militares não aderiram ao movimento e o Forte de Copacabana ficou sozinho na luta contra as tropas do governo. Em um último gesto suicida, os dezoito rebeldes remanescentes marcharam pela orla em direção ao Forte do Leme, no episódio conhecido como Os Dezoito do Forte. Dos dezoito, apenas Siqueira Campos e Eduardo Gomes sobreviveram. Foram inaugurados o Hotel 7 de Setembro, na Avenida Rui Barbosa, no Flamengo e o Palácio Pedro Ernesto, sede do Conselho Municipal, na Cinelândia. O palácio foi construído no lugar do antigo Conselho Municipal, prédio em estilo neogótico do final do século XIX. Foi aberto o canal ligando a Lagoa Rodrigo de Freitas ao mar, como parte das obras de embelezamento da cidade para as comemorações do centenário da independência brasileira. O canal tinha por objetivo facilitar a renovação das águas da lagoa. Com a terra removida com a construção do canal, foi criada a Ilha dos Caiçaras na própria lagoa. Se iniciou o aterro entre a Praia da Saudade e a Fortaleza de São João que iria dar origem ao bairro da Urca\nTambém foi inaugurado o Hotel Glória, de autoria do arquiteto francês Joseph Gire, em estilo neoclássico. E o Prédio dos Correios na Rua Visconde de Itaboraí, no Centro. Herdeiros de Ferreira Viana adquiriram um terreno no bairro de São Conrado que daria origem ao atual Gávea Golf Club. Para a exposição de 1922 em comemoração ao centenário da independência brasileira, foram construídos vários prédios na região do Castelo. A maioria foi demolida após o término da exposição. Exceções foram: o Pavilhão das Indústrias, atual Museu Histórico Nacional; o Pavilhão da França, uma réplica do Petit Trianon de Versalhes que, após o término da exposição, foi doado à Academia Brasileira de Letras para lhe servir de sede e um prédio em estilo eclético que, mais tarde, iria abrigar o Museu da Imagem e do Som. Para abrigar os visitantes da exposição, foi construído, no bairro da Urca, o Hotel-Balneário da Urca: uma construção em estilo eclético dos arquitetos Archimedes Memória e Francisco Couchet. Em 1 de novembro, morreu, em sua cidade natal, o escritor carioca Lima Barreto, de ataque cardíaco. O escritor ficaria notabilizado por clássicos como \"Triste Fim de Policarpo Quaresma\" e \"O Homem que Sabia Javanês\". Em 1922, foi inaugurado o Cinema Floresta, na rua Jardim Botânico número 674.",
        "sup": "Logística/Manutenção de instalações/Manutenção de equipamentos e sistemas eléctricos/Sistemas de protecção eléctrica/Elemento de protecção/Fusível\nUm fusível é um dispositivo de segurança constituído por um fio condutor homogéneo (Matias et al., 2000, p. 11, 13-14 e 17).\nO fusível tem como função, suportar a corrente, interrompendo o circuito por fusão ou volatilização (Efeito de Joule), quando a corrente que o percorre transcende o valor da sua intensidade nominal. O fusível funde tanto ou mais depressa, quanto maior for a intensidade da corrente.\nQuando estamos perante casos de baixa tensão:\nAs principais características dos fusíveis são:\nQuando, por meio dos fusíveis, se pretende proteger uma instalação com vários circuitos derivados, é possível garantir uma certa selectividade, desde que as intensidades nominais dos fusíveis sejam convenientemente escolhidas.\nO sistema de protecção deve actuar somente na parte do circuito, onde houve um aumento de corrente, ou seja, deve apenas ser fundido o fusível que se encontra situado na zona do problema, de modo a que o outro circuito parcial não deixe de ser alimentado.\nPara a escolha do fusível, de acordo com as características dos circuitos a proteger, deve-se proceder à análise das respectivas curvas de intensidade de fusão – tempo de fusão, de modo a verificar se há ou não selectividade para determinados valores de corrente.\nEm geral, quando estamos na presença de sobrecargas, é apenas necessário que a intensidade de funcionamento do fusível a montante seja maior do que a do situado a jusante.\nQuando se trata de curto-circuitos, a situação é mais complicada, porque o fusível a montante alimenta outras derivações, encontrando-se a temperatura superior. Por isso, o seu tempo de actuação face ao defeito, irá depender de vários factores, como: valor da corrente do curto-circuito, correntes pedidas pelas várias derivações e dos tipos de fusíveis. \nQuando se trata de fusíveis do mesmo tipo, em geral, pode-se dizer que há selectividade entre dois fusíveis em série no circuito, se a intensidade nominal do fusível a montante, for pelo menos tripla da do fusível a jusante."
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
            await fetch("/health");
        } catch {
            // Requisição silenciosa de verificação
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

        if (words > 0 && words < 100) {
            if (shortTextWarning) shortTextWarning.style.display = "block";
            if (warningWordCount) warningWordCount.textContent = words;
        } else {
            if (shortTextWarning) shortTextWarning.style.display = "none";
        }
    }

    inputText.addEventListener("input", updateCharCount);

    btnClearText.addEventListener("click", () => {
        inputText.value = "";
        updateCharCount();
        if (shortTextWarning) shortTextWarning.style.display = "none";
        if (noticeUnchangedContainer) noticeUnchangedContainer.style.display = "none";
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
            const isUnchanged = (data.texto_original.trim() === data.texto_mutado.trim());

            if (isUnchanged) {
                badgeImpactStatus.textContent = "Texto Inalterado";
                badgeImpactStatus.className = "impact-badge notice-no-mutation";
                if (noticeUnchangedContainer) noticeUnchangedContainer.style.display = "block";
            } else {
                badgeImpactStatus.textContent = "Mutação Gerada";
                badgeImpactStatus.className = "impact-badge impact-preserved";
                if (noticeUnchangedContainer) noticeUnchangedContainer.style.display = "none";
            }

            displayOrigText.textContent = data.texto_original;
            displayMutText.textContent = data.texto_mutado;
            paneOrigLevel.textContent = "Original";
            paneMutLevel.textContent = isUnchanged ? "Original (Sem alteração)" : `Mutado (${data.operador})`;
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

        const isUnchanged = (data.texto_original.trim() === data.texto_mutado.trim());

        // Status do impacto
        if (isUnchanged) {
            badgeImpactStatus.textContent = "Texto Inalterado";
            badgeImpactStatus.className = "impact-badge notice-no-mutation";
            deltaClassVal.className = "impact-metric-num delta-neutral";
            deltaClassVal.textContent = "Sem alteração (Texto idêntico)";
            if (noticeUnchangedContainer) noticeUnchangedContainer.style.display = "block";
        } else {
            if (noticeUnchangedContainer) noticeUnchangedContainer.style.display = "none";
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
        }

        // Delta de Score Contínuo
        const deltaScoreSign = data.delta_score >= 0 ? `+${data.delta_score.toFixed(4)}` : data.delta_score.toFixed(4);
        deltaScoreVal.textContent = isUnchanged ? "0.0000" : deltaScoreSign;
        if (Math.abs(data.delta_score) < 0.0001 || isUnchanged) {
            deltaScoreVal.className = "impact-metric-num delta-neutral";
        } else if (data.delta_score > 0.05) {
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
