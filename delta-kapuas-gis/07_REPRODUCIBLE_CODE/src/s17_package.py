"""Quicklook, manifest and ZIP for the final Vensim-integration package.

Usage: python s17_package.py
Output: delta-kapuas-gis/DELTA_KAPUAS_25HD_GIS_FINAL_FOR_VENSIM.zip
"""
import hashlib
import shutil
import zipfile

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Patch

from common import ROOT

P = ROOT / "08_FINAL_FOR_VENSIM"
T = P / "02_THEMATIC_LAYERS"
INK, MUTED = "#0b0b0b", "#8a8984"
BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def quicklook():
    m = gpd.read_file(P / "01_MASTER_SPATIAL" / "DKP_25HD_MASTER_SPATIAL.gpkg", layer="DKP_25HD_MASTER_SPATIAL")
    fig, axs = plt.subplots(1, 4, figsize=(17, 6.2))
    with rasterio.open(T / "DKP_TREECOVER_STATUS_2024_PA.tif") as r:
        st = r.read(1); tr = r.transform
    ext = [tr.c, tr.c + tr.a * st.shape[1], tr.f + tr.e * st.shape[0], tr.f]
    axs[0].imshow(np.where(st == 0, np.nan, st), extent=ext, interpolation="nearest",
                  cmap=ListedColormap(["#e3e2dc", "#1c5cab", "#eb6834"]), vmin=1, vmax=3)
    axs[0].set_title("Status tutupan pohon 2000→2024\n(proksi, BUKAN peta hutan)", loc="left", fontsize=9)
    axs[0].legend(handles=[Patch(color="#e3e2dc", label="tanpa tutupan pohon 2000"),
                           Patch(color="#1c5cab", label="tutupan pohon persisten"),
                           Patch(color="#eb6834", label="gross loss 2001–2024")],
                  loc="upper center", bbox_to_anchor=(0.5, -0.06), fontsize=7, frameon=False)
    with rasterio.open(T / "DKP_TREECOVER_LOSS_YEAR_2001_2024_PA.tif") as r:
        ly = r.read(1).astype(float)
    im = axs[1].imshow(np.where(ly == 0, np.nan, ly), extent=ext, interpolation="nearest",
                       cmap=LinearSegmentedColormap.from_list("b", BLUE), vmin=2001, vmax=2024)
    axs[1].set_title("Tahun gross tree-cover loss\n2001–2024 (Hansen v1.13)", loc="left", fontsize=9)
    fig.colorbar(im, ax=axs[1], orientation="horizontal", fraction=0.04, pad=0.06, label="tahun loss")
    with rasterio.open(T / "DKP_MANGROVE_GMW2020_PA.tif") as r:
        mg = r.read(1); mtr = r.transform
    mext = [mtr.c, mtr.c + mtr.a * mg.shape[1], mtr.f + mtr.e * mg.shape[0], mtr.f]
    axs[2].imshow(np.where(mg == 1, 1, np.nan), extent=mext, interpolation="nearest", cmap=ListedColormap(["#1baf7a"]))
    axs[2].set_title("Mangrove GMW v3.0 (2020)\ndalam Project Area", loc="left", fontsize=9)
    sd = gpd.read_file(T / "DKP_SOIL_DEPTH_CLASS_PA.gpkg")
    cls = {"Peat": "#6b3d1f", "Mangrove": "#1baf7a", "Mineral": "#e3e2dc"}
    for k, c in cls.items():
        sub = sd[sd.SOIL == k]
        if k == "Peat":
            sub = sub.assign(DEEP=[d != "-" and float(d.split("-")[0]) >= 300 for d in sub.DEPTH_CLASS_CM])
            sub[~sub.DEEP].plot(ax=axs[3], color="#b07a4f", lw=0)
            sub[sub.DEEP].plot(ax=axs[3], color=c, lw=0)
        else:
            sub.plot(ax=axs[3], color=c, lw=0)
    axs[3].set_title("Tanah gambut & sedimen mangrove dalam PA\n(Laporan Gambut 2025; belum divalidasi independen)", loc="left", fontsize=9)
    axs[3].legend(handles=[Patch(color="#b07a4f", label="gambut 50–300 cm"), Patch(color="#6b3d1f", label="gambut ≥ 300 cm"),
                           Patch(color="#1baf7a", label="sedimen mangrove"), Patch(color="#e3e2dc", label="mineral / gambut < 50 cm")],
                  loc="upper center", bbox_to_anchor=(0.5, -0.06), fontsize=7, frameon=False, ncol=2)
    for ax in axs:
        m.boundary.plot(ax=ax, color=INK, lw=0.35)
        ax.set_xlim(m.total_bounds[0] - 0.02, m.total_bounds[2] + 0.02)
        ax.set_ylim(m.total_bounds[1] - 0.02, m.total_bounds[3] + 0.02)
        ax.set_aspect(1 / np.cos(np.radians(0.65)))
        ax.tick_params(labelsize=7)
        ax.set_xlabel(""); ax.set_ylabel("")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axs[0].set_ylabel("Lintang (°)", fontsize=8)
    fig.suptitle("Delta Kapuas 25 HD: layer tematik Project Area (garis hitam = 25 poligon PA)", x=0.01, ha="left", fontsize=11)
    out = P / "05_QUICKLOOK"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "DKP_THEMATIC_QUICKLOOK.png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def copy_support():
    src = T / "source_AOI"
    src.mkdir(exist_ok=True)
    for f in (ROOT / "02_REMOTE_SENSING_DATA").glob("*.tif"):
        shutil.copy2(f, src / f.name)
    shutil.copy2(ROOT / "02_REMOTE_SENSING_DATA" / "HANSEN_GFC_v1.13_AOI_metadata.json", src)
    q = P / "04_QA_DOCS"
    for f in [ROOT / "01_BOUNDARY_QA" / "PROJECT_AREA_25HD_BOUNDARY_AUDIT.xlsx",
              ROOT / "01_BOUNDARY_QA" / "SK_25HD_BOUNDARY_AUDIT.xlsx",
              ROOT / "01_BOUNDARY_QA" / "SPATIAL_DOMAIN_RECONCILIATION.md",
              ROOT / "04_VALIDATION" / "PULAU_MAYA_ANOMALY_INVESTIGATION.md",
              ROOT / "04_VALIDATION" / "SPATIAL_ACCURACY_AND_UNCERTAINTY.md",
              ROOT / "04_VALIDATION" / "HCV_VS_SATELLITE_COMPARISON.xlsx",
              ROOT / "07_REPRODUCIBLE_CODE" / "PROVENANCE.md"]:
        shutil.copy2(f, q / f.name)


