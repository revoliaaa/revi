// Builds the Plan Vivo REDD+/ARR area deck from Export_Output_Gambut_M.xlsx figures.
// Same visual identity as build_deck.js (DECK.md). Signature element: the 2.468,51 ha area bar.
// Usage: node build/build_luasan_pv.js <out.pptx> [apply_theme.js path]
const pptxgen = require("pptxgenjs");

const OUT = process.argv[2] || "Luasan_REDD_ARR_Plan_Vivo.pptx";
const APPLY_THEME = process.argv[3];

const HEX = {
  ink: "1B2420", forest: "163A2E", lindung: "1F5A45", akasia: "9C967F", copper: "B5551F",
  amber: "C8901E", leaf: "7FB096", river: "3E78A8",
  muted: "5F6B65", hair: "D5DBD6", tint: "EEF2EE", white: "FFFFFF", pale: "C8D6CD",
};
const THEME = {
  name: "Mayawana Karbon",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: HEX.ink, lt1: HEX.white, dk2: HEX.forest, lt2: HEX.tint,
    accent1: HEX.lindung, accent2: HEX.akasia, accent3: HEX.copper, accent4: HEX.amber,
    accent5: HEX.leaf, accent6: HEX.river, hlink: HEX.lindung, folHlink: HEX.muted,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "Luasan REDD+ dan ARR — Metode Plan Vivo";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const COL = {
  ink: C.text1, forest: C.text2, white: C.background1, tint: C.background2,
  lindung: C.accent1, akasia: C.accent2, copper: C.accent3, amber: C.accent4, leaf: C.accent5, river: C.accent6,
};
const DISPLAY = "Cambria";
const W = 13.333, MX = 0.6, CW = W - 2 * MX;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: COL.white },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.45, w: 9, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2, margin: 0, valign: "top" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.8, w: CW, h: 1.15, fontFace: DISPLAY, fontSize: 28, bold: true, color: COL.ink, margin: 0, valign: "top", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.23, y: 6.92, w: 0.5, h: 0.25, fontSize: 10, color: HEX.muted, align: "right" },
});
pres.defineSlideMaster({
  title: "COVER",
  background: { color: COL.forest },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.9, w: CW, h: 0.35, fontSize: 14, bold: true, color: COL.leaf, charSpacing: 3, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 1.4, w: 11, h: 1.7, fontFace: DISPLAY, fontSize: 40, bold: true, color: COL.white, margin: 0, valign: "top", align: "left" }, text: "" } },
  ],
});

// ---------- helpers ----------
function T(s, text, o) {
  s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: COL.ink, valign: "top" }, o));
}
let sectionTitle = "";
function slide(master, kicker, title, notes) {
  const s = pres.addSlide({ masterName: master, sectionTitle });
  if (kicker) s.addText(kicker, { placeholder: "kicker" });
  if (title) s.addText(title, { placeholder: "title" });
  if (notes) s.addNotes(notes);
  return s;
}
function section(t) { sectionTitle = t; pres.addSection({ title: t }); }
function source(s, text) {
  T(s, text, { x: MX, y: 6.55, w: CW - 0.6, h: 0.25, fontSize: 10, color: HEX.muted, italic: true });
}
function hline(s, x, y, w, color, width = 0.75) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: color || HEX.hair, width } });
}
const fmt = (n, d = 2) => n.toLocaleString("id-ID", { minimumFractionDigits: d, maximumFractionDigits: d });

