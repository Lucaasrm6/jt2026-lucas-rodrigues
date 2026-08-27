from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "analysis" / "final_results.json"
TEMPORAL = ROOT / "analysis" / "temporal_proxy_results.json"
ROBUSTNESS = ROOT / "analysis" / "decision_robustness_results.json"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

BG = "#ffffff"
INK = "#172033"
MUTED = "#5b6576"
GRID = "#d9dee7"
ACCENT = "#2563eb"
ACCENT_2 = "#0f766e"
WARN = "#b45309"
LIGHT = "#eef2f7"


def esc(value):
    return html.escape(str(value))


def svg_start(width, height, title):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f"<title>{esc(title)}</title>",
        f'<rect width="100%" height="100%" fill="{BG}"/>',
        "<style>"
        f"text{{font-family:Arial,Helvetica,sans-serif;fill:{INK}}}"
        ".title{font-size:24px;font-weight:700}"
        f".sub{{font-size:14px;fill:{MUTED}}}"
        ".label{font-size:14px}"
        f".small{{font-size:12px;fill:{MUTED}}}"
        ".value{font-size:13px;font-weight:700}"
        "</style>",
    ]


def text(x, y, value, css="label", anchor="start"):
    return f'<text x="{x}" y="{y}" class="{css}" text-anchor="{anchor}">{esc(value)}</text>'


def rect(x, y, width, height, fill, rx=4):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" fill="{fill}"/>'


def line(x1, y1, x2, y2, stroke=GRID, width=1):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"/>'


def circle(cx, cy, radius, fill, stroke=BG):
    return f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def save(name, parts):
    parts.append("</svg>")
    (OUT / name).write_text("\n".join(parts), encoding="utf-8")


final = json.loads(FINAL.read_text(encoding="utf-8"))
temporal = json.loads(TEMPORAL.read_text(encoding="utf-8"))
robustness = json.loads(ROBUSTNESS.read_text(encoding="utf-8"))

# 1) Profile: absolute monetization vs capital efficiency.
q1 = final["q1_profile"]
profiles = [("1Q", q1["1"]), ("2Q", q1["2"]), ("3Q", q1["3"]), ("4+", q1["4"])]
width, height = 980, 590
parts = svg_start(width, height, "Perfil: monetização absoluta versus eficiência de capital")
parts += [
    text(55, 48, "Perfil: monetização absoluta × eficiência de capital", "title"),
    text(55, 74, "O perfil que cobra mais por noite não é o que usa melhor o capital de aquisição.", "sub"),
    text(55, 120, "Preço-noite exibido mediano (R$)", "label"),
]
max_night = max(row["night"] for _, row in profiles)
x0, max_width = 165, 720
for index, (label, row) in enumerate(profiles):
    y = 145 + index * 54
    bar_width = max_width * row["night"] / max_night
    parts += [
        text(140, y + 21, label, "label", "end"),
        rect(x0, y, bar_width, 30, ACCENT if label == "4+" else ACCENT_2),
        text(x0 + bar_width + 10, y + 21, f"R$ {row['night']:,.0f}".replace(",", "."), "value"),
    ]
parts += [
    line(55, 375, 925, 375),
    text(55, 412, "Eficiência de capital — R$ de preço-noite por R$100 mil de preço-pedido", "label"),
]
capital_values = [(label, 100000 * row["cei"]) for label, row in profiles]
max_capital = max(value for _, value in capital_values)
for index, (label, value) in enumerate(capital_values):
    y = 435 + index * 32
    bar_width = max_width * value / max_capital
    parts += [
        text(140, y + 17, label, "label", "end"),
        rect(x0, y, bar_width, 22, ACCENT if label == "2Q" else ACCENT_2),
        text(x0 + bar_width + 10, y + 17, f"R$ {value:.1f}".replace(".", ","), "value"),
    ]
parts.append(text(925, 568, "Fonte: Airbnb Price_AV + VivaReal; preço exibido e preço-pedido, não realizados.", "small", "end"))
save("01_perfil_monetizacao_eficiencia.svg", parts)

