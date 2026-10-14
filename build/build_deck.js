// Builds the redesigned deck following DECK.md (antislop-decks skill).
// Usage: node build/build_deck.js <out.pptx> [apply_theme.js path]
const path = require("path");
const pptxgen = require("pptxgenjs");

const OUT = process.argv[2] || "Analisis_Multiusaha_Kehutanan_Mayawana_Persada.pptx";
const APPLY_THEME = process.argv[3];
const ROOT = path.resolve(__dirname, "..");

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
pres.title = "Analisis Multiusaha Kehutanan Karbon — PT Mayawana Persada";
pres.author = "PT Mayawana Persada";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const COL = {
  ink: C.text1, forest: C.text2, white: C.background1, tint: C.background2,
  lindung: C.accent1, akasia: C.accent2, copper: C.accent3, muted: C.accent4, hair: C.accent5, leaf: C.accent6,
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
  slideNumber: { x: 12.23, y: 6.92, w: 0.5, h: 0.25, fontSize: 10, color: COL.muted, align: "right" },
});
pres.defineSlideMaster({
  title: "DIVIDER",
  background: { color: COL.forest },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: 4.2, y: 2.55, w: 8.4, h: 0.35, fontSize: 14, bold: true, color: COL.leaf, charSpacing: 3, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 4.2, y: 3.0, w: 8.4, h: 1.6, fontFace: DISPLAY, fontSize: 36, bold: true, color: COL.white, margin: 0, valign: "top", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.23, y: 6.92, w: 0.5, h: 0.25, fontSize: 10, color: COL.leaf, align: "right" },
});
pres.defineSlideMaster({
  title: "COVER",
  background: { color: COL.forest },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.9, w: CW, h: 0.35, fontSize: 14, bold: true, color: COL.leaf, charSpacing: 3, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 1.4, w: 10.5, h: 1.7, fontFace: DISPLAY, fontSize: 40, bold: true, color: COL.white, margin: 0, valign: "top", align: "left" }, text: "" } },
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
function source(s, text, dark) {
  T(s, text, { x: MX, y: 6.55, w: CW - 0.6, h: 0.25, fontSize: 10, color: dark ? COL.leaf : COL.muted, italic: true });
}

// Signature element: the concession split bar (66.908 ha budidaya : 71.350 ha lindung).
const HA_PROD = 66908.4, HA_LIND = 71349.6, HA_TOT = HA_PROD + HA_LIND;
const P_PROD = HA_PROD / HA_TOT;
function splitBar(s, x, y, w, h, focus, dark) {
  const off = dark ? "2E5246" : HEX.hair; // hex: inactive segment
  const prodOn = focus === "prod" || focus === "both";
  const lindOn = focus === "lindung" || focus === "both";
  const gap = Math.max(0.03, w * 0.006);
  const wp = w * P_PROD - gap / 2, wl = w - wp - gap;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: wp, h, fill: { color: prodOn ? COL.akasia : off }, line: { type: "none" }, objectName: "rasio-budidaya" });
  s.addShape(pres.shapes.RECTANGLE, { x: x + wp + gap, y, w: wl, h, fill: { color: lindOn ? (dark ? COL.leaf : COL.lindung) : off }, line: { type: "none" }, objectName: "rasio-lindung" });
  return { wp, wl, gap };
}
const FOCUS_LABEL = {
  both: "PBPH 138.258 ha  ·  budidaya 66.908  |  lindung 71.350",
  prod: "Fokus: kawasan budidaya 66.908 ha",
  lindung: "Fokus: kawasan lindung 71.350 ha",
};
function locator(s, focus, dark) {
  splitBar(s, MX, 7.0, 1.6, 0.1, focus, dark);
  T(s, FOCUS_LABEL[focus], { x: MX + 1.75, y: 6.93, w: 5, h: 0.25, fontSize: 10, color: dark ? COL.leaf : COL.muted });
}
function arrow(s, x1, y1, x2, y2, color, o = {}) {
  s.addShape(pres.shapes.LINE, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    flipH: x2 < x1, flipV: y2 < y1,
    line: Object.assign({ color, width: 1.5, endArrowType: "triangle" }, o),
  });
}
function hline(s, x, y, w, color, width = 0.75) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: color || COL.hair, width } });
}
function chip(s, text, x, y, w, color, o = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.34, rectRadius: 0.17, fill: { color }, line: { type: "none" } });
  T(s, text, Object.assign({ x, y, w, h: 0.34, fontSize: 11, bold: true, color: COL.white, align: "center", valign: "middle" }, o));
}
const fmt = (n) => n.toLocaleString("id-ID");

// =====================================================================
section("Pembuka");

// 1 · Cover
{
  const s = slide("COVER", "ANALISIS STRATEGIS  ·  PT MAYAWANA PERSADA",
    "Satu izin, dua portofolio: kayu dan karbon di PBPH ±138.258 ha",
    "Deck ini menganalisis kelayakan Multiusaha Kehutanan (MUK) di PBPH PT Mayawana Persada: mempertahankan HTI akasia pada kawasan budidaya dan mengembangkan Pemanfaatan Jasa Lingkungan (PJL) karbon pada kawasan lindung. Kerangka analisis: legal feasibility, carbon integrity, business feasibility, decision pathway.");
  T(s, "Analisis kelayakan Multiusaha Kehutanan — mengembangkan kawasan lindung menjadi Pemanfaatan Jasa Lingkungan karbon, tanpa menghentikan HTI akasia", { x: MX, y: 3.15, w: 9.6, h: 0.8, fontSize: 16, color: "C8D6CD" });
  const y = 4.75, h = 0.62;
  const { wp } = splitBar(s, MX, y, CW, h, "both", true);
  T(s, [{ text: "66.908 ha", options: { fontFace: DISPLAY, fontSize: 24, bold: true, color: COL.white, breakLine: true } },
        { text: "Kawasan budidaya · HTI akasia", options: { fontSize: 13, color: "C8D6CD" } }], { x: MX, y: y + h + 0.18, w: wp, h: 0.8 });
  T(s, [{ text: "71.350 ha", options: { fontFace: DISPLAY, fontSize: 24, bold: true, color: COL.white, breakLine: true } },
        { text: "Kawasan lindung · kandidat karbon", options: { fontSize: 13, color: "C8D6CD" } }], { x: MX + wp + 0.1, y: y + h + 0.18, w: CW - wp - 0.1, h: 0.8 });
  T(s, "Analisis awal — perlu dikonfirmasi dengan dokumen PBPH/RKUPH dan data spasial aktual", { x: MX, y: 6.9, w: 8, h: 0.25, fontSize: 10, color: COL.leaf, italic: true });
}

