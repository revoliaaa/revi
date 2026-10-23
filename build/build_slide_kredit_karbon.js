// Builds a one-slide summary of the LPHD carbon credit potential, in the DECK.md visual system.
// Usage: node build/build_slide_kredit_karbon.js <out.pptx> [apply_theme.js path]
const pptxgen = require("pptxgenjs");

const OUT = process.argv[2] || "Potensi_Kredit_Karbon_LPHD.pptx";
const APPLY_THEME = process.argv[3];

const HEX = {
  ink: "1B2420", forest: "163A2E", lindung: "1F5A45", akasia: "9C967F", copper: "B5551F",
  muted: "5F6B65", hair: "D5DBD6", tint: "EEF2EE", leaf: "7FB096", white: "FFFFFF",
};
const THEME = {
  name: "Mayawana Karbon",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: HEX.ink, lt1: HEX.white, dk2: HEX.forest, lt2: HEX.tint,
    accent1: HEX.lindung, accent2: HEX.akasia, accent3: HEX.copper, accent4: HEX.muted,
    accent5: HEX.hair, accent6: HEX.leaf, hlink: HEX.lindung, folHlink: HEX.muted,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "Potensi Kredit Karbon LPHD";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const COL = {
  ink: C.text1, forest: C.text2, white: C.background1, tint: C.background2,
  lindung: C.accent1, akasia: C.accent2, copper: C.accent3, muted: C.accent4, hair: C.accent5, leaf: C.accent6,
};
const DISPLAY = "Cambria";
const W = 13.333, MX = 0.6, CW = W - 2 * MX;

pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: COL.white },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.45, w: 9, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2, margin: 0, valign: "top" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.8, w: CW, h: 1.15, fontFace: DISPLAY, fontSize: 28, bold: true, color: COL.ink, margin: 0, valign: "top", align: "left" }, text: "" } },
  ],
});

function T(s, text, o) {
  s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: COL.ink, valign: "top" }, o));
}
function hline(s, x, y, w) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: COL.hair, width: 0.75 } });
}
// Proportional split bar: segments [{ v, color, name }].
function splitBar(s, x, y, w, h, segs) {
  const tot = segs.reduce((a, b) => a + b.v, 0);
  const gap = 0.03;
  let cx = x;
  segs.forEach((g, i) => {
    const sw = Math.max(0.04, (w - gap * (segs.length - 1)) * g.v / tot);
    s.addShape(pres.shapes.RECTANGLE, { x: cx, y, w: sw, h, fill: { color: g.color }, line: { type: "none" }, objectName: g.name });
    cx += sw + gap;
  });
}

