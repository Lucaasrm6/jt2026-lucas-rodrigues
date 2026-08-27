# Relatório — recomendação de investimento em Itapema

## Resumo executivo

> **Minha recomendação:** começar a diligência por **apartamentos de 2 quartos em Morretes**.  
> **Alternativa:** **Centro 2Q**.  
> **Confiança:** moderada.  
> **Condição de reversão:** se Morretes operar com ocupação mais de **20% inferior** ao Centro, minha escolha muda para Centro 2Q.

Morretes 2Q combina preço-noite exibido mediano de **R$498**, preço-pedido mediano de **R$790 mil**, evidência Tier A e o maior índice de eficiência de capital entre os segmentos robustos avaliados.

A principal incerteza foi testada até o limite permitido pelo `Price_AV`: as transições de calendário por lead-time **não favorecem Morretes**, mas também não identificam reservas ou ocupação. Esse resultado aumenta a cautela e sustenta a classificação de confiança moderada, sem fornecer base semântica para substituir a condição de reversão.

## Respostas diretas às quatro perguntas

| Pergunta | Minha resposta |
|---|---|
| **1. Melhor perfil** | **Apartamento de 2 quartos para investimento.** 4+ quartos têm maior preço-noite absoluto; 1–2Q têm maior eficiência de capital. |
| **2. Melhor localização em receita** | **Meia Praia no agregado robusto**. Quando comparo perfis equivalentes por quartos, **Centro** lidera em 2Q/3Q. |
| **3. Características associadas a maior preço-noite** | Mais **quartos**, **banheiros** e operação **profissional** aparecem associados a valores maiores no modelo; estrutural R²≈33%, completo R²≈40%. |
| **4. O que comprar hoje** | **Morretes 2Q**, com Centro 2Q como alternativa e condição explícita de reversão. |

---

## 1. Melhor perfil de imóvel

> **RESPOSTA DIRETA:** para investimento, eu escolheria **2 quartos**. Para maximizar apenas preço-noite absoluto, o vencedor é **4+ quartos**.

![Perfil: monetização absoluta versus eficiência de capital](figures/01_perfil_monetizacao_eficiencia.svg)

### Potencial operacional

| Quartos | n | Preço-noite mediano |
|---|---:|---:|
| Studio | 8 | R$435 |
| 1Q | 106 | R$434 |
| 2Q | 333 | R$480 |
| 3Q | 390 | R$694 |
| 4+ | 74 | **R$1.065** |

### Eficiência de capital

| Quartos | Preço-noite | Preço-pedido mediano | CEI |
|---|---:|---:|---:|
| 1Q | R$434 | R$750 mil | 0,000578 |
| **2Q** | R$480 | R$810 mil | **0,000593** |
| 3Q | R$694 | R$1,80 mi | 0,000385 |
| 4+ | R$1.065 | R$3,60 mi | 0,000296 |

O custo de aquisição dos imóveis maiores cresce mais rápido que o preço-noite. Portanto, a resposta de monetização absoluta (**4+ quartos**) é diferente da resposta de alocação eficiente de capital (**1–2 quartos; 2Q na liderança do CEI**).

---

## 2. Melhor localização

> **RESPOSTA DIRETA:** **Meia Praia** é a melhor localização no agregado robusto. Em comparações por número de quartos, **Centro** lidera os recortes de 2Q e 3Q.

| Bairro | n | Preço-noite mediano |
|---|---:|---:|
| **Meia Praia** | **607** | **R$600** |
| Centro | 193 | R$587 |
| Morretes | 68 | R$500 |

Tabuleiro tem estimativa pontual de R$610, mas n=17 e permanece exploratório.

A comparação agregada esconde composição. Dentro de **2Q**, Centro = R$580, Morretes = R$498 e Meia Praia = R$460. Dentro de **3Q**, Centro = R$790 e Meia Praia = R$700.

A conclusão é deliberadamente dupla: **Meia Praia responde à pergunta agregada**, enquanto o controle por número de quartos mostra que o **Centro tem maior preço-noite em tipologias comparáveis de 2Q/3Q**.

---

## 3. Características associadas a maior preço-noite

> **RESPOSTA DIRETA:** no modelo, os sinais positivos mais relevantes para preço-noite são **mais quartos**, **mais banheiros** e **operação profissional**. A diferença de bairro fica menor depois de controlar as características observadas.

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

Os coeficientes são **associações, não efeitos causais**. Em particular, variáveis de host/operação podem refletir seleção e diferenças não observadas.

---

## 4. O que comprar hoje

> **RESPOSTA DIRETA:** **Morretes 2Q** é minha recomendação primária. **Centro 2Q** é a alternativa. Eu classifico a confiança como **moderada**.

![Matriz de investimento](figures/02_matriz_investimento.svg)

| Segmento | Tier | Noite | Preço-pedido | Viva n | CEI | CE90 |
|---|---|---:|---:|---:|---:|---:|
| **Morretes 2Q** | A | **R$498** | **R$790 mil** | **1.035** | **0,000630** | **3,12%** |
| Centro 1Q | B | R$450 | R$890 mil | 21 | 0,000506 | 2,50% |
| Centro 2Q | A | R$580 | R$1,15 mi | 87 | 0,000504 | 2,50% |
| Meia Praia 2Q | A | R$460 | R$1,07 mi | 241 | 0,000430 | 2,13% |
| Meia Praia 3Q | A | R$700 | R$1,882 mi | 1.658 | 0,000372 | 1,84% |

`CEI = preço-noite / preço-pedido`. O CE90 é o mesmo ranking multiplicado por 90 dias e ocupação hipotética de 55%; não é retorno observado.

