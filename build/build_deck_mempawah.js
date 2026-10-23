// Builds the interpretation deck for the Mempawah peat carbon review (see analisis-gambut-mempawah/DECK.md).
// Usage: node build/build_deck_mempawah.js <out.pptx> [apply_theme.js path]
const pptxgen = require("pptxgenjs");

const OUT = process.argv[2] || "Interpretasi_Karbon_Gambut_Mempawah.pptx";
const APPLY_THEME = process.argv[3];

const HEX = {
  ink: "1E1C19", peat: "2B241E", forest: "2F5D46", shrub: "8C9A5B", estate: "C08A3E",
  open: "B9AE9C", river: "3F7C85", alert: "B23A2E", muted: "6B655E", hair: "DCD8D2",
  tint: "F0F1EE", sage: "A9C2B1", white: "FFFFFF",
};
const THEME = {
  name: "Gambut Mempawah",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: HEX.ink, lt1: HEX.white, dk2: HEX.peat, lt2: HEX.tint,
    accent1: HEX.forest, accent2: HEX.shrub, accent3: HEX.estate, accent4: HEX.alert,
    accent5: HEX.muted, accent6: HEX.sage, hlink: HEX.forest, folHlink: HEX.muted,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "Interpretasi Review Perhitungan Karbon Gambut — Hutan Desa, KHG Sungai Mempawah";
pres.author = "Review perhitungan karbon";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const COL = {
  ink: C.text1, peat: C.text2, white: C.background1, tint: C.background2,
  forest: C.accent1, shrub: C.accent2, estate: C.accent3, alert: C.accent4, muted: C.accent5, sage: C.accent6,
};
const DISPLAY = "Cambria";
const W = 13.333, MX = 0.6, CW = W - 2 * MX;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: COL.white },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.45, w: 9, h: 0.3, fontSize: 12, bold: true, color: COL.forest, charSpacing: 2, margin: 0, valign: "top" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.8, w: CW, h: 1.15, fontFace: DISPLAY, fontSize: 28, bold: true, color: COL.ink, margin: 0, valign: "top", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.23, y: 6.92, w: 0.5, h: 0.25, fontSize: 10, color: COL.muted, align: "right" },
});
pres.defineSlideMaster({
  title: "COVER",
  background: { color: COL.peat },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.9, w: CW, h: 0.35, fontSize: 14, bold: true, color: COL.sage, charSpacing: 3, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 1.4, w: 11, h: 1.7, fontFace: DISPLAY, fontSize: 40, bold: true, color: COL.white, margin: 0, valign: "top", align: "left" }, text: "" } },
  ],
});

// ---------- helpers ----------
function T(s, text, o) {
  s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: COL.ink, valign: "top" }, o));
}
let sectionTitle = "";
function section(t) { sectionTitle = t; pres.addSection({ title: t }); }
function slide(master, kicker, title, notes) {
  const s = pres.addSlide({ masterName: master, sectionTitle });
  if (kicker) s.addText(kicker, { placeholder: "kicker" });
  if (title) s.addText(title, { placeholder: "title" });
  if (notes) s.addNotes(notes);
  return s;
}
function source(s, text, dark) {
  T(s, text, { x: MX + 4.1, y: 6.93, w: CW - 4.8, h: 0.25, fontSize: 10, color: dark ? COL.sage : COL.muted, italic: true });
}
function hline(s, x, y, w, color, width = 0.75) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: color || COL.hair, width } });
}
function arrow(s, x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    flipH: x2 < x1, flipV: y2 < y1, line: { color, width: 1.5, endArrowType: "triangle" },
  });
}
function chip(s, text, x, y, w, color) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.34, rectRadius: 0.17, fill: { color }, line: { type: "none" } });
  T(s, text, { x, y, w, h: 0.34, fontSize: 11, bold: true, color: COL.white, align: "center", valign: "middle" });
}
const id = (n, d = 0) => n.toLocaleString("id-ID", { minimumFractionDigits: d, maximumFractionDigits: d });

// Signature element: the 2026 land-cover bar of the 2.468,5 ha Hutan Desa.
const LC = [
  { k: "hs", name: "Hutan sekunder", ha: 1411.16, col: COL.forest },
  { k: "sb", name: "Semak belukar", ha: 608.69, col: COL.shrub },
  { k: "kb", name: "Perkebunan", ha: 359.14, col: COL.estate },
  { k: "lt", name: "Lahan terbuka", ha: 57.6, col: "B9AE9C" },
  { k: "sg", name: "Sungai", ha: 31.92, col: "3F7C85" },
];
const LC_TOT = LC.reduce((a, b) => a + b.ha, 0);
function lcBar(s, x, y, w, h, focus, dark) {
  const gap = Math.max(0.02, w * 0.004);
  const usable = w - gap * (LC.length - 1);
  let cx = x; const pos = {};
  LC.forEach((seg) => {
    const sw = usable * seg.ha / LC_TOT;
    const on = !focus || focus.includes(seg.k);
    s.addShape(pres.shapes.RECTANGLE, { x: cx, y, w: sw, h, fill: { color: on ? seg.col : (dark ? "453B32" : HEX.hair) }, line: { type: "none" }, objectName: "tutupan-" + seg.k });
    pos[seg.k] = { x: cx, w: sw };
    cx += sw + gap;
  });
  return pos;
}
function locator(s, focus, label) {
  lcBar(s, MX, 7.0, 1.6, 0.1, focus);
  T(s, label, { x: MX + 1.75, y: 6.93, w: 2.3, h: 0.25, fontSize: 10, color: COL.muted });
}

const NUM = '[>=1000]0"."000;0'; // thousands with a dot, independent of Office locale
const CHART_BASE = () => ({
  catAxisLabelColor: HEX.muted, valAxisLabelColor: HEX.muted, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  dataLabelFontFace: "+mn-lt", dataLabelColor: HEX.ink, dataLabelFontSize: 13, catAxisLabelFontSize: 13,
  valGridLine: { style: "none" }, catGridLine: { style: "none" }, showValue: true,
  titleFontFace: "+mn-lt", titleColor: HEX.muted, titleFontSize: 12, showTitle: true, dataLabelFormatCode: NUM,
});

// Figures from analisis-gambut-mempawah/Model_Koreksi_Karbon_Gambut_Mempawah.xlsx (recalculated).
const M = {
  cForest: 135.15, cPost: 14.8, efBio: 441.3, efPeatAdd: 12.65, rateA: 8.29, rateB: 27.62,
  baseA: 4233, netA: 1238, netB: 4126, netLowStock: 745, netBLowStock: 2483, factor: 0.2924,
  kurs: 16000, lphd: 0.6,
};
const rp = (t, usd) => t * M.lphd * usd * M.kurs / 1e6; // Rp juta / tahun

