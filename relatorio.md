# Relatório — recomendação de investimento em Itapema

## Resumo executivo

> **Recomendação primária:** **Morretes 2Q**.  
> **Alternativa:** **Centro 2Q**.  
> **Confiança:** moderada.  
> **Condição de reversão:** se Morretes operar com ocupação mais de **20% inferior** à do Centro, a escolha muda para Centro 2Q.

Morretes 2Q combina preço-noite exibido mediano de **R$498**, preço-pedido mediano de **R$790 mil**, evidência Tier A e o maior índice de eficiência de capital entre os segmentos robustos avaliados.

Em **4.000 reamostragens clusterizadas** por proprietário e anunciante, Morretes 2Q fica em primeiro em **69,8%** das vezes entre os cinco candidatos finais e supera Centro 2Q em **94,7%** das comparações pareadas. Essa é estabilidade condicional à amostra, **não é probabilidade de superioridade real**.

A base não observa receita nem ocupação realizadas. Por isso, a recomendação separa explicitamente o que é observado — preço-noite exibido e preço-pedido — do que é hipotético, como cenários de ocupação.

A principal incerteza foi testada até o limite permitido pelo `Price_AV`: as transições de calendário por antecedência **não favorecem Morretes**, mas também não identificam reservas ou ocupação. Esse sinal adverso entra na avaliação de risco e ajuda a justificar a confiança moderada.

## Respostas diretas às quatro perguntas

| Pergunta | Minha resposta |
|---|---|
| **1. Melhor perfil** | No universo comparável de **apartamentos**, eu escolheria **2 quartos para investimento**. 4+ quartos têm maior preço-noite absoluto; 1–2Q têm maior eficiência de capital. |
| **2. Melhor localização em receita** | A base **não mede receita realizada**. Usando preço-noite exibido como proxy operacional, **Meia Praia lidera no agregado robusto**. Quando comparo imóveis do mesmo número de quartos, **Centro** lidera em 2Q/3Q. |
| **3. Características associadas a maior preço-noite** | Mais **quartos**, **banheiros** e operação **profissional** aparecem associados a valores maiores no modelo; estrutural R²≈33%, completo R²≈40%. |
| **4. O que comprar hoje** | **Morretes 2Q**, com Centro 2Q como alternativa e condição explícita de reversão. |

---

## 1. Melhor perfil de imóvel

> **RESPOSTA DIRETA:** para investimento, eu escolheria **2 quartos**. Para maximizar apenas preço-noite absoluto, o vencedor é **4+ quartos**.

Para manter comparabilidade entre Airbnb e VivaReal, a análise de investimento foi restrita a **apartamentos**.

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

O custo de aquisição dos imóveis maiores cresce mais rápido que o preço-noite. Portanto, **monetização absoluta e eficiência de capital levam a respostas diferentes**: 4+ quartos lideram a primeira; 1–2 quartos, a segunda, com 2Q no maior CEI.

---

## 2. Melhor localização

> **RESPOSTA DIRETA:** como a base não observa receita realizada, uso **preço-noite exibido mediano** como proxy operacional. Nesse critério, **Meia Praia** lidera no agregado robusto. Em comparações por número de quartos, **Centro** lidera os recortes de 2Q e 3Q.

| Bairro | n | Preço-noite mediano |
|---|---:|---:|
| **Meia Praia** | **607** | **R$600** |
| Centro | 193 | R$587 |
| Morretes | 68 | R$500 |

Tabuleiro apresenta R$610, mas n=17 e permanece exploratório.

A comparação agregada esconde composição. Dentro de **2Q**, Centro = R$580, Morretes = R$498 e Meia Praia = R$460. Dentro de **3Q**, Centro = R$790 e Meia Praia = R$700.

A conclusão é, portanto, dupla: **Meia Praia responde à comparação agregada**, enquanto o controle por número de quartos mostra que o **Centro apresenta maior preço-noite em tipologias comparáveis de 2Q/3Q**.

---

## 3. Características associadas a maior preço-noite

> **RESPOSTA DIRETA:** no modelo, os sinais positivos mais relevantes são **mais quartos**, **mais banheiros** e **operação profissional**. A diferença entre bairros diminui depois de controlar as características observadas.

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

A especificação estrutural explica cerca de **33%** da variação; acrescentar variáveis operacionais e de host leva o R² a cerca de **40%**.

Os coeficientes são **associações, não efeitos causais**. Variáveis de host/operação podem refletir seleção e outras diferenças não observadas.

---

## 4. O que comprar hoje

> **RESPOSTA DIRETA:** **Morretes 2Q** é minha recomendação primária. **Centro 2Q** é a alternativa. A confiança é **moderada**.

