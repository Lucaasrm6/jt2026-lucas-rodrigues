# AI Log — fluxo principal de trabalho

> Este arquivo registra os prompts e respostas que efetivamente conduziram a análise.
>
> Foram removidos somente ruídos sem efeito no trabalho: saudações isoladas, comandos locais, tentativas de setup que não entraram na análise, mensagens repetidas de infraestrutura e credenciais. Nenhuma hipótese, correção, mudança metodológica ou resultado que afetou a decisão foi removido.

## Como ler

A investigação teve quatro ciclos e um patch final:

```text
framing
→ primeira decisão
→ tentativa de refutação
→ correções
→ freeze
→ auditoria do freeze
```

O ponto principal não é que a IA chegou a Morretes. A recomendação foi mantida somente depois de sobreviver a correções capazes de derrubá-la.

---

## Prompt 1 — definir o problema antes de procurar um vencedor

```text
This is the real Seazone Jovens Talentos AI Builder hackathon.

Read the official challenge and the five datasets.

Do not start from the internal thesis.

Before ranking anything:
1. define the business decision;
2. inventory datasets, grain, joins, dates, missingness and duplicates;
3. determine what Price_AV can and cannot mean;
4. distinguish displayed price, availability, realized revenue and occupancy;
5. define "best investment" before testing any segment;
6. treat compact units / Centro as an unvalidated hypothesis;
7. define comparable Airbnb × VivaReal segments without property-level matching;
8. state the assumptions that could reverse the recommendation.

Stop at CHECKPOINT 1.
Respond in Portuguese.
```

### Resposta — Checkpoint 1

A primeira inspeção encontrou 4.441 anúncios no Airbnb e apenas 999 com qualquer observação no `Price_AV`. O arquivo possui três capturas de janeiro e horizonte até abril de 2025, sem flag explícita de reserva.

Também ficou estabelecido que:

- `price` é preço exibido, não diária realizada;
- ausência de uma linha não prova reserva;
- Airbnb e VivaReal não possuem identificador físico comum;
- preço pedido no VivaReal não é preço de transação;
- studio e 1 quarto no Centro não deveriam ser tratados como a mesma evidência.

A unidade de comparação foi congelada como segmento comparável — bairro × quartos × tipo compatível.

O critério de decisão passou a separar potencial operacional, eficiência de capital, robustez de evidência e sensibilidade. A tese interna permaneceu hipótese.

---

## Prompt 2 — construir um ranking que pudesse ser sensível à interpretação

```text
CHECKPOINT 1 APPROVED.

Before ranking, make two refinements:
- Tier is a confidence label, not an automatic winner gate.
- Keep the observed Jan–Apr window as the primary analysis; do not annualize it as a headline result.

Now build Cycle 2.

Use three constructions:
A. displayed nightly price;
B. snapshot transitions only as a possible supplementary signal;
C. hypothetical occupancy only for sensitivity.

Also:
- audit Price_AV coverage bias;
- audit VivaReal validity and duplicates;
- compare absolute operating potential and capital efficiency separately;
- bootstrap ranking stability;
- build a Pareto view;
- calculate relative break-even / reversal conditions;
- test studio+Centro separately from 1Q+Centro.

Do not force a final recommendation yet.

Stop at CHECKPOINT 2.
```

### Resposta — Checkpoint 2

O subconjunto com preço mostrou forte seleção: os anúncios cobertos possuíam muito mais reviews e maior incidência de superhosts/profissionais do que os não cobertos.

No primeiro screen de eficiência, **Morretes 2Q** apareceu no topo. Centro 1Q, Centro 2Q e segmentos de Meia Praia permaneceram como alternativas relevantes.

A tese studio+Centro não pôde ser testada diretamente.

O bootstrap indicou Morretes como rank-1 mais frequente, mas isso foi tratado como estabilidade de reamostragem, não como probabilidade real de o segmento ser o melhor investimento.

A variável capaz de inverter a decisão ficou clara: **ocupação relativa entre os segmentos**, que não é observada no dataset.

---

## Prompt 3 — tentar derrubar o líder

A revisão do Checkpoint 2 encontrou problemas que não apareciam apenas olhando a tabela final. O próximo ciclo foi instruído a corrigir e testar esses pontos sem apagar o resultado anterior.

