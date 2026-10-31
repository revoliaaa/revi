"""Publication figures (static PNG, 300 dpi, light print theme).

Palette: categorical slots 1-3 of the validated reference palette (blue, orange,
aqua; all-pairs CVD dE >= 9.2). Aqua is < 3:1 on white -> every line is
direct-labelled. Sequential maps use a single-hue blue ramp.

Usage: python -I s10_figures.py <gmw_dir> [landsat_dir]
"""
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Patch

from common import ROOT, row_pixel_area_ha
from s03_zonal_stats import gmw_mosaic

FIG = ROOT / "06_PUBLICATION" / "figures"
COL = {"Kubu": "#2a78d6", "Padang Tikar": "#eb6834", "Pulau Maya": "#1baf7a"}
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True})


def save(fig, name):
    fig.savefig(FIG / name, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


def fig_study_area(gmw_dir):
    d = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "CONTEXT_DOMAIN_25DESA_BPS2020.gpkg")
    m, tr = gmw_mosaic(gmw_dir, 2020)
    fig, ax = plt.subplots(figsize=(6.4, 7.4))
    ext = [tr.c, tr.c + tr.a * m.shape[1], tr.f + tr.e * m.shape[0], tr.f]
    ax.imshow(np.where(m, 1, np.nan), extent=ext, cmap=ListedColormap(["#5c5b57"]), interpolation="nearest", zorder=3)
    for L, g in d.groupby("LANDSCAPE"):
        g.plot(ax=ax, facecolor=COL[L], alpha=0.22, edgecolor="none", zorder=2)
        g.boundary.plot(ax=ax, color=COL[L], linewidth=1.0, zorder=4)
    for r in d.itertuples():
        p = r.geometry.representative_point()
        ax.annotate(r.HD_ID[2:], (p.x, p.y), fontsize=6.5, color=INK, ha="center", va="center", zorder=5,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
    ax.set_xlim(109.12, 110.0); ax.set_ylim(-1.34, 0.11)
    ax.set_aspect(1 / np.cos(np.radians(0.6)))
    ax.set_xlabel("Longitude (°E)"); ax.set_ylabel("Latitude (°)")
    h = [Patch(facecolor=COL[k], alpha=0.35, edgecolor=COL[k], label=f"{k} (desa context)") for k in COL]
    h.append(Patch(facecolor="#5c5b57", label="Mangrove, GMW v3 2020"))
    ax.set_xticks(np.arange(109.2, 110.01, 0.2))
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=2, fontsize=7.5, frameon=False)
    ax.set_title("Delta Kapuas: 25 village (desa) context polygons\nmatched to the 25 Hutan Desa (numbers = HD_ID)",
                 fontsize=10, color=INK, loc="left")
    save(fig, "FIG1_STUDY_AREA_DESA_CONTEXT_GMW2020.png")


def fig_loss_map():
    with rasterio.open(ROOT / "02_REMOTE_SENSING_DATA" / "ANNUAL_TREE_COVER_LOSS_2001_2025_lossyear.tif") as r:
        ly = r.read(1)[::2, ::2]; tr = r.transform
    with rasterio.open(ROOT / "02_REMOTE_SENSING_DATA" / "FOREST_COVER_BASELINE_2000_canopy_pct.tif") as r:
        tc = r.read(1)[::2, ::2]
    d = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "CONTEXT_DOMAIN_25DESA_BPS2020.gpkg")
    ext = [tr.c, tr.c + tr.a * 2 * ly.shape[1], tr.f + tr.e * 2 * ly.shape[0], tr.f]
    fig, ax = plt.subplots(figsize=(6.4, 7.4))
    ax.imshow(np.where(tc > 30, 1, np.nan), extent=ext, cmap=ListedColormap(["#e3e2dc"]), interpolation="nearest")
    cmap = LinearSegmentedColormap.from_list("blue", BLUE_RAMP)
    im = ax.imshow(np.where((ly > 0) & (ly <= 24) & (tc > 30), ly.astype("int16") + 2000, np.nan), extent=ext, cmap=cmap,
                   vmin=2001, vmax=2024, interpolation="nearest")
    d.boundary.plot(ax=ax, color=INK, linewidth=0.5)
    ax.set_xlim(109.12, 110.0); ax.set_ylim(-1.34, 0.11)
    ax.set_aspect(1 / np.cos(np.radians(0.6))); ax.grid(False)
    cb = fig.colorbar(im, ax=ax, shrink=0.55, pad=0.02); cb.set_label("Year of gross tree-cover loss")
    ax.set_xticks(np.arange(109.2, 110.01, 0.2))
    ax.legend(handles=[Patch(facecolor="#e3e2dc", label="Tree cover 2000 (>30 % canopy), no loss detected")],
              loc="upper center", bbox_to_anchor=(0.5, -0.07), fontsize=7.5, frameon=False)
    ax.set_title("Gross tree-cover loss 2001–2024 (Hansen GFC v1.13, canopy >30 %)\nwithin desa context polygons and surroundings",
                 fontsize=10, color=INK, loc="left")
    ax.set_xlabel("Longitude (°E)"); ax.set_ylabel("Latitude (°)")
    save(fig, "FIG2_TREE_COVER_LOSS_YEAR_MAP.png")