### Por que Morretes 2Q

1. maior CEI entre os candidatos robustos avaliados;
2. Tier A, com 51 anúncios Airbnb precificados e 1.035 ofertas válidas no lado de aquisição;
3. preço-pedido mediano de R$790 mil, abaixo dos principais comparáveis;
4. o ranking sobreviveu às correções de Tier, operador, tamanho, validade e modelagem;
5. a principal evidência adversa — o proxy temporal — foi preservada e incorporada à confiança, em vez de descartada por não favorecer o líder.

### Condição de reversão

- Morretes perde para Centro se operar **>20% abaixo** em ocupação relativa.
- Equivalentemente, Centro precisa operar **>25% acima** de Morretes para ultrapassá-lo.

---

## Teste temporal da hipótese de ocupação

A recomendação depende do diferencial de ocupação. O `Price_AV` não possui flag de reserva, mas contém capturas do calendário em 06, 07 e 20 de janeiro. Isso permitiu construir um **teste suplementar de mudança de estado**, sem chamar o resultado de booking ou ocupação.

### Construção

Para cada par de capturas:

1. mantenho somente anúncios presentes nas duas capturas;
2. uso apenas o horizonte de datas de estadia comum às duas capturas;
3. classifico cada data como presente→ausente ou ausente→presente;
4. separo por lead-time em faixas definidas (`0–14`, `15–30`, `31–60`, `61–90` dias);
5. calculo a transição líquida `(presente→ausente − ausente→presente) / presente_inicial`;
6. padronizo os segmentos com os mesmos pesos de lead-time.

O par 06→07, de apenas um dia, possui movimento pequeno e não é usado como evidência principal. Para a apresentação pública, uso **07→20 jan (13 dias)** e não trato 06→20 como uma confirmação independente, porque as duas janelas longas compartilham a captura final de 20/01.

![Teste de robustez temporal](figures/03_proxy_temporal.svg)

| Segmento 2Q | Transição líquida padronizada 07→20 jan |
|---|---:|
| **Morretes 2Q** | **7,1%** |
| Meia Praia 2Q | 11,3% |
| Centro 2Q | 12,2% |

### Interpretação para a decisão

**O teste inclina contra Morretes.** Morretes 2Q tem menor transição líquida de calendário que Centro 2Q e Meia Praia 2Q no intervalo informativo.

Isso não foi ignorado. Pelo contrário, entra diretamente na classificação de **confiança moderada** e reforça a necessidade de validar ocupação antes da compra.

O limite do teste é semântico: uma data desaparecer do arquivo não demonstra que foi reservada, e uma data reaparecer mostra que o estado do calendário não é uma transição limpa de “disponível para vendido”. Consequentemente, **7,1%, 11,3% e 12,2% não são taxas de ocupação** e não podem ser comparadas diretamente ao limiar de reversão de 20%.

Assim, o proxy responde à pergunta “há um sinal temporal que favorece ou contradiz o líder?” — **há um sinal fraco que contradiz**. Ele não responde “qual é o diferencial de ocupação realizado entre Morretes e Centro?”. Essa variável permanece não observada.

---

## Posição sobre a tese interna

### Studio + Centro

> **RESPOSTA:** **inconclusivo**.

Não há studio comparável com preço no Airbnb nem oferta válida equivalente no VivaReal no recorte necessário. Não extrapolo 1Q para studio.

### 1Q + Centro

> **RESPOSTA:** **parcialmente sustentado**.

Centro 1Q é eficiente e testável, mas tem apenas 21 ofertas válidas no lado de aquisição e fica atrás de Morretes 2Q no screen.

**Minha posição:** a base sustenta que compactos podem ter boa eficiência, mas não sustenta Centro + studio/1Q como regra geral de compra. Para a decisão atual, continuo preferindo **Morretes 2Q**, sob a condição explícita de ocupação relativa.

---

## Cenário anual mecânico — não é previsão

Para Morretes 2Q, assumindo mecanicamente que o preço-noite de Jan–Abr permanece no restante do ano e ignorando custos:

| Ocupação hipotética | Receita bruta mecânica | Yield bruto mecânico |
|---|---:|---:|
| 40% | R$72,7 mil | 9,2% |
| 55% | R$100,0 mil | 12,7% |
| 70% | R$127,2 mil | 16,1% |

Não entram financiamento, gestão, plataforma, manutenção, mobília, valorização ou desconto entre preço pedido e transação. Esse quadro existe apenas para dar escala; **não é forecast**.

---

## Limitações que importam para a decisão

1. **Ocupação realizada não observada** — é a variável que pode inverter Morretes × Centro.
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

## Robustez e correções

Durante a análise, conclusões e implementações foram revisadas antes do fechamento:

- regra de Tier `OR → AND`;
- reconstrução do proxy temporal por lead-time e limitação explícita de sua semântica;
- linguagem de padronização por operador;
- retirada de claim causal de composição/tamanho;
- transformação correta `exp(β)-1` na regressão log-linear;
- referência de bairro substituída por contraste útil;
- Consistency Gate substituído por 14 checks programáticos reais.

O histórico de prompts, respostas e correções está em [`ai-log/01_ai_log.md`](ai-log/01_ai_log.md).

---

## Minha resposta final

> **Eu colocaria Morretes 2Q no topo da diligência de aquisição. Centro 2Q é minha alternativa. O teste temporal joga contra Morretes, mas não mede ocupação; por isso, a recomendação permanece condicional ao limiar de 20% e exige validação de ocupação realizada antes da compra.**