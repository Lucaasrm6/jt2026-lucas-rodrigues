🎥 **Vídeo (até 3 min):** [COLE_AQUI_O_LINK_PUBLICO_DO_GOOGLE_DRIVE]

# Hackathon Jovens Talentos AI Builder 2026 — Seazone
## Recomendação de investimento imobiliário em Itapema (SC)

## Decisão em uma frase

> **Eu começaria a diligência por um apartamento de 2 quartos em Morretes.** É o segmento robusto com melhor eficiência de capital no recorte observado, mas a recomendação é **condicional e de confiança moderada**: se Morretes operar com ocupação mais de **20% inferior** ao Centro, a decisão muda para **Centro 2Q**.

A base não observa ocupação nem receita realizada. Por isso, o resultado é uma regra de decisão auditável — não uma promessa de retorno.

## Por onde começar

| Se você quer… | Abra |
|---|---|
| A resposta completa | [`relatorio.md`](relatorio.md) |
| Como a análise evoluiu com IA | [`ai-log/01_ai_log.md`](ai-log/01_ai_log.md) |
| Setup de agentes, skills e lógica de prompts | [`ai-log/02_setup_metodo.md`](ai-log/02_setup_metodo.md) |
| Roteiro do vídeo | [`ROTEIRO_VIDEO.md`](ROTEIRO_VIDEO.md) |
| Dados originais | [`data/`](data/) |

---

# As quatro respostas

## 1. Qual o melhor perfil de imóvel?

Há duas respostas diferentes — e misturá-las levaria à decisão errada.

| Perfil | Preço-noite exibido mediano | Preço-pedido mediano | CEI |
|---|---:|---:|---:|
| 1Q | R$434 | R$750 mil | 0,000578 |
| **2Q** | R$480 | R$810 mil | **0,000593** |
| 3Q | R$694 | R$1,80 mi | 0,000385 |
| 4+ | **R$1.065** | R$3,60 mi | 0,000296 |

- **Maior potencial absoluto:** 4+ quartos.
- **Maior eficiência de capital:** 1–2 quartos.
- **Perfil recomendado para diligência:** 2 quartos.

`CEI = preço-noite exibido mediano / preço-pedido mediano`.

## 2. Qual a melhor localização em termos do proxy operacional observável?

Entre bairros com pelo menos 30 anúncios precificados:

| Bairro | n | Preço-noite exibido mediano |
|---|---:|---:|
| **Meia Praia** | **607** | **R$600** |
| Centro | 193 | R$587 |
| Morretes | 68 | R$500 |

Tabuleiro chega a R$610, mas com n=17 e permanece exploratório.

A comparação agregada, porém, mistura perfis diferentes. Dentro de **2Q**:

- Centro: **R$580**;
- Morretes: **R$498**;
- Meia Praia: **R$460**.

Dentro de **3Q**, Centro = R$790 e Meia Praia = R$700.

**Conclusão:** Meia Praia lidera o agregado robusto, mas Centro lidera nos recortes comparáveis de 2Q/3Q. Parte da diferença agregada é composição de quartos.

## 3. Quais características estão associadas a maior preço-noite?

Foi estimado um modelo OLS associativo sobre `log(preço-noite exibido mediano)` com **911 anúncios**, erros clusterizados por proprietário e Meia Praia como referência de bairro.

| Variável | Associação aproximada |
|---|---:|
| +1 quarto | **+19,0%** |
| +1 banheiro | **+15,0%** |
| +1 hóspede | +3,0% |
| operador profissional | **+22,9%** |
| superhost | −2,6%, n.s. |
| instant book | +2,0%, n.s. |
| log(reviews+1) | −8,4% |
| Centro vs Meia Praia | +5,6%, n.s. |

A especificação estrutural explica cerca de **33%** da variação; com variáveis operacionais/host, cerca de **40%**.

Esses resultados são **associativos, não causais**.

## 4. O que eu compraria hoje?