// 2 · Executive summary
{
  const s = slide("CONTENT", "KESIMPULAN EKSEKUTIF",
    "Peluang kuat, tetapi nilainya baru nyata setelah lolos tiga gate",
    "Hukum: PBPH pada Hutan Produksi dapat menjalankan Multiusaha Kehutanan, termasuk Pemanfaatan Jasa Lingkungan (PP 23/2021 Ps. 149). Kegiatan MUK harus dituangkan dalam RKUPH (Permen LHK 8/2021 Ps. 155).\n\nKarbon: penghentian land clearing, drainase/kanalisasi baru, perlindungan hutan, rewetting dan restorasi dapat menjadi sumber mitigasi — sepanjang legal, additional, dan metodologinya eligible.\n\nBisnis: skala kandidat ±72.000 ha menarik, tetapi keputusan investasi harus berbasis tCO2e eligible serta NPV karbon vs NPV HTI, bukan luas areal semata.");
  const rows = [
    ["1", "HUKUM", "Diizinkan.", "PBPH di Hutan Produksi boleh menjalankan Multiusaha Kehutanan termasuk jasa lingkungan; wajib dituangkan dalam RKUPH."],
    ["2", "KARBON", "Bersyarat.", "Perlindungan, rewetting, restorasi dan pengendalian kebakaran dapat dikreditkan — jika legal, additional dan metodologinya eligible."],
    ["3", "BISNIS", "Belum terbukti.", "Skala 71.350 ha menarik, tetapi keputusan harus berbasis tCO₂e eligible dan NPV karbon vs NPV HTI."],
  ];
  const x0 = MX, wL = 7.9, y0 = 2.2, rh = 1.3;
  rows.forEach((r, i) => {
    const y = y0 + i * rh;
    if (i > 0) hline(s, x0, y - 0.15, wL);
    T(s, r[0], { x: x0, y: y - 0.05, w: 0.6, h: 0.8, fontFace: DISPLAY, fontSize: 40, bold: true, color: COL.lindung });
    T(s, r[1], { x: x0 + 0.8, y, w: 1.5, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 2 });
    T(s, [{ text: r[2] + " ", options: { bold: true } }, { text: r[3] }], { x: x0 + 0.8, y: y + 0.32, w: wL - 0.8, h: 0.8, fontSize: 15 });
  });
  const px = 9.0, pw = W - MX - px;
  s.addShape(pres.shapes.RECTANGLE, { x: px, y: 2.05, w: pw, h: 3.9, fill: { color: COL.forest }, line: { type: "none" }, objectName: "panel-rekomendasi" });
  T(s, "REKOMENDASI", { x: px + 0.35, y: 2.4, w: pw - 0.7, h: 0.3, fontSize: 12, bold: true, color: COL.leaf, charSpacing: 2 });
  T(s, "Jalankan Legal–Carbon Feasibility Screening sebelum mengubah RKUPH dan sebelum menetapkan valuasi proyek.", { x: px + 0.35, y: 2.8, w: pw - 0.7, h: 2.9, fontFace: DISPLAY, fontSize: 20, bold: true, color: COL.white });
  source(s, "Dasar: PP 23/2021 Ps. 149; Permen LHK 8/2021 Ps. 155; Permenhut 6/2026 Ps. 6.");
  locator(s, "both");
}

// 3 · Existing condition — emission chain
{
  const s = slide("CONTENT", "KONDISI EXISTING",
    "Siklus HTI akasia saat ini menciptakan empat sumber emisi yang wajib dipetakan",
    "RKU/RKUPH telah mengarahkan pengusahaan HTI akasia; kini dipertimbangkan transformasi sebagian areal. Rantai kegiatan HTI — dari vegetasi existing, land clearing, pembangunan kanal & drainase, penanaman akasia, sampai panen dan rotasi — memunculkan empat sumber emisi yang perlu dipetakan sebagai baseline: kehilangan biomassa, emisi tanah gambut, kebakaran, dan emisi operasional.");
  const steps = ["Hutan / vegetasi existing", "Land clearing", "Kanal & drainase", "HTI akasia", "Panen & rotasi"];
  const n = steps.length, lineY = 2.75, step = CW / n;
  hline(s, MX + step / 2, lineY, step * (n - 1), COL.akasia, 2);
  steps.forEach((t, i) => {
    const cx = MX + step * i + step / 2;
    s.addShape(pres.shapes.OVAL, { x: cx - 0.17, y: lineY - 0.17, w: 0.34, h: 0.34, fill: { color: i === 0 ? COL.lindung : COL.akasia }, line: { color: COL.white, width: 2 } });
    T(s, String(i + 1).padStart(2, "0"), { x: cx - 1, y: lineY - 0.6, w: 2, h: 0.3, fontSize: 11, bold: true, color: COL.muted, align: "center" });
    T(s, t, { x: cx - 1.1, y: lineY + 0.32, w: 2.2, h: 0.6, fontSize: 15, bold: true, align: "center" });
  });
  const em = [
    [1, "Kehilangan biomassa", "Vegetasi dibuka untuk penanaman"],
    [2, "Emisi tanah gambut", "Muka air turun akibat drainase"],
    [3, "Kebakaran", "Lahan kering lebih mudah terbakar"],
    [4, "Operasional", "Panen, transport, rotasi"],
  ];
  const ey = 4.55;
  em.forEach(([si, t, d]) => {
    const cx = MX + step * si + step / 2;
    arrow(s, cx, lineY + 0.95, cx, ey - 0.08, COL.copper);
    T(s, [{ text: t, options: { bold: true, color: COL.copper, breakLine: true } }, { text: d, options: { color: COL.muted, fontSize: 13 } }],
      { x: cx - 1.1, y: ey, w: 2.2, h: 0.9, fontSize: 15, align: "center" });
  });
  T(s, "Keempat sumber ini menjadi bahan baseline: tanpa peta emisinya, tidak ada yang bisa diklaim sebagai pengurangan.", { x: MX, y: 5.75, w: CW, h: 0.4, fontSize: 14, color: COL.muted });
  locator(s, "prod");
}

// 4 · Transformation model — signature bar, full size
{
  const s = slide("CONTENT", "MODEL TRANSFORMASI",
    "PBPH tidak dilepas: portofolionya dibagi menjadi 66.908 ha kayu dan 71.350 ha karbon",
    "Model ini bukan melepas PBPH, tetapi mengubah portofolio kegiatan melalui Multiusaha Kehutanan.\n\nKawasan budidaya: kegiatan produksi tetap berjalan pada areal yang dipertahankan sebagai basis usaha kayu.\n\nKawasan lindung: kandidat perlindungan stok karbon, avoided conversion, restorasi/rewetting, pengendalian kebakaran dan peningkatan serapan — setelah screening.\n\nCatatan: pembagian ini adalah skenario analisis, bukan penetapan final; angka final mengikuti penataan ulang RKUPH.");
  const y = 2.3, h = 1.25;
  const { wp } = splitBar(s, MX, y, CW, h, "both");
  T(s, "48%", { x: MX + 0.3, y, w: 2, h, fontFace: DISPLAY, fontSize: 36, bold: true, color: COL.white, valign: "middle" });
  T(s, "52%", { x: MX + wp + 0.35, y, w: 2, h, fontFace: DISPLAY, fontSize: 36, bold: true, color: COL.white, valign: "middle" });
  const cy = y + h + 0.35, cw = wp - 0.4;
  T(s, [{ text: "66.908 ha · HTI / kayu", options: { bold: true, fontSize: 18, color: COL.ink, breakLine: true } },
        { text: "Produksi akasia tetap berjalan sebagai basis usaha kayu.", options: { fontSize: 15, color: COL.muted } }], { x: MX, y: cy, w: cw, h: 1.2 });
  T(s, [{ text: "71.350 ha · PJL karbon", options: { bold: true, fontSize: 18, color: COL.lindung, breakLine: true } },
        { text: "Perlindungan stok karbon, avoided conversion, restorasi/rewetting, pengendalian kebakaran — setelah screening.", options: { fontSize: 15, color: COL.muted } }], { x: MX + wp + 0.1, y: cy, w: CW - wp - 0.1, h: 1.2 });
  T(s, "Satu payung izin: PBPH ±138.258 ha", { x: MX, y: y - 0.45, w: 6, h: 0.3, fontSize: 13, bold: true, color: COL.muted });
  source(s, "Pembagian adalah skenario analisis; angka final mengikuti penataan ulang RKUPH. Luas: data stok karbon PBPH 2026.");
}

// =====================================================================
function divider(n, kicker, q, sub, notes) {
  const s = slide("DIVIDER", kicker, q, notes);
  T(s, String(n), { x: MX, y: 1.7, w: 3.2, h: 3.6, fontFace: DISPLAY, fontSize: 220, bold: true, color: COL.leaf, align: "left", valign: "middle" });
  T(s, sub, { x: 4.2, y: 4.75, w: 8.4, h: 0.4, fontSize: 15, color: "C8D6CD" });
  return s;
}

section("Gate 1 · Legal");
divider(1, "GATE 1  ·  LEGAL", "Apakah BAU legal dan areal\nbenar-benar eligible?", "Arsitektur hukum  ·  Uji legal baseline  ·  Screening areal");