```text
CHECKPOINT 2 IS PROVISIONALLY APPROVED.

Do not protect the current leader.

Fix and retest:

1. the Tier rule: the written rule requires evidence on both sides; audit the code;
2. rebuild the snapshot method by lead-time and do not call absence a booking;
3. test whether host/operator composition inflates the displayed-price result;
4. control acquisition-price comparisons for unit size and R$/m²;
5. audit VivaReal duplicates;
6. run validity-filter sensitivity;
7. replace ADR with "median displayed nightly price";
8. remove business claims not supported by these files;
9. audit the Pareto definition;
10. produce pairwise reversal thresholds.

Preserve previous artifacts and record every correction.

Stop at CHECKPOINT 3.
```

### Resposta — Checkpoint 3

A revisão confirmou um bug real na classificação de robustez: uma etapa usava `OR` onde a regra exigia `AND`. O bug foi corrigido. O ranking principal não mudou, mas a fronteira de Pareto mudou.

O método temporal foi rebaixado para um proxy fraco de transição de calendário. O sinal suplementar não favorecia Morretes, mas também não media ocupação.

A hipótese de que o preço de Morretes estivesse inflado por composição de operadores não derrubou o resultado.

O ajuste por tamanho mostrou que parte relevante do ticket menor vinha de unidades menores; mesmo na faixa comparável de área, Morretes continuava mais barato.

Depois das correções, Morretes 2Q permaneceu no topo do screen de eficiência, com estabilidade de rank-1 próxima de 63%.

A condição de reversão ficou mais útil do que um ranking absoluto: **se Morretes operar mais de 20% abaixo do Centro, a escolha muda.**

---

## Revisão pós-Checkpoint 3

Uma nova leitura do código encontrou quatro pontos que ainda exigiam cuidado:

- janelas 07→20 e 06→20 compartilham o mesmo snapshot final e não são confirmações independentes;
- a métrica chamada de “reabertura” não tinha o conjunto de risco necessário para ser interpretada como probabilidade;
- o ajuste de operador não deveria ser chamado de “mediana padronizada”;
- a frase “63% do desconto é tamanho” era causal demais para uma decomposição baseada em medianas.

Essas correções foram incorporadas ao Cycle 4.

---

## Prompt 4 — último ciclo analítico

```text
CHECKPOINT 3 APPROVED.

This is the FINAL MAJOR ANALYTICAL CYCLE.

After this cycle:
freeze analytical results,
verify,
run the Consistency Gate,
then move to README / AI log / video.

Required:

1. correct the snapshot-transition language;
2. freeze CAPITAL_EFFICIENCY_INDEX = median displayed nightly price / median asking acquisition price;
3. answer Q1 operating potential and capital efficiency separately;
4. answer Q2 overall and controlling for bedroom mix;
5. answer Q3 with one interpretable associative model with owner-clustered uncertainty;
6. create the final investment table;
7. keep CE90 only as a mechanical scenario, NOT a forecast;
8. calculate relative break-even;
9. separate Studio Centro and Centro 1Q verdicts;
10. choose a PRIMARY recommendation and ALTERNATIVE;
11. state confidence, reversal condition and pre-capital validation;
12. run independent reproduction of decisive numbers;
13. run a Consistency Gate;
14. return 5–7 video-safe numbers.

No external data.
No decorative ML.
Do not write the final README or video yet.

STOP at CHECKPOINT 4.
```

### Continuidade de execução

A execução foi interrompida antes do cálculo do Cycle 4. O estado não foi reconstruído de memória: sessão, checkpoints, engine e decision-log foram preservados e entregues a outro executor.

Antes de continuar, o novo agente recebeu um handoff obrigatório.

---

## Prompt 5 — handoff sem reiniciar a investigação

```text
We are continuing an active Seazone hackathon analysis.

The previous session and the current analytical state are available locally.

Do NOT restart the analysis from scratch.
Do NOT silently overwrite previous conclusions.

First reconstruct:
- current checkpoint;
- frozen definitions;
- corrections that must survive;
- current shortlist;
- exact pending task;
- source-of-truth files.

Return a HANDOFF CHECK.

Do not run Cycle 4 until I approve it.
```

### Resposta — HANDOFF CHECK

O novo executor confirmou:

- Checkpoints 1–3 concluídos;
- Cycle 4 ainda não executado;
- Morretes 2Q como líder provisório de eficiência;
- preço exibido ≠ receita;
- ocupação não observada;
- studio Centro não testável;
- bug de Tier e demais correções já incorporadas;
- arquivos legados de um exercício anterior não deveriam entrar no case.

Só depois desse check a continuação foi aprovada.