// Data (lembar perhitungan stok karbon LPHD)
const NET_VCU = 9807.43, VCU_LPHD = 5884;
const STOK_CO2E = 5202879, BUFFER = 2601440;
const POOLS = [ // [pool, ton C, ton CO2e]
  ["AGB", 10477, 38415], ["BGB", 30, 111], ["Litter", 314, 1152], ["Soil", 92387, 338752], ["Tuplah", 1315759, 4824448],
];
const STOK_C = 1418967;
const HA_ARR = 1443.1, HA_REDD = 1025.4;
const RP = { // [harga USD, porsi LPHD Rp, keseluruhan Rp]
  rows: [[5, 529601059, 882668431], [10, 1059202117, 1765336862], [15, 1588803176, 2648005293], [20, 2118404234, 3530673724]],
};
const fmt = (n) => n.toLocaleString("id-ID");
const fmt1 = (n) => n.toLocaleString("id-ID", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const pct = (n) => fmt1(n * 100) + "%";
const M = (rp) => Math.round(rp / 1e7); // Rp miliar ×100, shown with COMMA2

const s = pres.addSlide({ masterName: "CONTENT" });
s.addText("POTENSI KREDIT KARBON  ·  LPHD", { placeholder: "kicker" });
s.addText("Porsi LPHD 5.884 VCU bernilai Rp 0,53–2,12 miliar pada harga karbon 5–20 USD per VCU", { placeholder: "title" });
s.addNotes(
  "Net VCU seluruh areal 9.807,43 (setelah buffer 2.601.440 tCO2e dari stok 5.202.879 tCO2e). Porsi LPHD 60% = 5.884 VCU.\n" +
  "Nilai porsi LPHD: 20 USD Rp 2.118.404.234; 15 USD Rp 1.588.803.176; 10 USD Rp 1.059.202.117; 5 USD Rp 529.601.059.\n" +
  "Nilai keseluruhan (100%): 20 USD Rp 3.530.673.724; 15 USD Rp 2.648.005.293; 10 USD Rp 1.765.336.862; 5 USD Rp 882.668.431.\n" +
  "Kurs tersirat sekitar Rp18.000/USD. Stok per pool (tCO2e): AGB 38.415; BGB 111; serasah 1.152; tanah 338.752; tuplah 4.824.448.\n" +
  "Luas: hutan 1.443,1 ha (ARR), terdegradasi 1.025,4 ha (REDD).");

// ---- left: carbon stock -> credits table ----
const lx = MX, lw = 5.5;
const tblBase = { fontFace: "Calibri", fontSize: 12, color: HEX.ink, margin: [0.02, 0.08, 0.02, 0.08], valign: "middle" };
const th = (t, align = "right") => ({ text: t, options: { bold: true, color: HEX.muted, align, border: [{ type: "none" }, { type: "none" }, { pt: 1, color: HEX.hair }, { type: "none" }] } });
const rule = { pt: 0.75, color: HEX.hair };
const td = (t, o = {}) => ({ text: t, options: Object.assign({ align: "right", border: [{ type: "none" }, { type: "none" }, rule, { type: "none" }] }, o) });
const tl = (t, o = {}) => td(t, Object.assign({ align: "left" }, o));
const strong = { bold: true, color: HEX.lindung };
const stokRows = [[th("Pool", "left"), th("Ton karbon"), th("Ton CO₂e")]];
POOLS.forEach((p) => stokRows.push([tl(p[0]), td(fmt(p[1])), td(fmt(p[2]))]));
stokRows.push([tl("Total stok karbon", { bold: true }), td(fmt(STOK_C), { bold: true }), td(fmt(STOK_CO2E), { bold: true })]);
stokRows.push([tl("Buffer"), td(""), td(fmt(BUFFER))]);
stokRows.push([tl("Net VCU (100%)", strong), td(""), td(NET_VCU.toLocaleString("id-ID", { minimumFractionDigits: 2 }), strong)]);
stokRows.push([tl("Porsi LPHD (60%)", strong), td(""), td(fmt(VCU_LPHD), strong)]);
T(s, "Stok karbon dan kredit", { x: lx, y: 2.05, w: lw, h: 0.3, fontSize: 13, bold: true, color: COL.muted });
s.addTable(stokRows, Object.assign({ x: lx, y: 2.4, w: lw, colW: [2.1, 1.6, 1.8], rowH: 0.32, objectName: "tabel-stok" }, tblBase));

const ay = 6.15;
T(s, [{ text: "Luas areal  ", options: { fontSize: 12, color: COL.muted } },
      { text: fmt1(HA_ARR + HA_REDD) + " ha", options: { fontSize: 12, bold: true } }], { x: lx, y: ay, w: lw, h: 0.26 });
const wArr = (lw - 0.03) * HA_ARR / (HA_ARR + HA_REDD);
splitBar(s, lx, ay + 0.32, lw, 0.18, [
  { v: HA_ARR, color: COL.forest, name: "luas-arr" },
  { v: HA_REDD, color: COL.leaf, name: "luas-redd" },
]);
T(s, "Hutan · ARR  " + fmt1(HA_ARR) + " ha", { x: lx, y: ay + 0.58, w: wArr, h: 0.24, fontSize: 11, color: COL.muted });
T(s, "Terdegradasi · REDD  " + fmt1(HA_REDD) + " ha", { x: lx + wArr + 0.03, y: ay + 0.58, w: lw - wArr - 0.03, h: 0.24, fontSize: 11, color: COL.muted });

// ---- right: credit value per price scenario ----
const rx = 6.6, rw = W - MX - rx;
const COMMA2 = '0\\,00';
s.addChart(pres.charts.BAR, [
  { name: "Porsi LPHD (60%)", labels: RP.rows.map((r) => r[0] + " USD/VCU"), values: RP.rows.map((r) => M(r[1])) },
  { name: "Keseluruhan (100%)", labels: RP.rows.map((r) => r[0] + " USD/VCU"), values: RP.rows.map((r) => M(r[2])) },
], {
  x: rx, y: 1.95, w: rw, h: 3.05, barDir: "col", barGrouping: "clustered", barGapWidthPct: 55,
  chartColors: [HEX.lindung, HEX.hair],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: COMMA2,
  dataLabelFontFace: "+mn-lt", dataLabelColor: HEX.ink, dataLabelFontSize: 12,
  catAxisLabelColor: HEX.muted, catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 12,
  valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 420,
  valGridLine: { style: "none" }, catGridLine: { style: "none" },
  showTitle: true, title: "Potensi kredit karbon per skenario harga, Rp miliar",
  titleFontFace: "+mn-lt", titleColor: HEX.muted, titleFontSize: 12,
  showLegend: true, legendPos: "t", legendFontSize: 11, legendColor: HEX.muted, legendFontFace: "+mn-lt",
});
const rpRows = [[th("Harga", "left"), th("Porsi LPHD 60% (Rp)"), th("Keseluruhan 100% (Rp)")]];
RP.rows.slice().reverse().forEach((r) => rpRows.push([tl(r[0] + " USD/VCU"), td(fmt(r[1]), { bold: true, color: HEX.lindung }), td(fmt(r[2]))]));
s.addTable(rpRows, Object.assign({ x: rx, y: 5.15, w: rw, colW: [1.6, 2.2, rw - 3.8], rowH: 0.3, objectName: "tabel-skenario" }, tblBase));

T(s, "Kurs tersirat ±Rp18.000/USD. Sumber: perhitungan stok karbon LPHD.",
  { x: rx, y: 6.8, w: rw, h: 0.24, fontSize: 10, color: COL.muted, italic: true });

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (APPLY_THEME) {
    const { applyTheme } = require(APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("wrote", OUT);
})();
