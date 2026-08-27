from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "analysis" / "temporal_proxy_results.json"
FOCUS = [("Morretes", 2), ("Centro", 1), ("Centro", 2), ("Meia Praia", 2), ("Meia Praia", 3)]
BINS = ["0-14", "15-30", "31-60", "61-90"]


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name, low_memory=False)


def strip_accents(value):
    if pd.isna(value):
        return None
    return unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower().strip()


def canon_suburb(value):
    s = strip_accents(value)
    if not s:
        return None
    if "meia praia" in s:
        return "Meia Praia"
    if s == "centro":
        return "Centro"
    if "morretes" in s:
        return "Morretes"
    if "tabuleiro" in s or "taboleiro" in s:
        return "Tabuleiro"
    return str(value).strip()


def lead_bin(days: int):
    if days < 0:
        return None
    if days <= 14:
        return "0-14"
    if days <= 30:
        return "15-30"
    if days <= 60:
        return "31-60"
    if days <= 90:
        return "61-90"
    return "91+"


def seg_label(neighborhood: str, bedrooms: int) -> str:
    return f"{neighborhood} {bedrooms}Q"


details = load("Details_Itapema.csv")
mesh = load("Mesh_Ids_Data_Itapema.csv")
price = load("Price_AV_Itapema.csv")

price["cap_day"] = pd.to_datetime(price["aquisition_date"], errors="coerce").dt.normalize()
price["stay"] = pd.to_datetime(price["date"], errors="coerce").dt.normalize()

apartments = details[details["listing_type"].astype(str).str.lower().eq("apartamento")].merge(
    mesh[["airbnb_listing_id", "suburb"]], on="airbnb_listing_id", how="left"
)
apartments["bedrooms"] = pd.to_numeric(apartments["number_of_bedrooms"], errors="coerce").clip(upper=4)
apartments["suburb_canon"] = apartments["suburb"].map(canon_suburb)

segment_by_listing = {}
for neighborhood, bedrooms in FOCUS:
    ids = apartments[
        (apartments["suburb_canon"] == neighborhood) & (apartments["bedrooms"] == bedrooms)
    ]["airbnb_listing_id"]
    for listing_id in ids:
        segment_by_listing[listing_id] = seg_label(neighborhood, bedrooms)

snapshots = [pd.Timestamp(x) for x in sorted(price["cap_day"].dropna().unique())]
if len(snapshots) != 3:
    raise RuntimeError(f"Expected 3 acquisition snapshots, found {len(snapshots)}: {snapshots}")


def transition(early: pd.Timestamp, late: pd.Timestamp):
    early_rows = price[price["cap_day"] == early]
    late_rows = price[price["cap_day"] == late]

    listings_in_both = set(early_rows["airbnb_listing_id"]) & set(late_rows["airbnb_listing_id"])
    common_start = max(early_rows["stay"].min(), late_rows["stay"].min())
    common_end = min(early_rows["stay"].max(), late_rows["stay"].max())

    early_rows = early_rows[
        early_rows["airbnb_listing_id"].isin(listings_in_both)
        & early_rows["stay"].between(common_start, common_end)
    ]
    late_rows = late_rows[
        late_rows["airbnb_listing_id"].isin(listings_in_both)
        & late_rows["stay"].between(common_start, common_end)
    ]

    early_keys = set(zip(early_rows["airbnb_listing_id"], early_rows["stay"]))
    late_keys = set(zip(late_rows["airbnb_listing_id"], late_rows["stay"]))

    records = []
    for listing_id, stay in early_keys | late_keys:
        segment = segment_by_listing.get(listing_id)
        if segment is None:
            continue
        bucket = lead_bin((stay - early).days)
        if bucket not in BINS:
            continue
        records.append(
            (
                segment,
                bucket,
                (listing_id, stay) in early_keys,
                (listing_id, stay) in late_keys,
            )
        )

    frame = pd.DataFrame(records, columns=["segment", "lead_bin", "present_early", "present_late"])
    rows = []
    for (segment, bucket), group in frame.groupby(["segment", "lead_bin"]):
        present_early = int(group["present_early"].sum())
        present_to_absent = int((group["present_early"] & ~group["present_late"]).sum())
        absent_to_present = int((~group["present_early"] & group["present_late"]).sum())
        rows.append(
            {
                "segment": segment,
                "lead_bin": bucket,
                "present_early": present_early,
                "present_to_absent": present_to_absent,
                "absent_to_present": absent_to_present,
                "net_rate": (present_to_absent - absent_to_present) / present_early if present_early else None,
            }
        )

    grouped = pd.DataFrame(rows)
    weights = grouped.groupby("lead_bin")["present_early"].sum()
    weights = weights / weights.sum()

    standardized = {}
    for segment, segment_rows in grouped.groupby("segment"):
        segment_rows = segment_rows.set_index("lead_bin")
        numerator = 0.0
        weight_used = 0.0
        for bucket in BINS:
            if bucket in segment_rows.index and segment_rows.loc[bucket, "present_early"] > 0:
                weight = float(weights[bucket])
                numerator += weight * float(segment_rows.loc[bucket, "net_rate"])
                weight_used += weight
        standardized[segment] = round(numerator / weight_used, 3) if weight_used else None

    return {
        "gap_days": int((late - early).days),
        "standardized_net_transition": standardized,
        "by_lead_bin": grouped.to_dict(orient="records"),
    }


short_window = transition(snapshots[0], snapshots[1])
principal_window = transition(snapshots[1], snapshots[2])

result = {
    "definition": "lead-time-standardized net calendar transition = (present-to-absent - absent-to-present) / present_early",
    "interpretation": "supplementary calendar-state signal only; not booking, occupancy, or realized revenue",
    "short_window_06_to_07": short_window,
    "principal_window_07_to_20": principal_window,
    "decision_note": (
        "In the 13-day window, Morretes 2Q has a lower standardized net transition than Centro 2Q "
        "and Meia Praia 2Q. This weak signal does not favor Morretes, but it cannot quantify the >20% "
        "occupancy reversal condition."
    ),
}

OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("TEMPORAL ROBUSTNESS TEST")
print("=" * 72)
print("Principal window 07->20 Jan (13 days)")
for segment, value in principal_window["standardized_net_transition"].items():
    print(f"{segment:16s}: {100 * value:5.1f}%")
print("Interpretation: calendar-state signal only; not occupancy or bookings.")
print(f"Saved: {OUT.relative_to(ROOT)}")
