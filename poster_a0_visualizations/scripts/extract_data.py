"""Extract the model outputs used in the poster figures from the thesis workbooks.

Usage
-----
    python extract_data.py --results FINAL_THESIS_RESULTS.xlsx --out ../data

Only FINAL_THESIS_RESULTS.xlsx is read. HASIL_SIMULASI_VENSIM.xlsx is not used:
its numeric cells were damaged by a locale conversion on export (decimals read
as thousands separators, some cells turned into dates/times), so its values
cannot be trusted without re-exporting from Vensim.

Every value is written at full precision; rounding happens only in the labels
drawn by make_figures.py.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import openpyxl

SCEN = ["S1", "S2", "S3", "S4 USD6", "S4 USD10", "S4 USD15", "S4 USD20", "S4 USD35"]

# Rows in sheet "1A Tabel tesis" (column A label -> short key).
TABLE_ROWS = {
    "Deforestasi kumulatif 2025-2086 (ha)": "defor_cum_ha",
    "Deforestasi dihindari vs S1 (ha, 2025-2086)": "defor_avoided_vs_s1_ha",
    "Emisi dihindari / mitigasi fisik vs S1 (tCO2e, 2025-2086)": "emis_avoided_vs_s1_tco2e",
    "Hutan 2087 (ha)": "forest_2087_ha",
    "Kebutuhan minimum LPHD 2030-55 (Rp miliar/th)": "lphd_min_need_rp_bn_yr",
    "Belanja LPHD 2030-55 (Rp miliar/th)": "lphd_spend_rp_bn_yr",
    "Intensitas perlindungan 2030-55": "protection_intensity",
    "Pendapatan bersih RT bergantung 2030-55 (Rp/RT/th)": "hh_net_income_rp",
    "Pendapatan program per RT 2030-55 (Rp/RT/th)": "hh_programme_income_rp",
    "Kehilangan akses per RT 2030-55 (Rp/RT/th, asumsi)": "hh_access_loss_rp",
    "NPV proyek 10% (Rp miliar; cakupan biaya model)": "npv_project_rp_bn",
}

GRID_COLS = {
    "harga USD": "price_usd",
    "NPV proyek": "npv_project_rp_bn",
    "NPV mitra": "npv_partner_rp_bn",
    "cakupan minimum 2030-55": "coverage_min_share",
    "deforestasi dihindari S4-S3 (ha)": "defor_avoided_s4_s3_ha",
}


def rows(ws):
    return [r for r in ws.iter_rows(values_only=True) if any(c is not None for c in r)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.load_workbook(a.results, read_only=True, data_only=True)

    # 1. Scenario table (long format).
    tab = rows(wb["1A Tabel tesis"])
    header = list(tab[0])
    assert header[1:] == SCEN, header
    with open(a.out / "scenario_table.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["indicator", "label_in_workbook", "scenario", "value"])
        for r in tab[1:]:
            if r[0] in TABLE_ROWS:
                for s, v in zip(SCEN, r[1:]):
                    if v is not None:
                        w.writerow([TABLE_ROWS[r[0]], r[0], s, repr(float(v))])

    # 2. Stepwise contrasts (S2-S1, S3-S2, S4-S3, S4-S1) for avoided deforestation.
    comp = rows(wb["2 Perbandingan wajib"])
    with open(a.out / "stepwise_contrasts.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["contrast", "price_usd", "defor_avoided_ha", "emis_avoided_tco2e"])
        for r in comp[1:]:
            w.writerow([r[0], "" if r[9] is None else r[9], repr(float(r[1])), repr(float(r[2]))])

    # 3. Break-even prices.
    with open(a.out / "break_even_prices.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item", "usd_per_tco2e"])
        for r in rows(wb["3 Harga impas"])[1:]:
            w.writerow([r[0], "" if r[1] is None else repr(float(r[1]))])

    # 4. Price grid USD1-40 (one deterministic run per whole-dollar price).
    grid = rows(wb["4 Grid harga & ambang"])
    gh = list(grid[0])
    idx = {GRID_COLS[c]: gh.index(c) for c in GRID_COLS}
    with open(a.out / "price_grid.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(list(idx))
        for r in grid[1:]:
            w.writerow([repr(float(r[i])) for i in idx.values()])

    print("wrote", *sorted(p.name for p in a.out.glob("*.csv")))


if __name__ == "__main__":
    main()