// Signature element: the 2.468,51 ha area split into six eligibility classes.
const TOTAL = 2468.51;
const SEGS = [
  { k: "redd", name: "REDD+ layak", desc: "Hutan stabil 2016–2026", ha: 1369.20, col: COL.lindung },
  { k: "regen", name: "REDD+ bersyarat", desc: "Hutan regenerasi (semak → hutan)", ha: 41.94, col: COL.leaf },
  { k: "arr", name: "ARR layak", desc: "Semak 588,88 + lahan terbuka 2,38", ha: 591.26, col: COL.amber },
  { k: "kebun", name: "ARR bersyarat", desc: "Kebun, lewat agroforestri", ha: 351.30, col: COL.akasia },
  { k: "defor", name: "Tidak layak ARR", desc: "Bekas hutan yang dibuka 2016–2026", ha: 82.87, col: COL.copper },
  { k: "sungai", name: "Sungai", desc: "Dikeluarkan", ha: 31.92, col: COL.river },
];
function areaBar(s, x, y, w, h, focus, dark) {
  const off = dark ? "2E5246" : HEX.hair; // hex: inactive segment
  const gap = Math.max(0.025, w * 0.003);
  const usable = w - gap * (SEGS.length - 1);
  let cx = x;
  const pos = {};
  SEGS.forEach((g) => {
    const sw = Math.max(usable * g.ha / TOTAL, 0.02);
    const on = !focus || focus.includes(g.k);
    s.addShape(pres.shapes.RECTANGLE, { x: cx, y, w: sw, h, fill: { color: on ? g.col : off }, line: { type: "none" }, objectName: "luas-" + g.k });
    pos[g.k] = { x: cx, w: sw };
    cx += sw + gap;
  });
  return pos;
}
const FOCUS_LABEL = {
  all: "Area 2.468,51 ha",
  redd: "Fokus: hutan 1.411,16 ha (REDD+)",
  arr: "Fokus: non-hutan 1.057,35 ha (ARR)",
};
function locator(s, focusKey) {
  const focus = focusKey === "redd" ? ["redd", "regen"] : focusKey === "arr" ? ["arr", "kebun", "defor", "sungai"] : null;
  areaBar(s, MX, 7.0, 1.6, 0.1, focus, false);
  T(s, FOCUS_LABEL[focusKey], { x: MX + 1.75, y: 6.93, w: 5, h: 0.25, fontSize: 10, color: HEX.muted });
}
// Chart values are stored ×100 and labelled with a literal comma so decimals read "55,22" in any Office locale.
const COMMA2 = "#0\\,00";
const AXIS = { catAxisLabelColor: HEX.muted, valAxisLabelColor: HEX.muted, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", catAxisLabelFontSize: 12, dataLabelFontSize: 12, dataLabelColor: HEX.ink, catAxisLineShow: false, valGridLine: { style: "none" }, catGridLine: { style: "none" } };

// =====================================================================
section("Pembuka");

// 1 · Cover
{
  const s = slide("COVER", "ANALISIS LUASAN  ·  METODE PLAN VIVO (PV CLIMATE)",
    "1.411 ha hutan untuk REDD+, tetapi hanya 591 ha lahan yang layak ARR",
    "Deck ini membagi area 2.468,51 ha di KHG Sungai Mempawah (Kalimantan Barat) menjadi area yang layak REDD+ dan ARR berdasarkan tutupan lahan 2016, 2021 dan 2026. Asumsi: PV dibaca sebagai Plan Vivo; syarat 10 tahun mengikuti praktik VCS/CDM dan perlu dicek ke PV Climate Requirements terbaru.");
  T(s, "Pembagian area 2.468,51 ha di KHG Sungai Mempawah berdasarkan tutupan lahan 2016, 2021 dan 2026", { x: MX, y: 3.15, w: 10, h: 0.5, fontSize: 16, color: HEX.pale });
  const y = 4.6, h = 0.62;
  const pos = areaBar(s, MX, y, CW, h, null, true);
  const forestW = pos.regen.x + pos.regen.w - MX;
  T(s, [{ text: "1.411,16 ha", options: { fontFace: DISPLAY, fontSize: 24, bold: true, color: COL.white, breakLine: true } },
        { text: "Hutan 2026 · kandidat REDD+", options: { fontSize: 13, color: HEX.pale } }], { x: MX, y: y + h + 0.18, w: forestW, h: 0.8 });
  T(s, [{ text: "1.057,35 ha", options: { fontFace: DISPLAY, fontSize: 24, bold: true, color: COL.white, breakLine: true } },
        { text: "Non-hutan 2026 · kandidat ARR", options: { fontSize: 13, color: HEX.pale } }], { x: pos.arr.x, y: y + h + 0.18, w: W - MX - pos.arr.x, h: 0.8 });
  T(s, "OKTOBER 2026", { x: W - MX - 3, y: 0.9, w: 3, h: 0.35, fontSize: 14, bold: true, color: COL.leaf, charSpacing: 3, align: "right" });
  T(s, "Sumber: Export_Output_Gambut_M.xlsx · analisis awal, perlu verifikasi lapangan", { x: MX, y: 6.9, w: 8, h: 0.25, fontSize: 10, color: COL.leaf, italic: true });
}

// 2 · Ringkasan
{
  const s = slide("CONTENT", "RINGKASAN", "Tiga angka yang menentukan desain proyek",
    "REDD+: 1.369,2 ha hutan stabil, ditambah 41,94 ha hutan regenerasi yang perlu dicek definisi hutannya. ARR: hanya 591,3 ha yang lolos saringan dari 1.057,35 ha non-hutan. Deforestasi: angka 40,91 ha adalah net; angka bruto 82,87 ha yang dipakai untuk baseline.");
  const cards = [
    { big: "1.369,2", unit: "ha", head: "REDD+ layak", body: "Hutan stabil 2016–2026. Ditambah 41,94 ha hutan regenerasi, totalnya 1.411,16 ha.", col: COL.lindung },
    { big: "591,3", unit: "ha", head: "ARR layak", body: "Hanya 56% dari 1.057,35 ha non-hutan. Sisanya kebun, bekas hutan, atau sungai.", col: COL.amber },
    { big: "82,87", unit: "ha", head: "Deforestasi bruto 10 tahun", body: "Angka 40,91 ha adalah net. Baseline REDD+ memakai angka bruto.", col: COL.copper },
  ];
  const gap = 0.5, cw = (CW - 2 * gap) / 3, y = 2.25;
  cards.forEach((c, i) => {
    const x = MX + i * (cw + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.22, h: 0.22, fill: { color: c.col }, line: { type: "none" } });
    T(s, c.head.toUpperCase(), { x: x + 0.35, y: y - 0.02, w: cw - 0.35, h: 0.3, fontSize: 12, bold: true, color: HEX.muted, charSpacing: 2 });
    T(s, [{ text: c.big, options: { fontFace: DISPLAY, fontSize: 54, bold: true } }, { text: " " + c.unit, options: { fontSize: 20, color: HEX.muted } }], { x, y: y + 0.45, w: cw, h: 1.0 });
    T(s, c.body, { x, y: y + 1.6, w: cw, h: 1.0, fontSize: 15, color: HEX.muted });
  });
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: 5.35, w: CW, h: 0.85, fill: { color: COL.tint }, line: { type: "none" } });
  T(s, [{ text: "Sebelum menghitung kredit: ", options: { bold: true, color: COL.copper } }, { text: "perbaiki lima rumus di spreadsheet dan cek klasifikasi citra 2021, lalu hitung ulang baseline REDD+ dengan angka bruto.", options: { color: COL.ink } }],
    { x: MX + 0.3, y: 5.35, w: CW - 0.6, h: 0.85, fontSize: 16, valign: "middle" });
  locator(s, "all");
}

