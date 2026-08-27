from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "analysis" / "decision_robustness_results.json"
BUY_BOX_OUT = ROOT / "analysis" / "buy_box_morretes_2q.csv"

SEGMENTS = [
    ("Morretes", 2),
    ("Centro", 1),
    ("Centro", 2),
    ("Meia Praia", 2),
    ("Meia Praia", 3),
]
BOOTSTRAP_ITERATIONS = 4_000
RANDOM_SEED = 2026
CONDO_FEE_RANGE = (80.0, 5_000.0)
YEARLY_IPTU_RANGE = (100.0, 30_000.0)


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name, low_memory=False)


def strip_accents(value) -> str:
    if pd.isna(value):
        return ""
    text = unicodedata.normalize("NFKD", str(value))
    return "".join(char for char in text if not unicodedata.combining(char)).strip().lower()


def canon_suburb(value):
    text = strip_accents(value)
    if not text:
        return None
    if "meia praia" in text:
        return "Meia Praia"
    if "morretes" in text:
        return "Morretes"
    if text == "centro" or " centro" in f" {text}":
        return "Centro"
    if "tabuleiro" in text or "taboleiro" in text:
        return "Tabuleiro"
    return str(value).strip()


def segment_label(neighborhood: str, bedrooms: int | float) -> str:
    return f"{neighborhood} {int(bedrooms)}Q"


def build_airbnb() -> tuple[pd.DataFrame, pd.DataFrame]:
    details = load("Details_Itapema.csv")
    mesh = load("Mesh_Ids_Data_Itapema.csv")
    price = load("Price_AV_Itapema.csv")

    price["price"] = pd.to_numeric(price["price"], errors="coerce")
    listing_price = (
        price.groupby("airbnb_listing_id", as_index=False)["price"]
        .median()
        .rename(columns={"price": "displayed_nightly_price"})
    )

    all_air = details.merge(
        mesh[["airbnb_listing_id", "suburb"]], on="airbnb_listing_id", how="left"
    )
    all_air = all_air[
        all_air["listing_type"].astype(str).str.lower().eq("apartamento")
    ].copy()
    all_air["suburb_canon"] = all_air["suburb"].map(canon_suburb)
    all_air["bed_group"] = pd.to_numeric(
        all_air["number_of_bedrooms"], errors="coerce"
    ).clip(upper=4)
    all_air["segment"] = all_air.apply(
        lambda row: segment_label(row["suburb_canon"], row["bed_group"])
        if pd.notna(row["suburb_canon"]) and pd.notna(row["bed_group"])
        else None,
        axis=1,
    )

    priced = all_air.merge(listing_price, on="airbnb_listing_id", how="inner")
    priced = priced[
        priced.apply(
            lambda row: (row["suburb_canon"], int(row["bed_group"])) in SEGMENTS
            if pd.notna(row["suburb_canon"]) and pd.notna(row["bed_group"])
            else False,
            axis=1,
        )
    ].copy()
    priced["owner_cluster"] = priced["owner_id"].astype("string")
    missing_owner = priced["owner_cluster"].isna()
    priced.loc[missing_owner, "owner_cluster"] = (
        "listing:" + priced.loc[missing_owner, "airbnb_listing_id"].astype(str)
    )
    return all_air, priced


def build_vivareal() -> pd.DataFrame:
    viva = load("VivaReal_Itapema.csv").drop_duplicates("listing_id", keep="first").copy()
    for column in [
        "sale_price",
        "usable_area",
        "bedrooms",
        "monthly_condo_fee",
        "yearly_iptu",
        "parking_spaces",
    ]:
        viva[column] = pd.to_numeric(viva[column], errors="coerce")

    viva = viva[
        viva["listing_type"].astype(str).str.lower().eq("apartamento")
    ].copy()
    viva["suburb_canon"] = viva["suburb"].map(canon_suburb)
    viva["bed_group"] = viva["bedrooms"].clip(upper=4)
    viva["price_per_m2"] = viva["sale_price"] / viva["usable_area"]
    viva = viva[
        viva["sale_price"].ge(50_000)
        & viva["usable_area"].gt(0)
        & viva["usable_area"].le(1_000)
        & viva["price_per_m2"].between(1_000, 60_000)
    ].copy()
    viva = viva[
        viva.apply(
            lambda row: (row["suburb_canon"], int(row["bed_group"])) in SEGMENTS
            if pd.notna(row["suburb_canon"]) and pd.notna(row["bed_group"])
            else False,
            axis=1,
        )
    ].copy()
    viva["segment"] = viva.apply(
        lambda row: segment_label(row["suburb_canon"], row["bed_group"]), axis=1
    )
    viva["advertiser_cluster"] = viva["advertiser_name"].astype("string")
    missing_advertiser = viva["advertiser_cluster"].isna()
    viva.loc[missing_advertiser, "advertiser_cluster"] = (
        "listing:" + viva.loc[missing_advertiser, "listing_id"].astype(str)
    )
    return viva