// =====================================================================
section("Pembuka");

// 1 · Cover
{
  const s = slide("COVER", "REVIEW PERHITUNGAN KARBON  ·  HUTAN DESA, KHG SUNGAI MEMPAWAH",
    "Datanya valid, angka kreditnya belum",
    "Deck ini menafsirkan hasil review file Export_Output_Gambut_MEMPAWAH_1.xlsx. Pesan utamanya: data spasial (luas, kedalaman gambut, tutupan lahan) konsisten dan bisa dipakai; tetapi cara menghitung emisi dan kredit belum valid, sehingga angka kredit di file 4 sampai 13 kali terlalu tinggi. Batang di bawah adalah tutupan lahan 2026 seluas 2.468,5 ha — batang yang sama muncul kecil di kiri bawah setiap slide untuk menunjukkan bagian areal yang sedang dibahas.");
  T(s, "Kredit karbon realistis ±1.200–4.100 tCO₂e per tahun, bukan 13.700–15.600 tCO₂e seperti di file — dan additionality masih harus dibuktikan", { x: MX, y: 2.75, w: 10.2, h: 0.9, fontSize: 18, color: "D9D2C8" });
  const y = 4.55, h = 0.62;
  const pos = lcBar(s, MX, y, CW, h, null, true);
  const lab = (k, t1, t2, x, w) => T(s, [{ text: t1, options: { fontFace: DISPLAY, fontSize: 22, bold: true, color: COL.white, breakLine: true } },
    { text: t2, options: { fontSize: 13, color: "D9D2C8" } }], { x, y: y + h + 0.18, w, h: 0.8 });
  lab("hs", "1.411 ha", "Hutan sekunder", pos.hs.x, pos.hs.w);
  lab("sb", "609 ha", "Semak belukar", pos.sb.x, pos.sb.w);
  lab("kb", "359 ha", "Perkebunan", pos.kb.x, 2.0);
  T(s, "Lahan terbuka 57,6 · Sungai 31,9 ha", { x: W - MX - 3.2, y: y - 0.38, w: 3.2, h: 0.3, fontSize: 12, color: "D9D2C8", align: "right" });
  T(s, "OKTOBER 2026", { x: W - MX - 3, y: 0.9, w: 3, h: 0.35, fontSize: 14, bold: true, color: COL.sage, charSpacing: 3, align: "right" });
  T(s, "Tutupan lahan 2026 · total 2.468,5 ha · sumber: interpretasi citra pada file asal (sheet 2021)", { x: MX, y: 6.9, w: 9, h: 0.25, fontSize: 10, color: COL.sage, italic: true });
}

// 2 · Executive summary
{
  const s = slide("CONTENT", "KESIMPULAN",
    "Data spasial bisa dipakai; metode emisi harus diganti sebelum angka kredit dibawa ke pembeli",
    "Data spasial: luas overlay tutupan PL2022 × kedalaman gambut cocok dengan sheet Gambut (453,93 / 1.586 / 428,57 ha). Neraca tutupan 2016, 2021, 2026 masing-masing 2.468,5 ha. Kehilangan hutan bruto 82,87 ha dikurangi penambahan 41,94 ha = penurunan neto 40,91 ha.\n\nPerhitungan: ada empat kesalahan utama — emisi dari stok seluruh kolom gambut × 1,16%, laju 1,16% tanpa sumber, faktor 'Additional 43%' sebagai pengali, serta salah ketik/rujukan sel.\n\nKredit: model koreksi menghasilkan ±1.240 tCO2e/thn (konservatif) sampai ±4.130 tCO2e/thn (laju 2021–2026), dibandingkan 13.745–15.642 tCO2e/thn di file.");
  const rows = [
    ["DATA SPASIAL", "Valid.", "Luas per kedalaman, neraca tutupan lahan tiap tahun, dan matriks perubahan hutan saling cocok.", COL.forest],
    ["PERHITUNGAN", "Belum valid.", "Emisi dihitung dari stok seluruh kolom gambut × laju tanpa sumber; biomassa pohon tidak masuk.", COL.alert],
    ["KREDIT", "4–13× terlalu tinggi.", "Model koreksi: ±1.240–4.130 tCO₂e/thn. File: 13.745–15.642 tCO₂e/thn.", COL.alert],
  ];
  const x0 = MX, wL = 7.9, y0 = 2.2, rh = 1.3;
  rows.forEach((r, i) => {
    const y = y0 + i * rh;
    if (i > 0) hline(s, x0, y - 0.15, wL);
    s.addShape(pres.shapes.OVAL, { x: x0, y: y + 0.05, w: 0.42, h: 0.42, fill: { color: r[3] }, line: { type: "none" } });
    T(s, r[0], { x: x0 + 0.8, y, w: 3, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 2 });
    T(s, [{ text: r[1] + " ", options: { bold: true } }, { text: r[2] }], { x: x0 + 0.8, y: y + 0.32, w: wL - 0.8, h: 0.8, fontSize: 15 });
  });
  const px = 9.0, pw = W - MX - px;
  s.addShape(pres.shapes.RECTANGLE, { x: px, y: 2.05, w: pw, h: 3.9, fill: { color: COL.peat }, line: { type: "none" }, objectName: "panel-rekomendasi" });
  T(s, "REKOMENDASI", { x: px + 0.35, y: 2.4, w: pw - 0.7, h: 0.3, fontSize: 12, bold: true, color: COL.sage, charSpacing: 2 });
  T(s, "Pakai model koreksi sebagai baseline kerja, lalu kumpulkan bukti additionality sebelum membicarakan harga.", { x: px + 0.35, y: 2.8, w: pw - 0.7, h: 2.9, fontFace: DISPLAY, fontSize: 20, bold: true, color: COL.white });
  source(s, "Rincian 22 temuan: sheet Daftar_Temuan di Model_Koreksi_Karbon_Gambut_Mempawah.xlsx");
  locator(s, null, "Seluruh areal 2.468,5 ha");
}

// =====================================================================
section("Kondisi areal");