# 2) Investment matrix: asking price vs displayed nightly price.
candidates = final["q4_candidates"]
points = []
for row in candidates:
    bedrooms = int(row["bed_group"])
    label = f"{row['suburb_canon']} {bedrooms}Q"
    points.append(
        (
            label,
            float(row["asking"]) / 1e6,
            float(row["night"]),
            float(row["cei"]) * 100000,
            row["tier"],
        )
    )

width, height = 980, 600
parts = svg_start(width, height, "Matriz de investimento: preço-pedido versus preço-noite exibido")
parts += [
    text(55, 48, "Matriz de investimento — candidatos finais", "title"),
    text(55, 74, "Mais acima = maior preço-noite exibido; mais à esquerda = menor capital de aquisição.", "sub"),
]
left, right, top, bottom = 100, 910, 120, 500
xmin, xmax, ymin, ymax = 0.7, 2.0, 400, 750
for x in [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]:
    px = left + (x - xmin) / (xmax - xmin) * (right - left)
    parts += [line(px, top, px, bottom), text(px, bottom + 24, f"{x:.1f}".replace(".", ","), "small", "middle")]
for y in [400, 500, 600, 700]:
    py = bottom - (y - ymin) / (ymax - ymin) * (bottom - top)
    parts += [line(left, py, right, py), text(left - 12, py + 4, str(y), "small", "end")]
parts += [
    text((left + right) / 2, 550, "Preço-pedido mediano (R$ milhões)", "label", "middle"),
    '<text x="25" y="310" class="label" text-anchor="middle" transform="rotate(-90 25 310)">Preço-noite exibido mediano (R$)</text>',
]
for label, asking_millions, night, cei_100k, tier in points:
    px = left + (asking_millions - xmin) / (xmax - xmin) * (right - left)
    py = bottom - (night - ymin) / (ymax - ymin) * (bottom - top)
    fill = ACCENT if label == "Morretes 2Q" else (WARN if label == "Centro 2Q" else ACCENT_2)
    radius = 9 if tier == "A" else 7
    dx, dy = 12, -12
    if label == "Centro 1Q":
        dy = 22
    if label == "Meia Praia 3Q":
        dx = -12
    anchor = "end" if dx < 0 else "start"
    parts += [
        circle(px, py, radius, fill),
        text(px + dx, py + dy, label, "value", anchor),
        text(px + dx, py + dy + 16, f"R$ {cei_100k:.1f}/R$100 mil".replace(".", ","), "small", anchor),
    ]
parts += [
    rect(610, 95, 300, 42, LIGHT, 6),
    text(625, 112, "Morretes 2Q: maior CEI entre os", "small"),
    text(625, 130, "candidatos robustos do screen final.", "small"),
    text(910, 585, "CEI = preço-noite exibido / preço-pedido.", "small", "end"),
]
save("02_matriz_investimento.svg", parts)

# 3) Temporal robustness: use one informative 13-day window only.
values = temporal["principal_window_07_to_20"]["standardized_net_transition"]
selected = [
    ("Morretes 2Q", values["Morretes 2Q"]),
    ("Meia Praia 2Q", values["Meia Praia 2Q"]),
    ("Centro 2Q", values["Centro 2Q"]),
]
width, height = 980, 500
parts = svg_start(width, height, "Proxy temporal: transição líquida de calendário padronizada por lead-time")
parts += [
    text(55, 48, "Teste de robustez temporal — janela 07→20 jan (13 dias)", "title"),
    text(55, 74, "Transição líquida do estado do calendário, padronizada por lead-time. Não é ocupação.", "sub"),
]
x0, max_width, max_value = 220, 650, 0.14
for index, (label, value) in enumerate(selected):
    y = 125 + index * 82
    bar_width = max_width * value / max_value
    parts += [
        text(195, y + 28, label, "label", "end"),
        rect(x0, y, bar_width, 40, ACCENT if label == "Morretes 2Q" else ACCENT_2),
        text(x0 + bar_width + 12, y + 27, f"{value * 100:.1f}%".replace(".", ","), "value"),
    ]
