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
python analysis/generate_figures.py
python scripts/consistency_gate_final.py
```

Os comandos geram:

```text
analysis/final_results.json
analysis/temporal_proxy_results.json
figures/01_perfil_monetizacao_eficiencia.svg
figures/02_matriz_investimento.svg
figures/03_proxy_temporal.svg
```

O último comando audita a consistência semântica dos entregáveis finais (`README.md` e `relatorio.md`) e termina com código diferente de zero se algum dos 14 checks falhar.

## O que o pipeline reproduz

- Q1: preço-noite por perfil e índice de eficiência de capital;
- Q2: comparação de localização agregada e por número de quartos;
- Q3: regressão associativa log-linear, com incerteza clusterizada por proprietário;
- Q4: tabela dos segmentos candidatos, CEI e CE90;
- condição de reversão Morretes 2Q × Centro 2Q;
- teste temporal de mudança de estado do calendário, padronizado por lead-time;
- três visualizações usadas no README e no relatório.

## Definições

`CEI = preço-noite exibido mediano / preço-pedido mediano`

`CE90 = CEI × 90 × 0,55`

O CE90 usa ocupação **hipotética**, é pré-custos e não representa ROI observado.

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