def fig_annual_loss():
    a = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "TRENDS_ADMIN_DESA_CONTEXT_ANNUAL.csv").query("THRESHOLD_PCT==30")
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.axvspan(2000.5, 2014.5, color="#f3f2ee", zorder=0)
    ax.text(2001, 1, "Calibration window 2001–2014", color=MUTED, fontsize=7.5, transform=ax.get_xaxis_transform(), va="top")
    ax.text(2015, 1, "Held-out 2015–2024", color=MUTED, fontsize=7.5, transform=ax.get_xaxis_transform(), va="top")
    ax.axvline(2010.5, color=MUTED, lw=1, ls=(0, (3, 2)))
    ax.annotate("Hansen v1.13 reprocessing\nbreak: 2011+ reprocessed", xy=(2010.5, 0.86), xytext=(2001.3, 0.86),
                xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(), color=INK2, fontsize=7,
                va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    for L in COL:
        s = a[a.GROUP == L]
        ax.plot(s.YEAR, s.GROSS_LOSS_HA, color=COL[L], lw=2, marker="o", ms=3.2,
                markeredgecolor="white", markeredgewidth=0.6)
        off = {"Kubu": 0, "Padang Tikar": 300, "Pulau Maya": 0}[L]
        ax.annotate(L, (2024.3, s.GROSS_LOSS_HA.iloc[-1] + off), color=INK, fontsize=8, va="center")
    ax.set_xlim(2000.5, 2027.2); ax.set_ylim(0, None)
    ax.set_ylabel("Gross tree-cover loss (ha / yr)")
    ax.set_title("Annual gross tree-cover loss by landscape, desa context domain (canopy >30 %)",
                 fontsize=10, color=INK, loc="left")
    save(fig, "FIG3_ANNUAL_GROSS_LOSS_BY_LANDSCAPE.png")


def fig_benchmarks():
    a = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "TRENDS_ADMIN_DESA_CONTEXT_ANNUAL.csv").query("THRESHOLD_PCT==30 and GROUP=='ALL_25'")
    p = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "TRENDS_ADMIN_DESA_CONTEXT_PARAMS.csv").query("THRESHOLD_PCT==30 and GROUP=='ALL_25'").iloc[0]
    yrs = np.arange(2015, 2025)
    R14 = a.set_index("YEAR").loc[2014, "TC2000_NET_OF_GROSS_LOSS_HA (derived, not forest area)"]
    b3, r = [], R14
    for _ in yrs:
        b3.append(p.B3_k_per_yr * r); r -= b3[-1]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.bar(a.YEAR, a.GROSS_LOSS_HA, color="#c9c8c1", width=0.72, label="Observed (Hansen)", zorder=2)
    for name, y, c in [("B1 constant mean", np.full(len(yrs), p.B1_mean_ha_yr), COL["Kubu"]),
                       ("B2 linear trend", np.maximum(p.B2_intercept + p.B2_slope_ha_yr2 * yrs, 0), COL["Padang Tikar"]),
                       ("B3 constant proportional rate", np.array(b3), COL["Pulau Maya"])]:
        ax.plot(yrs, y, color=c, lw=2, zorder=3)
        ax.annotate(name, (2024.3, y[-1]), color=INK, fontsize=7.5, va="center")
    ax.axvline(2014.5, color=MUTED, lw=1, ls=(0, (3, 2)))
    ax.set_xlim(2000.5, 2029.5); ax.set_ylim(0, None)
    ax.set_ylabel("Gross tree-cover loss (ha / yr)")
    ax.legend(loc="upper left", fontsize=7.5, frameon=False)
    ax.set_title("Benchmarks fitted on 2001–2014, evaluated on held-out 2015–2024 (all 25 desa, canopy >30 %)",
                 fontsize=10, color=INK, loc="left")
    save(fig, "FIG4_BENCHMARKS_HELD_OUT.png")