// 6 · Legal architecture
{
  const s = slide("CONTENT", "ARSITEKTUR HUKUM",
    "Payung hukumnya sudah tersedia — perubahan masuk lewat RKUPH, bukan izin baru",
    "PP 23/2021 Ps. 149: PBPH pada Hutan Produksi dilakukan dengan Multiusaha Kehutanan, termasuk Pemanfaatan Jasa Lingkungan.\nPermen LHK 8/2021 Ps. 155: kegiatan Multiusaha Kehutanan dituangkan dalam RKUPH.\nPermen LHK 8/2021 Ps. 157: Pemanfaatan Jasa Lingkungan mencakup penyerapan dan/atau penyimpanan karbon.\nPermenhut 6/2026 Ps. 6: pemegang PBPH termasuk Pelaku Usaha dalam perdagangan karbon sektor kehutanan.");
  const regs = [
    ["PP 23/2021", "Pasal 149", "PBPH di Hutan Produksi dijalankan sebagai Multiusaha Kehutanan, termasuk jasa lingkungan."],
    ["Permen LHK 8/2021", "Pasal 155", "Kegiatan Multiusaha Kehutanan dituangkan dalam RKUPH."],
    ["Permen LHK 8/2021", "Pasal 157", "Jasa lingkungan mencakup penyerapan dan/atau penyimpanan karbon."],
    ["Permenhut 6/2026", "Pasal 6", "Pemegang PBPH termasuk Pelaku Usaha perdagangan karbon kehutanan."],
  ];
  const y0 = 2.2, rh = 1.0, wL = 8.2;
  regs.forEach((r, i) => {
    const y = y0 + i * rh;
    if (i > 0) hline(s, MX, y - 0.15, wL);
    T(s, [{ text: r[0], options: { bold: true, breakLine: true } }, { text: r[1], options: { color: COL.muted, fontSize: 13 } }],
      { x: MX, y, w: 2.5, h: 0.75, fontFace: DISPLAY, fontSize: 16 });
    T(s, r[2], { x: MX + 2.7, y, w: wL - 2.7, h: 0.75, fontSize: 15 });
  });
  const bx = 9.5, bw = W - MX - bx, by = 2.6, bh = 2.6;
  arrow(s, MX + wL + 0.15, by + bh / 2, bx - 0.12, by + bh / 2, COL.lindung, { width: 2 });
  s.addShape(pres.shapes.RECTANGLE, { x: bx, y: by, w: bw, h: bh, fill: { color: COL.lindung }, line: { type: "none" }, objectName: "kotak-rkuph" });
  T(s, [{ text: "RKUPH", options: { fontFace: DISPLAY, fontSize: 32, bold: true, breakLine: true } },
        { text: "Titik masuk perubahan model usaha. PBPH tetap menjadi payung izin.", options: { fontSize: 15 } }],
    { x: bx + 0.3, y: by + 0.35, w: bw - 0.6, h: bh - 0.6, color: COL.white });
  source(s, "Sumber resmi: PP 23/2021; Permen LHK 8/2021; Permenhut 6/2026.");
  locator(s, "both");
}

// 7 · Five legal-baseline tests
{
  const s = slide("CONTENT", "LEGAL BASELINE",
    "Lima uji legal baseline: jawaban awal positif, tetapi harus dibuktikan dengan dokumen",
    "Tidak semua emisi yang 'dihindari' boleh diklaim sebagai additional. Contoh uji pada kawasan lindung ±72.000 ha (jawaban awal perusahaan):\n1) Penetapan pada blok tersebut legal karena merupakan kawasan lindung yang diperuntukkan untuk multiusaha kehutanan, berdasarkan SK PBPH.\n2) RKU/RKT secara realisasi menjadi realistis untuk BAU-nya, dan membutuhkan waktu 5–10 tahun sejak berdirinya PBPH.\n3) Areal yang diperuntukkan untuk analisis multiusaha kehutanan adalah kawasan lindung; fungsi sebagai areal konservasi tetap terjaga sekaligus untuk Project Carbon. Catatan analis: bila areal sejak awal wajib dilindungi, additionality-nya paling rentan.\n4) Kegiatan produksi dalam PBPH tidak berhenti; yang bertambah adalah multiusaha pada kawasan lindung, terutama Project Carbon.\n5) Metodologi karbon yang akan digunakan nantinya sesuai dengan SRUK.");
  const rows = [
    ["Apakah penetapan blok tersebut legal?", "Ya — kawasan lindung diperuntukkan untuk MUK berdasarkan SK PBPH.", "Verifikasi SK PBPH", COL.lindung],
    ["Apakah RKU/RKT dan rekam jejak membuat BAU realistis?", "Realisasi RKU/RKT mendukung BAU; butuh 5–10 tahun sejak PBPH berdiri.", "Lampirkan realisasi RKT", COL.lindung],
    ["Apakah areal bukan kawasan yang sejak awal wajib dilindungi?", "Areal adalah kawasan lindung; fungsi konservasi tetap terjaga.", "Risiko additionality", COL.copper],
    ["Apakah kegiatan berhenti karena proyek, bukan kewajiban hukum?", "Produksi tidak berhenti; MUK karbon ditambahkan pada kawasan lindung.", "Didukung", COL.lindung],
    ["Apakah metodologi mengakui aktivitas dan sumber emisinya?", "Metodologi akan mengikuti SRUK.", "Tunggu metodologi", COL.akasia],
  ];
  const y0 = 2.35, rh = 0.8, xq = MX + 0.55, wq = 5.0, xa = xq + wq + 0.3, wa = 4.25, xs = W - MX - 1.95;
  T(s, "PERTANYAAN UJI", { x: xq, y: y0 - 0.4, w: wq, h: 0.25, fontSize: 11, bold: true, color: COL.muted, charSpacing: 2 });
  T(s, "JAWABAN AWAL", { x: xa, y: y0 - 0.4, w: wa, h: 0.25, fontSize: 11, bold: true, color: COL.muted, charSpacing: 2 });
  T(s, "CATATAN ANALIS", { x: xs, y: y0 - 0.4, w: 1.95, h: 0.25, fontSize: 11, bold: true, color: COL.muted, charSpacing: 2 });
  rows.forEach((r, i) => {
    const y = y0 + i * rh;
    hline(s, MX, y - 0.1, CW);
    T(s, String(i + 1), { x: MX, y: y - 0.02, w: 0.4, h: 0.5, fontFace: DISPLAY, fontSize: 22, bold: true, color: COL.lindung });
    T(s, r[0], { x: xq, y, w: wq, h: 0.65, fontSize: 14, bold: true });
    T(s, r[1], { x: xa, y, w: wa, h: 0.65, fontSize: 14, color: COL.muted });
    chip(s, r[2], xs, y + 0.02, 1.95, r[3]);
  });
  locator(s, "lindung");
}

// 8 · Screening A/B/C
{
  const s = slide("CONTENT", "SCREENING KANDIDAT",
    "Screening memisahkan areal yang bisa dikreditkan dari areal yang memang wajib dilindungi",
    "Tujuan screening: memisahkan area yang potensial dikreditkan dari area kewajiban atau berisiko.\nA · Prioritas tinggi: areal yang secara legal & kredibel masih dapat dikelola untuk produksi/HTI, memiliki stok karbon signifikan, dan penghindaran konversinya dapat dibuktikan additional → fokus feasibility.\nB · Restorasi: areal terdegradasi/drained dengan peluang rewetting, revegetasi, peningkatan stok karbon atau pengurangan risiko kebakaran → uji metodologi & biaya.\nC · Kewajiban: kawasan lindung, sempadan, puncak kubah gambut/habitat tertentu atau area lain yang memang wajib dilindungi → konservasi tetap penting, tetapi additionality kredit perlu diuji ketat.\nProporsi A/B/C belum diketahui; ditentukan oleh hasil screening spasial.");
  const cls = [
    ["A", "Prioritas tinggi", "Masih legal dikelola untuk produksi, stok karbon signifikan, penghindaran konversinya terbukti additional.", "Fokus feasibility", COL.lindung],
    ["B", "Restorasi", "Terdegradasi atau terdrainase; ada peluang rewetting, revegetasi, dan pengurangan risiko kebakaran.", "Uji metodologi & biaya", COL.leaf],
    ["C", "Kewajiban", "Sempadan, puncak kubah gambut, habitat tertentu — areal yang memang wajib dilindungi.", "Additionality diuji ketat", COL.copper],
  ];
  const gap = 0.5, cw = (CW - 2 * gap) / 3, y = 2.2;
  cls.forEach((c, i) => {
    const x = MX + i * (cw + gap);
    T(s, c[0], { x, y, w: 1.2, h: 1.1, fontFace: DISPLAY, fontSize: 66, bold: true, color: c[4] });
    T(s, c[1], { x: x + 1.15, y: y + 0.35, w: cw - 1.15, h: 0.5, fontSize: 18, bold: true });
    hline(s, x, y + 1.25, cw, c[4], 1.5);
    T(s, c[2], { x, y: y + 1.45, w: cw, h: 1.5, fontSize: 15 });
    T(s, "→ " + c[3], { x, y: y + 3.05, w: cw, h: 0.4, fontSize: 15, bold: true, color: c[4] === COL.leaf ? COL.lindung : c[4] });
  });
  source(s, "Proporsi kelas A/B/C belum diketahui — ditentukan oleh screening spasial atas 71.350 ha.");
  locator(s, "lindung");
}

