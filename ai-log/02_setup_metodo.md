# Setup e método de colaboração com IA

A conversa principal está em [`01_ai_log.md`](01_ai_log.md). Este arquivo documenta somente a arquitetura usada para conduzir a análise, sem repetir checkpoints ou respostas.

## Ambiente

O projeto foi preparado antes da análise para que regras, papéis e decisões não dependessem da memória de uma única sessão.

```text
CLAUDE.md
AGENTS.md

.agents/
├── agents.md
├── rules/
├── skills/
└── workflows/

.claude/
├── agents/
├── commands/
└── skills/

knowledge/
working/
```

`working/` manteve checkpoints, engines, resultados e decision-log por ciclo. Versões anteriores foram preservadas em vez de sobrescritas.

## Papéis

| Papel | Responsabilidade |
|---|---|
| Commander / Coordinator | escopo, prioridade, time-box e critical path |
| Data Detective / Data Analyst | grain, schema, joins, denominadores, qualidade e incerteza |
| Skeptic / Independent Reviewer | tentar refutar a conclusão e procurar explicações alternativas |
| Business Strategist | converter evidência em decisão, risco e condição de reversão |
| Builder | implementação mínima e reproduzível |
| Auditor | revisar evidência, código, consistência e entrega |
| Pitch Coach | comunicar apenas depois do freeze |

A separação foi deliberada: o executor da análise não deveria ser a única camada responsável por aceitá-la.

## Skills específicas do case

O pack genérico foi complementado com skills de domínio para o problema de investimento imobiliário e short stay:

- `real-estate-investment-analysis`
- `short-term-rental-economics`
- `investment-sensitivity`
- `comparable-market-design`
- `revenue-proxy-audit`

Elas formalizam três distinções que aparecem no resultado final:

```text
preço exibido ≠ receita realizada
preço pedido ≠ preço de transação
maior monetização ≠ maior eficiência de capital
```

Também foi usado `subagent-fallback` para que uma falha de delegação não interrompesse o processo.

## Workflows

### `/start-case`

```text
regras
→ Problem Brief
→ dados
→ hipóteses
→ evidência que mudaria confiança
→ checkpoints
→ implementação
```

### `/red-team`

```text
recomendação atual
→ principais incertezas
→ explicações alternativas
→ testes
→ confiança revisada
```

### `/final-audit`

```text
reprodução
→ revisão independente
→ testes críticos
→ Consistency Gate
→ auditoria de entrega
```

## Preparação do workflow

Não houve fine-tuning. O que foi iterado antes do desafio foi o processo de uso.

### Overengineering

Testes preliminares mostraram que era fácil aumentar a quantidade de verificações sem aumentar a qualidade da decisão. A regra passou a ser:

```text
DECISION
→ MAIN RISKS
→ DECISION-CHANGING TESTS
→ VERIFY
→ STOP
```

### Conclusões antigas reaparecendo

Isso motivou o `consistency-gate`: uma conclusão final precisa ser comparada com correções posteriores antes de ser liberada.

### Falha de subagente

`subagent-fallback` permite repetir uma delegação de forma limitada e, se necessário, executar o mesmo papel localmente, registrando a mudança.

### Excesso de contexto

Na preparação, contexto automático demais criou instabilidade no gateway. O setup foi alterado para manter regras essenciais persistentes e carregar skills específicas apenas quando necessárias.

## Engenharia dos prompts

Os prompts operacionais longos foram escritos principalmente em inglês porque, nos testes do setup, o Claude seguiu com mais consistência contratos longos de execução, nomes de artefatos e restrições `MUST / MUST NOT` nessa forma. As respostas de trabalho permaneceram em português.

A estrutura principal foi:

```text
STATE
→ RISK
→ TEST
→ FAILURE CONDITION
→ OUTPUT CONTRACT
→ STOP
```

**STATE** evita refazer o que já foi validado.  
**RISK** define o problema daquele ciclo.  
**TEST** força uma verificação que possa alterar a decisão.  
**FAILURE CONDITION** impede ajustar a régua depois de ver o número.  
**OUTPUT CONTRACT** facilita comparar ciclos.  
**STOP** separa execução de aprovação.

## Como o método evoluiu no case

**Cycle 1:** definir semântica e critério antes do ranking.

**Cycle 2:** testar leituras alternativas do `Price_AV`, viés de cobertura e estabilidade.

**Cycle 3:** atacar o líder com controles de Tier, operador, tamanho, duplicação e filtros.

**Cycle 4:** fechar as quatro perguntas com uma análise interpretável de drivers e uma decisão condicional.

**C4.1:** não abriu um quinto ciclo. Corrigiu apenas o que a auditoria pós-freeze encontrou: semi-elasticidade, referência de bairro, linguagem e um gate que não conseguia falhar.

## Persistência e troca de executor

Quando a execução principal ficou indisponível no início do Cycle 4, a investigação não foi reiniciada.

```text
sessão
+ checkpoints
+ decision-log
+ engines/results
→ HANDOFF CHECK
→ aprovação
→ continuidade
```

O novo executor só recebeu autorização para calcular depois de reconstruir o estado atual.

## O que ficou sob julgamento humano

As decisões que não foram automatizadas incluíram:

- tratar a tese interna como hipótese;
- congelar o critério antes do ranking;
- não anualizar a janela como resultado principal;
- preservar erros no histórico;
- pedir testes capazes de derrubar o líder;
- separar Q2 (potencial operacional) de Q4 (investimento);
- manter studio Centro como inconclusivo;
- rejeitar o primeiro freeze mesmo depois de um `PASS`;
- exigir que o gate final pudesse falhar.

A IA acelerou leitura, programação, geração de hipóteses e revisão. O controle do processo ficou concentrado em escolher qual incerteza merecia o próximo teste e quando havia evidência suficiente para avançar.