def replicated_median(values: np.ndarray, weights: np.ndarray) -> float:
    positive = weights > 0
    if not positive.any():
        return np.nan
    values = values[positive]
    weights = weights[positive]
    order = np.argsort(values)
    values = values[order]
    cumulative = np.cumsum(weights[order])
    total = int(cumulative[-1])
    lower_position = (total - 1) // 2
    upper_position = total // 2
    lower = values[np.searchsorted(cumulative, lower_position, side="right")]
    upper = values[np.searchsorted(cumulative, upper_position, side="right")]
    return float((lower + upper) / 2)


def bootstrap_segments(
    air: pd.DataFrame, viva: pd.DataFrame
) -> tuple[dict, dict]:
    rng = np.random.default_rng(RANDOM_SEED)
    labels = [segment_label(*segment) for segment in SEGMENTS]

    air_cluster_codes, air_clusters = pd.factorize(air["owner_cluster"], sort=True)
    viva_cluster_codes, viva_clusters = pd.factorize(viva["advertiser_cluster"], sort=True)
    air_values = air["displayed_nightly_price"].to_numpy(dtype=float)
    viva_values = viva["sale_price"].to_numpy(dtype=float)
    air_segment = air["segment"].to_numpy()
    viva_segment = viva["segment"].to_numpy()

    draws = {label: [] for label in labels}
    thresholds = []
    for _ in range(BOOTSTRAP_ITERATIONS):
        air_weights_by_cluster = rng.multinomial(
            len(air_clusters), np.full(len(air_clusters), 1 / len(air_clusters))
        )
        viva_weights_by_cluster = rng.multinomial(
            len(viva_clusters), np.full(len(viva_clusters), 1 / len(viva_clusters))
        )
        air_weights = air_weights_by_cluster[air_cluster_codes]
        viva_weights = viva_weights_by_cluster[viva_cluster_codes]

        iteration = {}
        for label in labels:
            night_mask = air_segment == label
            asking_mask = viva_segment == label
            night = replicated_median(air_values[night_mask], air_weights[night_mask])
            asking = replicated_median(
                viva_values[asking_mask], viva_weights[asking_mask]
            )
            cei = night / asking if night > 0 and asking > 0 else np.nan
            draws[label].append(cei)
            iteration[label] = cei
        thresholds.append(iteration["Centro 2Q"] / iteration["Morretes 2Q"])

    summary = {}
    for label in labels:
        values = np.asarray(draws[label], dtype=float)
        point_air = air.loc[air["segment"].eq(label), "displayed_nightly_price"]
        point_viva = viva.loc[viva["segment"].eq(label), "sale_price"]
        point_cei = float(point_air.median() / point_viva.median())
        low, median, high = np.quantile(values, [0.025, 0.5, 0.975])
        summary[label] = {
            "airbnb_listings": int(point_air.size),
            "airbnb_owner_clusters": int(
                air.loc[air["segment"].eq(label), "owner_cluster"].nunique()
            ),
            "vivareal_listings": int(point_viva.size),
            "vivareal_advertiser_clusters": int(
                viva.loc[viva["segment"].eq(label), "advertiser_cluster"].nunique()
            ),
            "displayed_nightly_price_median": float(point_air.median()),
            "asking_price_median": float(point_viva.median()),
            "cei_point": point_cei,
            "cei_bootstrap_median": float(median),
            "cei_bootstrap_95pct": [float(low), float(high)],
        }

    morretes = np.asarray(draws["Morretes 2Q"])
    centro = np.asarray(draws["Centro 2Q"])
    meia = np.asarray(draws["Meia Praia 2Q"])
    threshold_values = np.asarray(thresholds)
    draw_matrix = np.column_stack([np.asarray(draws[label]) for label in labels])
    row_maximum = np.nanmax(draw_matrix, axis=1)
    comparisons = {
        "interpretation": (
            "conditional stability across cluster-bootstrap resamples; not probability "
            "that a segment is truly superior"
        ),
        "iterations": BOOTSTRAP_ITERATIONS,
        "seed": RANDOM_SEED,
        "morretes_cei_above_centro_share": float(np.mean(morretes > centro)),
        "morretes_cei_above_meia_praia_share": float(np.mean(morretes > meia)),
        "rank1_share_among_final_candidates": {
            label: float(np.mean(draw_matrix[:, index] == row_maximum))
            for index, label in enumerate(labels)
        },
        "gross_break_even_occupancy_ratio_morretes_to_centro": {
            "point": float(
                summary["Centro 2Q"]["cei_point"]
                / summary["Morretes 2Q"]["cei_point"]
            ),
            "bootstrap_median": float(np.median(threshold_values)),
            "bootstrap_95pct": [
                float(np.quantile(threshold_values, 0.025)),
                float(np.quantile(threshold_values, 0.975)),
            ],
        },
    }
    return summary, comparisons