parts += [
    rect(55, 380, 870, 78, LIGHT, 7),
    text(75, 404, "Leitura: Morretes 2Q tem a menor transição líquida entre os 2Q comparados (7,1% vs 11,3% e 12,2%).", "label"),
    text(75, 428, "Esse sinal fraco não favorece Morretes, mas desaparecimento de data não comprova reserva e o proxy não mede", "small"),
    text(75, 447, "o diferencial de ocupação de >20% que inverteria a recomendação. Por isso permanece evidência suplementar.", "small"),
]
save("03_proxy_temporal.svg", parts)

# 4) Cluster-bootstrap uncertainty around capital efficiency.
bootstrap = robustness["cluster_bootstrap"]
comparison = robustness["comparisons"]
selected = []
for label in ["Morretes 2Q", "Centro 2Q", "Meia Praia 2Q"]:
    row = bootstrap[label]
    selected.append(
        (
            label,
            100000 * row["cei_point"],
            100000 * row["cei_bootstrap_95pct"][0],
            100000 * row["cei_bootstrap_95pct"][1],
        )
    )

width, height = 980, 560
parts = svg_start(width, height, "Robustez da decisão: bootstrap da eficiência de capital")
parts += [
    text(55, 48, "Robustez da decisão — 4.000 reamostragens", "title"),
    text(
        55,
        74,
        "Intervalos percentis com clusters de proprietário (Airbnb) e anunciante (VivaReal).",
        "sub",
    ),
]
left, right, top, bottom = 245, 900, 115, 380
xmin, xmax = 25, 75
for value in [25, 35, 45, 55, 65, 75]:
    px = left + (value - xmin) / (xmax - xmin) * (right - left)
    parts += [
        line(px, top, px, bottom),
        text(px, bottom + 24, str(value), "small", "middle"),
    ]
parts.append(
    text(
        (left + right) / 2,
        435,
        "R$ de preço-noite exibido por R$100 mil de preço-pedido",
        "label",
        "middle",
    )
)
for index, (label, point, low, high) in enumerate(selected):
    y = 155 + index * 88
    x_low = left + (low - xmin) / (xmax - xmin) * (right - left)
    x_high = left + (high - xmin) / (xmax - xmin) * (right - left)
    x_point = left + (point - xmin) / (xmax - xmin) * (right - left)
    fill = ACCENT if label == "Morretes 2Q" else ACCENT_2
    parts += [
        text(220, y + 5, label, "label", "end"),
        line(x_low, y, x_high, y, fill, 5),
        line(x_low, y - 9, x_low, y + 9, fill, 2),
        line(x_high, y - 9, x_high, y + 9, fill, 2),
        circle(x_point, y, 8, fill),
        text(
            x_high + 10,
            y + 5,
            f"{point:.1f} [{low:.1f}; {high:.1f}]".replace(".", ","),
            "small",
        ),
    ]

win_share = 100 * comparison["morretes_cei_above_centro_share"]
threshold = comparison["gross_break_even_occupancy_ratio_morretes_to_centro"]
threshold_low = 100 * threshold["bootstrap_95pct"][0]
threshold_high = 100 * threshold["bootstrap_95pct"][1]
parts += [
    rect(55, 465, 870, 68, LIGHT, 7),
    text(
        75,
        490,
        f"Morretes supera Centro em {win_share:.1f}% das reamostragens condicionais.".replace(
            ".", ","
        ),
        "label",
    ),
    text(
        75,
        515,
        (
            "Limiar bruto M/C: 80,0%; intervalo bootstrap "
            f"{threshold_low:.1f}%–{threshold_high:.1f}%. Não é probabilidade de superioridade real."
        ).replace(".", ","),
        "small",
    ),
]
save("04_robustez_decisao.svg", parts)

print("Generated figures:")
for path in sorted(OUT.glob("*.svg")):
    print("-", path.relative_to(ROOT))