| Segmento | Tier | Noite | Preço-pedido | Viva n | CEI | CE90 |
|---|---|---:|---:|---:|---:|---:|
| **Morretes 2Q** | **A** | **R$498** | **R$790 mil** | **1.035** | **0,000630** | **3,12%** |
| Centro 1Q | B | R$450 | R$890 mil | 21 | 0,000506 | 2,50% |
| Centro 2Q | A | R$580 | R$1,15 mi | 87 | 0,000504 | 2,50% |
| Meia Praia 2Q | A | R$460 | R$1,07 mi | 241 | 0,000430 | 2,13% |
| Meia Praia 3Q | A | R$700 | R$1,882 mi | 1.658 | 0,000372 | 1,84% |

**Recomendação primária:** Morretes 2Q.  
**Alternativa:** Centro 2Q.  
**Confiança:** moderada.

`CE90 = preço-noite exibido × 90 × ocupação hipotética de 55% / preço-pedido`. É um **cenário mecânico de eficiência**, não ROI observado.

### Condição que muda a decisão

> **Se Morretes operar com ocupação mais de 20% inferior ao Centro, eu mudo para Centro 2Q.**

A base fornecida não permite saber se esse limiar é atingido. Essa é a principal diligência antes de comprometer capital.

---

# Posição sobre a tese de compactos no Centro

### Studio + Centro

**Inconclusivo.** Não há observações comparáveis suficientes para validar ou rejeitar essa parte da tese. Não extrapolei 1Q para studio.

### 1Q + Centro

**Parcialmente sustentado.** É eficiente e testável, mas o lado de aquisição é fino (21 ofertas válidas) e o segmento fica abaixo de Morretes 2Q no screen final.

A leitura que sobrevive aos dados é mais ampla:

> **compactos podem ser eficientes, mas Centro não aparece como vencedor exclusivo e studio não pode ser validado com esta base.**

---

# Por que a recomendação é condicional

Cinco limitações importam mais que qualquer casa decimal do ranking:

1. ocupação real não é observada;
2. apenas 999 dos 4.441 anúncios aparecem no `Price_AV`, com seleção para anúncios mais maduros/profissionais;
3. a janela é Jan–Abr/2025, não um ano;
4. VivaReal contém preço pedido, não preço efetivamente transacionado;
5. Airbnb e VivaReal não possuem match físico de imóvel — a comparação é por segmento.

## Diligência antes de capital

1. ocupação real da Seazone por bairro × quartos;
2. preço efetivo de transação;
3. custos de condomínio, IPTU, gestão, plataforma e manutenção;
4. preço e ocupação fora de Jan–Abr;
5. dados de transações/tempo de venda caso saída faça parte do mandato.

---

# Como trabalhei com IA

O projeto começou com um setup versionado de **papéis especializados, skills e checkpoints**. A arquitetura completa está em [`ai-log/02_setup_metodo.md`](ai-log/02_setup_metodo.md).

O uso de IA não foi linear. Alguns pontos que mudaram o trabalho:

- a regra de Tier estava especificada com `AND`, mas uma etapa do código usava `OR`; a revisão encontrou e corrigiu;
- o proxy temporal foi inicialmente interpretado com força excessiva e acabou rebaixado a evidência suplementar;
- o primeiro C4 interpretou coeficientes log-lineares de forma inadequada e usou uma referência de bairro com amostra mínima;
- o primeiro `Consistency Gate` dizia `PASS`, mas os checks estavam hard-coded; o freeze foi recusado e o gate foi transformado em verificação programática.

A sequência principal de prompts e respostas está em [`ai-log/01_ai_log.md`](ai-log/01_ai_log.md).

---

# Como reproduzir

Requisitos: Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Para conferir o gate final depois de gerar os artefatos:

```bash
python scripts/consistency_gate_final.py
```

Os cinco CSVs oficiais já estão versionados em `data/`.

A implementação e os resultados finais da análise ficam em `analysis/` e `working/`; o relatório legível é [`relatorio.md`](relatorio.md).

---

# Em uma frase

**Morretes 2Q é o primeiro ativo que eu diligenciaria hoje; Centro 2Q é a alternativa se a ocupação real quebrar o limiar de 20%.**