def deduplication_sensitivity(air: pd.DataFrame, viva: pd.DataFrame) -> list[dict]:
    fingerprint = [
        "suburb_canon",
        "bed_group",
        "sale_price",
        "usable_area",
        "parking_spaces",
        "monthly_condo_fee",
        "yearly_iptu",
    ]
    deduped = viva.drop_duplicates(fingerprint, keep="first")
    rows = []
    for neighborhood, bedrooms in SEGMENTS:
        label = segment_label(neighborhood, bedrooms)
        air_segment = air[air["segment"].eq(label)]
        viva_segment = viva[viva["segment"].eq(label)]
        deduped_segment = deduped[deduped["segment"].eq(label)]

        owner_medians = air_segment.groupby("owner_cluster")[
            "displayed_nightly_price"
        ].median()
        advertiser_medians = viva_segment.groupby("advertiser_cluster")[
            "sale_price"
        ].median()
        baseline_asking = float(viva_segment["sale_price"].median())
        signature_asking = float(deduped_segment["sale_price"].median())
        baseline_cei = float(
            air_segment["displayed_nightly_price"].median() / baseline_asking
        )
        rows.append(
            {
                "segment": label,
                "baseline_vivareal_n": int(len(viva_segment)),
                "economic_signature_n": int(len(deduped_segment)),
                "baseline_asking_median": baseline_asking,
                "economic_signature_asking_median": signature_asking,
                "asking_median_change_pct": 100
                * (signature_asking / baseline_asking - 1),
                "baseline_cei": baseline_cei,
                "economic_signature_cei": float(
                    air_segment["displayed_nightly_price"].median()
                    / signature_asking
                ),
                "cluster_equalized_cei": float(
                    owner_medians.median() / advertiser_medians.median()
                ),
            }
        )
    return rows


def coverage_diagnostic(all_air: pd.DataFrame, priced_air: pd.DataFrame) -> list[dict]:
    rows = []
    for neighborhood, bedrooms in SEGMENTS:
        label = segment_label(neighborhood, bedrooms)
        total = all_air[
            all_air["suburb_canon"].eq(neighborhood)
            & all_air["bed_group"].eq(bedrooms)
        ]["airbnb_listing_id"].nunique()
        priced = priced_air[priced_air["segment"].eq(label)][
            "airbnb_listing_id"
        ].nunique()
        rows.append(
            {
                "segment": label,
                "all_apartment_listings": int(total),
                "priced_listings": int(priced),
                "price_coverage_rate": float(priced / total) if total else None,
            }
        )
    return rows