// =====================================================================
section("Gate 2 · Karbon");
divider(2, "GATE 2  ·  KARBON", "Apakah additionality dan metodologi dapat dipertahankan?", "Logika carbon accounting  ·  Stok & emisi  ·  Gambut");

// 10 · Carbon accounting logic
{
  const s = slide("CONTENT", "LOGIKA CARBON ACCOUNTING",
    "Unit karbon hanyalah selisih terverifikasi antara skenario baseline dan skenario proyek",
    "Baseline / BAU: RKU HTI dijalankan — pembukaan vegetasi yang legal, pembangunan/drainase kanal yang legal, rotasi tanaman, risiko emisi gambut/kebakaran → proyeksi emisi tanpa intervensi.\nProject scenario: MUK karbon dijalankan — perlindungan hutan, menghindari konversi yang eligible, rewetting/restorasi, pengendalian kebakaran, peningkatan stok karbon → emisi lebih rendah / serapan lebih tinggi.\nPotensi unit karbon = kinerja mitigasi yang terukur, additional, tervalidasi dan terverifikasi. Permenhut 6/2026 menempatkan baseline dan additionality sebagai elemen penting dalam aksi mitigasi/perdagangan karbon.");
  const lx = MX, lw = 2.6, bx = MX + lw + 0.2, full = 6.2, proj = 3.2, bh = 0.55;
  const y1 = 2.25, y2 = 3.1;
  T(s, "Baseline (BAU)", { x: lx, y: y1, w: lw, h: bh, fontSize: 15, bold: true, valign: "middle" });
  T(s, "Skenario proyek", { x: lx, y: y2, w: lw, h: bh, fontSize: 15, bold: true, valign: "middle" });
  s.addShape(pres.shapes.RECTANGLE, { x: bx, y: y1, w: full, h: bh, fill: { color: COL.akasia }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: bx, y: y2, w: proj, h: bh, fill: { color: COL.lindung }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: bx + proj, y: y2, w: full - proj, h: bh, fill: { color: COL.white }, line: { color: COL.copper, width: 1.5, dashType: "dash" } });
  T(s, "Potensi unit karbon", { x: bx + proj, y: y2, w: full - proj, h: bh, fontSize: 14, bold: true, color: COL.copper, align: "center", valign: "middle" });
  T(s, "emisi tanpa intervensi", { x: bx + 0.15, y: y1, w: 3, h: bh, fontSize: 13, color: COL.white, valign: "middle" });
  T(s, "emisi setelah MUK", { x: bx + 0.15, y: y2, w: 3, h: bh, fontSize: 13, color: COL.white, valign: "middle" });
  const rx = bx + full + 0.35, rw = W - MX - rx;
  T(s, [{ text: "Syarat agar selisih menjadi kredit", options: { bold: true, breakLine: true } },
        { text: "terukur · additional · tervalidasi · terverifikasi", options: { color: COL.copper, bold: true } }],
    { x: rx, y: y1 + 0.1, w: rw, h: 1.3, fontSize: 15 });
  T(s, "Ilustrasi, tidak berskala.", { x: bx, y: y2 + bh + 0.08, w: 3, h: 0.25, fontSize: 10, italic: true, color: COL.muted });
  const ly = 4.35, colw = (CW - 0.5) / 2;
  hline(s, MX, ly - 0.15, CW);
  const lists = [
    ["Pendorong emisi baseline (RKU HTI)", ["Pembukaan vegetasi yang legal", "Pembangunan & drainase kanal yang legal", "Rotasi tanaman", "Risiko emisi gambut & kebakaran"]],
    ["Intervensi proyek (MUK karbon)", ["Perlindungan hutan & hindari konversi eligible", "Rewetting & restorasi", "Pengendalian kebakaran", "Peningkatan stok karbon"]],
  ];
  lists.forEach(([h, items], i) => {
    const x = MX + i * (colw + 0.5);
    T(s, h, { x, y: ly, w: colw, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 1 });
    T(s, items.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < items.length - 1 } })), { x, y: ly + 0.4, w: colw, h: 1.6, fontSize: 15, paraSpaceAfter: 4 });
  });
  source(s, "Permenhut 6/2026 menempatkan baseline dan additionality sebagai elemen penting aksi mitigasi/perdagangan karbon.");
  locator(s, "both");
}

const CHART_BASE = () => ({
  catAxisLabelColor: HEX.muted, valAxisLabelColor: HEX.muted, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  dataLabelFontFace: "+mn-lt", dataLabelColor: HEX.ink, dataLabelFontSize: 13, catAxisLabelFontSize: 13,
  valGridLine: { style: "none" }, catGridLine: { style: "none" }, showValue: true,
  titleFontFace: "+mn-lt", titleColor: HEX.muted, titleFontSize: 12, showTitle: true,
});

// 11 · Carbon stock — big number + chart
{
  const s = slide("CONTENT", "STOK KARBON 2026",
    "Kawasan lindung menyimpan 70,3 juta tCO₂e — 4,8 kali stok kawasan budidaya",
    "Kawasan budidaya (produksi): 66.908,4 ha × 59,5 tC/ha = 3.981.049,8 tC, setara 14.597.182,6 tCO2e.\nKawasan lindung: 71.349,644 ha × 268,6 tC/ha = 19.164.514,4 tC, setara 70.269.886,1 tCO2e.\nKandungan karbon per hektar kawasan lindung 4,5 kali kawasan budidaya. Stok ini juga menjadi eksposur risiko permanence/kebakaran.");
  T(s, [{ text: "70,3", options: { fontFace: DISPLAY, fontSize: 80, bold: true, color: COL.lindung, breakLine: true } },
        { text: "juta tCO₂e tersimpan di kawasan lindung", options: { fontSize: 16, bold: true } }], { x: MX, y: 2.1, w: 4.6, h: 2.0 });
  const ty = 4.45;
  hline(s, MX, ty - 0.1, 4.4);
  [["Kandungan karbon", "268,6 vs 59,5 tC/ha"], ["Luas", "71.350 vs 66.908 ha"]].forEach((r, i) => {
    T(s, r[0], { x: MX, y: ty + i * 0.55, w: 2.0, h: 0.4, fontSize: 14, color: COL.muted });
    T(s, r[1], { x: MX + 2.0, y: ty + i * 0.55, w: 2.4, h: 0.4, fontSize: 14, bold: true, align: "right" });
  });
  T(s, "lindung vs budidaya", { x: MX, y: ty + 1.1, w: 4.4, h: 0.3, fontSize: 11, italic: true, color: COL.muted, align: "right" });
  s.addChart(pres.charts.BAR, [{ name: "Setara CO₂ (juta tCO₂e)", labels: ["Kawasan budidaya", "Kawasan lindung"], values: [14.6, 70.3] }],
    Object.assign(CHART_BASE(), {
      x: 5.6, y: 2.1, w: 7.1, h: 3.9, barDir: "bar", barGapWidthPct: 45, chartColors: [HEX.akasia, HEX.lindung],
      dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", valAxisHidden: true, valAxisMaxVal: 80,
      title: "Stok karbon setara CO₂, juta tCO₂e (2026)", showLegend: false, catAxisLineShow: false,
    }));
  source(s, "Data: stok karbon PBPH PT Mayawana Persada 2026 (lihat Lampiran B).");
  locator(s, "lindung");
}

