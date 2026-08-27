# Índice de colaboração com IA

Este diretório preserva a trilha de trabalho e facilita localizar as intervenções que mudaram a análise. O índice não substitui os registros completos.

## Artefatos

| Arquivo | Conteúdo | Integridade |
|---|---|---|
| [`01_ai_log.md`](01_ai_log.md) | Prompts e respostas literais da sessão analítica original | Registro legível, com conclusões antigas preservadas e correções nos ciclos seguintes |
| [`02_setup_metodo.md`](02_setup_metodo.md) | Ambiente, papéis, skills, workflows e decisões de processo | Descrição do método de colaboração |
| [`03_sessao_original_claude.jsonl`](03_sessao_original_claude.jsonl) | Exportação bruta da sessão original | Fonte integral, sem edição editorial |

## Intervenções críticas

1. **Semântica antes do ranking:** [`Prompt 1 — framing e auditoria semântica`](01_ai_log.md#prompt-1--framing-e-auditoria-semântica) separou preço exibido, preço-pedido e receita não observada.
2. **Cobertura, bootstrap e break-even:** [`Checkpoint 2`](01_ai_log.md#claude--checkpoint-2-resposta-literal) tornou seleção de preço e incerteza visíveis antes da recomendação.
3. **Correção do Tier e do proxy temporal:** [`Prompt 3`](01_ai_log.md#prompt-3--correção-metodológica--robustez) exigiu `AND` nos dois lados da amostra e proibiu tratar movimento de calendário como reserva.
4. **Freeze analítico e gate:** [`Prompt 4`](01_ai_log.md#prompt-4--cycle-4--freeze-analítico) consolidou as quatro respostas e o processo de consistência.
5. **Correção log-linear e claims antigos:** [`Prompt 5`](01_ai_log.md#prompt-5--auditoria-pós-c4--c41) substituiu `β×100` por `100×(exp(β)−1)` e removeu linguagem não sustentada.

## Regra de leitura

Conclusões em checkpoints antigos fazem parte do histórico e podem ter sido corrigidas depois. Para a posição vigente, use [`README.md`](../README.md), [`relatorio.md`](../relatorio.md) e os scripts em [`analysis/`](../analysis/). Para conferir a evolução, leia os prompts/checkpoints em ordem.