---

## Prompt 6 — executar o freeze

```text
APPROVED.

Execute the original Cycle 4.

Preserve Checkpoints 1–3.
Use only the current Itapema source-of-truth files.
Do not use legacy exercise files as evidence.

Do not search external data.
Do not produce README, slides or video yet.
Do not convert displayed price into realized revenue.
Do not call CE90 observed ROI.

Answer all four official questions separately.
Run verification and the Consistency Gate.

Stop only when CHECKPOINT 4 is complete.
```

### Resposta — Checkpoint 4

O Cycle 4 fechou as quatro perguntas com:

- maior potencial absoluto: 4+ quartos;
- maior eficiência de capital: 1–2 quartos;
- Meia Praia com maior mediana agregada entre bairros de amostra robusta;
- Centro mais forte em algumas comparações controladas por quartos;
- Q3 com 911 listings;
- Morretes 2Q como recomendação primária condicional;
- Centro 2Q como alternativa;
- studio+Centro inconclusivo;
- Centro 1Q parcialmente sustentado.

A primeira versão do checkpoint declarou `Consistency Gate: PASS`.

O freeze ainda não foi aprovado.

---

## Auditoria do Checkpoint 4

A revisão do código encontrou três problemas silenciosos:

1. em um modelo log-linear, alguns coeficientes estavam sendo lidos como `β×100`, em vez de `exp(β)-1`;
2. a categoria de referência do bairro era uma célula com amostra muito pequena, tornando percentuais grandes pouco úteis para a decisão;
3. os 14 itens do Consistency Gate estavam hardcoded como `True`.

O terceiro ponto era especialmente importante: um gate que não consegue falhar não é verificação.

---

## Prompt 7 — C4.1, patch cirúrgico

```text
CHECKPOINT 4 IS NOT YET APPROVED.

This is a C4.1 PATCH, not a new analytical cycle.

Do not rerun unrelated analyses.

1. Correct log-linear interpretation with:
   100 * (exp(beta) - 1)

2. Use Meia Praia as a meaningful neighborhood reference
   or report direct pairwise contrasts:
   Centro vs Meia Praia,
   Centro vs Morretes,
   Meia Praia vs Morretes.

3. Do not attribute R² to individual variables without decomposition.

4. Qualify Q2 by sample size.

5. Correct Q1 wording:
   4+ bedrooms has the highest absolute displayed-price potential;
   studio and 1Q are essentially tied.

6. Remove unsupported business claims.

7. Replace the hard-coded Consistency Gate
   with actual programmatic checks against final artifacts.

8. Update only the affected sections.

Return the corrected coefficients, contrasts, gate result,
recommendation status and video-safe numbers.

STOP.
```

### Resposta — C4.1 FINAL PATCH

A interpretação da Q3 foi corrigida:

| Variável | Associação aproximada |
|---|---:|
| +1 quarto | +19,0% |
| +1 banheiro | +15,0% |
| operador profissional | +22,9% |
| log(reviews+1) | −8,4% |

Os contrastes de bairro passaram a ser reportados diretamente:

| Comparação | Associação |
|---|---:|
| Centro vs Meia Praia | +5,6% |
| Centro vs Morretes | +11,1% |
| Meia Praia vs Morretes | +5,3% |

A linguagem de Q1/Q2 foi corrigida e claims não suportados foram removidos.

O Consistency Gate foi transformado em verificação programática e o resultado final reportado foi **PASS — 14/14**.

A recomendação **não mudou**:

> **Morretes 2Q, condicional, confiança moderada.**

A condição que pode derrubá-la permaneceu explícita:

> se Morretes operar mais de 20% abaixo do Centro nas premissas comparáveis, a decisão se inverte.

Os dados disponíveis não permitem afirmar se esse limiar é alcançado.

---

## Estado final da análise

Sete números seguros para comunicação:

1. Morretes 2Q — preço-noite exibido mediano: **R$ 498**;
2. preço-pedido mediano: **R$ 790 mil**;
3. CE90 — 90 dias, 55% hipotéticos: **3,1% do preço de aquisição**;
4. reversão: **>20% de desvantagem operacional relativa**;
5. studio+Centro: **inconclusivo por ausência de observações comparáveis**;
6. modelo estrutural: **R² ≈ 33%**; adicionando variáveis operacionais: **≈ 40%**;
7. os dois eixos discordam: **4+ quartos lideram monetização absoluta; 1–2 quartos lideram eficiência de capital**.
