from __future__ import annotations

import json
import math
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "analysis" / "final_results.json"


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name, low_memory=False)


def strip_accents(value) -> str:
    if pd.isna(value):
        return ""
    s = unicodedata.normalize("NFKD", str(value))
    return "".join(c for c in s if not unicodedata.combining(c)).strip().lower()


def canon_suburb(value):
    """Canonicalize decision neighborhoods while preserving other valid Mesh labels.

    Q1/Q2/Q4 explicitly filter the named candidate neighborhoods. Q3 uses the full
    apartment+priced+located sample, so non-candidate Mesh neighborhoods must not be
    silently discarded.
    """
    s = strip_accents(value)
    if not s:
        return None
    if "meia praia" in s:
        return "Meia Praia"
    if "morretes" in s:
        return "Morretes"
    if "tabuleiro" in s or "taboleiro" in s:
        return "Tabuleiro"
    if s == "centro" or " centro" in f" {s}":
        return "Centro"
    if "canto da praia" in s:
        return "Canto da Praia"
    if "alto sao bento" in s:
        return "Alto Sao Bento"
    if "casa branca" in s:
        return "Casa Branca"
    # Keep other observed location labels for the Q3 control instead of deleting rows.
    return str(value).strip()


def as_bool(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower().isin(["true", "1", "yes", "sim"])


def fmt(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return None if np.isnan(v) else float(v)
    return v


# 1. Load and build one-row-per-Airbnb-listing frame
details = load("Details_Itapema.csv")
hosts = load("Hosts_ids_Itapema.csv")
mesh = load("Mesh_Ids_Data_Itapema.csv")
price = load("Price_AV_Itapema.csv")
viva = load("VivaReal_Itapema.csv")

price["price"] = pd.to_numeric(price["price"], errors="coerce")
listing_price = price.groupby("airbnb_listing_id", as_index=False)["price"].median()
listing_price = listing_price.rename(columns={"price": "displayed_nightly_price"})

hosts1 = hosts.drop_duplicates("owner_id", keep="first").copy()
host_cols = [c for c in ["owner_id", "is_superhost"] if c in hosts1.columns]

air = details.merge(mesh[["airbnb_listing_id", "suburb"]], on="airbnb_listing_id", how="left")
air = air.merge(listing_price, on="airbnb_listing_id", how="inner")
if host_cols:
    air = air.merge(hosts1[host_cols], on="owner_id", how="left")

air = air[air["listing_type"].astype(str).str.lower().eq("apartamento")].copy()
air["suburb_canon"] = air["suburb"].map(canon_suburb)
air["bedrooms"] = pd.to_numeric(air["number_of_bedrooms"], errors="coerce")
air["bed_group"] = air["bedrooms"].clip(upper=4)
air["bathrooms"] = pd.to_numeric(air["number_of_bathrooms"], errors="coerce")
air["guests"] = pd.to_numeric(air["number_of_guests"], errors="coerce")
air["reviews"] = pd.to_numeric(air["number_of_reviews"], errors="coerce")
air["professional"] = as_bool(air["is_professional"]).astype(int)
air["instant_book"] = as_bool(air["can_instant_book"]).astype(int)
if "is_superhost" in air.columns:
    air["superhost"] = as_bool(air["is_superhost"]).astype(int)
else:
    air["superhost"] = 0

# 2. Acquisition frame — valid apartment asking prices only
v = viva.drop_duplicates("listing_id", keep="first").copy()
v = v[v["listing_type"].astype(str).str.lower().eq("apartamento")].copy()
v["sale_price"] = pd.to_numeric(v["sale_price"], errors="coerce")
v["usable_area"] = pd.to_numeric(v["usable_area"], errors="coerce")
v["bedrooms_n"] = pd.to_numeric(v["bedrooms"], errors="coerce")
v["bed_group"] = v["bedrooms_n"].clip(upper=4)
v["suburb_canon"] = v["suburb"].map(canon_suburb)
v["ppm2"] = v["sale_price"] / v["usable_area"]
v["valid"] = (
    v["sale_price"].ge(50_000)
    & v["usable_area"].gt(0)
    & v["usable_area"].le(1000)
    & v["ppm2"].ge(1000)
    & v["ppm2"].le(60_000)
)
v = v[v["valid"]].copy()

# 3. Q1 — profile: operating potential vs capital efficiency
q1_air = (
    air.dropna(subset=["bed_group", "displayed_nightly_price"])
    .groupby("bed_group")
    .agg(n=("airbnb_listing_id", "nunique"), night=("displayed_nightly_price", "median"))
)
q1_viva = (
    v.dropna(subset=["bed_group", "sale_price"])
    .groupby("bed_group")
    .agg(viva_n=("listing_id", "nunique"), asking=("sale_price", "median"))
)
q1 = q1_air.join(q1_viva, how="inner")
q1["cei"] = q1["night"] / q1["asking"]

# 4. Q2 — location overall and within bedroom mix
focus = ["Meia Praia", "Centro", "Morretes", "Tabuleiro"]
q2 = (
    air[air["suburb_canon"].isin(focus)]
    .groupby("suburb_canon")
    .agg(n=("airbnb_listing_id", "nunique"), night=("displayed_nightly_price", "median"))
    .sort_values("night", ascending=False)
)
q2_mix = (
    air[air["suburb_canon"].isin(["Meia Praia", "Centro", "Morretes"])]
    .dropna(subset=["bed_group"])
    .groupby(["suburb_canon", "bed_group"])
    .agg(n=("airbnb_listing_id", "nunique"), night=("displayed_nightly_price", "median"))
)

# 5. Q4 — candidate comparable segments
air_seg = (
    air.dropna(subset=["suburb_canon", "bed_group"])
    .groupby(["suburb_canon", "bed_group"])
    .agg(air_n=("airbnb_listing_id", "nunique"), night=("displayed_nightly_price", "median"))
)
viva_seg = (
    v.dropna(subset=["suburb_canon", "bed_group"])
    .groupby(["suburb_canon", "bed_group"])
    .agg(viva_n=("listing_id", "nunique"), asking=("sale_price", "median"), area=("usable_area", "median"), ppm2=("ppm2", "median"))
)
segments = air_seg.join(viva_seg, how="inner").reset_index()
segments["cei"] = segments["night"] / segments["asking"]
segments["ce90"] = segments["cei"] * 90 * 0.55
segments["tier"] = np.where(
    (segments["air_n"] >= 30) & (segments["viva_n"] >= 30),
    "A",
    np.where((segments["air_n"] >= 15) & (segments["viva_n"] >= 15), "B", "exploratory"),
)

focus_candidates = [("Morretes", 2), ("Centro", 1), ("Centro", 2), ("Meia Praia", 2), ("Meia Praia", 3)]
candidates = segments[
    segments.apply(lambda r: (r["suburb_canon"], int(r["bed_group"])) in focus_candidates, axis=1)
].sort_values("cei", ascending=False)

# 6. Q3 — associative log-price model, owner-clustered uncertainty
# Use the full apartment + priced + located sample. This is the 911-listing frame
# independently reproduced during the hackathon; candidate-neighborhood filters are
# used for Q2/Q4, not to delete controls from Q3.
reg = air[air["suburb_canon"].notna()].copy()
reg = reg[
    reg["displayed_nightly_price"].gt(0)
    & reg["bedrooms"].notna()
    & reg["bathrooms"].notna()
    & reg["guests"].notna()
    & reg["owner_id"].notna()
].copy()
reg["log_price"] = np.log(reg["displayed_nightly_price"])
reg["log_reviews"] = np.log1p(reg["reviews"].fillna(0))

formula1 = "log_price ~ bedrooms + bathrooms + guests + C(suburb_canon, Treatment(reference='Meia Praia'))"
formula2 = formula1 + " + professional + superhost + instant_book + log_reviews"

m1 = smf.ols(formula1, data=reg).fit(cov_type="cluster", cov_kwds={"groups": reg["owner_id"]})
m2 = smf.ols(formula2, data=reg).fit(cov_type="cluster", cov_kwds={"groups": reg["owner_id"]})


def pct(beta: float) -> float:
    return 100 * (math.exp(beta) - 1)


coef = {}
for key, label in [
    ("bedrooms", "bedrooms"),
    ("bathrooms", "bathrooms"),
    ("guests", "guests"),
    ("professional", "professional"),
    ("superhost", "superhost"),
    ("instant_book", "instant_book"),
    ("log_reviews", "log_reviews"),
]:
    if key in m2.params:
        coef[label] = {"beta": float(m2.params[key]), "pct_assoc": pct(float(m2.params[key])), "pvalue": float(m2.pvalues[key])}


def nb_key(name: str) -> str:
    return f"C(suburb_canon, Treatment(reference='Meia Praia'))[T.{name}]"


b_centro = float(m2.params.get(nb_key("Centro"), 0.0))
b_morretes = float(m2.params.get(nb_key("Morretes"), 0.0))
contrasts = {
    "Centro_vs_Meia_Praia": pct(b_centro),
    "Morretes_vs_Meia_Praia": pct(b_morretes),
    "Centro_vs_Morretes": pct(b_centro - b_morretes),
    "Meia_Praia_vs_Morretes": pct(-b_morretes),
}

# 7. Store readable, machine-checkable results
result = {
    "semantics": {
        "price_av": "median displayed nightly price; not realized revenue or observed occupancy",
        "viva_price": "asking price; not transaction price",
        "comparison": "segment-level; no physical Airbnb-VivaReal property match",
    },
    "coverage": {
        "details_listings": int(details["airbnb_listing_id"].nunique()),
        "price_av_listings": int(price["airbnb_listing_id"].nunique()),
    },
    "q1_profile": {str(int(idx)): {k: fmt(vv) for k, vv in row.items()} for idx, row in q1.to_dict("index").items()},
    "q2_location": {str(idx): {k: fmt(vv) for k, vv in row.items()} for idx, row in q2.to_dict("index").items()},
    "q4_candidates": candidates.to_dict(orient="records"),
    "q3": {
        "n": int(m2.nobs),
        "r2_structural": float(m1.rsquared),
        "r2_with_operational": float(m2.rsquared),
        "coefficients": coef,
        "neighborhood_contrasts_pct": contrasts,
        "interpretation": "associative, not causal",
    },
    "reversal": {
        "primary": "Morretes 2Q",
        "alternative": "Centro 2Q",
        "condition": "Morretes operating occupancy >20% below Centro reverses the CEI comparison",
        "observed_in_data": False,
    },
}

OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=fmt), encoding="utf-8")

print("FINAL ANALYSIS")
print("=" * 72)
print("Q1 profile")
print(q1.round(6).to_string())
print("\nQ2 location")
print(q2.round(2).to_string())
print("\nFinal candidates")
print(candidates[["suburb_canon", "bed_group", "tier", "air_n", "night", "viva_n", "asking", "cei", "ce90"]].round(6).to_string(index=False))
print("\nQ3")
print(f"n={int(m2.nobs)} R2 structural={m1.rsquared:.3f} R2 full={m2.rsquared:.3f}")
for name, vals in coef.items():
    print(f"{name:14s} beta={vals['beta']:+.4f} assoc={vals['pct_assoc']:+.1f}% p={vals['pvalue']:.4g}")
print("contrasts:", {k: round(v, 1) for k, v in contrasts.items()})
print(f"\nSaved: {OUT.relative_to(ROOT)}")
