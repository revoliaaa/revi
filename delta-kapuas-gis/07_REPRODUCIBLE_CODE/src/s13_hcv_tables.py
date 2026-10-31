"""Transcription of the landscape-level HCV land-cover tables (6 epochs) and
consistency checks.

Sources (text extracted from the PDF reports, supplied by the researcher):
  Kubu         : 'HCV Kubu Lanskap.pdf', Tabel 14 (PDF p. 59-60), total 32,468.00 ha
  Padang Tikar : 'HCV Padang Tikar Lanskap.pdf', Tabel 15 (PDF p. 63-64), total 76,370.00 ha
  Pulau Maya   : 'FINAL_HCV Report_Pulau Maya_24022025.docx.pdf', Tabel 15 (PDF p. 52), total 16,103.00 ha

Pulau Maya: the text extraction lost empty cells for 6 classes. Their years were
reconstructed so that every column sums to 16,103.00 ha (the reconstruction is
unique to within 0.01 ha rounding); those cells carry QUALITY = RECONSTRUCTED_BY_COLUMN_TOTAL.
Check them against the PDF table before publication.

Outputs: 07_REPRODUCIBLE_CODE/inputs/HCV_LANDCOVER_TABLES_FROM_REPORTS.csv (long)
         04_VALIDATION/HCV_TABLE_INTEGRITY.csv
Usage: python -I s13_hcv_tables.py
"""
import numpy as np
import pandas as pd

from common import CODE, HCV_AREA_HA, ROOT

Y = [2000, 2003, 2009, 2014, 2019, 2024]
N = np.nan
# class -> (FOREST_TYPE, IS_NATURAL_FOREST)
CLS = {
    "Hutan Lahan Kering Primer": ("DRYLAND", 1), "Hutan Lahan Kering Sekunder": ("DRYLAND", 1),
    "Hutan Mangrove Primer": ("MANGROVE", 1), "Hutan Mangrove Sekunder": ("MANGROVE", 1),
    "Hutan Rawa Primer": ("PEAT_SWAMP", 1), "Hutan Rawa Sekunder": ("PEAT_SWAMP", 1),
    "Hutan Tanaman": ("PLANTATION_FOREST", 0),
}
T = {
    ("Kubu", "Tabel 14, PDF p.59-60"): {
        "Hutan Lahan Kering Sekunder": [2571.82, 2571.82, 2571.82, 2571.82, 2464.07, 2627.37],
        "Hutan Mangrove Primer": [0, 0, 7.02, 0, 0, 0.00],
        "Hutan Mangrove Sekunder": [9270.07, 9154.41, 9136.94, 12771.02, 7121.58, 10317.27],
        "Hutan Rawa Primer": [763.29, 763.29, 763.29, 763.29, 0.00, 0.00],
        "Hutan Rawa Sekunder": [13745.95, 13676.82, 8595.82, 10819.59, 14184.00, 11731.86],
        "Hutan Tanaman": [0, 0, 0, 1.34, 0, 37.94],
        "Lahan Terbuka": [271.99, 271.99, 18.81, 701.75, 94.63, 167.64],
        "Pemukiman": [0, 0, 442.81, 0, 0.49, 4.57],
        "Perkebunan": [0, 0, 429.09, 871.90, 539.43, 92.64],
        "Pertambangan": [0, 0, 0.00, 0, 9.92, 0],
        "Pertanian Lahan Kering": [103.64, 67.35, 67.35, 63.35, 1036.45, 322.15],
        "Pertanian Lahan Kering Campur": [671.93, 676.80, 432.44, 1105.53, 1156.11, 272.68],
        "Rawa": [0, 0, 0, 0, 0, 12.07],
        "Sawah": [22.86, 78.49, 751.58, 78.49, 0.12, 3.45],
        "Semak Belukar": [0, 0, 10.68, 10.68, 108.02, 140.82],
        "Semak Belukar Rawa": [4640.15, 4773.35, 8534.69, 1385.79, 5350.72, 6504.14],
        "Tambak": [74.32, 101.70, 101.70, 102.51, 72.57, 2.90],
        "Tubuh Air": [331.99, 331.99, 603.98, 1220.94, 329.90, 230.49],
    },
    ("Padang Tikar", "Tabel 15, PDF p.63-64"): {
        "Hutan Lahan Kering Sekunder": [1221.38, 1221.38, 1210.67, 1210.67, 1146.20, 1731.84],
        "Hutan Mangrove Sekunder": [32467.94, 32467.94, 32424.73, 32009.84, 29844.88, 31463.83],
        "Hutan Rawa Sekunder": [30926.74, 30262.00, 29401.80, 27567.15, 23981.91, 24457.68],
        "Lahan Terbuka": [521.56, 541.30, 706.18, 1261.09, 387.85, 375.56],
        "Perkebunan": [0, 0, 1.45, 645.77, 268.83, 1401.75],
        # Row missing from Tabel 15 in 2024; Tabel 16 per-HD Pemukiman 2024 sums to 173.38 ha
        "Pemukiman": [0, 0, 0, 0, 0, 173.50],
        "Pertanian Lahan Kering": [1769.85, 1769.85, 4883.81, 5146.85, 3895.28, 103.15],
        "Pertanian Lahan Kering Campur": [0, 0, 0, 0, 0, 2997.74],
        "Rawa": [30.78, 30.78, 30.78, 30.78, 0, 101.30],
        "Sawah": [3023.79, 3023.79, 1289.72, 1289.72, 3.75, 290.46],
        "Semak Belukar": [88.73, 88.73, 37.46, 27.17, 268.01, 190.50],
        "Semak Belukar Rawa": [6114.02, 6759.01, 6178.18, 6919.78, 16320.98, 12126.60],
        "Tambak": [0, 0, 0, 55.95, 55.95, 50.67],
        "Tubuh Air": [205.21, 205.21, 205.21, 205.21, 196.36, 905.42],
    },
    ("Pulau Maya", "Tabel 15, PDF p.52"): {
        "Hutan Lahan Kering Sekunder": [0, 0, 0, 0, 0, 580.63],
        "Hutan Mangrove Sekunder": [7941.11, 7941.11, 7941.11, 6978.25, 6843.77, 10617.08],
        "Hutan Rawa Sekunder": [3621.93, 3517.76, 3338.68, 2052.21, 1410.76, 742.31],
        "Lahan Terbuka": [21.31, 21.31, 1.99, 238.70, 72.62, 24.51],
        "Pemukiman": [186.72, 186.72, 186.72, 186.72, 0, 10.47],
        "Perkebunan": [0, 0, 0, 0, 0, 51.70],
        "Pertanian Lahan Kering": [0, 0, 0, 0, 144.76, 0],
        "Pertanian Lahan Kering Campur": [0, 0, 0, 0, 0, 10.74],
        "Rawa": [106.48, 106.48, 106.48, 106.48, 0, 211.84],
        "Sawah": [0.19, 0.19, 0.19, 0.19, 0, 0],
        "Semak Belukar": [635.88, 635.88, 655.20, 655.20, 655.19, 74.24],
        "Semak Belukar Rawa": [3422.48, 3526.65, 3705.72, 5718.34, 6714.59, 3531.19],
        "Tubuh Air": [166.90, 166.90, 166.90, 166.90, 261.31, 248.30],
    },
}
PM_RECONSTRUCTED = {"Hutan Lahan Kering Sekunder", "Pemukiman", "Perkebunan", "Pertanian Lahan Kering",
                    "Pertanian Lahan Kering Campur", "Rawa", "Sawah"}


