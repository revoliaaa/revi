# -*- coding: utf-8 -*-
"""Bangun dokumen roadmap (Markdown) dari data.py.

    python3 build_md.py ../Roadmap_HD_Pasir_PVClimate.md
"""
import sys

from data import (ACTIVITIES, BASIS, COMPLETION, DOC_CHECKLIST, MILESTONES, RISKS, ROLES, SOURCES, STEP2,
                  TOOLS, TRANSITION, month_label)


def esc(s):
    return str(s).replace("|", "/").replace("\n", " ")


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def build():
    ms = {m["code"]: m for m in MILESTONES}
    L = []
    w = L.append

    w("# Integrated Community Carbon Development Roadmap — Hutan Desa Pasir")
    w("**Plan Vivo PV Climate · SETAPAK 4 & Post-SETAPAK 4**  ")
    w("Kabupaten Mempawah, Kalimantan Barat · Implementing Organization: SAMPAN Kalimantan · "
      "Community Institution: LPHD Pasir · Programme: SETAPAK 4 (didukung TAF)  ")
    w("Versi kerja: Oktober 2026 · Bulan program 1 = Oktober 2026\n")

    w("## Ringkasan")
    w("SETAPAK 4 selesai ketika **PIN Hutan Desa Pasir disetujui Plan Vivo dan proyek tercantum di Project pipeline** "
      "(M7). Pendanaan TAF berakhir **September 2027 (bulan 12)**, sehingga PIN harus diajukan paling lambat **Mei 2027 "
      "(bulan 8)**. Review awal Plan Vivo ±6 minggu dan satu putaran CAR/NIR (±4 minggu review) membuat keputusan "
      "paling cepat **Agustus–September 2027**. Tanggal ini tidak dapat dijamin. Jika Plan Vivo meminta lebih dari "
      "satu putaran revisi, penerimaan pipeline akan jatuh **setelah TAF berakhir** (buffer Okt–Des 2027).\n")
    w("Konsekuensi jadwal 12 bulan:")
    w("- **FPIC tahap i–ii harus selesai Maret 2027 (bulan 6).** Ini ketat untuk proses yang timeline-nya ditentukan "
      "komunitas. Jika komunitas butuh waktu lebih, pengajuan PIN yang mundur, bukan FPIC yang dipercepat.")
    w("- **M3, M4 dan M5 berjalan paralel sejak bulan 3.** Tenaga ahli karbon perlu dikontrak di bulan 2.")
    w("- **Indikator kontrak TAF sebaiknya dua lapis:** *PIN submitted* (Mei 2027) sebagai indikator wajib, dan "
      "*pipeline acceptance* (Sep 2027) sebagai target. Siapkan opsi no-cost extension atau anggaran jembatan untuk "
      "menindaklanjuti review Plan Vivo pada Okt–Des 2027.\n")
    w("Pipeline bukan registrasi dan belum menghasilkan kredit. Registrasi baru terjadi setelah PDD lolos review dan "
      "proyek divalidasi (M9). Kredit yang dapat di-retire (vPVC) baru terbit setelah verifikasi (M11). Semua itu ada di "
      "STEP 2 dan membutuhkan pendanaan baru.\n")
    w("Tiga temuan dari pemeriksaan dokumen resmi mengubah rencana:")
    w("1. **Metodologi adalah risiko terbesar.** Desa Pasir berada di pesisir dan dikenal dengan ekosistem mangrovenya "
      "(Mempawah Mangrove Park). Saat ini Plan Vivo baru menyetujui PM001 (Agriculture & Forestry Carbon Benefit "
      "Assessment, untuk intervensi serapan seperti restorasi) dan PM002 (agroforestri). *Coastal Blue Carbon "
      "Methodology* dan *Mangrove Conservation Module* masih berada di Methodology Pipeline. PDD hanya boleh diajukan "
      "dengan metodologi yang sudah disetujui, jadi M5.4 dijadikan decision gate.")
    w("2. **FPIC di PV Climate bertahap.** Project Requirements V5.7 §2.6.4 meminta keputusan kolektif minimal pada tiga "
      "titik: (i) mempertimbangkan proyek, (ii) terlibat dalam desain, (iii) mengimplementasikan proyek. Tahap i–ii "
      "diselesaikan di SETAPAK 4 (M3.5). Tahap iii masuk STEP 2 sebelum validasi.")
    w("3. **Ada batas waktu setelah pipeline.** PDD wajib diajukan ≤3 tahun setelah PIN disetujui, dan validasi wajib "
      "selesai ≤3 tahun setelah PDD diajukan (Procedures Manual V3.9 §2.2, §4.4). Pendanaan STEP 2 perlu dicari sejak "
      "bulan 12, bukan setelah SETAPAK 4 berakhir.\n")

    w("### Tiga lapis kewajiban")
    w("Setiap aktivitas di matriks diberi kode basis agar jelas mana yang wajib dan mana yang disarankan:\n")
    w(table(["Kode", "Arti", "Contoh"], [
        ("PV", BASIS["PV"], "PIN Template V1.4, FPIC bertahap, GRM, ≥60% pendapatan PVC ke komunitas"),
        ("ID", BASIS["ID"], "Persetujuan Pengelolaan Hutan Desa & LPHD; Perpres 110/2025; Permenhut 6/2026 (offset kehutanan, PADIATAPA bagi KUPS); "
                            "pencatatan SRN/SRUK; MRA Indonesia–Plan Vivo (Sept 2025)"),
        ("PM", BASIS["PM"], "PKS SAMPAN–LPHD, pre-submission call, data room, Go/No-Go"),
    ]))
    w("")

    # ---------------- A
    w("## A. Integrated Project Lifecycle Visualization (Output 1)")
    w("Ringkasan dua tahap ada di `Roadmap_HD_Pasir_PVClimate.pptx` slide 1: STEP 1 (5 tahap: Institutional Readiness, "
      "FPIC & Community, Carbon Feasibility, PIN Submission, PIN Review → PV Pipeline), Transition / Project Handover, lalu "
      "STEP 2 (PDD, Validation, Registration, Implementation & Annual Report, Verification, Issuance, Carbon Sales & Benefit "
      "Sharing). Roadmap detail satu slide 16:9 ada di slide 2. Strukturnya:\n")
    w("```")
    w("STEP 1 · SETAPAK 4 (teal)                                   ┆ GATE ┆  STEP 2 · POST-SETAPAK 4 (navy)")
    w("(M1)─(M2)─(M3)─(M4)─(M5)─(M6)─<M7>  ═══════════════════════ ┆ PIPE ┆ ═ (M8)─<M9>─(M10)─<M11>─(M12)")
    w("          └── M3 ∥ M4 ∥ M5 paralel (bln 3–10) ──┘           ┆ LINE ┆      M12 paralel sejak M8")
    w("( ) = milestone internal     < > = persetujuan eksternal (Plan Vivo / VVB)     ┆ = batas SETAPAK 4")
    w("```\n")
    w("Aturan visual yang dipakai: satu alur tersambung; teal untuk STEP 1 dan navy untuk STEP 2; garis putus-putus "
      "oranye di Pipeline Acceptance; lingkaran untuk milestone internal dan belah ketupat untuk persetujuan "
      "eksternal (M7, M9, M11); kotak putus-putus untuk aktivitas paralel. Panel bawah menegaskan bahwa pipeline ≠ "
      "registrasi ≠ issuance dan menjelaskan tiga jenis unit (fPVC, rPVC, vPVC).\n")
    w("**Urutan resmi siklus PV Climate** (Procedures Manual V3.9, Figure 1): Project Screening (PIN Review) → "
      "PDD submission & assessment → Validation & Registration → Annual Reporting (issuance PVC) → Periodic Verification.\n")
    w("**Tahap yang berjalan paralel atau berbeda menurut jenis proyek:**")
    w("- *Macroscale vs Microscale.* Proyek dengan manfaat karbon <10.000 tCO2e/tahun boleh memakai validasi dan "
      "verifikasi microscale oleh Plan Vivo bersama Independent Expert. Biayanya lebih rendah, tetapi unitnya tidak "
      "bisa mendapat label CCP (ICVCM) atau CORSIA. Proyek di atas ambang itu wajib memakai VVB.")
    w("- *Jenis unit menurut intervensi.* fPVC dapat terbit saat validasi hanya untuk intervensi serapan (restorasi). "
      "Intervensi pengurangan emisi (konservasi) baru menghasilkan rPVC lewat Annual Report, lalu vPVC setelah "
      "verifikasi. Hanya vPVC yang dapat di-retire.")
    w("- *Monitoring berjalan sejak registrasi.* Annual Report wajib tiap 12 bulan (periode pertama berakhir ≤12 bulan "
      "setelah registrasi) dan dapat memuat issuance request. Verifikasi pertama wajib ≤5 tahun setelah validasi.")
    w("- *Start date retroaktif.* Start date Project Area boleh hingga 5 tahun sebelum validasi selesai. Kegiatan "
      "perlindungan atau restorasi yang terdokumentasi sejak STEP 1 berpotensi masuk Project Period, jika additionality "
      "dapat dipertahankan.")
    w("- *Komersialisasi (M12)* dapat dimulai paralel sejak M8 dalam bentuk offtake atau pre-finance, tetapi "
      "penyerahan unit mengikuti issuance.\n")

    # ---------------- B
    w("## B. Master Milestone Matrix")
    w("Versi lengkap yang dapat difilter (dengan kolom status, % progres dan tanggal) ada di "
      "`Milestone_Matrix_HD_Pasir_PVClimate.xlsx` sheet **Master_Matrix**.\n")
    w("### STEP 1 — SETAPAK 4 (tingkat aktivitas)")
    rows = []
    for m in [m for m in MILESTONES if m["step"] == 1]:
        rows.append((f"**STEP 1**", "SETAPAK 4", f"**{m['code']} {m['title']}**", "", m["output"].replace("\n", " "), "", "",
                     f"**{COMPLETION[m['code']]}**"))
        for a in [a for a in ACTIVITIES if a[1] == m["code"]]:
            code, _, name, sub, deliv, evid, pic, acc, dep, *_ = a
            rows.append(("", "", code, f"**{name}** — {sub}", deliv, f"{pic} (A: {acc})", dep, f"Bukti: {evid}"))
    w(table(["Step", "Programme", "Milestone", "Activities", "Key Deliverables", "PIC", "Dependencies",
             "Completion Criteria"], rows))
    w("")
    w("### STEP 2 — Post-SETAPAK 4 (tingkat milestone & workstream)")
    w(table(["Step", "Programme", "Milestone", "Activities / workstreams", "Key Deliverables", "PIC", "Dependencies",
             "Completion Criteria"],
            [("STEP 2", "Post-SETAPAK 4", f"{s['code']} {ms[s['code']]['title']}", s["workstreams"],
              ms[s["code"]]["output"], "Project Coordinator (SAMPAN) + LPHD", s["prereq"], COMPLETION[s["code"]])
             for s in STEP2]))
    w("\nKode PIC: " + "; ".join(f"**{k}** = {v}" for k, v in ROLES.items()) + ". A = accountable.\n")

    # ---------------- C
    w("## C. STEP 1 Detailed Implementation Plan (SETAPAK 4)")
    w("### C1–C4. Activity breakdown, deliverable & bukti, PIC/accountable, dependencies")
    w("Tercakup di Matriks B, dengan kolom bukti verifikasi tersendiri di Excel. Prinsip pembagian peran:")
    w("- **SAMPAN Kalimantan** menjadi calon *Project Coordinator* (badan hukum dengan kehadiran in-country, sesuai "
      "syarat eligibility PV Climate) dan menanggung akuntabilitas dokumen ke Plan Vivo.")
    w("- **LPHD Pasir** menjadi accountable untuk keputusan komunitas: FPIC, GRM, intervensi, prinsip benefit-sharing, "
      "dan WFD.")
    w("- **Tenaga ahli karbon eksternal** mengerjakan M5 dan penyusunan PIN, dengan transfer pengetahuan ke GIS & Carbon "
      "Officer SAMPAN.\n")

    w("### C5. Timeline (pelaksanaan sejak Oktober 2026)")
    w(table(["Milestone", "Mulai", "Selesai", "Durasi", "Jenis", "Catatan"],
            [(f"{m['code']} {m['title']}", month_label(m["start"]), month_label(m["end"]),
              f"{m['end'] - m['start'] + 1} bln", "Eksternal" if m["type"] == "EXT" else "Internal",
              {"M3": "Keputusan FPIC i–ii Mar 2027; tanpa buffer — risiko utama",
               "M4": "Paralel dengan M3/M5; M4.4 selesai sebelum PIN; M4.5–M4.6 lanjut setelah PIN",
               "M5": "Paralel; M5.4 = decision gate metodologi (Feb 2027)",
               "M6": "Submission paling lambat Mei 2027",
               "M7": "Indikatif: review ±6 mgg + 1 putaran CAR/NIR; >1 putaran → lewat Sep 2027"}.get(m["code"], ""))
             for m in MILESTONES if m["step"] == 1]))
    w("")
    w("### C6. Critical path")
    crit = [a[0] for a in ACTIVITIES if a[13]]
    w("`" + " → ".join(crit) + "`\n")
    w("Rantai yang paling menentukan: **legalitas (M1.4) → stakeholder & SEP (M2.1/M2.5) → pra-FPIC (M3.1) → pemetaan "
      "partisipatif (M3.3) → keputusan FPIC i–ii (M3.5) → tutupan lahan & driver (M5.2/M5.3) → metodologi (M5.4) → "
      "estimasi & Go/No-Go (M5.5/M5.6) → draft, review LPHD, final dan submit PIN (M6.2–M6.6) → review Plan Vivo "
      "(M7.1–M7.5)**. Jalur ini **tidak punya float** terhadap akhir TAF (bulan 12). Setiap keterlambatan satu bulan "
      "sebelum Mei 2027 langsung mengurangi waktu review Plan Vivo sebelum September 2027.\n")

    w("### C7. Integrasi 17 Plan Vivo Participatory Tools")
    w(table(["Tool", "Nama", "Dipakai di", "Status tahap PIN", "Status tahap PDD"], TOOLS))
    w("\nCatatan: FPIC dan edukasi tentang proyek lewat *community meeting* bersifat **wajib** di tahap PIN, begitu pula "
      "*stakeholder analysis* dan *E&S risk assessment* (Plan Vivo E&S Risk Management Procedures). Tool 11b dipilih "
      "karena konteks pesisir dan mangrove.\n")

    w("### C8. Document readiness checklist")
    w(table(["ID", "Dokumen", "Sumber", "Basis"], DOC_CHECKLIST))
    w("\nIsi minimum PIN (Procedures Manual §2.1): intervensi yang diusulkan; Project Region/Area beserta hak lahan dan "
      "hak karbon; keterlibatan pemangku kepentingan; kondisi tata guna lahan, livelihood dan ekologi tanpa proyek; "
      "output dan outcome; hambatan; risiko E&S dan potensi double counting; tata kelola dan administrasi; kapasitas "
      "serta rencana dukungan teknis.\n")

    w("### C9. Risk & bottleneck")
    w(table(["ID", "Risiko", "Milestone", "Kemungkinan", "Dampak", "Mitigasi"], RISKS))
    w("")
    w("### C10. Program completion criteria (SETAPAK 4)")
    w("SETAPAK 4 dinyatakan tercapai bila:")
    w("1. **Target wajib program:** PIN final diajukan ke Plan Vivo dengan bukti fee paling lambat Mei 2027 (M6), dan Plan Vivo menyatakan "
      "PIN disetujui sehingga proyek tercantum di Project pipeline (M7).")
    w("2. **Prasyarat kualitas:** BA FPIC tahap i–ii, GRM aktif, peta partisipatif dan KML, feasibility report dengan "
      "keputusan Go/No-Go, serta prinsip benefit-sharing tersedia di data room.")
    w("3. **Handover:** paket serah terima (Bagian E) ditandatangani SAMPAN dan LPHD.")
    w("4. **Jika keputusan Plan Vivo belum keluar** sebelum TAF berakhir (September 2027): laporkan status *PIN submitted, under "
      "review* lengkap dengan log komunikasi. Jangan melaporkannya sebagai *accepted*. Sisa tindak lanjut review "
      "masuk anggaran transisi.\n")

    # ---------------- D
    w("## D. STEP 2 Development Outlook (Post-SETAPAK 4)")
    w("STEP 2 **bukan kewajiban capaian SETAPAK 4**. Angka biaya adalah asumsi perencanaan, bukan tarif Plan Vivo, dan "
      "harus dikonfirmasi dengan dokumen *Costs & fees* Plan Vivo serta penawaran VVB/IE.\n")
    for s in STEP2:
        m = ms[s["code"]]
        w(f"### {s['code']} {m['title']} ({m['years']})")
        w(f"- **Workstream:** {s['workstreams']}")
        w(f"- **Syarat mulai:** {s['prereq']}")
        w(f"- **Dokumen utama:** {s['docs']}")
        w(f"- **Durasi indikatif:** {s['duration']}")
        w(f"- **Kebutuhan pendanaan (indikatif):** {s['funding']}")
        w(f"- **Mitra teknis/pendanaan potensial:** {s['partners']}")
        w(f"- **Ketergantungan pada STEP 1:** {s['dep']}")
        w(f"- **Batas waktu standar:** {s['deadline']}\n")

    # ---------------- E
    w("## E. Transition & Handover Framework")
    w("Hasil SETAPAK 4 menjadi fondasi PDD sebagai berikut:\n")
    w(table(["Aspek", "Status di akhir SETAPAK 4", "Dipakai untuk (STEP 2)"], [
        ("Dokumen diserahterimakan", "D01–D22 di data room terindeks (lihat C8)", "Lampiran PDD; bukti validasi"),
        ("Data tersedia", "Peta partisipatif & KML, peta tutupan historis, analisis driver, stakeholder register, GESI "
                          "baseline, output participatory tools, estimasi indikatif", "Project Region/Area, baseline, ToC"),
        ("Data gap menuju PDD", "Plot stok karbon (biomassa & karbon tanah mangrove); baseline sosial-ekonomi "
                                "rumah tangga; baseline biodiversitas; parameter leakage & risk buffer; monitoring plan",
         "M8 carbon accounting & safeguards"),
        ("Status legal", "SK Hutan Desa/LPHD terverifikasi; memo hak karbon & jalur otorisasi (Permenhut 6/2026, "
                         "SRN/SRUK, MRA)", "Bab hak lahan & karbon PDD; pencatatan nasional"),
        ("Persetujuan masyarakat", "FPIC tahap i–ii; GRM aktif", "FPIC tahap iii + Project Agreements sebelum validasi"),
        ("Pendanaan lanjutan", "Proposal PDD + validasi dikirim sebelum TAF berakhir (target Jul–Sep 2027)", "M8–M9 ±USD 85–180 rb (indikatif)"),
        ("Kesiapan tim & kelembagaan", "SAMPAN sebagai Project Coordinator; LPHD, KUPS, WFD aktif",
         "Implementasi & monitoring"),
        ("Risiko transisi", "Kekosongan pendanaan; turnover fasilitator; ekspektasi komunitas; jam 3 tahun PDD",
         "Bridge funding; komunikasi berkala; jadwal PDD"),
    ]))
    w("")

    # ---------------- F
    w("## F. Final Presentation Outputs")
    w(table(["Output", "Lokasi"], [
        ("1 — One-Page Integrated Roadmap", "`Roadmap_HD_Pasir_PVClimate.pptx` slide 1 (ringkasan) & slide 2 (detail)"),
        ("2 — Detailed SETAPAK 4 Milestone Table", "Bagian B di atas; Excel sheet `Master_Matrix` & `Gantt_Step1`"),
        ("3 — Post-SETAPAK 4 Roadmap", "PPTX slide 4; Bagian D; Excel `Step2_Outlook`"),
        ("4 — Timeline & Critical Path", "PPTX slide 3; Bagian C5–C6; Excel `Gantt_Step1`"),
        ("5 — Transition Readiness Checklist", "PPTX slide 5; daftar di bawah; Excel `Transition_Checklist`"),
    ]))
    w("\n### Output 5 — Transition Readiness Checklist")
    for t in TRANSITION:
        w(f"- [ ] **{t[0]}** ({t[1]}) {t[2]} — *bukti: {t[3]}*")
    w("")

    w("## Asumsi yang perlu dikonfirmasi")
    w("- Apakah indikator kontraktual TAF (berakhir September 2027) adalah M6 (PIN diajukan) atau M7 (pipeline "
      "acceptance), dan kemungkinan no-cost extension untuk tindak lanjut review.")
    w("- Luas, SK, dan fungsi kawasan Hutan Desa Pasir, serta proporsi mangrove dan non-mangrove. Dokumen ini "
      "mengasumsikan dominan mangrove pesisir.")
    w("- Status terbaru Methodology Pipeline Plan Vivo untuk mangrove/blue carbon saat M5.4 (bulan 8–9).")
    w("- Besaran fee Plan Vivo (PIN review, PDD/validasi, issuance) dari dokumen *Costs & fees* terbaru.")
    w("- Ketentuan teknis turunan Perpres 110/2025 dan Permenhut 6/2026 untuk Perhutanan Sosial, serta panduan "
      "implementasi MRA Plan Vivo dari KLH/Kemenhut.\n")

    w("## Referensi")
    for name, url in SOURCES:
        w(f"- [{name}]({url})")
    w("")
    return "\n".join(L)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "roadmap.md"
    open(out, "w", encoding="utf-8").write(build())
