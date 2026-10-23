// Builds a one-slide summary of VCU and carbon economic value (Plan Vivo, Mempawah peat site).
// Same visual identity as build_deck.js / build_luasan_pv.js. Figures match the VCU infographic defaults.
// Usage: node build/build_vcu_slide.js <out.pptx> [apply_theme.js path]
const pptxgen = require("pptxgenjs");

const OUT = process.argv[2] || "VCU_Nilai_Karbon.pptx";
const APPLY_THEME = process.argv[3];

const HEX = {
  ink: "1B2420", forest: "163A2E", lindung: "1F5A45", akasia: "9C967F", copper: "B5551F",
  amber: "C8901E", leaf: "7FB096", river: "3E78A8",
  muted: "5F6B65", hair: "D5DBD6", tint: "EEF2EE", white: "FFFFFF",
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
pres.title = "VCU dan Potensi Nilai Ekonomi Karbon";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const COL = {
  ink: C.text1, forest: C.text2, white: C.background1, tint: C.background2,
  lindung: C.accent1, akasia: C.accent2, copper: C.accent3, amber: C.accent4, leaf: C.accent5, river: C.accent6,
};
const DISPLAY = "Cambria";
const W = 13.333, MX = 0.6, CW = W - 2 * MX;

pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: COL.white },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.45, w: 9, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2, margin: 0, valign: "top" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.8, w: CW, h: 0.6, fontFace: DISPLAY, fontSize: 28, bold: true, color: COL.ink, margin: 0, valign: "top", align: "left" }, text: "" } },
  ],
});

function T(s, text, o) {
  s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: COL.ink, valign: "top" }, o));
}
function hline(s, x, y, w, color, width = 0.75) {
  s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: color || HEX.hair, width } });
}
const nf = (n, d = 0) => n.toLocaleString("id-ID", { minimumFractionDigits: d, maximumFractionDigits: d });

// ---- model (same defaults as the infographic) ----
const A = { bio: 100, def: 8.29, peat: 16, eff: 1, arr: 8, arrHa: 591.26, buf: 0.35, dur: 35, lphd: 0.6, fx: 16000 };
const bio = A.def * A.eff * A.bio * 44 / 12;
const peat = A.def * A.eff * A.peat * (A.dur + 1) / 2;
const arr = A.arrHa * A.arr;
const gross = bio + peat + arr, cut = gross * A.buf, net = gross - cut;
const val = (p) => net * p * A.fx;
const rp = (n) => n >= 1e9 ? "Rp " + nf(n / 1e9, 2) + " M" : "Rp " + nf(n / 1e6, 0) + " jt";

pres.addSection({ title: "VCU dan nilai karbon" });
const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "VCU dan nilai karbon" });
s.addText("POTENSI KREDIT KARBON  ·  PLAN VIVO  ·  KHG SUNGAI MEMPAWAH", { placeholder: "kicker" });
s.addText(`±${nf(net)} unit per tahun, senilai ${rp(val(10)).replace(" jt", " juta").replace(" M", " miliar")} pada US$10`, { placeholder: "title" });
s.addNotes(
  `Estimasi awal dengan rumus terkoreksi. REDD+ biomassa = ${nf(A.def, 2)} ha/tahun × ${A.bio} tC/ha × 44/12 = ${nf(bio)} tCO2e/tahun. ` +
  `REDD+ gambut = ${nf(A.def, 2)} × ${A.peat} tCO2e/ha/tahun × rata-rata ${(A.dur + 1) / 2} tahun berjalan = ${nf(peat)}. ` +
  `ARR = 591,26 ha × ${A.arr} tCO2e/ha/tahun = ${nf(arr)}. Total ${nf(gross)}, dipotong buffer 35% (${nf(cut)}) = ${nf(net)} unit/tahun, ${nf(net * A.dur)} unit selama ${A.dur} tahun. ` +
  `Karbon biomassa 100 tC/ha dan serapan ARR 8 tCO2e/ha/tahun adalah asumsi; ganti dengan FREL KLHK/plot lapangan. ` +
  `Pendapatan kotor: belum dikurangi biaya validasi, registrasi, MRV, restorasi; belum memperhitungkan masa tumbuh ARR dan kebocoran. ` +
  `Plan Vivo menerbitkan Plan Vivo Certificate (PVC); 1 unit = 1 tCO2e. Angka spreadsheet (6,34 dan 13.745 unit/tahun) tidak dipakai karena rumusnya salah.`
);

