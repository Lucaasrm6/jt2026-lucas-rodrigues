# Roteiro técnico com compartilhamento de tela — até 3 minutos

## Preparação

Deixe cinco abas abertas antes de gravar:

1. `README.md` no início;
2. seção **Robustez estatística do ranking** do README;
3. `analysis/buy_box_morretes_2q.csv`;
4. `ai-log/README.md`;
5. GitHub Actions, workflow `verify-analysis`.

---

## 0:00–0:20 — Repositório e decisão

**Tela:** início do `README.md`, mostrando a decisão em uma frase e o badge do workflow.

Este repositório transforma os cinco arquivos do desafio em uma decisão de capital. A prioridade é Morretes, dois quartos; Centro, dois quartos, é a alternativa. A confiança é moderada, com condição explícita de reversão.

## 0:20–0:55 — Quatro perguntas do desafio

**Tela:** tabela **Respostas do desafio — resumo executivo**.

Na primeira pergunta, dois quartos é o melhor perfil para investimento. Imóveis maiores monetizam mais, mas a aquisição cresce ainda mais.

Na localização, Meia Praia lidera no agregado robusto; controlando quartos, o Centro lidera em dois e três quartos. Essa inversão revela efeito de composição.

Para características, estimei uma regressão log-linear com 911 anúncios e erros clusterizados por proprietário. Quartos, banheiros e operação profissional aparecem associados a preços maiores, sem interpretação causal.

A tese de studio no Centro ficou inconclusiva. Centro, um quarto, tem apenas 21 ofertas válidas e não supera Morretes.

## 0:55–1:25 — Construção da métrica

**Tela:** seção **O que eu compraria hoje?**, com a matriz dos candidatos.

Antes do ranking, auditei a semântica. O `Price_AV` contém preço-noite exibido, não receita realizada. O VivaReal contém preço pedido, não transação. Sem chave comum entre as bases, comparei bairro e quartos.

O CEI divide preço-noite mediano por preço-pedido mediano. Morretes combina 498 reais por noite, 790 mil reais de aquisição e Tier A, que exige pelo menos trinta observações em cada base.

## 1:25–1:58 — Robustez e condição de reversão

**Tela:** figura e tabela **Robustez estatística do ranking**.

Executei quatro mil reamostragens por proprietário no Airbnb e anunciante no VivaReal. Morretes liderou 69,8% das vezes e superou Centro em 94,7% das comparações pareadas. Isso mede estabilidade amostral, não probabilidade de sucesso.

O sinal de calendário é desfavorável a Morretes e não foi chamado de ocupação. Se a ocupação realizada ficar mais de 20% abaixo da do Centro, a decisão muda.

## 1:58–2:20 — Cenários e buy box

**Tela:** `analysis/buy_box_morretes_2q.csv`, mostrando as colunas de preço, custos e flags.

Depois transformei o segmento em uma buy box com limites de preço, área, preço por metro quadrado, vaga e custos. Reduzi repetições por anunciante e assinatura econômica e publiquei doze leads históricos. Valores abaixo do percentil cinco recebem flags de diligência.

No cenário mecânico de 55% de ocupação e 30% de custos variáveis, o yield sobre preço pedido é 8,23% em Morretes e 6,48% no Centro. É sensibilidade, não previsão.

## 2:20–2:52 — Processo com IA e validação

**Tela:** `ai-log/README.md`; depois, aba do GitHub Actions.

O Antigravity estruturou agentes, skills, handoffs e checkpoints; o Claude Code implementou e executou as análises. Separei construção, revisão metodológica e auditoria, preservando respostas antigas e correções no AI log.

Esse processo encontrou uma regra de Tier com `OR` no lugar de `AND`, corrigiu a transformação dos coeficientes log-lineares e rebaixou o calendário de possível reserva para evidência suplementar. O repositório inclui sessão bruta, índice das intervenções e scripts reproduzíveis.

O GitHub Actions refaz análise, bootstrap e quatro figuras, encerrando com vinte verificações semânticas e numéricas. Os cinco CSVs originais permanecem inalterados.

## 2:52–3:00 — Fechamento

**Tela:** voltar à decisão em uma frase no início do README.

A entrega mostra por que Morretes lidera, quais limitações permanecem e qual evidência faria a decisão mudar.
