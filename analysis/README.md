# Análise reproduzível

## Execução

A partir da raiz do repositório:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python analysis/run_final_analysis.py
python analysis/temporal_proxy.py
python analysis/decision_robustness.py
python analysis/generate_figures.py
python scripts/consistency_gate_final.py
```

Os comandos geram:

```text
analysis/final_results.json
analysis/temporal_proxy_results.json
analysis/decision_robustness_results.json
analysis/buy_box_morretes_2q.csv
figures/01_perfil_monetizacao_eficiencia.svg
figures/02_matriz_investimento.svg
figures/03_proxy_temporal.svg
figures/04_robustez_decisao.svg
```

O último comando audita a consistência semântica dos entregáveis finais (`README.md` e `relatorio.md`) e termina com código diferente de zero se algum dos 14 checks falhar.

## O que o pipeline reproduz

- Q1: preço-noite por perfil e índice de eficiência de capital;
- Q2: comparação de localização agregada e por número de quartos;
- Q3: regressão associativa log-linear, com incerteza clusterizada por proprietário;
- Q4: tabela dos segmentos candidatos, CEI e CE90;
- condição de reversão Morretes 2Q × Centro 2Q;
- teste temporal de mudança de estado do calendário, padronizado por lead-time;
- bootstrap com 4.000 reamostragens clusterizadas por proprietário e anunciante;
- sensibilidade à deduplicação econômica e à equalização de clusters;
- cobertura seletiva do `Price_AV` por segmento;
- cenários líquidos mecânicos e fronteira de ocupação Morretes × Centro;
- buy box reproduzível de leads de Morretes 2Q;
- quatro visualizações usadas no README e no relatório.

## Definições

`CEI = preço-noite exibido mediano / preço-pedido mediano`

`CE90 = CEI × 90 × 0,55`

O CE90 usa ocupação **hipotética**, é pré-custos e não representa ROI observado.

### Bootstrap e condição de reversão

O bootstrap reamostra os clusters observados de **proprietário** no Airbnb e de **anunciante** no VivaReal. Seu intervalo percentil mede a estabilidade amostral do CEI condicionada à base observada; não corrige seleção do `Price_AV`, sazonalidade, duplicidade física não identificada ou ocupação ausente. A proporção de reamostragens em que um segmento lidera não deve ser lida como probabilidade de superioridade real.

A fronteira líquida usa medianas positivas observadas de condomínio e IPTU, cuja cobertura é incompleta, e uma grade explícita de ocupação e custo operacional variável. É um teste mecânico antes de financiamento e imposto de renda, não previsão de resultado.

### Buy box

O arquivo `analysis/buy_box_morretes_2q.csv` é um **screen de leads**, não uma lista de compras. Os filtros são derivados da distribuição de Morretes 2Q: preço-pedido até o P25, área entre P25 e P75, preço/m² até a mediana, ao menos uma vaga e condomínio/IPTU positivos informados. Uma regra de diversificação reduz títulos e assinaturas econômicas repetidas.

Os links e atributos vêm da captura de janeiro de 2025. Disponibilidade, endereço, documentação, estado do imóvel, custos e preço atual precisam ser verificados antes de qualquer decisão.

### Proxy temporal

O teste temporal compara datas presentes/ausentes entre capturas do `Price_AV`, somente para anúncios observados nas duas capturas e dentro do horizonte comum. As transições são estratificadas por lead-time (`0–14`, `15–30`, `31–60`, `61–90` dias) e padronizadas com pesos comuns entre os segmentos.

A métrica pública principal usa a janela 07→20/01 (13 dias):

`transição líquida = (presente→ausente − ausente→presente) / presente_inicial`

Essa métrica é **estado de calendário**, não ocupação. Uma data que desaparece não é tratada como reserva confirmada e uma data que reaparece evidencia que o processo não é uma transição limpa de disponibilidade para booking.

## Dados

O pipeline utiliza somente:

- `data/Details_Itapema.csv`
- `data/Hosts_ids_Itapema.csv`
- `data/Mesh_Ids_Data_Itapema.csv`
- `data/Price_AV_Itapema.csv`
- `data/VivaReal_Itapema.csv`

Airbnb e VivaReal são comparados por segmento, não por imóvel físico idêntico.