// ---- left: flow from emission reductions to net units ----
const lx = MX, lw = 6.55, y0 = 1.75;
T(s, "DARI PENGURANGAN EMISI KE UNIT BERSIH (tCO₂e/TAHUN)", { x: lx, y: y0, w: lw, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2 });
const labW = 2.35, bx = lx + labW + 0.15, vW = 0.85, bw = lw - labW - 0.15 - vW - 0.15;
const sc = bw / gross;
const rows = [
  { lab: "REDD+ biomassa", sub: "8,29 ha/th × 100 tC/ha × 44/12", v: bio, start: 0, col: COL.lindung },
  { lab: "REDD+ gambut", sub: `Terhindar, rata-rata ${A.dur} th`, v: peat, start: bio, col: COL.leaf },
  { lab: "ARR serapan", sub: "591,26 ha × 8 tCO₂e/ha", v: arr, start: bio + peat, col: COL.amber },
  { lab: "Potongan buffer 35%", sub: "Risiko dan ketidakpastian", v: -cut, start: gross - cut, col: COL.copper },
];
const rh = 0.66;
rows.forEach((r, i) => {
  const y = y0 + 0.45 + i * rh;
  T(s, [{ text: r.lab, options: { bold: true, breakLine: true } }, { text: r.sub, options: { fontSize: 11, color: HEX.muted } }], { x: lx, y, w: labW, h: 0.55, fontSize: 14 });
  s.addShape(pres.shapes.RECTANGLE, { x: bx + r.start * sc, y: y + 0.1, w: Math.abs(r.v) * sc, h: 0.3, fill: { color: r.col }, line: { type: "none" }, objectName: "aliran-" + i });
  T(s, (r.v < 0 ? "− " : "") + nf(Math.abs(r.v)), { x: bx + bw + 0.15, y: y + 0.05, w: vW, h: 0.4, fontSize: 14, align: "right", valign: "middle", color: r.v < 0 ? COL.copper : COL.ink });
  hline(s, lx, y + rh - 0.06, lw);
});
const ty = y0 + 0.45 + rows.length * rh + 0.02;
T(s, [{ text: "Unit bersih", options: { bold: true, breakLine: true } }, { text: `${nf(net * A.dur)} unit selama ${A.dur} tahun`, options: { fontSize: 11, color: HEX.muted } }], { x: lx, y: ty, w: labW, h: 0.55, fontSize: 15 });
s.addShape(pres.shapes.RECTANGLE, { x: bx, y: ty + 0.06, w: net * sc, h: 0.38, fill: { color: COL.forest }, line: { type: "none" }, objectName: "aliran-bersih" });
T(s, nf(net), { x: bx + bw + 0.15 - 0.4, y: ty, w: vW + 0.4, h: 0.5, fontFace: DISPLAY, fontSize: 20, bold: true, align: "right", valign: "middle" });

// ---- right: price scenarios ----
const rx = lx + lw + 0.55, rw = W - MX - rx;
T(s, "SKENARIO HARGA · KURS Rp 16.000", { x: rx, y: y0, w: rw, h: 0.3, fontSize: 12, bold: true, color: COL.lindung, charSpacing: 2 });
const BR = { border: [{ type: "none" }, { type: "none" }, { pt: 0.5, color: HEX.hair }, { type: "none" }] };
const H = (t, al = "right") => ({ text: t, options: { bold: true, color: HEX.muted, align: al, fontSize: 11, border: [{ type: "none" }, { type: "none" }, { pt: 1, color: HEX.ink }, { type: "none" }] } });
const trows = [[H("Harga/unit", "left"), H("Per tahun"), H("LPHD 60%/th"), H(`Total ${A.dur} th`)]];
[3, 5, 10, 15].forEach((p) => {
  const sel = p === 10;
  const o = (al) => Object.assign({ align: al, bold: sel, color: HEX.ink, fill: sel ? { color: HEX.tint } : undefined }, BR);
  trows.push([
    { text: "US$" + p, options: o("left") },
    { text: rp(val(p)), options: o("right") },
    { text: rp(val(p) * A.lphd), options: Object.assign(o("right"), { color: sel ? HEX.ink : HEX.muted }) },
    { text: rp(val(p) * A.dur), options: o("right") },
  ]);
});
s.addTable(trows, { x: rx, y: y0 + 0.45, w: rw, colW: [1.0, 1.35, 1.35, 1.333], rowH: 0.42, fontSize: 14, color: HEX.ink, fontFace: "Calibri", valign: "middle", margin: [0.02, 0.08, 0.02, 0.08] });

// big callout under the table
const cy = y0 + 0.45 + 5 * 0.42 + 0.3;
T(s, [{ text: rp(val(10) * A.lphd).replace(" jt", " juta"), options: { fontFace: DISPLAY, fontSize: 30, bold: true, color: COL.amber } }, { text: "  per tahun untuk LPHD pada US$10", options: { fontSize: 14, color: HEX.muted } }],
  { x: rx, y: cy, w: rw, h: 0.6, valign: "middle" });
T(s, `Rp ${nf(val(10) * A.lphd * A.dur / 1e9, 1)} miliar selama ${A.dur} tahun · pendapatan kotor, sebelum biaya proyek`, { x: rx, y: cy + 0.6, w: rw, h: 0.3, fontSize: 12, color: HEX.muted });

// ---- bottom: assumptions strip ----
const ay = 5.95, ah = 0.62;
s.addShape(pres.shapes.RECTANGLE, { x: MX, y: ay, w: CW, h: ah, fill: { color: COL.tint }, line: { type: "none" } });
T(s, [
  { text: "Asumsi: ", options: { bold: true, color: COL.copper } },
  { text: "biomassa 100 tC/ha dan serapan ARR 8 tCO₂e/ha/th belum ada datanya; ganti dengan FREL KLHK atau plot. ", options: { color: COL.ink } },
  { text: "Dari data: ", options: { bold: true, color: COL.lindung } },
  { text: "laju bruto 8,29 ha/th, emisi gambut +16 tCO₂e/ha/th, buffer 35%, porsi LPHD 60%.", options: { color: COL.ink } },
], { x: MX + 0.25, y: ay, w: CW - 0.5, h: ah, fontSize: 13, valign: "middle" });
T(s, "Sumber: Export_Output_Gambut_M.xlsx. Plan Vivo menerbitkan PVC (1 unit = 1 tCO₂e). Angka spreadsheet (6,34 dan 13.745 unit/th) tidak dipakai karena rumusnya salah.",
  { x: MX, y: 6.8, w: CW, h: 0.25, fontSize: 10, color: HEX.muted, italic: true });

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (APPLY_THEME) {
    const { applyTheme } = require(APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("wrote", OUT);
})();