def fixed_cost_assumptions(viva: pd.DataFrame) -> dict:
    assumptions = {}
    for neighborhood, bedrooms in SEGMENTS:
        label = segment_label(neighborhood, bedrooms)
        segment = viva[viva["segment"].eq(label)]
        condo = segment.loc[
            segment["monthly_condo_fee"].between(*CONDO_FEE_RANGE),
            "monthly_condo_fee",
        ]
        iptu = segment.loc[
            segment["yearly_iptu"].between(*YEARLY_IPTU_RANGE), "yearly_iptu"
        ]
        assumptions[label] = {
            "monthly_condo_fee_median_observed": float(condo.median()),
            "monthly_condo_fee_plausible_n": int(condo.size),
            "yearly_iptu_median_observed": float(iptu.median()),
            "yearly_iptu_plausible_n": int(iptu.size),
            "annual_fixed_property_cost": float(12 * condo.median() + iptu.median()),
        }
    return assumptions


def build_scenarios(bootstrap: dict, fixed_costs: dict) -> tuple[list[dict], list[dict]]:
    net_scenarios = []
    for label, values in bootstrap.items():
        for occupancy in [0.40, 0.55, 0.70]:
            for variable_cost_share in [0.20, 0.30, 0.40]:
                gross = values["displayed_nightly_price_median"] * 365 * occupancy
                net = (
                    gross * (1 - variable_cost_share)
                    - fixed_costs[label]["annual_fixed_property_cost"]
                )
                net_scenarios.append(
                    {
                        "segment": label,
                        "occupancy_assumption": occupancy,
                        "variable_operating_cost_share_assumption": variable_cost_share,
                        "annual_gross_mechanical": float(gross),
                        "annual_net_before_financing_and_income_taxes": float(net),
                        "net_yield_on_asking_price": float(
                            net / values["asking_price_median"]
                        ),
                    }
                )

    morretes = bootstrap["Morretes 2Q"]
    centro = bootstrap["Centro 2Q"]
    frontier = []
    for variable_cost_share in [0.20, 0.30, 0.40]:
        for centro_occupancy in [0.40, 0.55, 0.70]:
            centro_net_yield = (
                centro["displayed_nightly_price_median"]
                * 365
                * centro_occupancy
                * (1 - variable_cost_share)
                - fixed_costs["Centro 2Q"]["annual_fixed_property_cost"]
            ) / centro["asking_price_median"]
            required_morretes_occupancy = (
                centro_net_yield * morretes["asking_price_median"]
                + fixed_costs["Morretes 2Q"]["annual_fixed_property_cost"]
            ) / (
                morretes["displayed_nightly_price_median"]
                * 365
                * (1 - variable_cost_share)
            )
            frontier.append(
                {
                    "centro_occupancy_assumption": centro_occupancy,
                    "variable_operating_cost_share_assumption": variable_cost_share,
                    "morretes_break_even_occupancy": float(
                        required_morretes_occupancy
                    ),
                    "morretes_to_centro_occupancy_ratio": float(
                        required_morretes_occupancy / centro_occupancy
                    ),
                }
            )
    return net_scenarios, frontier