def fig_pulau_maya_mangrove():
    z = pd.read_csv(ROOT / "03_LAND_COVER_CHANGE" / "ZONAL_ADMIN_DESA_CONTEXT.csv").query("LANDSCAPE=='Pulau Maya'")
    import json
    buf = json.load(open(ROOT / "04_VALIDATION" / "GMW_OUTSIDE_DESA_BUFFER.json"))["Pulau Maya"]
    yrs = [1996, 2007, 2010, 2015, 2016, 2019, 2020]
    gm = [z[f"MANGROVE_GMW_{y}_HA"].sum() + buf[str(y)] for y in yrs]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(yrs, gm, color=COL["Pulau Maya"], lw=2, marker="o", ms=4, markeredgecolor="white")
    ax.annotate("GMW v3 mangrove, 5 desa + 1 km buffer (upper bound for the HCV area)", (1996, gm[0] + 450), color=INK, fontsize=7.5, va="bottom")
    ax.plot([2019, 2024], [6844, 10617], color=INK, lw=1.2, ls=(0, (2, 2)), marker="s", ms=5)
    ax.annotate("HCV 2019: 6,844 ha", (2019, 6844), xytext=(-8, -4), textcoords="offset points", ha="right", fontsize=7.5)
    ax.annotate("HCV 2024: 10,617 ha", (2024, 10617), xytext=(6, 0), textcoords="offset points", fontsize=7.5, va="center")
    ax.set_xlim(1994, 2029.5); ax.set_ylim(0, 12000)
    ax.set_ylabel("Mangrove area (ha)")
    ax.set_title("Pulau Maya: HCV mangrove totals vs independent GMW v3 series", fontsize=10, color=INK, loc="left")
    save(fig, "FIG5_PULAU_MAYA_HCV_VS_GMW.png")


def fig_pulau_maya_ndvi(ldir):
    imgs, tr = {}, None
    for y in (2019, 2024):
        with rasterio.open(Path(ldir) / f"LANDSAT_OLI_MEDIAN_{y}_NDVI_NDMI_MNDWI_NOBS.tif") as r:
            a = r.read(1).astype(float); tr = r.transform
            imgs[y] = np.where(a == -32768, np.nan, a / 1e4)
    msk = np.load(Path(ldir) / "_pm_masks.npz")
    ext = [tr.c, tr.c + tr.a * imgs[2019].shape[1], tr.f + tr.e * imgs[2019].shape[0], tr.f]
    d = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "CONTEXT_DOMAIN_25DESA_BPS2020.gpkg").query("LANDSCAPE=='Pulau Maya'")
    pa = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "PROJECT_AREA_25HD_CLEAN.gpkg").query("LANDSCAPE=='Pulau Maya'")
    fig = plt.figure(figsize=(13, 4.6))
    gs = fig.add_gridspec(1, 3, wspace=0.32)
    axs = [fig.add_subplot(gs[0, i]) for i in range(3)]
    cmap = LinearSegmentedColormap.from_list("blue", BLUE_RAMP)
    for ax, y in zip(axs[:2], (2019, 2024)):
        im = ax.imshow(imgs[y], extent=ext, cmap=cmap, vmin=0, vmax=0.9, interpolation="nearest")
        d.boundary.plot(ax=ax, color=MUTED, lw=0.4); pa.boundary.plot(ax=ax, color=INK, lw=0.9)
        ax.set_title(f"Landsat OLI median NDVI {y}", fontsize=9, loc="left")
    a, b = imgs[2019], imgs[2024]
    with rasterio.open(Path(ldir) / "LANDSAT_OLI_MEDIAN_2019_NDVI_NDMI_MNDWI_NOBS.tif") as r:
        mn = r.read(3).astype(float); mn = np.where(mn == -32768, np.nan, mn / 1e4)
    newv = msk["dom"] & ((a < 0.4) | (mn > 0)) & (b >= 0.6)
    axs[2].imshow(np.where(msk["gm"], 1, np.nan), extent=ext, cmap=ListedColormap(["#d9d8d2"]), interpolation="nearest")
    rr, cc = np.nonzero(newv & msk["pa"])
    xs, ys = tr.c + (cc + 0.5) * tr.a, tr.f + (rr + 0.5) * tr.e
    axs[2].scatter(xs, ys, s=9, color=COL["Padang Tikar"], edgecolor="white", linewidth=0.3, zorder=5)
    pa_ha = float((row_pixel_area_ha(tr, newv.shape[0])[:, None] * (newv & msk["pa"])).sum())
    newv_title = f"Newly vegetated 2019→2024 (NDVI ≥ 0.6)\ninside Project Area: {pa_ha:.1f} ha (1 dot = 1 pixel, enlarged)"
    d.boundary.plot(ax=axs[2], color=MUTED, lw=0.4); pa.boundary.plot(ax=axs[2], color=INK, lw=0.9)
    axs[2].set_title(newv_title, fontsize=9, loc="left")
    axs[2].legend(handles=[Patch(facecolor="#d9d8d2", label="GMW 2020 mangrove"),
                           Patch(facecolor=COL["Padang Tikar"], label="Newly vegetated pixel (in PA)"),
                           Patch(facecolor="none", edgecolor=INK, label="Project Area"),
                           Patch(facecolor="none", edgecolor=MUTED, label="BPS desa")],
                  loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=7, frameon=False)
    for ax in axs:
        ax.grid(False); ax.set_aspect(1 / np.cos(np.radians(1.1)))
        ax.set_xlim(*d.total_bounds[[0, 2]] + [-0.01, 0.01]); ax.set_ylim(*d.total_bounds[[1, 3]] + [-0.01, 0.01])
        ax.set_xlabel("Longitude (°E)"); ax.set_ylabel(""); ax.set_xticks([109.3, 109.5, 109.7])
    axs[0].set_ylabel("Latitude (°)")
    for ax in axs[1:]:
        ax.set_yticklabels([])
    cax = axs[1].inset_axes([1.03, 0.1, 0.035, 0.8])
    fig.colorbar(im, cax=cax, label="NDVI")
    fig.suptitle("Pulau Maya: no large-scale vegetation gain 2019→2024 (HCV reports +3,773 ha mangrove)",
                 x=0.125, y=1.0, ha="left", fontsize=10, color=INK)
    save(fig, "FIG6_PULAU_MAYA_LANDSAT_NDVI_2019_2024.png")


