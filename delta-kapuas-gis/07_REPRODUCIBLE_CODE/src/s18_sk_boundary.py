"""Build the 25-HD SK (Hutan Desa decree) boundary layer from 'SHP Gabungan Hutan Desa Delta Kapuas'.

Input (2026-10-31): .shp/.shx/.sbn/.sbx/.shp.xml, then .dbf and .prj supplied separately.
  * CRS: .prj = WGS_1984_UTM_Zone_49S (EPSG:32749), identical to the .shp.xml metadata.
  * HD assignment: (1) spatial = maximum overlap with the verified Project Area polygon (fallback nearest);
    (2) attribute = SK number (NO_SK_HPHD) matched to the SK table of the HCV reports, or NAMA_DESA for the
    Kemboja pieces (Kemboja SK 2024 is not in the attribute). The two are cross-checked and must agree.
    NAMA_LPHD is NOT used as key: the lineage shows it was overwritten with NAMOBJ (administrative village
    name), e.g. the 1,143 ha piece labelled 'Tanjungsatai' carries SK.5735 (Dusun Besar).
Lineage (.shp.xml): Merge of 'PL HD Kamboja 2023' (Kemboja HD intersected with land cover 2023 -> split into
pieces) and 'SHP Gabungan 25 Desa Dampingan_Delta Kapuas' (fields NO_SK_HPHD, LUAS_HPHD, NAMA_LPHD).

Outputs: 01_BOUNDARY_QA/SK_25HD_BOUNDARY.gpkg (dissolved per HD, EPSG:4326) and SK_25HD_BOUNDARY_AUDIT.xlsx
Usage: python s18_sk_boundary.py <SHP_Gabungan_Hutan_Desa_Delta_Kapuas.shp>
"""
import sys
import warnings

import geopandas as gpd
import pandas as pd
import pyogrio
from shapely.validation import explain_validity, make_valid

from common import CODE, ROOT, _GEOD

warnings.simplefilter("ignore")


def gha(g):
    return abs(_GEOD.geometry_area_perimeter(g)[0]) / 1e4 if g is not None and not g.is_empty else 0.0