def manifest():
    rows = []
    for f in sorted(P.rglob("*")):
        if f.is_file() and f.name != "MANIFEST.csv":
            rows.append({"PATH": str(f.relative_to(P)), "BYTES": f.stat().st_size,
                         "SHA256": hashlib.sha256(f.read_bytes()).hexdigest(), "INCLUDED": "YES", "NOTE": ""})
    refs = [
        ("REF: Landsat OLI median composites 2014/2019/2024 (Pulau Maya)", "repo delta-kapuas-gis/02_REMOTE_SENSING_DATA/landsat_pulau_maya (~67 MB)"),
        ("REF: Hansen GFC-2025-v1.13 tiles 00N_100E, 10N_100E", "https://storage.googleapis.com/earthenginepartners-hansen/GFC-2025-v1.13/ (SHA-256 in PROVENANCE.md)"),
        ("REF: GMW v3.0 gtiff 1996-2020", "https://zenodo.org/records/6894273"),
        ("REF: PeatDepth_Interpolated_10m_cm_49S_ABS.tif (Laporan Gambut 2025)", "TIDAK TERSEDIA - minta dari penyusun laporan"),
        ("REF: SHP Gabungan Hutan Desa Delta Kapuas (sumber SK)", "Diserahkan peneliti 31-10-2026; versi terolah: 01_MASTER_SPATIAL/DKP_25HD_SK_BOUNDARY.shp + layer SK_25HD_BOUNDARY di GPKG"),
    ]
    for p, n in refs:
        rows.append({"PATH": p, "BYTES": None, "SHA256": None, "INCLUDED": "NO", "NOTE": n})
    pd.DataFrame(rows).to_csv(P / "05_QUICKLOOK" / "MANIFEST.csv", index=False)


def zipit():
    z = ROOT / "DELTA_KAPUAS_25HD_GIS_FINAL_FOR_VENSIM.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(P.rglob("*")):
            if f.is_file():
                zf.write(f, "DELTA_KAPUAS_25HD_GIS_FINAL_FOR_VENSIM/" + str(f.relative_to(P)))
    with zipfile.ZipFile(z) as zf:
        assert zf.testzip() is None
        names = zf.namelist()
    need = [".shp", ".shx", ".dbf", ".prj"]
    assert all(any(n.endswith("DKP_25HD_MASTER_SPATIAL" + e) for n in names) for e in need)
    print(z, round(z.stat().st_size / 1e6, 1), "MB,", len(names), "files")


if __name__ == "__main__":
    quicklook()
    copy_support()
    manifest()
    zipit()