// 12 · Emissions by clearing cohort — column chart
{
  const s = slide("CONTENT", "EMISI KAWASAN BUDIDAYA",
    "Pembukaan 46.648 ha sejak 2021 melepas ±12,2 juta tCO₂ — hampir separuhnya dari kohort 2023",
    "Faktor emisi 20 tC/ha/th diterapkan pada luas yang dibuka per tahun, diakumulasi hingga 2026:\n2021: 4.884 ha → 2.148.960 tCO2\n2022: 8.162 ha → 2.992.733 tCO2\n2023: 19.221 ha → 5.638.160 tCO2\n2024: 1.571 ha → 345.620 tCO2\n2025: 1.890 ha → 277.200 tCO2\n2026: 10.920 ha → 800.800 tCO2\nTotal 46.648 ha; 3.420.853 tCO2/th; kumulatif 12.203.473 tCO2. Data ini adalah bukti BAU di kawasan budidaya, dan menjadi pembanding untuk baseline kawasan lindung.");
  const vals = [2.149, 2.993, 5.638, 0.346, 0.277, 0.801];
  s.addChart(pres.charts.BAR, [{ name: "Emisi CO₂ kumulatif (juta tCO₂)", labels: ["2021", "2022", "2023", "2024", "2025", "2026"], values: vals }],
    Object.assign(CHART_BASE(), {
      x: MX, y: 2.1, w: 8.0, h: 4.2, barDir: "col", barGapWidthPct: 55,
      chartColors: [HEX.akasia, HEX.akasia, HEX.copper, HEX.akasia, HEX.akasia, HEX.akasia],
      dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", valAxisHidden: true, valAxisMaxVal: 6.5,
      title: "Emisi CO₂ kumulatif s.d. 2026 per tahun pembukaan, juta tCO₂", showLegend: false,
    }));
  const sx = 9.2, sw = W - MX - sx;
  [["46.648 ha", "dibuka 2021–2026"], ["19.221 ha", "dibuka pada 2023 saja"], ["20 tC/ha/th", "faktor emisi yang dipakai"]].forEach((r, i) => {
    const y = 2.25 + i * 1.3;
    if (i > 0) hline(s, sx, y - 0.2, sw);
    T(s, [{ text: r[0], options: { fontFace: DISPLAY, fontSize: 28, bold: true, color: i === 1 ? COL.copper : COL.ink, breakLine: true } },
          { text: r[1], options: { fontSize: 14, color: COL.muted } }], { x: sx, y, w: sw, h: 1.0 });
  });
  source(s, "Data: emisi karbon kawasan budidaya PBPH PT Mayawana Persada (lihat Lampiran B).");
  locator(s, "prod");
}

// 13 · Peat: five mitigation sources
{
  const s = slide("CONTENT", "JIKA KONSESI BERGAMBUT",
    "Jika konsesi bergambut, ada lima sumber mitigasi — dan satu larangan: double counting",
    "Kanal dapat meningkatkan potensi mitigasi, sekaligus memperketat legal due diligence. Potensi pengurangan emisi bisa berasal dari beberapa sumber, tetapi tidak boleh double counting.\nConstraint: fungsi ekosistem gambut, kewajiban perlindungan, status kanal existing, legalitas baseline, permanence/reversal dan kebakaran harus masuk desain proyek.");
  const src = ["Avoided conversion", "Avoided peat drainage", "Rewetting / restorasi", "Fire risk reduction", "Biomass recovery"];
  const n = src.length, step = CW / n, d = 1.35, cy = 2.3;
  hline(s, MX + step / 2, cy + d / 2, step * (n - 1), COL.hair, 1.5);
  src.forEach((t, i) => {
    const cx = MX + step * i + step / 2;
    s.addShape(pres.shapes.OVAL, { x: cx - d / 2, y: cy, w: d, h: d, fill: { color: COL.lindung }, line: { color: COL.white, width: 3 }, objectName: "sumber-" + (i + 1) });
    T(s, String(i + 1), { x: cx - d / 2, y: cy, w: d, h: d, fontFace: DISPLAY, fontSize: 32, bold: true, color: COL.white, align: "center", valign: "middle" });
    T(s, t, { x: cx - 1.1, y: cy + d + 0.15, w: 2.2, h: 0.6, fontSize: 15, bold: true, align: "center" });
  });
  const by = 4.75;
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: by, w: CW, h: 1.45, fill: { color: COL.tint }, line: { type: "none" } });
  T(s, "CONSTRAINT YANG WAJIB MASUK DESAIN PROYEK", { x: MX + 0.3, y: by + 0.2, w: 8, h: 0.3, fontSize: 12, bold: true, color: COL.copper, charSpacing: 1 });
  const cons = ["Fungsi ekosistem gambut", "Kewajiban perlindungan", "Status kanal existing", "Legalitas baseline", "Permanence / reversal", "Kebakaran"];
  const cw = (CW - 0.6) / 3;
  cons.forEach((t, i) => {
    T(s, t, { x: MX + 0.3 + (i % 3) * cw, y: by + 0.6 + Math.floor(i / 3) * 0.38, w: cw, h: 0.35, fontSize: 15, bullet: true });
  });
  locator(s, "lindung");
}

// =====================================================================
section("Gate 3 · Bisnis");
divider(3, "GATE 3  ·  BISNIS", "Apakah risk-adjusted NPV karbon mengalahkan alternatif HTI?", "NPV HTI vs karbon  ·  Variabel nilai  ·  Risiko");

// 15 · NPV comparison
{
  const s = slide("CONTENT", "KELAYAKAN USAHA",
    "Bandingkan NPV, bukan harga karbon per hektar",
    "Skenario A · Lanjut HTI — Pendapatan: penjualan kayu akasia. Biaya & risiko: land clearing & pembangunan kanal; nursery, planting, silvikultur; harvesting & transport; kebakaran & gangguan; kewajiban lingkungan → NPV HTI.\nSkenario B · MUK Karbon — Pendapatan: unit karbon eligible; potensi PJL/HHBK lain. Biaya & risiko: opportunity cost kayu; proteksi/restorasi/rewetting; MRV, validasi & verifikasi; registrasi/developer/buffer; community & safeguard → NPV Karbon.\nGO jika risk-adjusted NPV Karbon > alternatif HTI + strategic value.");
  const zones = [
    ["SKENARIO A", "Lanjut HTI", ["Penjualan kayu akasia"], ["Land clearing & pembangunan kanal", "Nursery, planting, silvikultur", "Harvesting & transport", "Kebakaran & gangguan", "Kewajiban lingkungan"], COL.akasia, "NPV HTI"],
    ["SKENARIO B", "MUK karbon", ["Unit karbon eligible", "Potensi PJL / HHBK lain"], ["Opportunity cost kayu", "Proteksi, restorasi, rewetting", "MRV, validasi & verifikasi", "Registrasi, developer, buffer", "Community & safeguard"], COL.lindung, "NPV Karbon"],
  ];
  const gap = 1.0, zw = (CW - gap) / 2, y = 2.15;
  zones.forEach((z, i) => {
    const x = MX + i * (zw + gap);
    T(s, [{ text: z[0] + "  ", options: { fontSize: 12, color: COL.muted, bold: true, charSpacing: 2 } }, { text: z[1], options: { fontFace: DISPLAY, fontSize: 22, bold: true, color: z[4] === COL.akasia ? COL.ink : COL.lindung } }],
      { x, y, w: zw, h: 0.45 });
    hline(s, x, y + 0.6, zw, z[4], 2);
    const plus = z[2].map((t) => ({ text: "+  " + t, options: { breakLine: true } }));
    const minus = z[3].map((t, k) => ({ text: "−  " + t, options: { breakLine: k < z[3].length - 1, color: COL.muted } }));
    T(s, [{ text: "Pendapatan", options: { bold: true, breakLine: true } }, ...plus, { text: " ", options: { fontSize: 6, breakLine: true } },
          { text: "Biaya & risiko", options: { bold: true, breakLine: true } }, ...minus], { x, y: y + 0.8, w: zw, h: 2.8, fontSize: 15 });
    T(s, "→ " + z[5], { x, y: y + 3.45, w: zw, h: 0.35, fontSize: 16, bold: true, color: z[4] === COL.akasia ? COL.ink : COL.lindung });
  });
  T(s, "vs", { x: MX + zw, y: y + 1.7, w: gap, h: 0.6, fontFace: DISPLAY, fontSize: 24, italic: true, color: COL.muted, align: "center" });
  const gy = 6.15;
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: gy, w: CW, h: 0.5, fill: { color: COL.tint }, line: { type: "none" } });
  T(s, [{ text: "GO ", options: { bold: true, color: COL.copper } }, { text: "jika risk-adjusted NPV karbon > NPV HTI + nilai strategis", options: { bold: true } }],
    { x: MX + 0.3, y: gy, w: CW - 0.6, h: 0.5, fontSize: 15, valign: "middle" });
  locator(s, "both");
}