def fig_hcv_harmonised():
    c = pd.read_csv(ROOT / "04_VALIDATION" / "HCV_HARMONISED_SERIES.csv")
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.6))
    for ax, g in zip(axs, ["Kubu", "Padang Tikar", "Pulau Maya", "ALL_25"]):
        d = c[c.GROUP == g]
        col = COL.get(g, INK)
        ax.axvspan(2016.5, 2025.5, color="#f3f2ee", zorder=0)
        ax.plot(d.YEAR, d["S2_HCV2000_MINUS_AREA_SCALED_LOSS_HA"] / 1000, color=MUTED, lw=2, ls=(0, (3, 2)),
                label="Satellite-harmonised (HCV 2000 − Hansen loss)")
        ax.plot(d.YEAR, d.HCV_NATURAL_FOREST_HA / 1000, color=col, lw=2, marker="o", ms=4, markeredgecolor="white",
                label="HCV natural forest")
        ax.set_title("All 25 HD" if g == "ALL_25" else g, fontsize=9.5, loc="left", color=INK)
        ax.set_xticks([2000, 2009, 2019]); ax.set_xlim(1998, 2026)
        lo, hi = d[["S2_HCV2000_MINUS_AREA_SCALED_LOSS_HA", "HCV_NATURAL_FOREST_HA"]].min().min() / 1000, d[["S2_HCV2000_MINUS_AREA_SCALED_LOSS_HA", "HCV_NATURAL_FOREST_HA"]].max().max() / 1000
        pad = (hi - lo) * 0.15 + 0.5
        ax.set_ylim(lo - pad, hi + pad)
    axs[0].set_ylabel("Natural forest (thousand ha)")
    axs[0].text(2017, 0.04, "held-out", transform=axs[0].get_xaxis_transform(), fontsize=7, color=MUTED)
    h, l = axs[3].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, fontsize=8, frameon=False, bbox_to_anchor=(0.5, -0.06))
    fig.suptitle("HCV natural-forest series vs a monotone, satellite-harmonised reference (canopy >30 %, area-scaled)",
                 x=0.06, ha="left", fontsize=10, color=INK, y=1.02)
    fig.tight_layout()
    save(fig, "FIG7_HCV_VS_SATELLITE_HARMONISED.png")


if __name__ == "__main__":
    FIG.mkdir(parents=True, exist_ok=True)
    fig_study_area(sys.argv[1]); fig_loss_map(); fig_annual_loss(); fig_benchmarks(); fig_pulau_maya_mangrove()
    fig_hcv_harmonised()
    if len(sys.argv) > 2:
        fig_pulau_maya_ndvi(sys.argv[2])