// =====================================================================
section("Pembagian luas");

// 3 · Area split
{
  const s = slide("CONTENT", "PEMBAGIAN LUAS", "Dari 2.468,51 ha, enam kelas kelayakan dengan aturan berbeda",
    "Kelas dibentuk dari matriks perubahan tutupan 2016–2026. Hutan stabil = hutan 2016 dikurangi kehilangan bruto 82,87 ha (1.452,07 − 82,87 = 1.369,20), sama dengan hutan 2026 dikurangi regenerasi 41,94 ha. ARR layak = semak dan lahan terbuka yang tidak pernah menjadi hutan dalam 10 tahun terakhir.");
  const y = 2.1, h = 0.75;
  const pos = areaBar(s, MX, y, CW, h, null, false);
  const forestEnd = pos.regen.x + pos.regen.w;
  hline(s, MX, y + h + 0.15, forestEnd - MX, HEX.muted, 1.25);
  hline(s, pos.arr.x, y + h + 0.15, W - MX - pos.arr.x, HEX.muted, 1.25);
  T(s, "Hutan 2026 · 1.411,16 ha", { x: MX, y: y + h + 0.22, w: 5, h: 0.3, fontSize: 12, bold: true, color: HEX.muted });
  T(s, "Non-hutan 2026 · 1.057,35 ha", { x: pos.arr.x, y: y + h + 0.22, w: 5, h: 0.3, fontSize: 12, bold: true, color: HEX.muted });

  const BR = { border: [{ type: "none" }, { type: "none" }, { pt: 0.5, color: HEX.hair }, { type: "none" }] };
  const H = (t, al = "left") => ({ text: t, options: { bold: true, color: HEX.muted, align: al, fontSize: 12, border: [{ type: "none" }, { type: "none" }, { pt: 1, color: HEX.ink }, { type: "none" }] } });
  const rows = [[H(""), H("Kelas"), H("Isi"), H("Luas (ha)", "right"), H("Porsi", "right"), H("Aturan", "left")]];
  const rule = {
    redd: "Masuk area REDD+", regen: "Cek definisi hutan dulu", arr: "Masuk area ARR",
    kebun: "Perlu agroforestri + persetujuan pemilik", defor: "Dibuka < 10 tahun, bukan kredit ARR", sungai: "Dikeluarkan",
  };
  SEGS.forEach((g) => {
    rows.push([
      { text: "■", options: Object.assign({ color: g.col, fontSize: 16 }, BR) },
      { text: g.name, options: Object.assign({ bold: true }, BR) },
      { text: g.desc, options: Object.assign({ color: HEX.muted }, BR) },
      { text: fmt(g.ha), options: Object.assign({ align: "right" }, BR) },
      { text: fmt(g.ha / TOTAL * 100, 1) + "%", options: Object.assign({ align: "right", color: HEX.muted }, BR) },
      { text: rule[g.k], options: Object.assign({}, BR) },
    ]);
  });
  s.addTable(rows, { x: MX, y: 3.65, w: CW, colW: [0.35, 2.0, 3.6, 1.35, 1.0, 3.833], rowH: 0.36, fontSize: 13, color: HEX.ink, fontFace: "Calibri", valign: "middle", margin: [0.02, 0.08, 0.02, 0.08] });
  source(s, "Sumber: sheet Tuplah (2), matriks perubahan tutupan 2016–2026. Total 2.468,51 ha.");
  locator(s, "all");
}