// 16 · Value drivers table
{
  const s = slide("CONTENT", "VARIABEL NILAI",
    "Empat variabel menentukan apakah 71.350 ha benar-benar bankable",
    "Eligible area: berapa ha lolos legal & methodological screening? Data: kawasan lindung 71.349,6 ha (kandidat ±72.000 ha); kawasan budidaya 66.000 ha.\nNet tCO2e: konservatif 7,4 juta; base 12,0 juta; upside 16,6 juta tCO2e.\nNet carbon price: harga jual dikurangi fee, pajak/PNBP & transaction cost — konservatif US$4,0; base US$8,0; upside US$16,0 per tCO2e.\nOpportunity cost: margin HTI yang dilepas + biaya transisi/restorasi — konservatif ±US$23 juta; base ±US$37 juta; upside ±US$51 juta.\nJangan membuat proyeksi revenue sebelum keempat variabel ini memiliki rentang konservatif–base–upside.");
  const hdr = (t, al = "right") => ({ text: t, options: { bold: true, color: HEX.muted, fontSize: 12, align: al, border: [{ type: "none" }, { type: "none" }, { pt: 1, color: HEX.ink }, { type: "none" }] } });
  const rowB = { border: [{ type: "none" }, { type: "none" }, { pt: 0.75, color: HEX.hair }, { type: "none" }] };
  const name = (a, b) => ({ text: [{ text: a, options: { bold: true, breakLine: true } }, { text: b, options: { fontSize: 12, color: HEX.muted } }], options: Object.assign({ valign: "middle" }, rowB) });
  const num = (t, base) => ({ text: t, options: Object.assign({ align: "right", valign: "middle", bold: !!base, fill: base ? { color: HEX.tint } : undefined, fontFace: base ? undefined : undefined }, rowB) });
  const rows = [
    [hdr("Variabel", "left"), hdr("Konservatif"), hdr("Base"), hdr("Upside")],
    [name("Eligible area", "ha yang lolos screening legal & metodologi"), { text: "Kandidat 71.349,6 ha — luas eligible belum diketahui", options: Object.assign({ colspan: 3, align: "center", italic: true, color: HEX.copper, valign: "middle" }, rowB) }],
    [name("Net tCO₂e", "6 tahun"), num("7,4 juta"), num("12,0 juta", true), num("16,6 juta")],
    [name("Net carbon price", "US$/tCO₂e, setelah fee, pajak/PNBP, biaya transaksi"), num("4,0"), num("8,0", true), num("16,0")],
    [name("Opportunity cost", "margin HTI dilepas + biaya transisi/restorasi"), num("±US$23 juta"), num("±US$37 juta", true), num("±US$51 juta")],
  ];
  s.addTable(rows, { x: MX, y: 2.15, w: CW, colW: [5.33, 2.2, 2.2, 2.4], rowH: [0.45, 0.85, 0.85, 0.85, 0.85], fontSize: 15, color: HEX.ink, fontFace: "Calibri", margin: [0.06, 0.12, 0.06, 0.12] });
  T(s, "Jangan memproyeksikan revenue sebelum keempat variabel punya rentang konservatif–base–upside.", { x: MX, y: 6.15, w: CW, h: 0.35, fontSize: 14, bold: true, color: COL.lindung });
  locator(s, "lindung");
}

// 17 · Revenue vs opportunity cost chart
{
  const s = slide("CONTENT", "SKENARIO NILAI",
    "Pada skenario konservatif, pendapatan karbon hanya ±US$6,5 juta di atas opportunity cost",
    "Pendapatan bersih = net tCO2e × net carbon price (6 tahun): konservatif 7,4 juta × US$4 ≈ US$29,5 juta; base 12,0 juta × US$8 = US$96 juta; upside 16,6 juta × US$16 ≈ US$265 juta.\nOpportunity cost: US$23 / 37 / 51 juta.\nSelisih: ±US$6,5 juta (konservatif), ±US$59 juta (base), ±US$214 juta (upside) — sebelum biaya MRV, validasi, registrasi, restorasi dan buffer. Pada skenario konservatif, biaya-biaya ini berpotensi menghabiskan seluruh selisih.");
  s.addChart(pres.charts.BAR, [
    { name: "Pendapatan karbon bersih", labels: ["Konservatif", "Base", "Upside"], values: [29.5, 96, 265] },
    { name: "Opportunity cost HTI", labels: ["Konservatif", "Base", "Upside"], values: [23, 37, 51] },
  ], Object.assign(CHART_BASE(), {
    x: MX, y: 2.1, w: 8.2, h: 4.25, barDir: "col", barGrouping: "clustered", barGapWidthPct: 60, chartColors: [HEX.lindung, HEX.akasia],
    dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", valAxisHidden: true, valAxisMaxVal: 300,
    title: "US$ juta, 6 tahun, sebelum biaya MRV, restorasi & buffer", showLegend: true, legendPos: "t", legendFontSize: 12, legendColor: HEX.muted, legendFontFace: "+mn-lt",
  }));
  const sx = 9.3, sw = W - MX - sx;
  T(s, [{ text: "+6,5", options: { fontFace: DISPLAY, fontSize: 54, bold: true, color: COL.copper, breakLine: true } },
        { text: "US$ juta selisih konservatif", options: { fontSize: 15, bold: true } }], { x: sx, y: 2.25, w: sw, h: 1.6 });
  hline(s, sx, 4.05, sw);
  T(s, "Biaya MRV, validasi, registrasi dan buffer belum dikurangi — pada skenario konservatif biaya ini bisa menghapus seluruh selisih.", { x: sx, y: 4.2, w: sw, h: 1.6, fontSize: 15, color: COL.muted });
  source(s, "Pendapatan = net tCO₂e × net carbon price (slide 16). Selisih base ±US$59 juta; upside ±US$214 juta.");
  locator(s, "lindung");
}

