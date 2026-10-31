"""Build the ADMIN-DESA CONTEXT domain: the 25 BPS desa polygons whose names
match the 25 HD.

IMPORTANT: this is NOT the Hutan Desa (SK) boundary and NOT the carbon Project
Area. Desa polygons contain settlements, agriculture and plantations outside the
HD, and coastal desa polygons may omit intertidal mangrove that lies inside an HD.
The domain is used only (i) as landscape context and (ii) to test that the
zonal-statistics pipeline runs correctly before the Project Area shapefile is
supplied.

Usage: python s01_build_context_domain.py <path/to/idn_admin_boundaries.gdb>
"""
import sys

import geopandas as gpd
import pandas as pd
import pyogrio
from shapely.validation import explain_validity

from common import AOI_BBOX, HD_COLS, HD_TABLE, ROOT, _GEOD


def geodesic_ha(geom):
    return abs(_GEOD.geometry_area_perimeter(geom)[0]) / 1e4


def main(gdb):
    raw = pyogrio.read_dataframe(gdb, layer="idn_admin4",
                                 where="adm2_name IN ('Kubu Raya','Kayong Utara')")
    hd = pd.DataFrame(HD_TABLE, columns=HD_COLS)
    rows = []
    for r in hd.itertuples():
        m = raw[(raw.adm4_name == r.ADMIN_DESA) & (raw.adm3_name == r.KECAMATAN)
                & (raw.adm2_name == r.REGENCY)]
        if len(m) != 1:
            raise SystemExit(f"{r.HD_NAME}: expected 1 desa match, got {len(m)}")
        g = m.iloc[0]
        rows.append({**r._asdict(), "ADMIN_PCODE": g.adm4_pcode, "BPS_AREA_SQKM_ATTR": g.area_sqkm,
                     "BPS_VERSION": g.version, "BPS_VALID_ON": str(g.valid_on)[:10], "geometry": g.geometry})
    gdf = gpd.GeoDataFrame(rows, crs=raw.crs).drop(columns=["Index"])
    gdf["SPATIAL_DOMAIN"] = "ADMIN_DESA_CONTEXT (BPS 2020) - NOT HD, NOT PROJECT AREA"

    # --- QA ---
    gdf["IS_VALID"] = gdf.geometry.is_valid
    gdf["VALIDITY_NOTE"] = gdf.geometry.apply(explain_validity)
    gdf["N_PARTS"] = gdf.geometry.apply(lambda g: len(getattr(g, "geoms", [g])))
    gdf["GEODESIC_AREA_HA"] = gdf.geometry.apply(geodesic_ha)
    gdf["ATTR_VS_GEODESIC_PCT"] = 100 * (gdf.BPS_AREA_SQKM_ATTR * 100 - gdf.GEODESIC_AREA_HA) / gdf.GEODESIC_AREA_HA
    b = gdf.total_bounds
    gdf["INSIDE_AOI"] = (b[0] >= AOI_BBOX[0]) & (b[1] >= AOI_BBOX[1]) & (b[2] <= AOI_BBOX[2]) & (b[3] <= AOI_BBOX[3])

    # pairwise overlaps (geodesic ha)
    ov = []
    sidx = gdf.sindex
    for i, gi in enumerate(gdf.geometry):
        for j in sidx.query(gi, predicate="intersects"):
            if j <= i:
                continue
            inter = gi.intersection(gdf.geometry.iloc[j])
            a = geodesic_ha(inter) if not inter.is_empty else 0.0
            if a > 0.01:
                ov.append({"A": gdf.HD_ID.iloc[i], "B": gdf.HD_ID.iloc[j], "OVERLAP_HA": a})
    ov = pd.DataFrame(ov, columns=["A", "B", "OVERLAP_HA"])

    out = ROOT / "01_BOUNDARY_QA"
    gdf.to_file(out / "CONTEXT_DOMAIN_25DESA_BPS2020.gpkg", layer="desa_context", driver="GPKG")
    qa = gdf.drop(columns="geometry")
    land = qa.groupby("LANDSCAPE")["GEODESIC_AREA_HA"].sum().rename("DESA_GEODESIC_HA").to_frame()
    with pd.ExcelWriter(out / "CONTEXT_DOMAIN_25DESA_QA.xlsx") as xw:
        pd.DataFrame({"ITEM": ["Source", "Layer", "Version", "Valid on", "CRS", "AOI bbox", "Total bounds",
                               "Features", "All valid", "Pairwise overlaps > 0.01 ha", "Total geodesic area (ha)",
                               "Caveat"],
                      "VALUE": ["HDX COD-AB Indonesia (BPS / OCHA ROAP), idn_admin_boundaries.gdb", "idn_admin4",
                                gdf.BPS_VERSION.iloc[0], gdf.BPS_VALID_ON.iloc[0], str(gdf.crs), str(AOI_BBOX),
                                str(tuple(round(x, 4) for x in b)), len(gdf), bool(gdf.IS_VALID.all()),
                                len(ov), round(gdf.GEODESIC_AREA_HA.sum(), 1),
                                "Administrative village polygons; NOT Hutan Desa SK boundary and NOT carbon Project Area."]}
                     ).to_excel(xw, sheet_name="SUMMARY", index=False)
        qa.to_excel(xw, sheet_name="PER_DESA", index=False)
        land.reset_index().to_excel(xw, sheet_name="BY_LANDSCAPE", index=False)
        ov.to_excel(xw, sheet_name="OVERLAPS", index=False)
    print(qa[["HD_ID", "HD_NAME", "ADMIN_DESA", "GEODESIC_AREA_HA", "ATTR_VS_GEODESIC_PCT", "IS_VALID", "N_PARTS"]].round(2).to_string())
    print(land.round(0))
    print("bounds", b, "inside AOI", bool(gdf.INSIDE_AOI.all()), "overlaps", len(ov))


if __name__ == "__main__":
    main(sys.argv[1])