def main():
    rows, integ = [], []
    for (L, src), tab in T.items():
        df = pd.DataFrame(tab, index=Y).T
        tot = df.sum()
        for y in Y:
            integ.append({"LANDSCAPE": L, "YEAR": y, "SUM_OF_CLASSES_HA": round(tot[y], 2),
                          "REPORTED_TOTAL_HA": HCV_AREA_HA[L], "DIFF_HA": round(tot[y] - HCV_AREA_HA[L], 2)})
        for c, vals in tab.items():
            ft, nat = CLS.get(c, ("NONFOREST", 0))
            for y, v in zip(Y, vals):
                q = "TRANSCRIBED"
                if L == "Pulau Maya" and c in PM_RECONSTRUCTED:
                    q = "RECONSTRUCTED_BY_COLUMN_TOTAL"
                if L == "Padang Tikar" and c == "Pemukiman":
                    q = "ADDED_FROM_TABEL16_ROW_MISSING_IN_TABEL15 (Tabel16 sum 173.38; total-closing 173.50)"
                rows.append({"LANDSCAPE": L, "YEAR": y, "HCV_CLASS": c, "IS_FOREST": nat, "FOREST_TYPE": ft,
                             "AREA_HA": v, "DOMAIN": "HCV_STUDY_AREA", "SOURCE_REPORT": src, "QUALITY": q,
                             "VERIFIED": "NO - check against PDF"})
    out = pd.DataFrame(rows)
    out.to_csv(CODE / "inputs" / "HCV_LANDCOVER_TABLES_FROM_REPORTS.csv", index=False)
    ig = pd.DataFrame(integ)
    ig.to_csv(ROOT / "04_VALIDATION" / "HCV_TABLE_INTEGRITY.csv", index=False)
    print(ig.to_string())
    assert ig.DIFF_HA.abs().max() < 0.05, "column sums do not match reported totals"
    f = out[out.IS_FOREST == 1].pivot_table(index=["LANDSCAPE", "FOREST_TYPE"], columns="YEAR", values="AREA_HA", aggfunc="sum")
    print(f.round(0))
    print(out[out.IS_FOREST == 1].pivot_table(index="LANDSCAPE", columns="YEAR", values="AREA_HA", aggfunc="sum").round(0))


if __name__ == "__main__":
    main()