// 3 · Peat
{
  const s = slide("CONTENT", "GAMBUT",
    "Hampir seluruh areal bergambut, dan 2.015 ha di antaranya berstatus fungsi lindung",
    "Overlay PL2022 × peta kedalaman (sheet Export_Output): bergambut <50 cm 453,93 ha (fungsi budidaya EG, KHG Mempawah–Peniti); gambut 100–200 cm 1.586,01 ha dan 200–300 cm 428,57 ha (fungsi lindung EG, KHG Mempawah–Duri).\nStok C = luas × tebal × 10.000 × BD × fraksi C. Dengan BD 0,11/0,08/0,06 dan C 0,51 dari file: 63.664 + 970.638 + 327.856 = 1.362.158 tC (4,99 juta tCO2e). Rerata tertimbang 551,8 tC/ha — bukan jumlah kerapatan dibagi 3 seperti di file.\nPenting: stok ini adalah cadangan. Deforestasi tidak melepas seluruh kolom gambut sekaligus; emisi gambut terjadi bertahap lewat drainase (FE per ha per tahun) dan kebakaran.");
  s.addChart(pres.charts.BAR, [{ name: "Luas (ha)", labels: ["Bergambut < 50 cm", "Gambut 100–200 cm", "Gambut 200–300 cm"], values: [454, 1586, 429] }],
    Object.assign(CHART_BASE(), {
      x: MX, y: 2.1, w: 7.6, h: 4.2, barDir: "bar", barGapWidthPct: 45, chartColors: [HEX.shrub, HEX.forest, HEX.peat],
      dataLabelPosition: "outEnd", valAxisHidden: true, valAxisMaxVal: 1900, catAxisLineShow: false,
      title: "Luas per kelas kedalaman gambut, ha", showLegend: false,
    }));
  const sx = 8.9, sw = W - MX - sx;
  [["1,36 juta tC", "stok karbon gambut (4,99 juta tCO₂e)", COL.ink], ["82%", "areal di fungsi lindung ekosistem gambut", COL.forest], ["Cadangan", "bukan emisi — gambut lepas bertahap lewat drainase dan kebakaran", COL.alert]].forEach((r, i) => {
    const y = 2.2 + i * 1.35;
    if (i > 0) hline(s, sx, y - 0.2, sw);
    T(s, [{ text: r[0], options: { fontFace: DISPLAY, fontSize: 28, bold: true, color: r[2], breakLine: true } },
          { text: r[1], options: { fontSize: 14, color: COL.muted } }], { x: sx, y, w: sw, h: 1.1 });
  });
  source(s, "Sumber: sheet Export_Output & Gambut (file asal); BD dan fraksi C perlu dikonfirmasi uji lab.");
  locator(s, null, "Seluruh areal 2.468,5 ha");
}

// 4 · Land-cover change
{
  const s = slide("CONTENT", "PERUBAHAN TUTUPAN 2016–2026",
    "Dalam lima tahun terakhir hutan hilang 138 ha dan perkebunan melonjak dari 26 ha menjadi 359 ha",
    "Tutupan per tahun (ha):\nHutan sekunder 1.452,07 → 1.549,28 → 1.411,16\nSemak belukar 967,94 → 857,33 → 608,69\nPerkebunan 6,33 → 26,04 → 359,14\nLahan terbuka 0 → 0 → 57,6\nMatriks 2016–2026: hutan → lahan terbuka 55,22 ha; hutan → kebun 7,85 ha; hutan → semak 19,81 ha (bruto 82,87 ha); semak → hutan 41,94 ha.\nIni bukti ancaman yang nyata (dipakai untuk additionality dan leakage), tetapi kenaikan hutan +97 ha pada 2016→2021 harus dijelaskan — regenerasi atau beda interpretasi citra?");
  const yrs = ["2016", "2021", "2026"];
  s.addChart(pres.charts.BAR, [
    { name: "Hutan sekunder", labels: yrs, values: [1452, 1549, 1411] },
    { name: "Semak belukar", labels: yrs, values: [968, 857, 609] },
    { name: "Perkebunan", labels: yrs, values: [6, 26, 359] },
    { name: "Lahan terbuka", labels: yrs, values: [0, 0, 58] },
  ], Object.assign(CHART_BASE(), {
    x: MX, y: 2.1, w: 8.2, h: 4.25, barDir: "col", barGrouping: "clustered", barGapWidthPct: 50,
    chartColors: [HEX.forest, HEX.shrub, HEX.estate, HEX.open], dataLabelPosition: "outEnd", dataLabelFontSize: 11,
    valAxisHidden: true, valAxisMaxVal: 1750, title: "Luas tutupan lahan, ha",
    showLegend: true, legendPos: "t", legendFontSize: 12, legendColor: HEX.muted, legendFontFace: "+mn-lt",
  }));
  const sx = 9.3, sw = W - MX - sx;
  [["−138 ha", "hutan sekunder, 2021→2026 (1,8%/thn)", COL.alert], ["13,8×", "luas perkebunan, 2021→2026", COL.estate], ["+97 ha", "hutan 2016→2021 — wajib dijelaskan ke VVB", COL.muted]].forEach((r, i) => {
    const y = 2.2 + i * 1.35;
    if (i > 0) hline(s, sx, y - 0.2, sw);
    T(s, [{ text: r[0], options: { fontFace: DISPLAY, fontSize: 28, bold: true, color: r[2], breakLine: true } },
          { text: r[1], options: { fontSize: 14, color: COL.muted } }], { x: sx, y, w: sw, h: 1.1 });
  });
  source(s, "Sumber: sheet 2021 dan Tuplah (2) file asal.");
  locator(s, ["hs", "kb", "lt"], "Hutan, kebun, lahan terbuka");
}

// =====================================================================
section("Validitas perhitungan");