// =====================================================================
section("REDD+");

// 4 · Forest trend + rates
{
  const s = slide("CONTENT", "REDD+ · BASELINE DEFORESTASI", "Kehilangan hutan bruto 82,87 ha, dua kali angka net yang dipakai",
    "Luas hutan sekunder: 2016 1.452,07 ha; 2021 1.549,28 ha; 2026 1.411,16 ha. Selisih 2016–2026 = 40,91 ha (net). Matriks perubahan menunjukkan kehilangan bruto 82,87 ha dan regenerasi 41,94 ha. Regenerasi tidak boleh mengurangi angka deforestasi di baseline. Lonjakan 2021 bisa berarti laju makin cepat atau galat klasifikasi citra 2021; periksa sebelum memilih periode referensi.");
  const lx = MX, lw = 6.3;
  T(s, "LUAS HUTAN SEKUNDER (HA)", { x: lx, y: 2.05, w: lw, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2 });
  s.addChart(pres.charts.LINE, [{ name: "Hutan sekunder", labels: ["2016", "2021", "2026"], values: [145207, 154928, 141116] }], Object.assign({}, AXIS, {
    x: lx, y: 2.4, w: lw, h: 3.7, chartColors: [HEX.lindung], lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 9,
    showValue: true, dataLabelPosition: "t", dataLabelFormatCode: "#\\.##0\\,00", valAxisHidden: true, valAxisMinVal: 135000, valAxisMaxVal: 160000,
    showLegend: false, showTitle: false,
  }));
  T(s, "Sumbu tidak dimulai dari nol supaya perubahan terlihat.", { x: lx, y: 6.1, w: lw, h: 0.25, fontSize: 11, color: HEX.muted, italic: true });

  const rx = MX + lw + 0.6, rw = W - MX - rx;
  T(s, "LAJU DEFORESTASI", { x: rx, y: 2.05, w: rw, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2 });
  const BR = { border: [{ type: "none" }, { type: "none" }, { pt: 0.5, color: HEX.hair }, { type: "none" }] };
  const H = (t, al = "right") => ({ text: t, options: { bold: true, color: HEX.muted, align: al, fontSize: 12, border: [{ type: "none" }, { type: "none" }, { pt: 1, color: HEX.ink }, { type: "none" }] } });
  const r = (cells, bold) => cells.map((t, i) => ({ text: t, options: Object.assign({ align: i ? "right" : "left", bold: !!bold, color: bold ? HEX.copper : HEX.ink }, BR) }));
  s.addTable([
    [H("Periode", "left"), H("Luas (ha)"), H("Ha/tahun"), H("%/tahun")],
    r(["Bruto 2016–2026", "82,87", "8,29", "0,57%"], true),
    r(["Net 2016–2026", "40,91", "4,09", "0,28%"]),
    r(["2021–2026 saja", "138,12", "27,62", "1,78%"]),
  ], { x: rx, y: 2.45, w: rw, colW: [1.933, 1.1, 1.1, 1.1], rowH: 0.42, fontSize: 14, color: HEX.ink, fontFace: "Calibri", valign: "middle", margin: [0.02, 0.08, 0.02, 0.08] });
  s.addShape(pres.shapes.RECTANGLE, { x: rx, y: 4.5, w: rw, h: 1.6, fill: { color: COL.tint }, line: { type: "none" } });
  T(s, [{ text: "Data 2021 janggal. ", options: { bold: true, color: COL.copper } },
        { text: "Hutan naik 97 ha lalu turun 138 ha. Bisa jadi laju makin cepat, bisa juga galat klasifikasi citra. Periksa sebelum memilih periode referensi.", options: { color: COL.ink } }],
    { x: rx + 0.25, y: 4.5, w: rw - 0.5, h: 1.6, fontSize: 15, valign: "middle" });
  source(s, "Sumber: sheet Tuplah (2), klasifikasi tutupan 2016, 2021, 2026. % per tahun dihitung dari luas hutan 2016.");
  locator(s, "redd");
}

