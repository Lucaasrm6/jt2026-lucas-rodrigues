from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "README.md", ROOT / "relatorio.md"]
ROBUSTNESS = ROOT / "analysis" / "decision_robustness_results.json"
BUY_BOX = ROOT / "analysis" / "buy_box_morretes_2q.csv"

for path in [*FILES, ROBUSTNESS, BUY_BOX]:
    if not path.exists():
        raise SystemExit(f"BLOCKED: arquivo obrigatório ausente: {path.relative_to(ROOT)}")

text = "\n".join(p.read_text(encoding="utf-8") for p in FILES)
robustness = json.loads(ROBUSTNESS.read_text(encoding="utf-8"))
with BUY_BOX.open(encoding="utf-8", newline="") as handle:
    buy_box_rows = list(csv.DictReader(handle))
bootstrap_win_share = robustness["comparisons"][
    "morretes_cei_above_centro_share"
]
bootstrap_win_share_text = f"{100 * bootstrap_win_share:.1f}%".replace(".", ",")


def no_regex(pattern: str, flags: int = re.I) -> bool:
    return re.search(pattern, text, flags) is None


def has_regex(pattern: str, flags: int = re.I) -> bool:
    return re.search(pattern, text, flags) is not None


checks = [
    (
        "01_sem_adr_nao_qualificado",
        no_regex(r"\bADR\b"),
        "usar 'preço-noite exibido', não ADR",
    ),
    (
        "02_sem_claim_de_receita_realizada",
        no_regex(r"receita realizada\s*(?:=|:|de\s+R\$|foi\s+R\$|é\s+R\$)|(?:faturamento|receita)\s+realizad[oa]\s+(?:de|foi)\s+R\$"),
        "a base não pode receber valor de receita realizada",
    ),
    (
        "03_sem_claim_de_demanda_anual",
        no_regex(r"(?:centro|morretes|meia praia).{0,60}(?:demanda|procura).{0,30}(?:ano todo|anual|year[- ]round)"),
        "não inferir demanda anual/sazonalidade fora da janela",
    ),
    (
        "04_sem_claim_de_liquidez_ou_valorizacao",
        no_regex(r"(?:tem|possui|oferece|apresenta|maior|melhor)\s+(?:liquidez|valorização)"),
        "profundidade de oferta não prova liquidez/valorização",
    ),
    (
        "05_sem_snapshots_chamados_independentes",
        no_regex(r"(?:snapshots?|pares?|janelas?)\s+(?:são\s+)?independentes"),
        "janelas sobrepostas não são confirmações independentes",
    ),
    (
        "06_sem_claim_63pct_tamanho",
        no_regex(r"63\s*%[^\n]{0,80}(?:tamanho|área)|(?:tamanho|área)[^\n]{0,80}63\s*%"),
        "não atribuir causalmente 63% do desconto ao tamanho",
    ),
    (
        "07_sem_probabilidade_de_reabertura",
        no_regex(r"probabilidade\s+de\s+reabertura|reopening\s+probability"),
        "transições de calendário não são probabilidade de reabertura",
    ),
    (
        "08_studio_e_1q_separados",
        has_regex(r"studio\s*\+?\s*centro") and has_regex(r"1q\s*\+?\s*centro"),
        "studio e 1Q Centro precisam de vereditos separados",
    ),
    (
        "09_ce90_rotulado_como_cenario",
        has_regex(r"CE90[^\n]{0,180}(?:cenário|cenario)") and has_regex(r"CE90[^\n]{0,220}(?:não é retorno observado|não ROI observado|não é ROI observado)"),
        "CE90 deve ser cenário, não retorno observado",
    ),
    (
        "10_preco_pedido_nao_transacao",
        has_regex(r"preço[- ]pedido\s*[^\n]{0,20}[≠]|preço[- ]pedido[^\n]{0,80}não[^\n]{0,30}transa"),
        "preço pedido não é preço de transação",
    ),
    (
        "11_q3_associativa_nao_causal",
        has_regex(r"associativ") and has_regex(r"não caus"),
        "Q3 deve ser interpretada como associação, não causalidade",
    ),
    (
        "12_anual_mecanico_nao_forecast",
        has_regex(r"cenário anual mecânico") and has_regex(r"não é previsão|não é forecast|não é\s+forecast"),
        "cenário anual deve ser claramente não-previsão",
    ),
    (
        "13_q2_robustez_amostral",
        has_regex(r"pelo menos 30 anúncios|amostra robusta") and has_regex(r"tabuleiro[^\n]{0,100}explorat"),
        "Q2 deve qualificar Meia Praia por robustez e Tabuleiro como exploratório",
    ),
    (
        "14_sem_coeficientes_antigos_c4",
        no_regex(r"\+17[,.]4\s*%|\+14[,.]0\s*%|\+20[,.]7\s*%|centro\s*\+\s*78\s*%"),
        "não deixar interpretações antigas da regressão no entregável final",
    ),
    (
        "15_bootstrap_clusterizado_documentado",
        has_regex(r"4\.000\s+reamostrag")
        and has_regex(r"proprietário[^\n]{0,100}anunciante|anunciante[^\n]{0,100}proprietário"),
        "bootstrap deve declarar iterações e unidades de cluster",
    ),
    (
        "16_bootstrap_nao_e_probabilidade_real",
        bootstrap_win_share_text in text
        and has_regex(r"não (?:é|representa) probabilidade"),
        "estabilidade condicional não deve virar probabilidade de superioridade real",
    ),
    (
        "17_cobertura_seletiva_quantificada",
        has_regex(r"22[,.]3\s*%") and has_regex(r"cobertura[^\n]{0,120}(?:seletiv|Price_AV)"),
        "risco de seleção do Price_AV deve ser quantificado",
    ),
    (
        "18_cenario_liquido_nao_e_previsao",
        has_regex(r"cenário líquido mecânico")
        and has_regex(r"antes de financiamento")
        and has_regex(r"não é previsão"),
        "cenário líquido deve manter premissas e limites explícitos",
    ),
    (
        "19_buy_box_e_apenas_screen_historico",
        has_regex(r"buy box")
        and has_regex(r"(?:janeiro|jan)[^\n]{0,20}2025")
        and has_regex(r"(?:disponibilidade|dados)[^\n]{0,100}(?:verific|confirm)"),
        "buy box deve ser tratada como screen histórico sujeito a verificação",
    ),
    (
        "20_resultados_de_robustez_machine_checkable",
        0.90 <= bootstrap_win_share <= 1.0
        and abs(
            robustness["comparisons"]
            ["gross_break_even_occupancy_ratio_morretes_to_centro"]["point"]
            - 0.8
        )
        <= 0.001
        and len(buy_box_rows) == 12
        and all(80 <= float(row["monthly_condo_fee"]) <= 5_000 for row in buy_box_rows)
        and all(100 <= float(row["yearly_iptu"]) <= 30_000 for row in buy_box_rows)
        and all(row.get("diligence_flags") for row in buy_box_rows),
        "números publicados e buy box plausível devem continuar reproduzíveis",
    ),
]

failed = []
print("FINAL CONSISTENCY GATE")
print("=" * 72)
for name, ok, rule in checks:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}: {rule}")
    if not ok:
        failed.append(name)

print("=" * 72)
if failed:
    print(f"BLOCKED ({len(checks) - len(failed)}/{len(checks)}): " + ", ".join(failed))
    sys.exit(1)

print(f"PASS ({len(checks)}/{len(checks)})")
sys.exit(0)
