"""Boundary QA for the 25 carbon Project Area polygons (Objective 1).

Run this as soon as the original shapefile is available. It does NOT repair
silently: the clean GeoPackage is written only with documented operations
(reprojection to EPSG:4326, make_valid on invalid features) and every
operation is logged in the audit workbook.

Checks: CRS present, geometry validity, empty/null geometries, multipart count,
geodesic area (WGS84), attribute-area agreement (any numeric field whose name
contains luas/area/ha), exact-duplicate geometries, duplicate names, pairwise
overlaps (ha), union-vs-sum area, HD name matching (exact -> alias -> fuzzy;
fuzzy matches are FLAGGED, never auto-accepted), and totals vs PDD
(111,123.20 ha) and the previous shapefile check (111,123.17 ha).

Usage:
  python -I s06_project_area_qa.py <project_area.shp|gpkg> <name_field> [out_dir]
Then:
  python -I s03_zonal_stats.py <out_dir>/PROJECT_AREA_25HD_CLEAN.gpkg PROJECT_AREA <gmw_dir> <out_csv>
"""
import difflib
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.validation import explain_validity, make_valid

from common import HD_COLS, HD_TABLE, PDD_PROJECT_AREA_HA, PRIOR_SHP_PROJECT_AREA_HA, ROOT, _GEOD

ALIASES = {  # observed spelling variants (extend after inspecting the shapefile; never guess silently)
    "dabung": "Dabong", "sei bemban": "Sungai Bemban", "sui bemban": "Sungai Bemban",
    "seruat ii": "Seruat Dua", "seruat 2": "Seruat Dua", "padang tikar i": "Padang Tikar 1",
    # Project shapefile v. 21-05-2026 labels this LPHD "Padang Tikar"; the 25-HD design contains a single
    # Padang Tikar HD ("Padang Tikar 1") and the polygon lies 100 % inside BPS desa Padang Tikar I.
    "padang tikar": "Padang Tikar 1",
    "padang tikar satu": "Padang Tikar 1", "sei jawi": "Sungai Jawi", "sei besar": "Sungai Besar",
}


def norm(s):
    s = str(s).lower().replace("hutan desa", "").replace("lphd", "").replace("hd ", "").strip()
    return " ".join(s.split())


def match_name(raw, names):
    n = norm(raw)
    for k in names:
        if norm(k) == n:
            return k, "EXACT"
    if n in ALIASES:
        return ALIASES[n], "ALIAS"
    best = difflib.get_close_matches(n, [norm(k) for k in names], n=1, cutoff=0.75)
    if best:
        k = [x for x in names if norm(x) == best[0]][0]
        return k, "FUZZY_NEEDS_REVIEW"
    return None, "UNMATCHED"


def gha(g):
    return abs(_GEOD.geometry_area_perimeter(g)[0]) / 1e4 if g is not None and not g.is_empty else 0.0