def build_buy_box(viva: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    segment = viva[viva["segment"].eq("Morretes 2Q")].copy()
    thresholds = {
        "asking_price_max_p25": float(segment["sale_price"].quantile(0.25)),
        "usable_area_min_p25": float(segment["usable_area"].quantile(0.25)),
        "usable_area_max_p75": float(segment["usable_area"].quantile(0.75)),
        "price_per_m2_max_median": float(segment["price_per_m2"].median()),
        "parking_spaces_min": 1,
        "monthly_condo_fee_plausible_range": list(CONDO_FEE_RANGE),
        "yearly_iptu_plausible_range": list(YEARLY_IPTU_RANGE),
        "asking_price_review_below_p05": float(segment["sale_price"].quantile(0.05)),
        "price_per_m2_review_below_p05": float(segment["price_per_m2"].quantile(0.05)),
    }
    eligible = segment[
        segment["sale_price"].le(thresholds["asking_price_max_p25"])
        & segment["usable_area"].between(
            thresholds["usable_area_min_p25"], thresholds["usable_area_max_p75"]
        )
        & segment["price_per_m2"].le(thresholds["price_per_m2_max_median"])
        & segment["parking_spaces"].ge(thresholds["parking_spaces_min"])
        & segment["monthly_condo_fee"].between(*CONDO_FEE_RANGE)
        & segment["yearly_iptu"].between(*YEARLY_IPTU_RANGE)
    ].copy()

    # This signature is a conservative diversification rule, not proof that two ads
    # refer to the same physical unit. It avoids returning repeated economic profiles.
    eligible["title_key"] = eligible["listing_title"].map(strip_accents)
    eligible = eligible.drop_duplicates(
        ["advertiser_cluster", "title_key"], keep="first"
    )
    economic_signature = [
        "sale_price",
        "usable_area",
        "parking_spaces",
        "monthly_condo_fee",
        "yearly_iptu",
    ]
    eligible = eligible.sort_values(
        ["sale_price", "price_per_m2", "monthly_condo_fee", "yearly_iptu", "listing_id"]
    ).drop_duplicates(economic_signature, keep="first")
    eligible["diligence_flags"] = eligible.apply(
        lambda row: ";".join(
            flag
            for flag, condition in [
                (
                    "preco_pedido_abaixo_p05",
                    row["sale_price"] < thresholds["asking_price_review_below_p05"],
                ),
                (
                    "preco_m2_abaixo_p05",
                    row["price_per_m2"]
                    < thresholds["price_per_m2_review_below_p05"],
                ),
            ]
            if condition
        )
        or "sem_alerta_quantitativo",
        axis=1,
    )
    shortlist = eligible.head(12).copy()
    shortlist.insert(0, "screen_rank", np.arange(1, len(shortlist) + 1))
    shortlist["price_per_m2"] = shortlist["price_per_m2"].round(2)
    for column in [
        "sale_price",
        "usable_area",
        "monthly_condo_fee",
        "yearly_iptu",
        "parking_spaces",
    ]:
        shortlist[column] = shortlist[column].astype(int)
    shortlist["snapshot_note"] = (
        "lead da base de jan-2025; disponibilidade e dados exigem verificacao"
    )
    columns = [
        "screen_rank",
        "listing_id",
        "link_url",
        "listing_title",
        "sale_price",
        "usable_area",
        "price_per_m2",
        "monthly_condo_fee",
        "yearly_iptu",
        "parking_spaces",
        "advertiser_name",
        "aquisition_date",
        "diligence_flags",
        "snapshot_note",
    ]
    shortlist[columns].to_csv(BUY_BOX_OUT, index=False)
    metadata = {
        "definition": (
            "screen of leads, not purchase recommendations; links and listing facts "
            "come from the Jan-2025 dataset and require current verification"
        ),
        "thresholds": thresholds,
        "eligible_before_economic_signature_dedup": int(
            len(
                segment[
                    segment["sale_price"].le(thresholds["asking_price_max_p25"])
                    & segment["usable_area"].between(
                        thresholds["usable_area_min_p25"],
                        thresholds["usable_area_max_p75"],
                    )
                    & segment["price_per_m2"].le(
                        thresholds["price_per_m2_max_median"]
                    )
                    & segment["parking_spaces"].ge(thresholds["parking_spaces_min"])
                    & segment["monthly_condo_fee"].between(*CONDO_FEE_RANGE)
                    & segment["yearly_iptu"].between(*YEARLY_IPTU_RANGE)
                ]
            )
        ),
        "eligible_after_diversification_dedup": int(len(eligible)),
        "shortlist_rows": int(len(shortlist)),
        "output": str(BUY_BOX_OUT.relative_to(ROOT)),
    }
    return metadata, shortlist


def validate_outputs(
    bootstrap: dict,
    comparisons: dict,
    frontier: list[dict],
    buy_box: dict,
    shortlist: pd.DataFrame,
) -> None:
    expected_labels = {segment_label(*segment) for segment in SEGMENTS}
    if set(bootstrap) != expected_labels:
        raise RuntimeError("Bootstrap output does not contain all final candidates")
    rank_shares = comparisons["rank1_share_among_final_candidates"]
    if not np.isclose(sum(rank_shares.values()), 1.0):
        raise RuntimeError("Rank-1 shares do not sum to one")
    if not all(
        0 < values["cei_bootstrap_95pct"][0]
        <= values["cei_bootstrap_median"]
        <= values["cei_bootstrap_95pct"][1]
        for values in bootstrap.values()
    ):
        raise RuntimeError("Invalid bootstrap interval")
    if len(frontier) != 9 or not all(
        0 < row["morretes_break_even_occupancy"] < 1 for row in frontier
    ):
        raise RuntimeError("Invalid net break-even frontier")
    if len(shortlist) != 12 or shortlist["listing_id"].duplicated().any():
        raise RuntimeError("Buy-box shortlist must contain 12 unique leads")
    if not shortlist["monthly_condo_fee"].between(*CONDO_FEE_RANGE).all():
        raise RuntimeError("Buy-box contains implausible condo fee placeholders")
    if not shortlist["yearly_iptu"].between(*YEARLY_IPTU_RANGE).all():
        raise RuntimeError("Buy-box contains implausible IPTU placeholders")
    if shortlist["diligence_flags"].isna().any():
        raise RuntimeError("Buy-box must expose quantitative diligence flags")
    if buy_box["eligible_after_diversification_dedup"] < len(shortlist):
        raise RuntimeError("Buy-box metadata is inconsistent with the shortlist")


def main() -> None:
    all_air, air = build_airbnb()
    viva = build_vivareal()
    bootstrap, comparisons = bootstrap_segments(air, viva)
    deduplication = deduplication_sensitivity(air, viva)
    coverage = coverage_diagnostic(all_air, air)
    fixed_costs = fixed_cost_assumptions(viva)
    scenarios, frontier = build_scenarios(bootstrap, fixed_costs)
    buy_box, shortlist = build_buy_box(viva)
    validate_outputs(bootstrap, comparisons, frontier, buy_box, shortlist)

    result = {
        "semantics": {
            "bootstrap": (
                "sampling uncertainty conditional on observed listings and clusters; "
                "does not correct selection bias, seasonality, or unobserved occupancy"
            ),
            "deduplication": (
                "economic-signature stress test; similar ads can still be distinct units"
            ),
            "net_scenarios": (
                "mechanical assumptions, not forecast or observed return; asking price is "
                "not transaction price"
            ),
            "fixed_costs": (
                "medians among positive observed VivaReal values; coverage is incomplete"
            ),
        },
        "cluster_bootstrap": bootstrap,
        "comparisons": comparisons,
        "price_coverage": coverage,
        "deduplication_sensitivity": deduplication,
        "fixed_cost_assumptions": fixed_costs,
        "net_scenarios": scenarios,
        "net_break_even_frontier": frontier,
        "buy_box": buy_box,
    }
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("DECISION ROBUSTNESS")
    print("=" * 72)
    for label, values in bootstrap.items():
        low, high = values["cei_bootstrap_95pct"]
        print(
            f"{label:16s} CEI={values['cei_point']:.6f} "
            f"cluster-bootstrap 95%=[{low:.6f}, {high:.6f}]"
        )
    print(
        "Morretes 2Q > Centro 2Q in paired bootstrap resamples: "
        f"{100 * comparisons['morretes_cei_above_centro_share']:.1f}%"
    )
    print(
        "Morretes 2Q rank-1 share among final candidates: "
        f"{100 * comparisons['rank1_share_among_final_candidates']['Morretes 2Q']:.1f}%"
    )
    threshold = comparisons["gross_break_even_occupancy_ratio_morretes_to_centro"]
    print(
        "Gross break-even occupancy ratio M/C: "
        f"{threshold['point']:.3f} "
        f"(bootstrap 95% {threshold['bootstrap_95pct'][0]:.3f}-"
        f"{threshold['bootstrap_95pct'][1]:.3f})"
    )
    print(f"Buy-box leads saved: {len(shortlist)}")
    print(f"Saved: {OUT.relative_to(ROOT)}")
    print(f"Saved: {BUY_BOX_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