// 5 · Where lost forest went
{
  const s = slide("CONTENT", "REDD+ · PEMICU", "Dua pertiga hutan yang hilang kini menjadi lahan terbuka",
    "Hutan yang hilang 2016–2026 (82,87 ha): lahan terbuka 55,22 ha, semak belukar 19,81 ha, perkebunan 7,85 ha. Di sisi lain, 41,94 ha semak tumbuh kembali menjadi hutan. Hutan regenerasi bisa masuk REDD+ hanya bila memenuhi definisi hutan (≥0,25 ha, tajuk ≥30%, tinggi ≥5 m).");
  const lw = 7.4;
  T(s, "HUTAN 2016 → TUTUPAN 2026 (HA)", { x: MX, y: 2.05, w: lw, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2 });
  s.addChart(pres.charts.BAR, [{ name: "Luas", labels: ["Hutan → lahan terbuka", "Hutan → semak belukar", "Hutan → perkebunan", "Semak → hutan (regenerasi)"], values: [5522, 1981, 785, 4194] }], Object.assign({}, AXIS, {
    x: MX, y: 2.4, w: lw, h: 3.9, barDir: "bar", catAxisOrientation: "maxMin", barGapWidthPct: 60,
    chartColors: [HEX.copper, HEX.copper, HEX.copper, HEX.leaf],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: COMMA2, valAxisHidden: true, valAxisMaxVal: 6500, showLegend: false,
  }));
  const rx = MX + lw + 0.6, rw = W - MX - rx;
  T(s, [{ text: "82,87", options: { fontFace: DISPLAY, fontSize: 54, bold: true, color: COL.copper } }, { text: " ha", options: { fontSize: 20, color: HEX.muted } }], { x: rx, y: 2.3, w: rw, h: 1.0 });
  T(s, "kehilangan hutan bruto, dasar baseline REDD+", { x: rx, y: 3.3, w: rw, h: 0.4, fontSize: 15, color: HEX.muted });
  hline(s, rx, 3.95, rw);
  T(s, [{ text: "41,94", options: { fontFace: DISPLAY, fontSize: 40, bold: true, color: COL.lindung } }, { text: " ha", options: { fontSize: 18, color: HEX.muted } }], { x: rx, y: 4.15, w: rw, h: 0.8 });
  T(s, "regenerasi, dihitung terpisah. Tidak mengurangi angka deforestasi.", { x: rx, y: 4.95, w: rw, h: 0.7, fontSize: 15, color: HEX.muted });
  source(s, "Sumber: sheet Tuplah (2), Perubahan Loss dan Perubahan Gain 2016–2026.");
  locator(s, "redd");
}

// =====================================================================
section("ARR");