// 5 · Core error: method comparison
{
  const s = slide("CONTENT", "KESALAHAN INTI",
    "File menghitung emisi dari stok seluruh kolom gambut; yang hilang saat deforestasi adalah biomassa dan oksidasi bertahap",
    "Rumus di file (Tuplah!P53, Tuplah (2)!Q41): emisi tahunan = total stok CO2e gambut seluruh area (termasuk semak, kebun, lahan terbuka; seluruh kolom 1,5 m) × 1,16%. Konsekuensinya: (1) gambut di lahan non-hutan ikut dihitung sebagai 'hutan yang terdeforestasi'; (2) seluruh kolom gambut dianggap teroksidasi; (3) karbon pohon tidak masuk sama sekali.\n\nCara yang benar: emisi tahun t = luas deforestasi tahun t × (stok C biomassa hutan − stok C pasca) × 44/12 + luas kumulatif terdeforestasi × (FE gambut pasca − FE gambut hutan). Kredit bersih = baseline × efektivitas × (1 − leakage) × (1 − buffer) × (1 − ketidakpastian).");
  const colW = (CW - 0.5) / 2, y0 = 2.2;
  const steps = (x, head, color, items) => {
    chip(s, head, x, y0, 2.6, color);
    items.forEach((t, i) => {
      const y = y0 + 0.65 + i * 0.95;
      s.addShape(pres.shapes.RECTANGLE, { x, y, w: colW, h: 0.72, fill: { color: COL.tint }, line: { type: "none" } });
      T(s, t[0], { x: x + 0.2, y: y + 0.1, w: 0.5, h: 0.5, fontFace: DISPLAY, fontSize: 20, bold: true, color });
      T(s, t[1], { x: x + 0.75, y: y + 0.08, w: colW - 0.95, h: 0.6, fontSize: 14, valign: "middle" });
      if (i < items.length - 1) arrow(s, x + colW / 2, y + 0.74, x + colW / 2, y + 0.93, HEX.muted);
    });
  };
  steps(MX, "DI FILE", COL.alert, [
    ["1", "Stok C gambut seluruh areal (2,15 juta tC), termasuk lahan non-hutan"],
    ["×", "Laju 1,16%/thn — sumber tidak tercatat"],
    ["×", "\"Additional 43%\" dipakai sebagai pengali"],
    ["=", "Biomassa pohon tidak masuk; satu kolom gambut dianggap lepas"],
  ]);
  steps(MX + colW + 0.5, "SEHARUSNYA", COL.forest, [
    ["1", "Luas deforestasi per tahun dari data aktivitas yang terverifikasi"],
    ["×", "Selisih stok biomassa: 135,1 → 14,8 tC/ha (441 tCO₂/ha)"],
    ["+", "Oksidasi gambut kumulatif: +12,6 tCO₂/ha/thn di lahan terdeforestasi"],
    ["×", "Efektivitas × (1 − leakage) × (1 − buffer) — additionality diuji terpisah"],
  ]);
  source(s, "Rumus koreksi diterapkan di sheet Baseline_REDD (model koreksi).");
  locator(s, ["hs"], "Hutan sekunder 1.411 ha");
}

// 6 · Four blocks, four numbers
{
  const s = slide("CONTENT", "HASIL YANG SALING BERTENTANGAN",
    "Empat blok di file memberi empat angka kredit berbeda — semuanya jauh dari hasil model koreksi",
    "Kredit bersih per tahun (tCO2e):\nTuplah (2)!S46 (×0,65): 15.642\nTuplah!R57 (×0,35): 13.745\nTuplah (2)!G57 (blok IKHB): 9.807 — memakai AGB 22291 (salah ketik ×100) dan menjumlah per-ha dengan total\nTuplah (2)!S36: 6 — Q31 merujuk tCO2e per ha (P37), bukan total\nModel koreksi: 4.126 (laju neto 2021–2026, 27,6 ha/thn) dan 1.238 (laju bruto 2016–2026, 8,29 ha/thn).\nAsumsi pengurang model koreksi: efektivitas 43% (diambil dari angka 'Additional' file), leakage 15%, buffer 20% → faktor 0,29.");
  const labels = ["File · Tuplah (2) S46", "File · Tuplah R57", "File · blok IKHB G57", "Koreksi · laju 2021–26", "Koreksi · konservatif", "File · Tuplah (2) S36"];
  s.addChart(pres.charts.BAR, [{ name: "tCO₂e/thn", labels, values: [15642, 13745, 9807, 4126, 1238, 6] }],
    Object.assign(CHART_BASE(), {
      x: MX, y: 2.1, w: 8.4, h: 4.3, barDir: "bar", barGapWidthPct: 40,
      chartColors: [HEX.alert, HEX.alert, HEX.alert, HEX.forest, HEX.forest, HEX.alert],
      dataLabelPosition: "outEnd", valAxisHidden: true, valAxisMaxVal: 19000, catAxisLineShow: false, catAxisOrientation: "maxMin",
      title: "Kredit bersih, tCO₂e per tahun", showLegend: false,
    }));
  const sx = 9.5, sw = W - MX - sx;
  T(s, [{ text: "3,8–12,6×", options: { fontFace: DISPLAY, fontSize: 40, bold: true, color: COL.alert, breakLine: true } },
        { text: "selisih angka file terhadap model koreksi", options: { fontSize: 15, bold: true } }], { x: sx, y: 2.25, w: sw, h: 1.5 });
  hline(s, sx, 3.95, sw);
  T(s, "Angka 6 tCO₂e/thn juga salah: sel Q31 mengambil nilai per hektare, bukan total areal.", { x: sx, y: 4.1, w: sw, h: 1.4, fontSize: 15, color: COL.muted });
  source(s, "Model koreksi: rerata 10 tahun; efektivitas 43%, leakage 15%, buffer 20%.");
  locator(s, ["hs"], "Hutan sekunder 1.411 ha");
}

// 7 · Error table
{
  const s = slide("CONTENT", "TEMUAN TEKNIS",
    "Salah ketik dan salah rujukan sel melipatgandakan angka hingga 100 kali",
    "Daftar lengkap 22 temuan ada di sheet Daftar_Temuan. Yang ditampilkan di sini adalah kesalahan mekanis (bukan metodologis) yang paling besar dampaknya. Semua bisa diperbaiki cepat, tetapi menunjukkan perlunya satu tabel parameter yang dirujuk oleh semua rumus, bukan angka yang diketik ulang di setiap blok.");
  const H = (t) => ({ text: t, options: { bold: true, color: HEX.muted, fontSize: 12 } });
  const rows = [[H("Lokasi"), H("Masalah"), H("Dampak")]];
  [
    ["Tuplah (2) B57, B59, C60", "AGB 22291, litter 66876, tanah 196568 — seharusnya 222,91 / 668,73 / 1.965,68", "Nilai ×100; baris BGB benar (64,64)"],
    ["Tuplah (2) Q31", "Merujuk P37 = tCO₂e per ha, bukan total", "Kredit 6 tCO₂e/thn"],
    ["Tuplah D55, D63 · Tuplah (2) D33, D43", "Kolom stok memakai kolom emisi (C), bukan luas (B)", "Stok kebun 14,8–23,4 juta tC"],
    ["Tuplah (2) D34", "Fraksi C diketik 45, bukan 0,45", "Stok semak 27,4 juta tC"],
    ["Tuplah (2) C61–D64", "Biomassa per-ha dijumlah dengan stok total, lalu ×50% dan ×35", "Satuan bercampur"],
    ["Antar-blok", "Tebal 0,25–1,5 m; BD 0,06–0,13; fraksi C 0,2–0,55; stok hutan 79,7 / 98,8 / 135,1 tC/ha", "Stok gambut 0,8–34,5 juta tC"],
    ["Tuplah R52 · Tuplah (2) S30", "\"Net VCU\" ×0,35 di satu blok, ×0,65 di blok lain; kurs 18.000 vs 16.000", "Hasil berbeda ±2×"],
  ].forEach((r) => rows.push(r.map((t, j) => ({ text: t, options: j === 2 ? { color: HEX.alert } : {} }))));
  s.addTable(rows, {
    x: MX, y: 2.05, w: CW, colW: [3.2, 5.6, 3.33], rowH: 0.52, fontSize: 13, color: HEX.ink, fontFace: "Calibri",
    margin: [0.05, 0.1, 0.05, 0.1], valign: "middle",
    border: { type: "solid", pt: 0.75, color: HEX.hair },
  });
  source(s, "Sumber: pemeriksaan rumus & nilai tersimpan pada file asal (22 temuan).");
  locator(s, null, "Seluruh areal 2.468,5 ha");
}