![Matriz de investimento](figures/02_matriz_investimento.svg)

| Segmento | Tier | Noite | Preço-pedido | Viva n | CEI | CE90 |
|---|---|---:|---:|---:|---:|---:|
| **Morretes 2Q** | A | **R$498** | **R$790 mil** | **1.035** | **0,000630** | **3,12%** |
| Centro 1Q | B | R$450 | R$890 mil | 21 | 0,000506 | 2,50% |
| Centro 2Q | A | R$580 | R$1,15 mi | 87 | 0,000504 | 2,50% |
| Meia Praia 2Q | A | R$460 | R$1,07 mi | 241 | 0,000430 | 2,13% |
| Meia Praia 3Q | A | R$700 | R$1,882 mi | 1.658 | 0,000372 | 1,84% |

`CEI = preço-noite / preço-pedido`. O CE90 multiplica o mesmo índice por 90 dias e ocupação hipotética de 55%; **não é retorno observado**.

**Tier é uma classificação de robustez da amostra:** A exige pelo menos 30 observações em cada lado da comparação; B, pelo menos 15; abaixo disso o segmento é exploratório.

### Por que Morretes 2Q

1. maior CEI entre os candidatos robustos avaliados;
2. Tier A, com 51 anúncios Airbnb precificados e 1.035 ofertas válidas no lado de aquisição;
3. preço-pedido mediano de R$790 mil, abaixo dos principais comparáveis;
4. o ranking permaneceu estável após correções de Tier, operador, tamanho, validade e modelagem;
5. o sinal temporal adverso foi incorporado à confiança, em vez de ser descartado por não favorecer o líder.
6. a vantagem sobre Centro 2Q aparece em 94,7% das reamostragens pareadas e sobrevive à deduplicação de estresse.

### Condição de reversão

- Morretes perde para Centro se operar **>20% abaixo** em ocupação relativa.
- Equivalentemente, Centro precisa operar **>25% acima** de Morretes para ultrapassá-lo.

O limiar pontual exige ocupação Morretes/Centro de **80,0%**. O intervalo bootstrap é amplo, de **52,6% a 104,7%**, e inclui cenários em que Morretes precisaria igualar ou superar a ocupação do Centro. A regra de 20% é uma fronteira pontual para diligência, não uma certeza.

---

## Robustez estatística e sensibilidade de duplicidade

O bootstrap usa **4.000 reamostragens** (semente fixa) e preserva os clusters de **proprietário** no Airbnb e **anunciante** no VivaReal. Isso evita tratar todos os anúncios de um grande operador como observações plenamente independentes.

![Robustez da decisão por bootstrap](figures/04_robustez_decisao.svg)

| Segmento | Clusters Air/Viva | CEI | Intervalo bootstrap 95% | Rank 1 entre finalistas |
|---|---:|---:|---:|---:|
| **Morretes 2Q** | 40 / 121 | **0,000630** | **0,000499–0,000714** | **69,8%** |
| Centro 1Q | 20 / 16 | 0,000506 | 0,000442–0,000750 | 26,2% |
| Centro 2Q | 41 / 42 | 0,000504 | 0,000314–0,000644 | 4,0% |
| Meia Praia 2Q | 163 / 68 | 0,000430 | 0,000386–0,000490 | 0,0% |
| Meia Praia 3Q | 275 / 192 | 0,000372 | 0,000342–0,000381 | 0,0% |

Morretes 2Q supera a alternativa Centro 2Q em **94,7%** das reamostragens pareadas. Nem 69,8% nem 94,7% representam probabilidade de o investimento ser realmente melhor: o procedimento mede ruído amostral condicionado ao recorte observado e não corrige cobertura, sazonalidade, ocupação ou qualidade física.

### Deduplicação e peso dos operadores

Como anúncios diferentes podem descrever unidades repetidas, apliquei uma deduplicação de estresse por assinatura econômica observada. Ela é conservadora e não prova identidade física.

| Segmento | Viva n base → assinatura | Preço-pedido base → assinatura | Variação |
|---|---:|---:|---:|
| **Morretes 2Q** | 1.035 → 873 | R$790 mil → R$789 mil | **−0,1%** |
| Centro 2Q | 87 → 75 | R$1,15 mi → R$1,227 mi | +6,7% |
| Meia Praia 2Q | 241 → 222 | R$1,07 mi → R$1,100 mi | +2,8% |

O ranking permanece. Em um teste adicional que dá o mesmo peso a cada proprietário e anunciante, o CEI é **0,000612** para Morretes 2Q e **0,000389** para Centro 2Q.

### Cobertura seletiva do preço