// 6 · ARR sieve
{
  const s = slide("CONTENT", "ARR · SARINGAN KELAYAKAN", "Dari 1.057 ha non-hutan, hanya 591 ha lolos saringan ARR",
    "Langkah saringan: non-hutan 2026 1.057,35 ha; keluarkan sungai 31,92 ha; keluarkan bekas hutan yang dibuka 2016–2026 sebesar 82,87 ha (lahan terbuka 55,22, semak 19,81, kebun 7,85), karena ARR mensyaratkan lahan sudah non-hutan minimal 10 tahun; pisahkan kebun 351,30 ha sebagai kategori bersyarat. Sisa ARR layak 591,26 ha = semak 588,88 + lahan terbuka 2,38.");
  const NON = 1057.35;
  const steps = [
    { label: "Non-hutan 2026", sub: "Titik awal", amt: NON, col: null },
    { label: "Keluarkan sungai", sub: "Bukan daratan", amt: 31.92, col: COL.river },
    { label: "Keluarkan bekas hutan 2016–2026", sub: "Terbuka 55,22 · semak 19,81 · kebun 7,85", amt: 82.87, col: COL.copper },
    { label: "Pisahkan kebun", sub: "Bersyarat: agroforestri", amt: 351.30, col: COL.akasia },
  ];
  const lx = MX, lw = 3.3, bx = MX + lw + 0.3, bw = 3.6, vx = bx + bw + 0.25, vw = 1.6;
  const y0 = 2.15, rh = 0.78;
  let remain = NON;
  const removed = [];
  steps.forEach((st, i) => {
    const y = y0 + i * rh;
    if (st.col) { remain -= st.amt; removed.push(st); }
    T(s, [{ text: st.label, options: { bold: true, breakLine: true } }, { text: st.sub, options: { fontSize: 12, color: HEX.muted } }], { x: lx, y, w: lw, h: 0.65, fontSize: 15 });
    const scale = bw / NON;
    s.addShape(pres.shapes.RECTANGLE, { x: bx, y: y + 0.12, w: remain * scale, h: 0.32, fill: { color: COL.amber }, line: { type: "none" } });
    let cx = bx + remain * scale + 0.03;
    removed.forEach((r) => {
      s.addShape(pres.shapes.RECTANGLE, { x: cx, y: y + 0.12, w: Math.max(r.amt * scale - 0.03, 0.02), h: 0.32, fill: { color: r.col, transparency: r === st ? 0 : 65 }, line: { type: "none" } });
      cx += r.amt * scale;
    });
    T(s, (st.col ? "− " : "") + fmt(st.amt) + " ha", { x: vx, y: y + 0.08, w: vw, h: 0.4, fontSize: 15, align: "right", color: st.col ? HEX.muted : HEX.ink });
    hline(s, lx, y + rh - 0.06, vx + vw - lx);
  });
  const fy = y0 + steps.length * rh + 0.05;
  T(s, [{ text: "ARR layak", options: { bold: true, breakLine: true } }, { text: "Semak 588,88 + lahan terbuka 2,38", options: { fontSize: 12, color: HEX.muted } }], { x: lx, y: fy, w: lw, h: 0.65, fontSize: 16 });
  s.addShape(pres.shapes.RECTANGLE, { x: bx, y: fy + 0.08, w: remain * bw / NON, h: 0.42, fill: { color: COL.amber }, line: { type: "none" } });
  T(s, fmt(remain) + " ha", { x: vx - 0.4, y: fy + 0.02, w: vw + 0.4, h: 0.5, fontFace: DISPLAY, fontSize: 24, bold: true, align: "right" });

  const rx = vx + vw + 0.45, rw = W - MX - rx;
  s.addShape(pres.shapes.RECTANGLE, { x: rx, y: 2.15, w: rw, h: 3.95, fill: { color: COL.tint }, line: { type: "none" } });
  T(s, [{ text: "Bekas hutan 82,87 ha", options: { bold: true, breakLine: true } },
        { text: "boleh direstorasi, tetapi tidak dihitung sebagai kredit ARR.", options: { color: HEX.muted, breakLine: true } },
        { text: " ", options: { fontSize: 8, breakLine: true } },
        { text: "Kebun 351,30 ha", options: { bold: true, breakLine: true } },
        { text: "masuk hanya lewat agroforestri jenis rawa gambut dengan persetujuan pemilik lahan.", options: { color: HEX.muted } }],
    { x: rx + 0.2, y: 2.35, w: rw - 0.4, h: 3.6, fontSize: 14 });
  source(s, "Syarat non-hutan minimal 10 tahun mengikuti praktik VCS/CDM; cek ke PV Climate Requirements versi terbaru.");
  locator(s, "arr");
}

// 7 · Land-cover shift
{
  const s = slide("CONTENT", "ARR · RISIKO KONVERSI", "Semak berkurang 359 ha seiring kebun bertambah 353 ha",
    "Perubahan luas 2016 → 2026: hutan −40,91; semak belukar −359,25; pertanian −10,23; perkebunan +352,81; lahan terbuka +57,60. Perkebunan tumbuh dari 6,33 ha (2016) menjadi 359,14 ha (2026), terutama setelah 2021 (26,04 ha). Pemicu utama perubahan lahan adalah ekspansi kebun. Ini menguatkan argumen ancaman untuk REDD+, tetapi juga berarti area ARR berupa semak rawan dikonversi selama proyek.");
  const lw = 7.6;
  T(s, "PERUBAHAN LUAS 2016 → 2026 (HA)", { x: MX, y: 2.05, w: lw, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2 });
  s.addChart(pres.charts.BAR, [{ name: "Perubahan", labels: ["Hutan", "Semak belukar", "Pertanian", "Perkebunan", "Lahan terbuka"], values: [-4091, -35925, -1023, 35281, 5760] }], Object.assign({}, AXIS, {
    x: MX, y: 2.4, w: lw, h: 3.9, barDir: "bar", catAxisOrientation: "maxMin", barGapWidthPct: 55, catAxisLabelPos: "low",
    chartColors: [HEX.copper, HEX.copper, HEX.copper, HEX.river, HEX.river],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "+#0\\,00;−#0\\,00", valAxisHidden: true, valAxisMinVal: -45000, valAxisMaxVal: 45000, showLegend: false,
  }));
  const rx = MX + lw + 0.6, rw = W - MX - rx;
  T(s, "PERKEBUNAN (HA)", { x: rx, y: 2.05, w: rw, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2 });
  [["2016", "6,33"], ["2021", "26,04"], ["2026", "359,14"]].forEach(([yr, v], i) => {
    const y = 2.45 + i * 0.7;
    T(s, yr, { x: rx, y, w: 1, h: 0.55, fontSize: 15, color: HEX.muted, valign: "middle" });
    T(s, v, { x: rx + 1, y, w: rw - 1, h: 0.55, fontFace: DISPLAY, fontSize: i === 2 ? 30 : 22, bold: true, align: "right", valign: "middle", color: i === 2 ? COL.river : COL.ink });
    hline(s, rx, y + 0.62, rw);
  });
  s.addShape(pres.shapes.RECTANGLE, { x: rx, y: 4.75, w: rw, h: 1.35, fill: { color: COL.tint }, line: { type: "none" } });
  T(s, "Ekspansi kebun mendukung argumen ancaman REDD+, tetapi area ARR rawan dikonversi.", { x: rx + 0.25, y: 4.75, w: rw - 0.5, h: 1.35, fontSize: 15, valign: "middle" });
  source(s, "Sumber: sheet Tuplah (2), luas per kelas tutupan 2016, 2021, 2026.");
  locator(s, "arr");
}