// 8 · Corrected model flow
{
  const s = slide("CONTENT", "MODEL KOREKSI",
    "Dengan data proyek sendiri, baseline ±4.230 tCO₂e/thn menghasilkan ±1.240 tCO₂e kredit bersih per tahun",
    "Parameter (sheet Parameter): AGB 222,91 + BGB 64,64 t BK/ha × 0,47 = 135,15 tC/ha. Stok pasca-deforestasi ditimbang menurut matriks 2016–2026: lahan terbuka 2,5 (67%), perkebunan 63 (9%), semak 30 (24%) = 14,8 tC/ha. Faktor emisi biomassa = (135,15 − 14,8) × 44/12 = 441,3 tCO2/ha.\nFE gambut pasca tertimbang: 35/40/19 → 31,65; dikurangi FE hutan terdrainase 19 = +12,65 tCO2/ha/thn per ha terdeforestasi (kumulatif).\nLaju bruto 2016–2026 = 82,87/10 = 8,29 ha/thn. Baseline rerata 10 tahun = 3.657 (biomassa) + 577 (gambut) = 4.233 tCO2e/thn. Kredit bersih = 4.233 × 0,43 × 0,85 × 0,80 = 1.238 tCO2e/thn.\nTidak termasuk: kebakaran, DOC, CH4/N2O (konservatif). Untuk VM0048, laju diganti data aktivitas yurisdiksi Verra.");
  const items = [
    ["8,29", "ha/thn", "Laju deforestasi bruto 2016–2026"],
    ["441", "tCO₂/ha", "Emisi biomassa saat hutan dibuka"],
    ["+12,6", "tCO₂/ha/thn", "Tambahan oksidasi gambut, kumulatif"],
    ["4.233", "tCO₂e/thn", "Baseline, rerata 10 tahun"],
    ["× 0,29", "", "Efektivitas 43% · leakage 15% · buffer 20%"],
  ];
  const n = items.length, gap = 0.22, bw = (CW - gap * (n - 1) - 2.6) / n;
  items.forEach((it, i) => {
    const x = MX + i * (bw + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y: 2.35, w: bw, h: 2.2, fill: { color: COL.tint }, line: { type: "none" } });
    T(s, [{ text: it[0], options: { fontFace: DISPLAY, fontSize: 28, bold: true, breakLine: true } }, { text: it[1] || " ", options: { fontSize: 12, color: COL.muted } }],
      { x: x + 0.15, y: 2.5, w: bw - 0.3, h: 0.95, align: "center" });
    T(s, it[2], { x: x + 0.15, y: 3.55, w: bw - 0.3, h: 0.9, fontSize: 13, align: "center" });
  });
  const rx = MX + n * (bw + gap);
  s.addShape(pres.shapes.RECTANGLE, { x: rx, y: 2.35, w: W - MX - rx, h: 2.2, fill: { color: COL.forest }, line: { type: "none" } });
  T(s, [{ text: "1.238", options: { fontFace: DISPLAY, fontSize: 36, bold: true, color: COL.white, breakLine: true } }, { text: "tCO₂e/thn kredit bersih", options: { fontSize: 13, color: COL.white } }],
    { x: rx + 0.15, y: 2.6, w: W - MX - rx - 0.3, h: 1.6, align: "center" });
  T(s, "Belum termasuk: emisi kebakaran gambut, DOC, CH₄/N₂O. Tanpa itu, baseline sengaja konservatif.", { x: MX, y: 4.95, w: CW, h: 0.4, fontSize: 14, color: COL.muted });
  T(s, "Untuk registrasi Verra (VM0048), laju dan lokasi deforestasi baseline diambil dari data aktivitas yurisdiksi yang disediakan Verra, bukan dari laju proyek sendiri.", { x: MX, y: 5.45, w: CW, h: 0.7, fontSize: 14, color: COL.muted });
  source(s, "Sheet Baseline_REDD, Model_Koreksi_Karbon_Gambut_Mempawah.xlsx.");
  locator(s, ["hs"], "Hutan sekunder 1.411 ha");
}