def main(shp):
    raw = pyogrio.read_dataframe(shp)
    has_dbf = "NO_SK_HPHD" in raw.columns
    log = [("input", shp), ("records", len(raw)), ("attributes", "dbf present" if has_dbf else "none (.dbf missing)"),
           ("crs_file", str(raw.crs))]
    if raw.crs is None:
        raw = raw.set_crs(32749)
        log.append(("crs", "EPSG:32749 assigned from .shp.xml metadata (.prj missing)"))
    assert raw.crs.to_epsg() == 32749
    raw["SRC_FID"] = range(len(raw))
    raw["VALID_INPUT"] = raw.geometry.is_valid
    raw["VALIDITY_NOTE"] = raw.geometry.apply(explain_validity)
    raw["UTM_HA_INPUT"] = raw.area / 1e4
    bad = ~raw.VALID_INPUT
    raw.loc[bad, "geometry"] = raw.loc[bad, "geometry"].apply(make_valid)
    if bad.any():
        log.append(("make_valid", list(raw.loc[bad, "SRC_FID"])))
    # keep polygonal parts only after make_valid
    raw["geometry"] = raw.geometry.apply(lambda g: g if g.geom_type in ("Polygon", "MultiPolygon")
                                         else gpd.GeoSeries([g]).explode().loc[lambda s: s.geom_type.isin(["Polygon", "MultiPolygon"])].union_all())
    raw["UTM_HA"] = raw.area / 1e4
    degen = raw.UTM_HA < 0.01
    if degen.any():
        log.append(("dropped degenerate (<0.01 ha)", list(raw.loc[degen, "SRC_FID"])))
    sk = raw[~degen].copy()

    pa = gpd.read_file(ROOT / "01_BOUNDARY_QA" / "PROJECT_AREA_25HD_CLEAN.gpkg").to_crs(32749)
    rows = []
    for r in sk.itertuples():
        ov = pa.geometry.intersection(r.geometry).area / 1e4
        if ov.max() > 0.001:
            j, how = ov.idxmax(), "MAX_OVERLAP"
        else:
            j, how = pa.geometry.distance(r.geometry).idxmin(), "NEAREST (no overlap)"
        rows.append({"SRC_FID": r.SRC_FID, "HD_ID": pa.HD_ID[j], "HD_NAME": pa.HD_NAME[j], "ASSIGN_METHOD": how,
                     "OVERLAP_WITH_ASSIGNED_PA_HA": ov[j], "N_PA_OVERLAPPED": int((ov > 0.001).sum()),
                     "PCT_OF_PIECE_IN_PA": 100 * ov[j] / r.UTM_HA, "UTM_HA": r.UTM_HA,
                     "DIST_TO_PA_M": float(pa.geometry[j].distance(r.geometry))})
    asg = pd.DataFrame(rows)
    if has_dbf:
        tabsk = pd.read_csv(CODE / "inputs" / "HCV_SK_AREAS.csv")
        norm = lambda x: "".join(str(x).upper().split()).replace("PSL-0", "PSL.0")
        sk_map = {norm(a): b for a, b in zip(tabsk.SK_NUMBER, tabsk.HD_NAME)}
        attr = sk.set_index("SRC_FID")
        def by_attr(f):
            n = attr.loc[f, "NO_SK_HPHD"]
            if isinstance(n, str) and n.strip():
                return sk_map.get(norm(n), "UNMATCHED_SK:" + n.strip()), "SK_NUMBER"
            if f <= 9:   # pieces from the 'PL HD Kamboja 2023' input of the Merge (lineage)
                return "Kemboja", "LINEAGE_KAMBOJA_INPUT (NAMA_DESA=%s)" % attr.loc[f, "NAMA_DESA"]
            return "UNKNOWN", "-"
        aa = [by_attr(f) for f in asg.SRC_FID]
        asg["HD_BY_ATTRIBUTE"] = [a for a, _ in aa]
        asg["ATTRIBUTE_KEY"] = [b for _, b in aa]
        asg["DBF_NAMA_LPHD"] = asg.SRC_FID.map(attr.NAMA_LPHD)
        asg["DBF_NAMA_DESA"] = asg.SRC_FID.map(attr.NAMA_DESA)
        asg["DBF_NO_SK_HPHD"] = asg.SRC_FID.map(attr.NO_SK_HPHD).astype(str).str.strip()
        asg["AGREE"] = asg.HD_BY_ATTRIBUTE == asg.HD_NAME
        log.append(("spatial vs attribute (SK number) agreement", f"{int(asg.AGREE.sum())}/{len(asg)}"))
        assert asg.AGREE.all(), asg[~asg.AGREE]
    sk = sk[["SRC_FID", "geometry"]].merge(asg[["SRC_FID", "HD_ID", "HD_NAME"]], on="SRC_FID")
    assert (asg.N_PA_OVERLAPPED <= 1).all(), "an SK piece overlaps more than one PA polygon - check manually"

    # pairwise overlaps between SK pieces (merge artefacts)
    ov = []
    sidx = sk.sindex
    for i, gi in enumerate(sk.geometry):
        for j in sidx.query(gi, predicate="intersects"):
            if j > i:
                a = gi.intersection(sk.geometry.iloc[j]).area / 1e4
                if a > 0.01:
                    ov.append({"FID_A": sk.SRC_FID.iloc[i], "HD_A": sk.HD_NAME.iloc[i], "FID_B": sk.SRC_FID.iloc[j],
                               "HD_B": sk.HD_NAME.iloc[j], "OVERLAP_HA": a})
    ov = pd.DataFrame(ov, columns=["FID_A", "HD_A", "FID_B", "HD_B", "OVERLAP_HA"])

    d = sk.dissolve(by=["HD_ID", "HD_NAME"], as_index=False, aggfunc={"SRC_FID": lambda s: ",".join(map(str, s))})
    d = d.rename(columns={"SRC_FID": "SRC_FIDS"})
    d["N_PIECES"] = d.SRC_FIDS.str.count(",") + 1
    d["SK_GEOM_UTM_HA"] = d.area / 1e4
    tab = pd.read_csv(CODE / "inputs" / "HCV_SK_AREAS.csv")[["HD_NAME", "LANDSCAPE", "SK_AREA_HA", "SK_NUMBER"]]
    d = d.merge(tab, on="HD_NAME", how="left")
    from common import HD_COLS, HD_TABLE
    d["REGENCY"] = d.HD_NAME.map(pd.DataFrame(HD_TABLE, columns=HD_COLS).set_index("HD_NAME").REGENCY)
    d["GEOM_MINUS_TABLE_HA"] = d.SK_GEOM_UTM_HA - d.SK_AREA_HA
    d["GEOM_MINUS_TABLE_PCT"] = 100 * d.GEOM_MINUS_TABLE_HA / d.SK_AREA_HA
    # A1: is the PA inside the SK?
    pa_d = pa.set_index("HD_ID")
    d["PA_UTM_HA"] = d.HD_ID.map(pa_d.area / 1e4)
    d["PA_INSIDE_SK_HA"] = [pa_d.geometry[h].intersection(g).area / 1e4 for h, g in zip(d.HD_ID, d.geometry)]
    d["PA_OUTSIDE_SK_HA"] = d.PA_UTM_HA - d.PA_INSIDE_SK_HA
    d["PA_INSIDE_SK_PCT"] = 100 * d.PA_INSIDE_SK_HA / d.PA_UTM_HA
    d["SK_NOT_IN_PA_HA"] = d.SK_GEOM_UTM_HA - d.PA_INSIDE_SK_HA
    d["FLAG"] = [";".join(x for x in [
        "GEOM_VS_TABLE>2%" if abs(p) > 2 else "",
        "PA_OUTSIDE_SK>1%" if 100 - q > 1 else ""] if x) or "OK" for p, q in zip(d.GEOM_MINUS_TABLE_PCT, d.PA_INSIDE_SK_PCT)]
    out = d.to_crs(4326)
    out["SK_GEOM_GEODESIC_HA"] = out.geometry.apply(gha)
    out["SPATIAL_DOMAIN"] = "SK_HD (SHP Gabungan Hutan Desa Delta Kapuas; HD assigned spatially)"
    out = out.sort_values("HD_ID")
    out.to_file(ROOT / "01_BOUNDARY_QA" / "SK_25HD_BOUNDARY.gpkg", layer="sk_25hd", driver="GPKG")

    land = out.drop(columns="geometry").groupby("LANDSCAPE")[["SK_AREA_HA", "SK_GEOM_UTM_HA", "SK_GEOM_GEODESIC_HA",
                                                              "PA_UTM_HA", "PA_INSIDE_SK_HA", "PA_OUTSIDE_SK_HA"]].sum()
    land.loc["ALL_25"] = land.sum()
    summ = pd.DataFrame([
        ("Records in file", len(raw)), ("Degenerate dropped", int(degen.sum())), ("Invalid repaired", int(bad.sum())),
        ("HD after dissolve", len(out)), ("Pieces overlapping >1 PA", int((asg.N_PA_OVERLAPPED > 1).sum())),
        ("Pieces with no PA overlap (nearest)", int((asg.ASSIGN_METHOD != "MAX_OVERLAP").sum())),
        ("Spatial vs attribute (SK number) agreement", f"{int(asg.AGREE.sum())}/{len(asg)}" if has_dbf else "n/a (no dbf)"),
        ("CRS", "EPSG:32749 (.prj)" if has_dbf else "EPSG:32749 (.shp.xml)"),
        ("Pairwise SK overlaps > 0.01 ha", len(ov)),
        ("SK geometry total UTM49S (ha)", round(out.SK_GEOM_UTM_HA.sum(), 2)),
        ("SK geometry total geodesic (ha)", round(out.SK_GEOM_GEODESIC_HA.sum(), 2)),
        ("SK table total (ha)", out.SK_AREA_HA.sum()),
        ("PA inside SK (ha, UTM)", round(out.PA_INSIDE_SK_HA.sum(), 2)),
        ("PA outside SK (ha, UTM)", round(out.PA_OUTSIDE_SK_HA.sum(), 2)),
        ("Assumption A1 (PA within SK)",
         ("HOLDS" if out.PA_OUTSIDE_SK_HA.sum() < 1 else
          f"HOLDS WITHIN TOLERANCE: {100 * out.PA_INSIDE_SK_HA.sum() / out.PA_UTM_HA.sum():.2f} % of PA inside SK; "
          f"{out.PA_OUTSIDE_SK_HA.sum():.1f} ha edge slivers (max {out.PA_OUTSIDE_SK_HA.max():.1f} ha per HD)"
          if out.PA_OUTSIDE_SK_HA.sum() < 0.005 * out.PA_UTM_HA.sum() else "VIOLATED - see PER_HD")),
    ], columns=["CHECK", "RESULT"])
    with pd.ExcelWriter(ROOT / "01_BOUNDARY_QA" / "SK_25HD_BOUNDARY_AUDIT.xlsx") as xw:
        summ.to_excel(xw, sheet_name="SUMMARY", index=False)
        out.drop(columns="geometry").to_excel(xw, sheet_name="PER_HD", index=False)
        land.reset_index().to_excel(xw, sheet_name="BY_LANDSCAPE", index=False)
        asg.to_excel(xw, sheet_name="PIECE_ASSIGNMENT", index=False)
        ov.to_excel(xw, sheet_name="SK_OVERLAPS", index=False)
        pd.DataFrame(log, columns=["STEP", "DETAIL"]).astype(str).to_excel(xw, sheet_name="LOG", index=False)
    pd.set_option("display.width", 250)
    print(summ.to_string(index=False))
    print(out[["HD_ID", "HD_NAME", "N_PIECES", "SK_AREA_HA", "SK_GEOM_UTM_HA", "GEOM_MINUS_TABLE_PCT", "PA_INSIDE_SK_PCT",
               "PA_OUTSIDE_SK_HA", "FLAG"]].round(2).to_string(index=False))
    print(land.round(1))


if __name__ == "__main__":
    main(sys.argv[1])