// =====================================================================
section("Konteks dan tindak lanjut");

// 8 · Peat function
{
  const s = slide("CONTENT", "STATUS GAMBUT", "82% area berada di fungsi lindung ekosistem gambut",
    "Overlay KHG: fungsi lindung (KHG Sungai Mempawah – Sungai Duri, gambut 100–300 cm) ±2.016 ha; fungsi budidaya (KHG Sungai Mempawah – Sungai Peniti, bergambut <50 cm) ±453 ha. Di fungsi lindung, konversi sudah dilarang (PP 71/2014 jo. PP 57/2016), sehingga additionality REDD+ harus menunjukkan larangan tidak efektif di lapangan.");
  const y = 2.2, h = 0.7, gap = 0.04;
  const wl = (CW - gap) * 2016 / 2469;
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y, w: wl, h, fill: { color: COL.lindung }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: MX + wl + gap, y, w: CW - wl - gap, h, fill: { color: COL.akasia }, line: { type: "none" } });
  T(s, "Lindung · ±2.016 ha (82%)", { x: MX + 0.2, y, w: wl - 0.4, h, fontSize: 16, bold: true, color: COL.white, valign: "middle" });
  T(s, "Budidaya · ±453 ha", { x: MX + wl + gap + 0.15, y, w: CW - wl - 0.3, h, fontSize: 14, bold: true, color: COL.white, valign: "middle" });

  const cols = [
    { head: "Dampak untuk REDD+", body: "Konversi di fungsi lindung sudah dilarang aturan. Additionality harus menunjukkan larangan itu tidak efektif. Kehilangan hutan 82,87 ha menjadi buktinya." },
    { head: "Dampak untuk ARR", body: "Restorasi perlu pembasahan ulang (sekat kanal) dan jenis asli rawa gambut. Kebun di fungsi lindung punya dasar untuk dipulihkan." },
    { head: "Data gambut yang dipakai", body: "Gambut 100–200 cm ±1.587 ha, 200–300 cm ±429 ha, bergambut <50 cm ±453 ha. Kedalaman ini harus masuk ke hitungan stok, bukan 1,5 m seragam." },
  ];
  const g2 = 0.5, cw = (CW - 2 * g2) / 3, cy = 3.45;
  cols.forEach((c, i) => {
    const x = MX + i * (cw + g2);
    hline(s, x, cy, cw, HEX.ink, 1);
    T(s, c.head, { x, y: cy + 0.15, w: cw, h: 0.4, fontSize: 17, bold: true, fontFace: DISPLAY });
    T(s, c.body, { x, y: cy + 0.65, w: cw, h: 2.0, fontSize: 15, color: HEX.muted });
  });
  source(s, "Sumber: Export_Output (overlay PL2022 KLHK × peta KHG). Luas dibulatkan per poligon.");
  locator(s, "all");
}