// 9 · Sensitivity + value to LPHD
{
  const s = slide("CONTENT", "SENSITIVITAS & NILAI UNTUK LPHD",
    "Pilihan laju deforestasi mengubah kredit 3,3 kali; nilai bagi LPHD jutaan, bukan miliaran rupiah per tahun",
    "Matriks sensitivitas kredit bersih rerata (tCO2e/thn): stok hutan 135,1 tC/ha → 1.238 (laju 8,29 ha/thn) / 4.126 (laju 27,6 ha/thn); stok 79,67 tC/ha → 745 / 2.483.\nNilai porsi LPHD = kredit × 60% × harga × Rp 16.000. Skenario konservatif: USD 5 → Rp 59 juta; USD 10 → Rp 119 juta; USD 15 → Rp 178 juta per tahun. Skenario laju 2021–2026: Rp 198 / 396 / 594 juta per tahun. File asal mencantumkan ±Rp 3,7 miliar per tahun pada USD 15.\nHarga REDD+ di pasar sukarela beberapa tahun terakhir umumnya di bawah USD 15 kecuali ada label/premium kualitas; perlakukan USD 15 sebagai skenario atas.");
  const gx = MX, gy = 2.75, cw2 = 2.35, ch = 1.1, lw = 2.5;
  T(s, "Laju 8,29 ha/thn", { x: gx + lw, y: gy - 0.45, w: cw2, h: 0.35, fontSize: 13, bold: true, color: COL.muted, align: "center" });
  T(s, "Laju 27,6 ha/thn", { x: gx + lw + cw2 + 0.1, y: gy - 0.45, w: cw2, h: 0.35, fontSize: 13, bold: true, color: COL.muted, align: "center" });
  const mat = [["Stok hutan 135,1 tC/ha", 1238, 4126], ["Stok hutan 79,7 tC/ha", 745, 2483]];
  mat.forEach((r, i) => {
    const y = gy + i * (ch + 0.1);
    T(s, r[0], { x: gx, y, w: lw - 0.15, h: ch, fontSize: 13, bold: true, color: COL.muted, valign: "middle" });
    [r[1], r[2]].forEach((v, j) => {
      const x = gx + lw + j * (cw2 + 0.1);
      const strong = i === 0 && j === 0;
      s.addShape(pres.shapes.RECTANGLE, { x, y, w: cw2, h: ch, fill: { color: strong ? COL.forest : COL.tint }, line: { type: "none" } });
      T(s, [{ text: id(v), options: { fontFace: DISPLAY, fontSize: 28, bold: true, color: strong ? COL.white : COL.ink, breakLine: true } },
            { text: "tCO₂e/thn", options: { fontSize: 12, color: strong ? COL.white : COL.muted } }], { x, y: y + 0.15, w: cw2, h: ch - 0.2, align: "center" });
    });
  });
  T(s, "Kotak hijau = asumsi dasar model koreksi.", { x: gx, y: gy + 2 * (ch + 0.1) + 0.05, w: 7.5, h: 0.3, fontSize: 12, color: COL.muted });
  const sx = 8.3, sw = W - MX - sx;
  T(s, "PORSI LPHD (60%), RP JUTA PER TAHUN", { x: sx, y: 2.3, w: sw, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 1 });
  const H = (t) => ({ text: t, options: { bold: true, color: HEX.muted, fontSize: 12, align: "right" } });
  const rows = [[{ text: "Harga", options: { bold: true, color: HEX.muted, fontSize: 12 } }, H("Konservatif"), H("Laju 2021–26")]];
  [5, 10, 15].forEach((p) => rows.push([{ text: "USD " + p, options: {} }, { text: id(rp(M.netA, p)), options: { align: "right" } }, { text: id(rp(M.netB, p)), options: { align: "right" } }]));
  rows.push([{ text: "File asal, USD 15", options: { color: HEX.alert } }, { text: "±3.750", options: { color: HEX.alert, align: "right", bold: true } }, { text: "", options: {} }]);
  s.addTable(rows, { x: sx, y: 2.7, w: sw, colW: [1.7, 1.38, 1.35], rowH: 0.48, fontSize: 15, color: HEX.ink, fontFace: "Calibri", margin: [0.04, 0.08, 0.04, 0.08], valign: "middle", border: { type: "solid", pt: 0.75, color: HEX.hair } });
  T(s, "Kurs Rp 16.000/USD diseragamkan; USD 15 adalah skenario atas untuk REDD+.", { x: sx, y: 5.3, w: sw, h: 0.7, fontSize: 13, color: COL.muted });
  source(s, "Sheet Sensitivitas & Baseline_REDD (model koreksi).");
  locator(s, ["hs"], "Hutan sekunder 1.411 ha");
}

// =====================================================================
section("Additionality & leakage");

// 10 · Additionality
{
  const s = slide("CONTENT", "ADDITIONALITY",
    "Titik terlemah additionality adalah hukum: gambut lindung memang sudah dilarang dibuka",
    "Additionality bukan faktor pengali — hapus 'Additional 43%' dari rumus; bila maksudnya seberapa besar proyek menekan deforestasi, namai 'efektivitas proyek' dan dukung dengan rencana kegiatan.\n\nUji (mis. alat VCS VT0008):\n1. Regulatory surplus — PP 71/2014 jo. PP 57/2016 melarang pembukaan/drainase di fungsi lindung EG, sehingga harus dibuktikan larangan tidak ditegakkan. Bukti tersedia: hutan −138 ha, kebun 26→359 ha, lahan terbuka baru 57,6 ha. Tambah hotspot/area terbakar (FIRMS/SiPongi), catatan penegakan hukum, laju deforestasi di KHG yang sama di luar proyek.\n2. Hambatan investasi — arus kas LPHD dengan dan tanpa karbon; daftar dana publik yang sudah masuk (BRGM, dana desa, PS) agar tidak diklaim ulang.\n3. Praktik umum — bandingkan dengan Hutan Desa lain di KHG Mempawah tanpa proyek karbon.\nTambahan: jelaskan +97 ha hutan 2016→2021; uji akurasi peta ≥85–90%; daftar SRN-PPI; cegah klaim ganda; otorisasi/corresponding adjustment bila dijual internasional.");
  const tests = [
    ["1", "Regulatory surplus", "RAWAN", COL.alert, "Fungsi lindung EG sudah melarang pembukaan dan drainase. Buktikan larangan tidak ditegakkan.", "Data sendiri: hutan −138 ha, kebun 26→359 ha. Tambah hotspot, catatan penegakan, laju di luar proyek."],
    ["2", "Hambatan investasi", "PERLU DATA", COL.estate, "LPHD tidak punya dana untuk patroli, sekat kanal, regu damkar, rehabilitasi tanpa karbon.", "Arus kas dengan/tanpa karbon; daftar dana BRGM, dana desa, PS yang sudah masuk."],
    ["3", "Praktik umum", "PERLU DATA", COL.estate, "Perlindungan aktif belum umum di Hutan Desa sekitar.", "Bandingkan Hutan Desa lain di KHG Mempawah tanpa proyek karbon."],
  ];
  const y0 = 2.1, rh = 1.2;
  T(s, "UJI", { x: MX + 0.7, y: y0, w: 3, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 2 });
  T(s, "MENGAPA", { x: MX + 4.6, y: y0, w: 3, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 2 });
  T(s, "BUKTI YANG DIPERLUKAN", { x: MX + 8.4, y: y0, w: 3.7, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 2 });
  tests.forEach((t, i) => {
    const y = y0 + 0.45 + i * rh;
    hline(s, MX, y - 0.1, CW);
    T(s, t[0], { x: MX, y, w: 0.6, h: 0.7, fontFace: DISPLAY, fontSize: 32, bold: true, color: t[3] });
    T(s, t[1], { x: MX + 0.7, y, w: 3.6, h: 0.4, fontSize: 16, bold: true });
    chip(s, t[2], MX + 0.7, y + 0.5, 1.6, t[3]);
    T(s, t[4], { x: MX + 4.6, y, w: 3.55, h: 1.15, fontSize: 14 });
    T(s, t[5], { x: MX + 8.4, y, w: CW - 8.4, h: 1.15, fontSize: 14, color: COL.muted });
  });
  T(s, "Hapus \"Additional 43%\" dari rumus: additionality adalah uji lulus/gagal, bukan pengali emisi.", { x: MX, y: 6.25, w: CW, h: 0.4, fontSize: 15, bold: true, color: COL.alert });
  source(s, "Dasar: PP 71/2014 jo. PP 57/2016; alat additionality VCS (VT0008).");
  locator(s, ["hs", "kb", "lt"], "Hutan, kebun, lahan terbuka");
}