def main(path, name_field, out_dir=None):
    out_dir = Path(out_dir or ROOT / "01_BOUNDARY_QA")
    out_dir.mkdir(parents=True, exist_ok=True)
    src = gpd.read_file(path)
    log = [("input", str(path)), ("features", len(src)), ("crs_input", str(src.crs))]
    if src.crs is None:
        raise SystemExit("BLOCKED: shapefile has no CRS (.prj missing). Supply the .prj; do not guess.")
    g = src.to_crs("EPSG:4326").copy()
    g["SRC_FID"] = range(len(g))
    g["IS_EMPTY"] = g.geometry.is_empty | g.geometry.isna()
    g["IS_VALID_INPUT"] = g.geometry.is_valid
    g["VALIDITY_NOTE"] = g.geometry.apply(lambda x: explain_validity(x) if x is not None else "NULL")
    g["N_PARTS"] = g.geometry.apply(lambda x: len(getattr(x, "geoms", [x])) if x is not None else 0)
    g["GEODESIC_AREA_HA_INPUT"] = g.geometry.apply(gha)
    fixed = ~g.IS_VALID_INPUT & ~g.IS_EMPTY
    if fixed.any():
        g.loc[fixed, "geometry"] = g.loc[fixed, "geometry"].apply(make_valid)
        log.append(("make_valid applied to", list(g.loc[fixed, "SRC_FID"])))
    g["GEODESIC_AREA_HA"] = g.geometry.apply(gha)
    g["UTM49S_PLANAR_AREA_HA"] = g.to_crs(32749).area / 1e4   # PDD/attribute convention (WGS84 / UTM 49S)
    g["AREA_CHANGE_BY_REPAIR_HA"] = g.GEODESIC_AREA_HA - g.GEODESIC_AREA_HA_INPUT
    # attribute areas
    for c in src.columns:
        if c != "geometry" and any(k in c.lower() for k in ["luas", "area", "ha"]) and pd.api.types.is_numeric_dtype(src[c]):
            g[f"ATTR_{c}"] = src[c].values
            g[f"DIFF_{c}_HA"] = src[c].values - g.GEODESIC_AREA_HA
    # names
    names = [r[1] for r in HD_TABLE]
    m = g[name_field].apply(lambda x: match_name(x, names))
    g["HD_NAME"] = [a for a, _ in m]
    g["NAME_MATCH"] = [b for _, b in m]
    hd = pd.DataFrame(HD_TABLE, columns=HD_COLS)[["HD_ID", "HD_NAME", "LANDSCAPE", "REGENCY"]]
    g = g.merge(hd, on="HD_NAME", how="left")
    # duplicates & overlaps
    wkb = g.geometry.apply(lambda x: x.wkb if x is not None else b"")
    g["DUP_GEOMETRY"] = wkb.duplicated(keep=False)
    g["DUP_HD"] = g.HD_NAME.notna() & g.HD_NAME.duplicated(keep=False)
    ov = []
    sidx = g.sindex
    for i, gi in enumerate(g.geometry):
        for j in sidx.query(gi, predicate="intersects"):
            if j > i:
                a = gha(gi.intersection(g.geometry.iloc[j]))
                if a > 0.01:
                    ov.append({"FID_A": i, "HD_A": g.HD_NAME.iloc[i], "FID_B": j, "HD_B": g.HD_NAME.iloc[j], "OVERLAP_HA": a})
    ov = pd.DataFrame(ov, columns=["FID_A", "HD_A", "FID_B", "HD_B", "OVERLAP_HA"])
    union_ha = gha(g.geometry.union_all())
    tot = g.GEODESIC_AREA_HA.sum()
    tot_utm = g.UTM49S_PLANAR_AREA_HA.sum()
    # name-location consistency against the BPS desa context layer (if built)
    ctx_path = ROOT / "01_BOUNDARY_QA" / "CONTEXT_DOMAIN_25DESA_BPS2020.gpkg"
    loc = pd.DataFrame()
    if ctx_path.exists():
        ctx = gpd.read_file(ctx_path)
        recs = []
        for r in g.itertuples():
            a = ctx.geometry.intersection(r.geometry).apply(gha)
            same = float(a[ctx.HD_NAME == r.HD_NAME].sum()) if r.HD_NAME else 0.0
            top = ctx.assign(a=a).sort_values("a", ascending=False).iloc[0]
            recs.append({"SRC_FID": r.SRC_FID, "HD_NAME": r.HD_NAME,
                         "PCT_IN_SAME_NAME_DESA": 100 * same / r.GEODESIC_AREA_HA,
                         "LARGEST_OVERLAP_DESA": top.ADMIN_DESA, "PCT_IN_LARGEST": 100 * top.a / r.GEODESIC_AREA_HA,
                         "PCT_OUTSIDE_ALL_25_DESA": 100 * (1 - a.sum() / r.GEODESIC_AREA_HA)})
        loc = pd.DataFrame(recs)
        loc["FLAG"] = loc.PCT_IN_SAME_NAME_DESA.apply(lambda v: "OK" if v >= 50 else "NAME_LOCATION_MISMATCH_WITH_BPS_DESA")
    missing = sorted(set(names) - set(g.HD_NAME.dropna()))
    summary = pd.DataFrame([
        ("Features", len(g), "25 expected"),
        ("CRS (input)", str(src.crs), ""),
        ("Invalid geometries (input)", int((~g.IS_VALID_INPUT).sum()), "repaired with make_valid, logged"),
        ("Empty/null geometries", int(g.IS_EMPTY.sum()), ""),
        ("Exact duplicate geometries", int(g.DUP_GEOMETRY.sum()), ""),
        ("Polygons per HD > 1", int(g.DUP_HD.sum()), "multiple features mapped to one HD"),
        ("Pairwise overlaps > 0.01 ha", len(ov), f"{ov.OVERLAP_HA.sum():.2f} ha"),
        ("Sum of geodesic areas, WGS84 ellipsoid (ha)", round(tot, 2), "reference area used in all zonal statistics"),
        ("Sum of UTM 49S planar areas (ha)", round(tot_utm, 2), f"PDD convention; geodesic - planar = {tot - tot_utm:+.2f} ha (UTM scale distortion)"),
        ("Area of union (ha)", round(union_ha, 2), "sum - union = double-counted area"),
        ("PDD Project Area (ha)", PDD_PROJECT_AREA_HA, f"UTM49S sum - PDD: {tot_utm - PDD_PROJECT_AREA_HA:+.2f} ha; geodesic - PDD: {tot - PDD_PROJECT_AREA_HA:+.2f} ha"),
        ("Previous shapefile check (ha)", PRIOR_SHP_PROJECT_AREA_HA, f"UTM49S sum - previous: {tot_utm - PRIOR_SHP_PROJECT_AREA_HA:+.2f} ha"),
        ("PA polygons not mainly inside same-name BPS desa", int((loc.FLAG != "OK").sum()) if len(loc) else "n/a",
         "admin desa != HD location; see NAME_LOCATION sheet"),
        ("Unmatched / fuzzy names", int((g.NAME_MATCH.isin(['UNMATCHED', 'FUZZY_NEEDS_REVIEW'])).sum()), "review manually"),
        ("HD with no polygon", len(missing), ", ".join(missing)),
    ], columns=["CHECK", "RESULT", "NOTE"])
    status = "PASS" if (len(g) == 25 and not missing and len(ov) == 0 and not g.DUP_HD.any()
                        and abs(tot_utm - PDD_PROJECT_AREA_HA) < 1.0
                        and not g.NAME_MATCH.isin(["UNMATCHED", "FUZZY_NEEDS_REVIEW"]).any()) else "CONDITIONAL - REVIEW"
    summary.loc[len(summary)] = ("GATE 1 STATUS", status, "")
    with pd.ExcelWriter(out_dir / "PROJECT_AREA_25HD_BOUNDARY_AUDIT.xlsx") as xw:
        summary.to_excel(xw, sheet_name="SUMMARY", index=False)
        g.drop(columns="geometry").to_excel(xw, sheet_name="PER_POLYGON", index=False)
        ov.to_excel(xw, sheet_name="OVERLAPS", index=False)
        if len(loc):
            loc.to_excel(xw, sheet_name="NAME_LOCATION_VS_BPS_DESA", index=False)
        g.groupby("LANDSCAPE", dropna=False)["GEODESIC_AREA_HA"].sum().reset_index().to_excel(xw, sheet_name="BY_LANDSCAPE", index=False)
        pd.DataFrame(log, columns=["STEP", "DETAIL"]).astype(str).to_excel(xw, sheet_name="PROCESSING_LOG", index=False)
    clean = g[g.HD_ID.notna()].copy()
    clean["SPATIAL_DOMAIN"] = "PROJECT_AREA"
    clean[["HD_ID", "HD_NAME", "LANDSCAPE", "REGENCY", "SPATIAL_DOMAIN", "SRC_FID", "NAME_MATCH",
           "GEODESIC_AREA_HA", "UTM49S_PLANAR_AREA_HA", "geometry"]].to_file(out_dir / "PROJECT_AREA_25HD_CLEAN.gpkg", layer="project_area", driver="GPKG")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main(*sys.argv[1:4])