// 9 · Spreadsheet fixes
{
  const s = slide("CONTENT", "SHEET TUPLAH (2)", "Lima rumus perlu dikoreksi sebelum menghitung kredit",
    "1) P31 = O37*P30: rata-rata tCO2e/ha seluruh tutupan dikali 0,0116 tanpa luas, hasil 22,67 tCO2e/tahun. Seharusnya luas hutan × laju deforestasi × faktor emisi per ha hutan; sumber laju 0,0116 perlu dicantumkan. 2) D33 memakai C33 (Emisi), seharusnya B33 (Luas). 3) D34 memakai 45, seharusnya 0,45; kesalahan sama di sheet Tuplah D55/D63. 4) E31:E34 memakai 1,5 m untuk semua kelas; BD dan C beda antar-sheet (0,08/0,45; 0,10/0,55; 0,12/0,51). 5) Biomassa di atas permukaan belum dihitung; emisi gambut dihitung tahunan dari selisih faktor emisi.");
  const BR = { border: [{ type: "none" }, { type: "none" }, { pt: 0.5, color: HEX.hair }, { type: "none" }] };
  const H = (t) => ({ text: t, options: { bold: true, color: HEX.muted, fontSize: 12, border: [{ type: "none" }, { type: "none" }, { pt: 1, color: HEX.ink }, { type: "none" }] } });
  const rows = [[H("#"), H("Sel"), H("Masalah"), H("Dampak"), H("Perbaikan")]];
  [
    ["1", "P31", "Emisi tahunan tidak dikali luas", "22,67 tCO₂e/tahun untuk 1.411 ha hutan", "Luas hutan × laju × faktor emisi per ha; cantumkan sumber laju 0,0116"],
    ["2", "D33", "Stok kebun memakai kolom Emisi (C33)", "Stok kebun 6.464.520", "Ganti C33 dengan B33 (Luas)"],
    ["3", "D34", "Fraksi karbon tertulis 45", "Stok semak 27.391.050", "Ganti 45 dengan 0,45; sama di Tuplah D55, D63"],
    ["4", "E31:E34", "Kedalaman gambut seragam 1,5 m", "Stok gambut salah per kelas", "Pakai kedalaman per poligon; samakan BD dan C antar-sheet"],
    ["5", "—", "Biomassa hutan belum dihitung", "Emisi deforestasi terlalu kecil", "Tambah karbon biomassa (FREL KLHK atau plot); emisi gambut tahunan"],
  ].forEach((r) => rows.push(r.map((t, i) => ({ text: t, options: Object.assign({ bold: i === 2, color: i === 0 ? HEX.copper : i === 3 ? HEX.muted : HEX.ink, fontFace: i === 1 ? "Courier New" : "Calibri" }, BR) }))));
  s.addTable(rows, { x: MX, y: 2.15, w: CW, colW: [0.45, 1.25, 3.3, 3.0, 4.133], rowH: 0.62, fontSize: 14, color: HEX.ink, valign: "middle", margin: [0.03, 0.08, 0.03, 0.08] });
  source(s, "Sumber: rumus di sheet Tuplah (2) dan Tuplah, Export_Output_Gambut_M.xlsx.");
  locator(s, "all");
}

// 10 · Next steps (close)
{
  const s = slide("COVER", "LANGKAH BERIKUT", "Kunci luasan dulu, baru hitung kredit",
    "Urutan kerja: (1) cek klasifikasi citra 2021; (2) cek hutan regenerasi 41,94 ha terhadap definisi hutan; (3) konfirmasi syarat kelayakan di PV Climate Requirements; (4) perbaiki lima rumus dan pilih nilai biomassa; (5) hitung ulang baseline REDD+ dengan laju bruto dan potensi ARR untuk 591 ha.");
  const steps = [
    ["Cek data", "Klasifikasi citra 2021 dan definisi hutan untuk 41,94 ha regenerasi"],
    ["Cek standar", "Syarat 10 tahun REDD+ dan ARR di PV Climate Requirements terbaru"],
    ["Perbaiki model", "Lima rumus, kedalaman gambut, dan nilai biomassa hutan rawa sekunder"],
    ["Hitung ulang", "Baseline REDD+ dengan laju bruto; potensi ARR untuk 591 ha"],
  ];
  const gap = 0.4, sw = (CW - 3 * gap) / 4, y = 3.45;
  steps.forEach(([h, d], i) => {
    const x = MX + i * (sw + gap);
    hline(s, x, y, sw, HEX.leaf, 1);
    T(s, String(i + 1), { x, y: y + 0.15, w: sw, h: 0.5, fontFace: DISPLAY, fontSize: 26, bold: true, color: COL.leaf });
    T(s, h, { x, y: y + 0.75, w: sw, h: 0.4, fontSize: 17, bold: true, color: COL.white });
    T(s, d, { x, y: y + 1.2, w: sw, h: 1.1, fontSize: 14, color: HEX.pale });
  });
  areaBar(s, MX, 6.0, CW, 0.22, null, true);
  T(s, "Area 2.468,51 ha · REDD+ 1.411,16 ha · ARR layak 591,26 ha", { x: MX, y: 6.4, w: CW, h: 0.3, fontSize: 12, color: COL.leaf });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (APPLY_THEME) {
    const { applyTheme } = require(APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("wrote", OUT);
})();