// 11 · ARR eligibility
{
  const s = slide("CONTENT", "KELAYAKAN ARR",
    "Dari 1.025 ha yang dihitung sebagai ARR, hanya ±591 ha kandidat kuat",
    "Luas ARR di file (Tuplah (2)!C68) = 591,26 + 82,87 + 351,3 = 1.025,43 ha.\n• 591,26 ha semak belukar stabil: kandidat kuat ARR dan pembasahan ulang. Di gambut terdrainase, ARR tanpa rewetting tetap menghasilkan emisi gambut di skenario proyek. Rewetting dapat menurunkan FE dari ±19 menuju mendekati 0 tCO2/ha/thn — berpotensi lebih besar dari serapan pohon — tetapi butuh desain hidrologi tingkat KHG.\n• 82,87 ha hutan yang hilang 2016–2026: tidak eligible ARR di VCS (dibuka <10 tahun sebelum proyek); masuk akuntansi REDD+.\n• 351,3 ha perkebunan aktif: jangan dijadikan ARR murni karena memicu activity-shifting leakage; jadikan zona paludikultur/agroforestri.\nLuas REDD+ di file (1.443,06 ha) juga memasukkan sungai 31,92 ha — keluarkan.");
  const parts = [
    { v: 591.26, name: "Semak belukar stabil", note: "Kandidat ARR + pembasahan ulang", col: COL.forest },
    { v: 351.3, name: "Perkebunan aktif", note: "Paludikultur/agroforestri, bukan ARR", col: COL.estate },
    { v: 82.87, name: "Hutan hilang 2016–2026", note: "Tidak eligible ARR → akuntansi REDD+", col: COL.alert },
  ];
  const tot = parts.reduce((a, b) => a + b.v, 0), by = 2.5, bh = 0.9, gap = 0.04;
  let x = MX; const usable = CW - gap * 2;
  parts.forEach((p, i) => {
    const w = usable * p.v / tot;
    s.addShape(pres.shapes.RECTANGLE, { x, y: by, w, h: bh, fill: { color: p.col }, line: { type: "none" } });
    T(s, id(p.v, 0) + " ha", { x: x + 0.15, y: by, w: Math.max(w - 0.3, 0.9), h: bh, fontFace: DISPLAY, fontSize: i === 2 ? 16 : 24, bold: true, color: COL.white, valign: "middle" });
    x += w + gap;
  });
  T(s, "Total 1.025 ha diklaim ARR di file", { x: MX, y: by - 0.4, w: 6, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 1 });
  const cw3 = (CW - 0.6) / 3;
  parts.forEach((p, i) => {
    const xx = MX + i * (cw3 + 0.3), yy = 3.85;
    s.addShape(pres.shapes.OVAL, { x: xx, y: yy + 0.05, w: 0.28, h: 0.28, fill: { color: p.col }, line: { type: "none" } });
    T(s, [{ text: p.name, options: { bold: true, fontSize: 16, breakLine: true } }, { text: p.note, options: { fontSize: 14, color: COL.muted } }], { x: xx + 0.45, y: yy, w: cw3 - 0.45, h: 1.0 });
  });
  hline(s, MX, 5.15, CW);
  T(s, "Di gambut terdrainase, ARR tanpa pembasahan ulang tetap mengeluarkan emisi gambut. Pembasahan ulang bisa menurunkan FE dari ±19 menuju mendekati 0 tCO₂/ha/thn, tetapi perlu desain hidrologi di tingkat KHG.", { x: MX, y: 5.3, w: CW, h: 0.8, fontSize: 14 });
  source(s, "Sumber: Tuplah (2)!C68 file asal; aturan VCS ARR (tidak ada pembukaan ekosistem alami 10 thn sebelum proyek).");
  locator(s, ["sb", "kb", "lt"], "Semak, kebun, lahan terbuka");
}

// 12 · Leakage
{
  const s = slide("CONTENT", "LEAKAGE",
    "Leakage di gambut punya empat jalur; yang terbesar adalah 359 ha kebun yang bisa berpindah",
    "1. Activity-shifting: jangan gusur kebun 359 ha — jadikan zona paludikultur/agroforestri (jelutung rawa, sagu, kopi liberika). Petakan pelaku pembukaan lahan; intensifikasi lahan budidaya yang ada di luar kubah gambut (zona <50 cm, 454 ha). Tetapkan sabuk leakage di KHG yang sama, pantau dengan citra & periode yang sama. Potongan 15% di model adalah sementara.\n2. Market leakage: relevan bila produksi komoditas turun; dengan paludikultur produksi tetap ada.\n3. Hidrologis (khas gambut): kanal di luar batas mengeringkan gambut di dalam dan sebaliknya. Batas mengikuti sub-KHG atau diberi zona penyangga; inventarisasi kanal; sekat kanal bersama BRGM, desa, konsesi sekitar; pantau TMAT di dalam & luar (target ≤ 0,4 m, PP 57/2016).\n4. Kebakaran: dihitung sebagai risiko reversal di buffer non-permanen (kemungkinan >20%). MPA/regu damkar, sumur bor, peringatan dini berbasis hotspot.");
  // nested zones diagram
  const dx = MX, dy = 2.1, dw = 5.4, dh = 4.4;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: dx, y: dy, w: dw, h: dh, rectRadius: 0.25, fill: { color: COL.tint }, line: { color: HEX.hair, width: 1 } });
  T(s, "KHG Sungai Mempawah", { x: dx + 0.25, y: dy + 0.15, w: 4, h: 0.3, fontSize: 12, bold: true, color: COL.muted });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: dx + 0.5, y: dy + 0.6, w: dw - 1.0, h: dh - 1.0, rectRadius: 0.22, fill: { color: COL.white }, line: { color: HEX.estate, width: 1.5, dashType: "dash" } });
  T(s, "Sabuk leakage", { x: dx + 0.75, y: dy + 0.75, w: 3, h: 0.3, fontSize: 12, bold: true, color: COL.estate });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: dx + 1.1, y: dy + 1.3, w: dw - 2.2, h: dh - 2.3, rectRadius: 0.18, fill: { color: COL.forest }, line: { type: "none" } });
  T(s, [{ text: "Hutan Desa", options: { bold: true, fontSize: 15, breakLine: true } }, { text: "2.468,5 ha", options: { fontFace: DISPLAY, fontSize: 24, bold: true } }],
    { x: dx + 1.1, y: dy + 1.3, w: dw - 2.2, h: dh - 2.3, color: COL.white, align: "center", valign: "middle" });
  const ways = [
    ["Pemindahan kegiatan", "Kebun 359 ha → zona paludikultur/agroforestri, bukan digusur. Pantau sabuk leakage.", COL.estate],
    ["Pasar", "Abaikan secara terdokumentasi bila produksi tetap berjalan lewat paludikultur.", COL.shrub],
    ["Hidrologi", "Batas ikut sub-KHG; sekat kanal bersama BRGM & tetangga; pantau TMAT ≤ 0,4 m.", "3F7C85"],
    ["Kebakaran", "Risiko reversal → buffer >20%; regu damkar, sumur bor, peringatan dini.", COL.alert],
  ];
  const lx = 6.5, lw2 = W - MX - lx;
  ways.forEach((w, i) => {
    const y = 2.15 + i * 1.08;
    if (i > 0) hline(s, lx, y - 0.12, lw2);
    T(s, String(i + 1), { x: lx, y, w: 0.5, h: 0.6, fontFace: DISPLAY, fontSize: 26, bold: true, color: w[2] });
    T(s, [{ text: w[0], options: { bold: true, fontSize: 16, breakLine: true } }, { text: w[1], options: { fontSize: 14, color: COL.muted } }], { x: lx + 0.6, y, w: lw2 - 0.6, h: 0.95 });
  });
  source(s, "Potongan leakage 15% di model bersifat sementara — ganti dengan hasil modul metodologi terpilih.");
  locator(s, ["kb"], "Perkebunan 359 ha");
}

