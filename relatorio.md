# Relatório — recomendação de investimento em Itapema

## Decisão executiva

**Recomendação primária:** apartamento de **2 quartos em Morretes**, como primeira opção de diligência, com **confiança moderada**.

O segmento combina preço-noite exibido mediano de **R$498**, preço-pedido mediano de **R$790 mil**, evidência Tier A e o maior índice de eficiência de capital entre os segmentos robustos avaliados. A decisão é condicional: se Morretes operar com ocupação **mais de 20% inferior** ao Centro, Centro 2Q passa a ser a alternativa mais defensável.

A base não observa ocupação real, então esse limiar é a principal diligência antes de capital.

---

## 1. Melhor perfil de imóvel

Há duas respostas diferentes, dependendo do objetivo.

### Potencial operacional

| Quartos | n | Preço-noite mediano |
|---|---:|---:|
| Studio | 8 | R$435 |
| 1Q | 106 | R$434 |
| 2Q | 333 | R$480 |
| 3Q | 390 | R$694 |
| 4+ | 74 | **R$1.065** |

**4+ quartos** têm o maior preço-noite absoluto.

### Eficiência de capital

| Quartos | Preço-noite | Preço-pedido mediano | CEI |
|---|---:|---:|---:|
| 1Q | R$434 | R$750 mil | 0,000578 |
| 2Q | R$480 | R$810 mil | **0,000593** |
| 3Q | R$694 | R$1,80 mi | 0,000385 |
| 4+ | R$1.065 | R$3,60 mi | 0,000296 |

**1–2 quartos** são os perfis mais eficientes. O custo de aquisição dos imóveis maiores cresce mais rápido que o preço-noite.

---

## 2. Melhor localização

Entre bairros com pelo menos 30 anúncios precificados:

| Bairro | n | Preço-noite mediano |
|---|---:|---:|
| **Meia Praia** | **607** | **R$600** |
| Centro | 193 | R$587 |
| Morretes | 68 | R$500 |

Tabuleiro tem estimativa pontual de R$610, mas n=17 e permanece exploratório.

A comparação agregada esconde composição. Dentro de **2Q**, Centro = R$580, Morretes = R$498 e Meia Praia = R$460. Dentro de **3Q**, Centro = R$790 e Meia Praia = R$700.

Portanto, **Meia Praia lidera o agregado robusto**, mas **Centro lidera dentro dos perfis 2Q/3Q comparáveis**.

---

## 3. Características associadas a maior preço-noite

Modelo OLS associativo sobre `log(preço-noite exibido mediano)`, com **911 anúncios** e erros clusterizados por proprietário. Meia Praia é a referência de bairro.

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

A especificação estrutural explica cerca de **33%** da variação; acrescentar variáveis operacionais/host leva o R² a cerca de **40%**.

Esses coeficientes são associações. Variáveis de host/operação podem ser endógenas e não devem ser lidas como efeito causal de intervenção.

---

## 4. O que comprar hoje

| Segmento | Tier | Noite | Preço-pedido | Viva n | CEI | CE90 |
|---|---|---:|---:|---:|---:|---:|
| **Morretes 2Q** | A | **R$498** | **R$790 mil** | **1.035** | **0,000630** | **3,12%** |
| Centro 1Q | B | R$450 | R$890 mil | 21 | 0,000506 | 2,50% |
| Centro 2Q | A | R$580 | R$1,15 mi | 87 | 0,000504 | 2,50% |
| Meia Praia 2Q | A | R$460 | R$1,07 mi | 241 | 0,000430 | 2,13% |
| Meia Praia 3Q | A | R$700 | R$1,882 mi | 1.658 | 0,000372 | 1,84% |

`CEI = preço-noite / preço-pedido`. O CE90 é o mesmo ranking multiplicado por 90 dias e ocupação hipotética de 55%; não é retorno observado.

### Reversão

- Morretes perde para Centro se operar **>20% abaixo** em ocupação relativa.
- Centro precisa operar **>25% acima** de Morretes para ultrapassá-lo.
- Meia Praia 2Q precisa de aproximadamente **+47%** sobre Morretes.

Como a ocupação não é observada, a decisão é condicional.

---

## Posição sobre a tese interna

### Studio + Centro

**Inconclusivo.** Não há studio comparável com preço no Airbnb nem oferta válida equivalente no VivaReal no recorte necessário. Não extrapolo 1Q para studio.

### 1Q + Centro

**Parcialmente sustentado.** Centro 1Q é eficiente e testável, mas tem apenas 21 ofertas válidas no lado de aquisição e fica atrás de Morretes 2Q no screen.

A tese que sobrevive aos dados é mais ampla: **compactos podem ser eficientes, mas Centro não aparece como vencedor exclusivo e studio não pode ser validado.**

---

## Cenário anual mecânico — não é previsão

Para Morretes 2Q, assumindo mecanicamente que o preço-noite de Jan–Abr permanece no restante do ano e ignorando custos:

| Ocupação hipotética | Receita bruta | Yield bruto mecânico |
|---|---:|---:|
| 40% | R$72,7 mil | 9,2% |
| 55% | R$100,0 mil | 12,7% |
| 70% | R$127,2 mil | 16,1% |

Não entram financiamento, gestão, plataforma, manutenção, mobília, valorização ou desconto entre preço pedido e transação.

Esse quadro existe apenas para dar escala à ordem de grandeza. A análise principal permanece na janela observada e o cenário anual **não é forecast**.

---

## Limitações que importam para a decisão

1. **Ocupação real não observada** — é a variável que pode inverter Morretes × Centro.
2. **Cobertura seletiva de preço** — 999/4.441 anúncios aparecem no `Price_AV`.
3. **Janela Jan–Abr** — não mede sazonalidade anual.
4. **Preço-pedido ≠ transação.**
5. **Airbnb e VivaReal não têm match físico de imóvel** — comparações são por segmento.

## Diligência antes de comprometer capital

1. ocupação interna da Seazone por bairro e número de quartos;
2. preço de transação por segmento;
3. condomínio, IPTU, gestão, plataforma e manutenção;
4. preço e ocupação fora de Jan–Abr;
5. tempo de venda e transações fechadas, se a decisão também considerar saída.

---

## Nota metodológica sobre `Price_AV`

O arquivo contém múltiplas capturas do calendário e preço exibido, mas não possui flag confiável de reserva/ocupação. Portanto:

- preço exibido não é receita realizada;
- presença/ausência de uma data não é tratada como booking confirmado;
- o método temporal foi mantido apenas como evidência suplementar e não entrou no ranking principal;
- ocupação é usada somente em cenários explícitos.

## Robustez e correções

Durante a análise, algumas conclusões foram rebaixadas ou corrigidas depois de revisão de código:

- regra de Tier `OR → AND`;
- interpretação do proxy de transição de calendário;
- linguagem de padronização por operador;
- claim causal de composição/tamanho;
- transformação correta `exp(β)-1` na regressão log-linear;
- referência de bairro substituída por contraste útil;
- Consistency Gate substituído por checks programáticos reais.

O histórico de prompts, respostas e correções está em [`ai-log/01_ai_log.md`](ai-log/01_ai_log.md).
