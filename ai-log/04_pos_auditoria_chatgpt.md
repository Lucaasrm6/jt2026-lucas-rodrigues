# Registro técnico — pós-auditoria com ChatGPT Work

**Data:** 2026-08-27
**Escopo solicitado por Lucas:** analisar o repositório e os forks, identificar como o projeto poderia chegar ao primeiro lugar e implementar melhorias pelo conector GitHub sem quebrar o trabalho existente. Vídeos ficaram fora do escopo desta rodada.

> Este arquivo é um registro técnico verificável, não uma transcrição completa do chat do conector. A sessão original integral permanece em `03_sessao_original_claude.jsonl`.

## Guardrails adotados

1. auditar árvore, histórico, branches, permissões e CI antes de editar;
2. reproduzir o pipeline original e os 14 checks em ambiente isolado;
3. preservar os cinco CSVs oficiais sem alteração;
4. adicionar a robustez em script separado antes de mudar a narrativa;
5. não aumentar a confiança se os novos testes contradissessem o líder;
6. trabalhar em branch separada e entregar por pull request.

## Baseline reproduzida

- commit auditado: `784d33994bc1d8aa312e5a53e08819eebad34fd1`;
- `analysis/run_final_analysis.py`: passou;
- `analysis/temporal_proxy.py`: passou;
- `analysis/generate_figures.py`: passou;
- `scripts/consistency_gate_final.py`: 14/14 checks;
- conclusão de base preservada: Morretes 2Q como prioridade de diligência, Centro 2Q como alternativa, confiança moderada.

## Perguntas adicionadas na pós-auditoria

1. O CEI permanece líder ao respeitar concentração por proprietário e anunciante?
2. A repetição econômica de anúncios no VivaReal altera a mediana de aquisição?
3. Qual é a incerteza do limiar de ocupação Morretes/Centro?
4. O ranking sobrevive a custos fixos observados e custos variáveis explícitos?
5. Quais leads do snapshot passam por uma buy box definida antes da ordenação?
6. Quanto do cadastro de cada segmento realmente aparece no `Price_AV`?

## Resultados que mudaram a entrega

- **4.000 reamostragens clusterizadas:** Morretes 2Q ocupa o primeiro lugar em 69,8% das reamostragens entre os cinco finalistas e supera Centro 2Q em 94,7% das comparações pareadas.
- **Interpretação limitada:** essas frequências medem estabilidade condicional; não são probabilidade de superioridade real e não corrigem ocupação, sazonalidade ou seleção.
- **Limiar de ocupação:** ponto Morretes/Centro = 80,0%; intervalo bootstrap 95% = 52,6%–104,7%. A regra anterior de “20% abaixo” foi mantida como ponto de referência, mas ganhou um intervalo explícito.
- **Deduplicação de estresse:** Morretes 2Q passa de 1.035 para 873 assinaturas econômicas e sua mediana muda de R$790 mil para R$789 mil (−0,1%). O líder não muda.
- **Equalização de clusters:** CEI Morretes 2Q = 0,000612; Centro 2Q = 0,000389.
- **Cobertura seletiva:** `Price_AV` cobre 22,3% de Morretes 2Q, 35,5% de Centro 2Q e 25,9% de Meia Praia 2Q. A confiança permaneceu moderada.
- **Cenário líquido mecânico 55%/30%:** yield sobre preço-pedido de 8,24% em Morretes, 6,48% no Centro e 5,39% em Meia Praia, antes de financiamento e imposto de renda.
- **Buy box:** 12 leads publicados a partir de critérios reproduzíveis; links e atributos são de janeiro de 2025 e exigem verificação atual.

## Correções durante a própria rodada

- O primeiro screen de leads ainda repetia títulos do mesmo anunciante. A regra foi endurecida para diversificar título + anunciante e assinatura econômica antes de selecionar os 12 leads.
- A comparação bootstrap foi expandida de três segmentos 2Q para os **cinco candidatos finais**, evitando apresentar apenas a comparação mais favorável. O relatório separa rank 1 global (69,8%) da comparação pareada Morretes/Centro 2Q (94,7%).
- A conclusão não foi promovida para “alta confiança”: o intervalo do break-even cruza 100% e a cobertura de preço de Morretes é a menor entre os três segmentos 2Q.

## Arquivos da rodada

- `analysis/decision_robustness.py`
- `analysis/decision_robustness_results.json` (gerado, não versionado)
- `analysis/buy_box_morretes_2q.csv`
- `figures/04_robustez_decisao.svg`
- `README.md`, `relatorio.md`, `analysis/README.md`
- `.github/workflows/verify.yml`
- `scripts/consistency_gate_final.py`

O workflow regenerará os resultados e executará 20 checks antes de aceitar a entrega.