// =====================================================================
section("Langkah berikutnya");

// 13 · Close
{
  const s = slide("COVER", "LANGKAH BERIKUTNYA",
    "Perbaiki data aktivitas dulu; harga dan pembeli menyusul",
    "Urutan kerja yang disarankan:\n1. Satu peta tutupan resolusi tinggi untuk 2016, 2021, 2026 + uji akurasi + matriks perubahan bruto per periode (termasuk 2021–2026).\n2. Satu tabel parameter: BD dan %C gambut dari lab per kelas kedalaman; stok biomassa hutan dari plot (SNI 7724:2019, CI 90%).\n3. Pilih jalur: Verra VM0048 + komponen WRC, atau skema domestik SPE-GRK; ganti laju dan faktor indikatif dengan nilai metodologi.\n4. Susun bab additionality dan rencana pengelolaan leakage di PDD.\n5. Hitung buffer dengan AFOLU Non-Permanence Risk Tool; seragamkan kurs dan pakai harga pasar terkini.\nLangkah pertama yang bisa dimulai minggu ini: pengadaan citra resolusi tinggi dan rencana ground check.");
  const steps = [
    ["01", "Satu peta tutupan", "Citra resolusi tinggi 2016/2021/2026, uji akurasi, matriks per periode"],
    ["02", "Satu tabel parameter", "BD & %C gambut dari lab; stok biomassa dari plot"],
    ["03", "Pilih metodologi", "VM0048 + WRC, atau skema domestik SPE-GRK"],
    ["04", "Bab PDD", "Additionality dan rencana pengelolaan leakage"],
    ["05", "Buffer & harga", "Non-Permanence Risk Tool; kurs dan harga terkini"],
  ];
  const n = steps.length, gap = 0.25, bw = (CW - gap * (n - 1)) / n, y = 3.3;
  steps.forEach((st, i) => {
    const x = MX + i * (bw + gap);
    const first = i === 0;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: bw, h: 2.4, fill: { color: first ? COL.forest : "3A3129" }, line: { type: "none" } });
    T(s, st[0], { x: x + 0.2, y: y + 0.2, w: bw - 0.4, h: 0.6, fontFace: DISPLAY, fontSize: 28, bold: true, color: first ? COL.white : COL.sage });
    T(s, [{ text: st[1], options: { bold: true, fontSize: 16, color: COL.white, breakLine: true } }, { text: st[2], options: { fontSize: 13, color: "D9D2C8" } }],
      { x: x + 0.2, y: y + 0.85, w: bw - 0.4, h: 1.45 });
  });
  T(s, "Mulai minggu ini: pengadaan citra resolusi tinggi dan rencana ground check.", { x: MX, y: 6.0, w: CW, h: 0.4, fontSize: 16, bold: true, color: COL.sage });
  lcBar(s, MX, 7.0, 1.6, 0.1, null, true);
  T(s, "Seluruh areal 2.468,5 ha", { x: MX + 1.75, y: 6.93, w: 3, h: 0.25, fontSize: 10, color: COL.sage });
}

// =====================================================================
section("Lampiran");

// 14 · Parameters
{
  const s = slide("CONTENT", "LAMPIRAN · PARAMETER MODEL KOREKSI",
    "Semua angka kredit di deck ini berasal dari parameter berikut — ubah di sheet Parameter",
    "Semua parameter dapat diubah di sheet Parameter pada Model_Koreksi_Karbon_Gambut_Mempawah.xlsx; sel kuning adalah asumsi kunci yang wajib dijustifikasi di PDD.");
  const H = (t) => ({ text: t, options: { bold: true, color: HEX.muted, fontSize: 12 } });
  const rows = [[H("Parameter"), H("Nilai"), H("Sumber")]];
  [
    ["Stok C biomassa hutan rawa sekunder", "135,1 tC/ha", "(AGB 222,91 + BGB 64,64) × 0,47 — file asal; verifikasi plot"],
    ["Stok C pasca-deforestasi (tertimbang)", "14,8 tC/ha", "Lahan terbuka 2,5 · kebun 63 · semak 30 (sheet Tutupan lahan)"],
    ["FE gambut hutan / pasca-deforestasi", "19 / 31,6 tCO₂/ha/thn", "IPCC 2013 Wetlands Supplement, Tabel 2.1"],
    ["Laju deforestasi", "8,29 ha/thn (alt. 27,6)", "Bruto 2016–2026 (alt. neto 2021–2026)"],
    ["Efektivitas proyek", "43%", "Angka \"Additional\" file asal — wajib dijustifikasi"],
    ["Leakage / buffer / ketidakpastian", "15% / 20% / 0%", "Indikatif — ganti dengan modul metodologi & NPRT"],
    ["Porsi LPHD · kurs", "60% · Rp 16.000/USD", "File asal; kurs diseragamkan"],
  ].forEach((r) => rows.push(r));
  s.addTable(rows, { x: MX, y: 2.05, w: CW, colW: [4.0, 2.8, 5.33], rowH: 0.5, fontSize: 14, color: HEX.ink, fontFace: "Calibri", margin: [0.05, 0.1, 0.05, 0.1], valign: "middle", border: { type: "solid", pt: 0.75, color: HEX.hair } });
  source(s, "Model_Koreksi_Karbon_Gambut_Mempawah.xlsx · sheet Parameter.");
  locator(s, null, "Seluruh areal 2.468,5 ha");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (APPLY_THEME) {
    const { applyTheme } = require(APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("wrote", OUT);
})();
