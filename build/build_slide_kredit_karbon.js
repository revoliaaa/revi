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
const POOL = { tuplah: 4824448, soil: 338752, lain: 38415 + 111 + 1152 }; // AGB + BGB + serasah
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
s.addText("Porsi LPHD 5.884 VCU bernilai Rp 0,53–2,12 miliar, tergantung harga karbon 5–20 USD", { placeholder: "title" });
s.addNotes(
  "Net VCU seluruh areal 9.807,43 (setelah buffer 2.601.440 tCO2e dari stok 5.202.879 tCO2e). Porsi LPHD 60% = 5.884 VCU.\n" +
  "Nilai porsi LPHD: 20 USD Rp 2.118.404.234; 15 USD Rp 1.588.803.176; 10 USD Rp 1.059.202.117; 5 USD Rp 529.601.059.\n" +
  "Nilai keseluruhan (100%): 20 USD Rp 3.530.673.724; 15 USD Rp 2.648.005.293; 10 USD Rp 1.765.336.862; 5 USD Rp 882.668.431.\n" +
  "Kurs tersirat sekitar Rp18.000/USD. Stok per pool (tCO2e): AGB 38.415; BGB 111; serasah 1.152; tanah 338.752; tuplah 4.824.448.\n" +
  "Luas: hutan 1.443,1 ha (ARR), terdegradasi 1.025,4 ha (REDD).");

// ---- left column: key figures ----
const lx = MX, lw = 4.3;
T(s, [{ text: fmt(VCU_LPHD), options: { fontFace: DISPLAY, fontSize: 54, bold: true, color: COL.lindung, breakLine: true } },
      { text: "VCU porsi LPHD (60%)", options: { fontSize: 15, bold: true } }], { x: lx, y: 2.1, w: lw, h: 1.35 });
T(s, [{ text: "dari ", options: { fontSize: 14, color: COL.muted } },
      { text: NET_VCU.toLocaleString("id-ID", { minimumFractionDigits: 2 }), options: { fontSize: 14, bold: true } },
      { text: " net VCU seluruh areal, setelah buffer " + fmt(BUFFER) + " tCO₂e", options: { fontSize: 14, color: COL.muted } }],
  { x: lx, y: 3.5, w: lw, h: 0.55 });

hline(s, lx, 4.25, lw);
T(s, [{ text: "Stok karbon  ", options: { fontSize: 13, color: COL.muted } },
      { text: fmt(STOK_CO2E) + " tCO₂e", options: { fontSize: 13, bold: true } }], { x: lx, y: 4.4, w: lw, h: 0.3 });
splitBar(s, lx, 4.78, lw, 0.24, [
  { v: POOL.tuplah, color: COL.lindung, name: "pool-tuplah" },
  { v: POOL.soil, color: COL.akasia, name: "pool-tanah" },
  { v: POOL.lain, color: COL.hair, name: "pool-lain" },
]);
const totPool = POOL.tuplah + POOL.soil + POOL.lain;
T(s, "Tuplah " + pct(POOL.tuplah / totPool) + "  ·  tanah " + pct(POOL.soil / totPool) + "  ·  AGB, BGB, serasah " + pct(POOL.lain / totPool),
  { x: lx, y: 5.1, w: lw, h: 0.28, fontSize: 11, color: COL.muted });

hline(s, lx, 5.55, lw);
T(s, [{ text: "Luas areal  ", options: { fontSize: 13, color: COL.muted } },
      { text: fmt1(HA_ARR + HA_REDD) + " ha", options: { fontSize: 13, bold: true } }], { x: lx, y: 5.7, w: lw, h: 0.3 });
const wArr = (lw - 0.03) * HA_ARR / (HA_ARR + HA_REDD);
splitBar(s, lx, 6.08, lw, 0.24, [
  { v: HA_ARR, color: COL.forest, name: "luas-arr" },
  { v: HA_REDD, color: COL.leaf, name: "luas-redd" },
]);
T(s, [{ text: "Hutan · ARR", options: { fontSize: 11, color: COL.muted, breakLine: true } },
      { text: fmt1(HA_ARR) + " ha", options: { fontSize: 12, bold: true } }], { x: lx, y: 6.4, w: wArr, h: 0.45 });
T(s, [{ text: "Terdegradasi · REDD", options: { fontSize: 11, color: COL.muted, breakLine: true } },
      { text: fmt1(HA_REDD) + " ha", options: { fontSize: 12, bold: true } }], { x: lx + wArr + 0.03, y: 6.4, w: lw - wArr - 0.03, h: 0.45 });

// ---- right: revenue by price scenario ----
const rx = 5.5, rw = W - MX - rx;
const COMMA2 = '0\\,00';
s.addChart(pres.charts.BAR, [
  { name: "Porsi LPHD (60%)", labels: RP.rows.map((r) => r[0] + " USD/VCU"), values: RP.rows.map((r) => M(r[1])) },
  { name: "Keseluruhan (100%)", labels: RP.rows.map((r) => r[0] + " USD/VCU"), values: RP.rows.map((r) => M(r[2])) },
], {
  x: rx, y: 2.0, w: rw, h: 4.55, barDir: "col", barGrouping: "clustered", barGapWidthPct: 55,
  chartColors: [HEX.lindung, HEX.hair],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: COMMA2,
  dataLabelFontFace: "+mn-lt", dataLabelColor: HEX.ink, dataLabelFontSize: 13,
  catAxisLabelColor: HEX.muted, catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 13,
  valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 400,
  valGridLine: { style: "none" }, catGridLine: { style: "none" },
  showTitle: true, title: "Nilai kredit per skenario harga, Rp miliar",
  titleFontFace: "+mn-lt", titleColor: HEX.muted, titleFontSize: 12,
  showLegend: true, legendPos: "t", legendFontSize: 12, legendColor: HEX.muted, legendFontFace: "+mn-lt",
});

T(s, "Kurs tersirat ±Rp18.000/USD. Sumber: perhitungan stok karbon LPHD (AGB, BGB, serasah, tanah, tuplah).",
  { x: rx, y: 6.72, w: rw, h: 0.28, fontSize: 10, color: COL.muted, italic: true });

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (APPLY_THEME) {
    const { applyTheme } = require(APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("wrote", OUT);
})();