O `Price_AV` cobre **22,3%** dos apartamentos Morretes 2Q presentes no cadastro, contra 35,5% no Centro 2Q e 25,9% em Meia Praia 2Q. Esse desequilíbrio é quantificado, mas não corrigido pelo bootstrap. É uma das razões para manter a confiança moderada.

---

## Teste temporal da hipótese de ocupação

A recomendação depende do diferencial de ocupação. O `Price_AV` não possui flag de reserva, mas contém capturas do calendário em 06, 07 e 20 de janeiro. Isso permite construir um **teste suplementar de mudança de estado**, sem interpretar o resultado como reserva ou ocupação realizada.

### Construção

Para cada par de capturas:

1. mantenho somente anúncios presentes nas duas capturas;
2. uso apenas o horizonte de datas de estadia comum às duas capturas;
3. classifico cada data como presente→ausente ou ausente→presente;
4. separo por faixas de antecedência (`0–14`, `15–30`, `31–60`, `61–90` dias);
5. calculo a transição líquida `(presente→ausente − ausente→presente) / presente_inicial`;
6. padronizo os segmentos com os mesmos pesos de antecedência.

O par 06→07, de apenas um dia, possui movimento pequeno e não é usado como evidência principal. Para a apresentação pública, uso **07→20 jan (13 dias)** e não trato 06→20 como confirmação independente, porque as duas janelas longas compartilham a captura final de 20/01.

![Teste de robustez temporal](figures/03_proxy_temporal.svg)

| Segmento 2Q | Transição líquida padronizada 07→20 jan |
|---|---:|
| **Morretes 2Q** | **7,1%** |
| Meia Praia 2Q | 11,3% |
| Centro 2Q | 12,2% |

### Interpretação para a decisão

**O sinal temporal é desfavorável a Morretes.** Morretes 2Q apresenta menor transição líquida de calendário que Centro 2Q e Meia Praia 2Q no intervalo informativo.

Esse resultado entra diretamente na classificação de **confiança moderada** e reforça a necessidade de validar ocupação antes da compra.

O limite do teste é semântico: uma data desaparecer do arquivo não demonstra que foi reservada, e o reaparecimento de datas mostra que o calendário não segue uma transição limpa de “disponível para reservado”. Consequentemente, **7,1%, 11,3% e 12,2% não são taxas de ocupação** e não podem ser comparadas diretamente ao limiar de reversão de 20%.

O teste responde, portanto, a uma pergunta restrita: **há um sinal temporal que favorece ou contradiz o líder?** Há um sinal fraco que contradiz. Ele não informa o diferencial de ocupação realizado entre Morretes e Centro.

---

## Posição sobre a tese interna

### Studio + Centro

> **RESPOSTA:** **inconclusivo**.

Não há studio comparável com preço no Airbnb nem oferta válida equivalente no VivaReal no recorte necessário. Não extrapolo o resultado de 1Q para studio.

### 1Q + Centro

> **RESPOSTA:** **parcialmente sustentado**.

Centro 1Q é eficiente e testável, mas tem apenas 21 ofertas válidas no lado de aquisição e fica atrás de Morretes 2Q na comparação final de investimento.

**Minha posição:** a base sustenta que compactos podem ter boa eficiência, mas não sustenta Centro + studio/1Q como regra geral de compra. Para a decisão atual, continuo preferindo **Morretes 2Q**, condicionado à validação da ocupação relativa.

---

## Cenário anual mecânico — não é previsão

Para Morretes 2Q, assumindo mecanicamente que o preço-noite de Jan–Abr permanece no restante do ano e ignorando custos:

| Ocupação hipotética | Receita bruta mecânica | Yield bruto mecânico |
|---|---:|---:|
| 40% | R$72,7 mil | 9,2% |
| 55% | R$100,0 mil | 12,7% |
| 70% | R$127,2 mil | 16,1% |

Não entram financiamento, gestão, plataforma, manutenção, mobília, valorização ou desconto entre preço pedido e transação. Esse quadro existe apenas para dar escala; **não é forecast**.

### Cenário líquido mecânico — não é previsão

Para uma comparação após custos, uso **55% de ocupação** e **30% de custo operacional variável**, iguais entre os segmentos. Condomínio e IPTU são medianas entre valores positivos observados no VivaReal — R$4,9 mil/ano em Morretes e cerca de R$7,0 mil nos demais — com cobertura incompleta.

