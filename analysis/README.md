# Análise reproduzível

## Execução

A partir da raiz do repositório:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python analysis/run_final_analysis.py
python scripts/consistency_gate_final.py
```

O primeiro comando de análise lê diretamente os cinco CSVs versionados em `data/` e grava:

```text
analysis/final_results.json
```

O segundo comando audita a consistência semântica dos entregáveis finais (`README.md` e `relatorio.md`) e termina com código diferente de zero se algum dos 14 checks falhar.

## O que o pipeline reproduz

- Q1: preço-noite por perfil e índice de eficiência de capital;
- Q2: comparação de localização agregada e por número de quartos;
- Q3: regressão associativa log-linear, com incerteza clusterizada por proprietário;
- Q4: tabela dos segmentos candidatos, CEI e CE90;
- condição de reversão Morretes 2Q × Centro 2Q.

## Definições

`CEI = preço-noite exibido mediano / preço-pedido mediano`

`CE90 = CEI × 90 × 0,55`

O CE90 usa ocupação **hipotética**, é pré-custos e não representa ROI observado.

O `Price_AV` é usado como fonte de preço exibido. A análise não trata presença/ausência de linha como reserva confirmada e não chama preço exibido de receita realizada.

## Dados

O pipeline utiliza somente:

- `data/Details_Itapema.csv`
- `data/Hosts_ids_Itapema.csv`
- `data/Mesh_Ids_Data_Itapema.csv`
- `data/Price_AV_Itapema.csv`
- `data/VivaReal_Itapema.csv`

Airbnb e VivaReal são comparados por segmento, não por imóvel físico idêntico.