// 18 · Risk register
{
  const s = slide("CONTENT", "RISK REGISTER AWAL",
    "Risiko terbesar adalah integritas baseline, bukan teknis MRV",
    "Tinggi — Legal baseline: BAU ternyata tidak legal / area wajib dilindungi → baseline 7,4–16,6 juta tCO2e hilang. Additionality: BAU lindung diuji lewat RKU/RKT, peta rencana, dan rekam jejak. Permanence/fire: kebakaran, reversal stok 70,27 juta tCO2e; persentase buffer belum ada.\nSedang — RKUPH transition: perubahan RKUPH belum disetujui → proyek tertunda. Market/price: proyeksi net price US$4/8 per tCO2e; acuan pasar US$7–10. Social safeguard: konflik tenurial & benefit sharing → biaya naik, registrasi tertunda.");
  const cols = [
    ["TINGGI", COL.copper, [
      ["Legal baseline", "BAU ternyata tidak legal atau areal wajib dilindungi → baseline 7,4–16,6 juta tCO₂e hilang"],
      ["Additionality", "BAU lindung harus dibuktikan lewat RKU/RKT, peta rencana dan rekam jejak"],
      ["Permanence / kebakaran", "Reversal atas stok 70,27 juta tCO₂e; persentase buffer belum ditetapkan"]]],
    ["SEDANG", COL.akasia, [
      ["Transisi RKUPH", "Perubahan RKUPH belum disetujui → proyek tertunda"],
      ["Pasar / harga", "Net price US$4–8 per tCO₂e vs acuan pasar US$7–10"],
      ["Social safeguard", "Konflik tenurial & benefit sharing → biaya naik, registrasi tertunda"]]],
  ];
  const gap = 0.6, cw = (CW - gap) / 2, y0 = 2.15;
  cols.forEach(([lvl, color, items], i) => {
    const x = MX + i * (cw + gap);
    chip(s, lvl, x, y0, 1.3, color);
    T(s, (i === 0 ? "3 risiko — semuanya menyangkut baseline & stok" : "3 risiko — jadwal, harga, sosial"), { x: x + 1.5, y: y0, w: cw - 1.5, h: 0.34, fontSize: 13, color: COL.muted, valign: "middle" });
    items.forEach(([h, d], k) => {
      const y = y0 + 0.6 + k * 1.2;
      hline(s, x, y, cw);
      T(s, [{ text: h, options: { bold: true, fontSize: 16, breakLine: true } }, { text: d, options: { fontSize: 14, color: COL.muted } }], { x, y: y + 0.12, w: cw, h: 1.0 });
    });
  });
  locator(s, "both");
}

// =====================================================================
section("Jalan ke depan");

// 19 · Pathway with the gate
{
  const s = slide("CONTENT", "LEGAL CARBON DEVELOPMENT PATHWAY",
    "Tujuh tahap, satu gate: RKUPH baru diubah setelah tahap 03",
    "Urutan kerja yang mengurangi risiko sunk cost: 01 Legal & spatial due diligence; 02 Carbon feasibility & methodology; 03 Business case NPV HTI vs karbon; [gate keputusan] 04 Perubahan/penyesuaian RKUPH; 05 DRAM/registrasi & validasi; 06 Implementasi, MRV & verifikasi; 07 Unit karbon & transaksi.\nGate keputusan utama berada setelah tahap 03: hanya lanjut perubahan RKUPH jika legal eligibility dan economics telah terbukti.\nPermenhut 6/2026 mengatur jalur perdagangan karbon oleh Pelaku Usaha, termasuk pemegang PBPH.");
  const st = ["Legal & spatial due diligence", "Carbon feasibility & metodologi", "Business case NPV HTI vs karbon", "Perubahan / penyesuaian RKUPH", "DRAM, registrasi & validasi", "Implementasi, MRV & verifikasi", "Unit karbon & transaksi"];
  const gateW = 0.7, step = (CW - gateW) / 7, y = 2.75;
  T(s, "FEASIBILITY — biaya rendah, bisa dihentikan", { x: MX, y: 2.15, w: step * 3, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 1 });
  T(s, "DEVELOPMENT — komitmen investasi", { x: MX + step * 3 + gateW, y: 2.15, w: step * 4, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 1 });
  st.forEach((t, i) => {
    const x = MX + step * i + (i >= 3 ? gateW : 0);
    const pre = i < 3;
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.05, y, w: step - 0.1, h: 0.08, fill: { color: pre ? COL.lindung : COL.akasia }, line: { type: "none" } });
    T(s, String(i + 1).padStart(2, "0"), { x: x + 0.05, y: y + 0.25, w: step - 0.1, h: 0.6, fontFace: DISPLAY, fontSize: 30, bold: true, color: pre ? COL.lindung : COL.akasia });
    T(s, t, { x: x + 0.05, y: y + 0.95, w: step - 0.2, h: 1.1, fontSize: 14, bold: pre });
  });
  const gx = MX + step * 3;
  s.addShape(pres.shapes.LINE, { x: gx + gateW / 2, y: 2.55, w: 0, h: 2.25, line: { color: COL.copper, width: 2.5, dashType: "dash" } });
  chip(s, "GATE", gx + gateW / 2 - 0.4, 4.85, 0.8, COL.copper);
  const by = 5.45;
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: by, w: CW, h: 0.85, fill: { color: COL.tint }, line: { type: "none" } });
  T(s, [{ text: "Gate keputusan setelah tahap 03: ", options: { bold: true, color: COL.copper } }, { text: "RKUPH hanya diubah jika legal eligibility dan economics sudah terbukti." }],
    { x: MX + 0.3, y: by, w: CW - 0.6, h: 0.85, fontSize: 16, valign: "middle" });
  source(s, "Permenhut 6/2026 mengatur jalur perdagangan karbon oleh Pelaku Usaha, termasuk pemegang PBPH.");
  locator(s, "both");
}

// 20 · Minimum data
{
  const s = slide("CONTENT", "DATA MINIMUM FEASIBILITY STUDY",
    "Sepuluh dokumen yang sudah dimiliki perusahaan menjadi bukti baseline",
    "Dokumen existing menjadi aset utama untuk membuktikan baseline dan menyaring eligibility. Output: legal eligible area → carbon eligible area → tCO2e → economics → GO / NO-GO.");
  const groups = [
    ["Legal & perencanaan", ["SK PBPH & perubahan", "RKUPH/RKU approved + peta", "RKT/RKTPH & realisasi", "Shapefile konsesi & blok", "Biaya, yield & margin HTI"]],
    ["Biofisik & historis", ["Peta gambut/FLEG & hidrologi", "Existing / rencana kanal", "Riwayat land clearing & planting", "Kebakaran & muka air", "Tutupan lahan historis"]],
  ];
  const gap = 0.6, cw = (CW - gap) / 2, y0 = 2.15;
  groups.forEach(([h, items], gi) => {
    const x = MX + gi * (cw + gap);
    T(s, h.toUpperCase(), { x, y: y0, w: cw, h: 0.3, fontSize: 12, bold: true, color: COL.muted, charSpacing: 2 });
    items.forEach((t, k) => {
      const y = y0 + 0.45 + k * 0.52;
      hline(s, x, y, cw);
      T(s, String(gi * 5 + k + 1).padStart(2, "0"), { x, y: y + 0.1, w: 0.5, h: 0.35, fontFace: DISPLAY, fontSize: 15, bold: true, color: COL.lindung });
      T(s, t, { x: x + 0.6, y: y + 0.1, w: cw - 0.6, h: 0.35, fontSize: 15 });
    });
  });
  const flow = ["Legal eligible area", "Carbon eligible area", "tCO₂e", "Economics", "GO / NO-GO"];
  const fy = 5.55, aw = 0.35, fw = (CW - aw * 4) / 5;
  flow.forEach((t, i) => {
    const x = MX + i * (fw + aw);
    const last = i === flow.length - 1;
    s.addShape(pres.shapes.RECTANGLE, { x, y: fy, w: fw, h: 0.6, fill: { color: last ? COL.copper : COL.forest }, line: { type: "none" } });
    T(s, t, { x, y: fy, w: fw, h: 0.6, fontSize: 14, bold: true, color: COL.white, align: "center", valign: "middle" });
    if (!last) arrow(s, x + fw + 0.05, fy + 0.3, x + fw + aw - 0.05, fy + 0.3, COL.muted);
  });
  T(s, "OUTPUT", { x: MX, y: fy - 0.35, w: 3, h: 0.25, fontSize: 11, bold: true, color: COL.muted, charSpacing: 2 });
  locator(s, "both");
}