| Segmento | Receita bruta mecânica | Custo fixo observado | Resultado líquido mecânico | Yield líquido/pedido |
|---|---:|---:|---:|---:|
| **Morretes 2Q** | R$100,0 mil | R$4,9 mil | **R$65,1 mil** | **8,24%** |
| Centro 2Q | R$116,4 mil | R$7,0 mil | R$74,5 mil | 6,48% |
| Meia Praia 2Q | R$92,3 mil | R$7,0 mil | R$57,7 mil | 5,39% |

O resultado é antes de financiamento e imposto de renda. A grade reproduzida no código varia ocupação entre 40%/55%/70% e custos variáveis entre 20%/30%/40%. Sob 55% de ocupação no Centro e 30% de custo variável, Morretes empata perto de **44,1%** de ocupação. O cenário líquido mecânico **não é previsão**, retorno observado ou recomendação de crédito.

### Buy box de diligência

A [`buy box`](analysis/buy_box_morretes_2q.csv) aplica regras derivadas da própria distribuição de Morretes 2Q:

- preço-pedido até o P25: **R$680 mil**;
- área entre P25 e P75: **65–70 m²**;
- preço/m² até a mediana: **R$11.551/m²**;
- pelo menos uma vaga;
- condomínio e IPTU positivos informados;
- diversificação de títulos e assinaturas econômicas repetidas.

O filtro encontra 80 linhas antes da diversificação, 33 depois dela e publica os 12 primeiros leads. Os cinco primeiros são:

| Lead | Pedido | Área | R$/m² | Condomínio | IPTU/ano |
|---|---:|---:|---:|---:|---:|
| [2666436700](https://www.vivareal.com.br/imovel/apartamento-2-quartos-morretes-bairros-itapema-com-garagem-69m2-venda-RS374000-id-2666436700/) | R$374 mil | 69 m² | R$5.420 | R$290 | R$490 |
| [2646969738](https://www.vivareal.com.br/imovel/apartamento-2-quartos-morretes-bairros-itapema-com-garagem-70m2-venda-RS450000-id-2646969738/) | R$450 mil | 70 m² | R$6.429 | R$250 | R$100 |
| [2688799819](https://www.vivareal.com.br/imovel/apartamento-2-quartos-morretes-bairros-itapema-com-garagem-66m2-venda-RS515000-id-2688799819/) | R$515 mil | 66 m² | R$7.803 | R$300 | R$500 |
| [2694368874](https://www.vivareal.com.br/imovel/apartamento-2-quartos-morretes-bairros-itapema-com-garagem-70m2-venda-RS520001-id-2694368874/) | R$520 mil | 70 m² | R$7.429 | R$300 | R$1.000 |
| [2768930018](https://www.vivareal.com.br/imovel/apartamento-2-quartos-morretes-bairros-itapema-com-garagem-70m2-venda-RS530000-id-2768930018/) | R$530 mil | 70 m² | R$7.571 | R$275 | R$480 |

É um **screen histórico, não uma recomendação de compra**. Os links e atributos são da base de janeiro de 2025; disponibilidade, endereço, documentação, estado, custos e preço atual precisam ser verificados.

---

## Limitações que importam para a decisão

1. **Ocupação realizada não observada** — é a variável que pode inverter Morretes × Centro.
2. **Cobertura seletiva de preço** — 999/4.441 anúncios aparecem no `Price_AV`; Morretes 2Q tem cobertura de 22,3%.
3. **Janela Jan–Abr** — não mede sazonalidade anual.
4. **Preço-pedido ≠ preço de transação.**
5. **Airbnb e VivaReal não têm correspondência física de imóvel** — as comparações são por segmento.

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
- reconstrução do proxy temporal por antecedência e limitação explícita de sua interpretação;
- correção da linguagem de padronização por operador;
- retirada de afirmação causal sobre composição/tamanho;
- transformação correta `exp(β)-1` na regressão log-linear;
- referência de bairro substituída por comparação mais informativa;
- bootstrap expandido para proprietário + anunciante e cinco candidatos finais;
- deduplicação de estresse, cenário líquido e buy box reproduzíveis;
- Consistency Gate ampliado de 14 para **20 verificações programáticas**.

O histórico de prompts, respostas e correções está em [`ai-log/01_ai_log.md`](ai-log/01_ai_log.md); o índice das intervenções críticas está em [`ai-log/README.md`](ai-log/README.md).

---

## Conclusão

> **Morretes 2Q é minha prioridade de diligência, com Centro 2Q como alternativa. O líder ocupa o primeiro lugar em 69,8% das reamostragens dos finalistas e supera Centro 2Q em 94,7% das comparações pareadas; esses números medem estabilidade amostral, não probabilidade de sucesso. A cobertura seletiva e o sinal temporal desfavorável mantêm a recomendação condicionada à validação de ocupação, custos e imóveis da buy box.**
