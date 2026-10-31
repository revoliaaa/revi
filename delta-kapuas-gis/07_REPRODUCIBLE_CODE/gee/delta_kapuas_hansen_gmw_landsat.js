/****************************************************************************************
 * Delta Kapuas 25-HD — Google Earth Engine replica of the Python workflow
 * STATUS: NOT EXECUTED in this study (no Earth Engine credentials were available).
 *         The Python scripts in ../src were executed and are the reference results.
 *         Use this script for independent replication; differences > 0.5 % in any
 *         per-HD area should be investigated (rasterisation rule, pixel-area method).
 *
 * Inputs (upload as assets first):
 *   PROJECT_AREA : 25 Project Area polygons with fields HD_ID, HD_NAME, LANDSCAPE
 *                  (output of s06_project_area_qa.py -> PROJECT_AREA_25HD_CLEAN.gpkg)
 *   or CONTEXT   : 01_BOUNDARY_QA/CONTEXT_DOMAIN_25DESA_BPS2020.gpkg (desa context only)
 ****************************************************************************************/

// ---- 1. Inputs -------------------------------------------------------------------------
var polygons = ee.FeatureCollection('projects/YOUR_PROJECT/assets/PROJECT_AREA_25HD_CLEAN'); // EDIT
var gfc = ee.Image('UMD/hansen/global_forest_change_2025_v1_13');
var thresholds = [10, 30, 50];
var years = ee.List.sequence(2001, 2025);
var pixelArea = ee.Image.pixelArea().divide(1e4);   // geodesic m2 -> ha

// ---- 2. Hansen tree cover 2000 and annual gross loss per HD ---------------------------
function hansenStats(t) {
  var tc = gfc.select('treecover2000').gt(t);            // GFW convention: canopy > t %
  var lossyear = gfc.select('lossyear');
  var bands = ee.Image.cat(
    years.map(function (y) {
      y = ee.Number(y);
      return pixelArea.updateMask(tc.and(lossyear.eq(y.subtract(2000))))
        .rename(ee.String('LOSS_').cat(y.format('%d')).cat('_GT' + t));
    })
  ).addBands(pixelArea.updateMask(tc).rename('TC2000_GT' + t + '_HA'));
  return bands.reduceRegions({
    collection: polygons, reducer: ee.Reducer.sum(),
    scale: 30, crs: gfc.select('lossyear').projection()    // native Hansen grid
  });
}
thresholds.forEach(function (t) {
  Export.table.toDrive({collection: hansenStats(t), description: 'HANSEN_ZONAL_GT' + t,
                        fileFormat: 'CSV'});
});

// ---- 3. Global Mangrove Watch v3 (community catalog) -----------------------------------
// GMW v3 is published in the awesome-gee-community-catalog; confirm asset path before use.
var gmw = ee.ImageCollection('projects/earthengine-legacy/assets/projects/sat-io/open-datasets/GMW/extent/gmw_v3');
// Each image = one year; reduce pixelArea masked by the mangrove image per polygon (as for Hansen).

// ---- 4. Landsat C2 L2 OLI epoch composites (2014, 2019, 2024) --------------------------
function maskL2(img) {
  var qa = img.select('QA_PIXEL');
  var bad = qa.bitwiseAnd(parseInt('11111', 2)).neq(0);   // fill, dilated cloud, cirrus, cloud, shadow
  var sr = img.select(['SR_B3', 'SR_B4', 'SR_B5', 'SR_B6']).multiply(0.0000275).add(-0.2);
  var ok = sr.reduce(ee.Reducer.min()).gte(0).and(sr.reduce(ee.Reducer.max()).lte(1));
  return sr.rename(['G', 'R', 'NIR', 'SWIR1']).updateMask(bad.not().and(ok))
           .copyProperties(img, ['system:time_start']);
}
function indices(img) {
  return ee.Image.cat(
    img.normalizedDifference(['NIR', 'R']).rename('NDVI'),
    img.normalizedDifference(['NIR', 'SWIR1']).rename('NDMI'),
    img.normalizedDifference(['G', 'SWIR1']).rename('MNDWI'));
}
function composite(year, sensors) {
  var col = ee.ImageCollection([]);
  sensors.forEach(function (s) { col = col.merge(ee.ImageCollection(s)); });
  col = col.filterBounds(polygons.geometry())
           .filterDate(year + '-01-01', year + '-12-31')
           .filter(ee.Filter.lt('CLOUD_COVER', 80))
           .map(maskL2).map(indices);
  return col.median().addBands(col.select('NDVI').count().rename('NOBS'));
}
var L8 = 'LANDSAT/LC08/C02/T1_L2', L9 = 'LANDSAT/LC09/C02/T1_L2';
var comps = {2014: composite(2014, [L8]), 2019: composite(2019, [L8]), 2024: composite(2024, [L8, L9])};
Object.keys(comps).forEach(function (y) {
  Export.image.toDrive({image: comps[y].toFloat(), description: 'LANDSAT_OLI_MEDIAN_' + y,
                        region: polygons.geometry().bounds(), scale: 30, crs: 'EPSG:4326', maxPixels: 1e10});
});
// NOTE: Python version uses Planetary Computer (same USGS C2 L2 product) and only path/row 121/061;
// GEE will include adjacent path/rows if they intersect -> observation counts can differ.