// 21 · Close with one action
{
  const s = slide("COVER", "REKOMENDASI KEPUTUSAN", "Lanjutkan ke feasibility study — bukan langsung ke pengembangan proyek",
    "Gate 1 · Legal: apakah BAU legal dan area benar-benar eligible? Blok lindung 71.349,6 ha berada dalam SK PBPH. Berikutnya: verifikasi SK PBPH, RKUPH & peta.\nGate 2 · Karbon: apakah additionality & metodologi dapat dipertahankan? Estimasi 7,4–16,6 juta tCO2e (6 th). Berikutnya: uji additionality & metodologi SRUK.\nGate 3 · Bisnis: apakah risk-adjusted NPV mengalahkan alternatif HTI? Proyeksi pendapatan bersih US$29,5–265 juta vs opportunity cost US$23–51 juta (6 th), sebelum biaya MRV, restorasi & buffer.\nJika ketiga gate lolos → perubahan RKUPH + pengembangan MUK karbon ±72.000 ha layak dilanjutkan.");
  const gates = [
    ["GATE 1 · LEGAL", "Blok lindung 71.349,6 ha berada dalam SK PBPH.", "Verifikasi SK PBPH, RKUPH & peta"],
    ["GATE 2 · KARBON", "Estimasi 7,4–16,6 juta tCO₂e dalam 6 tahun.", "Uji additionality & metodologi SRUK"],
    ["GATE 3 · BISNIS", "Pendapatan US$29,5–265 juta vs opportunity cost US$23–51 juta.", "Hitung NPV setelah biaya MRV, restorasi & buffer"],
  ];
  const gap = 0.45, gw = (CW - 2 * gap) / 3, y = 3.3;
  gates.forEach((g, i) => {
    const x = MX + i * (gw + gap);
    hline(s, x, y, gw, COL.leaf, 1);
    T(s, g[0], { x, y: y + 0.15, w: gw, h: 0.3, fontSize: 12, bold: true, color: COL.leaf, charSpacing: 2 });
    T(s, g[1], { x, y: y + 0.5, w: gw, h: 0.75, fontSize: 15, color: COL.white });
    T(s, [{ text: "Berikutnya: ", options: { bold: true, color: COL.leaf } }, { text: g[2], options: { color: "C8D6CD" } }], { x, y: y + 1.3, w: gw, h: 0.6, fontSize: 14 });
  });
  const ay = 5.45;
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: ay, w: CW, h: 0.8, fill: { color: COL.white }, line: { type: "none" } });
  T(s, [{ text: "Keputusan yang diminta: ", options: { bold: true, color: COL.copper } }, { text: "tugaskan Legal–Carbon Feasibility Screening atas 71.350 ha. Jika ketiga gate lolos → ubah RKUPH dan kembangkan MUK karbon.", options: { bold: true, color: COL.ink } }],
    { x: MX + 0.3, y: ay, w: CW - 0.6, h: 0.8, fontSize: 16, valign: "middle" });
  splitBar(s, MX, 6.75, 1.6, 0.1, "lindung", true);
  T(s, "Analisis awal — perlu dikonfirmasi dengan dokumen PBPH/RKUPH dan data spasial aktual", { x: MX + 1.75, y: 6.68, w: 9, h: 0.25, fontSize: 10, italic: true, color: COL.leaf });
}

// =====================================================================
section("Lampiran");

// 22 · Appendix A — scheme image
{
  const s = slide("CONTENT", "LAMPIRAN A", "Skema kerja sama: pemegang PBPH, perusahaan karbon, dan carbon developer",
    "Skema kerja sama Multiusaha Kehutanan pada PBPH: integrasi usaha awal HTI (akasia) dan pengembangan usaha karbon melalui perusahaan karbon sebagai proponen lain, dengan dukungan Carbon Developer. Mencakup dasar hukum, lingkup tiap pihak, Joint Project Committee, alur pelaksanaan proyek karbon (8 tahap), skema pembagian pendapatan (ilustrasi), serta hasil dan manfaat.");
  const h = 4.75, w = h * 1.5;
  s.addImage({ path: path.join(ROOT, "assets/skema_kerja_sama_pbph.png"), x: MX, y: 1.95, w, h, altText: "Skema kerja sama multiusaha kehutanan pada PBPH" });
  const tx = MX + w + 0.45, tw = W - MX - tx;
  const items = [["Perusahaan A", "Pemegang PBPH: izin, HTI akasia, alokasi areal karbon via RKUPH"], ["Perusahaan B", "Perusahaan karbon: co-proponent, investasi, MRV, pemasaran unit"], ["Carbon developer", "Studi kelayakan, PDD/DRAM, validasi & verifikasi"], ["Joint Project Committee", "Forum keputusan bersama: areal, anggaran, pembagian pendapatan"]];
  items.forEach(([h2, d], i) => {
    const y = 2.0 + i * 1.15;
    if (i > 0) hline(s, tx, y - 0.12, tw);
    T(s, [{ text: h2, options: { bold: true, breakLine: true } }, { text: d, options: { color: COL.muted, fontSize: 13 } }], { x: tx, y, w: tw, h: 1.0, fontSize: 15 });
  });
  locator(s, "both");
}

// 23 · Appendix B — data tables
{
  const s = slide("CONTENT", "LAMPIRAN B", "Data stok dan emisi karbon PBPH PT Mayawana Persada",
    "Sumber data: tabel stok karbon kawasan budidaya & lindung (2026) serta emisi karbon kawasan budidaya per tahun pembukaan 2021–2026, faktor emisi 20 tC/ha/th.");
  const BR = { border: [{ type: "none" }, { type: "none" }, { pt: 0.5, color: HEX.hair }, { type: "none" }] };
  const H = (t, al = "right") => ({ text: t, options: { bold: true, color: HEX.muted, align: al, border: [{ type: "none" }, { type: "none" }, { pt: 1, color: HEX.ink }, { type: "none" }] } });
  const c = (t, o = {}) => ({ text: t, options: Object.assign({ align: "right" }, BR, o) });
  const l = (t, o = {}) => ({ text: t, options: Object.assign({ align: "left", bold: true }, BR, o) });
  T(s, "STOK KARBON 2026", { x: MX, y: 1.95, w: 5, h: 0.25, fontSize: 11, bold: true, color: COL.lindung, charSpacing: 2 });
  s.addTable([
    [H("Kawasan", "left"), H("Luas (ha)"), H("Karbon (tC/ha)"), H("Stok (tC)"), H("Setara CO₂ (tCO₂e)")],
    [l("Budidaya (produksi)"), c("66.908,4"), c("59,5"), c("3.981.049,8"), c("14.597.182,6")],
    [l("Lindung"), c("71.349,6"), c("268,6"), c("19.164.514,4"), c("70.269.886,1", { bold: true, color: HEX.lindung })],
  ], { x: MX, y: 2.25, w: CW, colW: [3.13, 2.2, 2.2, 2.3, 2.3], rowH: 0.32, fontSize: 12, color: HEX.ink, fontFace: "Calibri", margin: [0.03, 0.08, 0.03, 0.08] });
  T(s, "EMISI KAWASAN BUDIDAYA PER TAHUN PEMBUKAAN", { x: MX, y: 3.45, w: 8, h: 0.25, fontSize: 11, bold: true, color: COL.lindung, charSpacing: 2 });
  const em = [["2021", "4.884", "97.680", "358.160", "2.148.960"], ["2022", "8.162", "163.240", "598.547", "2.992.733"], ["2023", "19.221", "384.420", "1.409.540", "5.638.160"], ["2024", "1.571", "31.420", "115.207", "345.620"], ["2025", "1.890", "37.800", "138.600", "277.200"], ["2026", "10.920", "218.400", "800.800", "800.800"]];
  const rows = [[H("Tahun", "left"), H("Luas (ha)"), H("Faktor emisi (tC/ha/th)"), H("Emisi (tC/th)"), H("Emisi (tCO₂/th)"), H("Emisi kumulatif (tCO₂)")]];
  em.forEach((r) => rows.push([l(r[0], { bold: false }), c(r[1]), c("20"), c(r[2]), c(r[3]), c(r[4], r[0] === "2023" ? { bold: true, color: HEX.copper } : {})]));
  rows.push([l("Total"), c("46.648", { bold: true }), c(""), c("932.960", { bold: true }), c("3.420.853", { bold: true }), c("12.203.473", { bold: true })]);
  s.addTable(rows, { x: MX, y: 3.75, w: CW, colW: [1.8, 1.9, 2.2, 2.0, 2.0, 2.23], rowH: 0.3, fontSize: 12, color: HEX.ink, fontFace: "Calibri", margin: [0.03, 0.08, 0.03, 0.08] });
  locator(s, "both");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (APPLY_THEME) {
    const { applyTheme } = require(APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("wrote", OUT);
})();
