from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "ai-log" / ".parts"
OUT = ROOT / "ai-log" / "01_ai_log.md"

header = """# AI Log — prompts principais e respostas literais

> As respostas do **Claude Code** abaixo foram transcritas literalmente do arquivo de sessão local (`e34984bc-5c7a-4a4b-993e-a3a502f49cf2.jsonl`). Não foram resumidas, reescritas ou corrigidas neste documento.
>
> Foram removidos apenas itens sem relação com o desenvolvimento analítico: saudações, comandos locais, tentativas iniciais de localização dos arquivos, retries e erros de infraestrutura/API.
>
> Quando uma conclusão antiga aparece numa resposta literal e depois é corrigida, ela permanece aqui exatamente como ocorreu; a correção aparece no ciclo seguinte.

"""

sections = [
    ("Prompt 1 — framing e auditoria semântica", "01_prompt1.txt", True),
    ("Claude — Checkpoint 1 (resposta literal)", "02_claude1.txt", False),
    ("Prompt 2 — refinamentos pré-ranking + Cycle 2", "03_prompt2.txt", True),
    ("Claude — Checkpoint 2 (resposta literal)", "04_claude2.txt", False),
    ("Prompt 3 — correção metodológica + robustez", "05_prompt3.txt", True),
    ("Claude — Checkpoint 3 (resposta literal)", "06_claude3.txt", False),
    ("Prompt 4 — Cycle 4 / freeze analítico", "07_prompt4.txt", True),
    ("Claude — início do Cycle 4 (resposta literal)", "08_claude4_start.txt", False),
]

chunks = [header]
for title, filename, as_code in sections:
    body = (PARTS / filename).read_text(encoding="utf-8").rstrip()
    chunks.append("\n---\n\n## " + title + "\n\n")
    if as_code:
        chunks.append("```text\n" + body + "\n```\n")
    else:
        chunks.append(body + "\n")

chunks.append("\n> **Transição editorial:** a execução do Cycle 4 foi interrompida pela infraestrutura antes dos cálculos. Erros de API e retries foram omitidos porque não alteraram o raciocínio. O estado foi preservado e a execução continuou no Antigravity.\n")

for title, filename, as_code in [
    ("Antigravity — Checkpoint 4 (resposta literal)", "09_antigravity_c4.txt", False),
    ("Prompt 5 — auditoria pós-C4 / C4.1", "10_prompt_c41.txt", True),
    ("Antigravity — C4.1 FINAL PATCH (resposta literal)", "11_antigravity_c41.txt", False),
]:
    body = (PARTS / filename).read_text(encoding="utf-8").rstrip()
    chunks.append("\n---\n\n## " + title + "\n\n")
    if as_code:
        chunks.append("```text\n" + body + "\n```\n")
    else:
        chunks.append(body + "\n")

OUT.write_text("".join(chunks), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")