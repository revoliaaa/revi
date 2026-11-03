import sys, json, copy, shutil, zipfile, os, re
sys.path.insert(0, "work")
import docx
from docx.oxml.ns import qn
from PIL import Image
import naskah as N
SRC = "paket/Makalah_Seminar_Hasil_Kalimantan_Barat_REVISI3.docx"; OUT = sys.argv[1]
d = docx.Document(SRC)
els = list(d.element.body.iterchildren())
def set_p(el, text):
    runs = el.findall(qn("w:r"))
    keep = None
    for r in runs:
        if r.find(qn("w:t")) is not None: keep = r; break
    for r in runs:
        if r is not keep: el.remove(r)
    for h in el.findall(qn("w:hyperlink")): el.remove(h)
    t = keep.find(qn("w:t")); t.text = text; t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    for extra in keep.findall(qn("w:t"))[1:]: keep.remove(extra)
for i, txt in N.T.items(): set_p(els[i], txt)
def cell_set(c, text):
    ps = c._tc.findall(qn("w:p"))
    for p in ps[1:]: c._tc.remove(p)
    p = ps[0]
    if p.find(qn("w:r")) is None:
        r = docx.oxml.OxmlElement("w:r"); tt = docx.oxml.OxmlElement("w:t"); r.append(tt); p.append(r)
    set_p(p, text)
tables = d.tables  # 0 Tabel1, 1 Tabel2, 2 Tabel3, 3 Tabel4
t2 = tables[1]
cell_set(t2.rows[1].cells[3], "HCV 2024 dan Hansen 2001–2024; rekap patroli 2024–2025; Dokumen Desain Proyek; Laporan Pendampingan SAMPAN Kalimantan")
cell_set(t2.rows[2].cells[3], "Harga pasar 2024; Dokumen Desain Proyek; PP 36/2024; biaya patroli Rp 260.000/HOK; diskonto 10 % (D)")
t3 = tables[2]
rows3 = [("S1", "Tanpa PS aktif: tanpa patroli, tanpa pembiayaan awal, tanpa penerimaan karbon; laju deforestasi BAU hasil kalibrasi; status HD tidak dicabut", "–", "Acuan kontrafaktual"),
         ("S2", "PS dengan pembiayaan awal: patroli aktual 2.533 HOK (2024, 20 HD) dan 3.011 HOK (2025, 25 HD), Rp 1,44 miliar; tanpa patroli berbayar setelah 2025; rehabilitasi dan KUPS sesuai struktur PS", "Pembiayaan awal proyek karbon", "S2−S1: PS + pembiayaan awal"),
         ("S3", "S2 + perdagangan karbon pada harga tetap USD 6, 10, 15, 20, dan 35/tCO₂e; dana dipakai setelah kas penerimaan tersedia", "Pembiayaan awal, lalu penerimaan karbon: 60 % dana kolektif LPHD, 40 % mitra", "S3−S2: perdagangan karbon; S3−S1: total"),
         ("B0–B4, R1–R2", "Pembagian dana fleksibel LPHD ke patroli, rehabilitasi, kebakaran, KUPS, dan kompensasi RT terdampak pada S3; B0 = alokasi asli (identik dengan S3)", "Dana fleksibel LPHD", "Selisih terhadap B0")]
while len(t3.rows) > 1 + len(rows3): t3._tbl.remove(t3.rows[-1]._tr)
for i, r in enumerate(rows3):
    for j, v in enumerate(r): cell_set(t3.rows[i + 1].cells[j], v)
R = N.R; f = N.f; D = N.D; E = N.E
cols = ["S1", "S2", "S3 USD6", "S3 USD10", "S3 USD20", "S3 USD35"]
t4 = tables[3]
hdr = ["Indikator", "S1", "S2", "S3 USD6", "S3 USD10", "S3 USD20", "S3 USD35"]
for j, v in enumerate(hdr): cell_set(t4.rows[0].cells[j], v)
dash = lambda k, v: "–" if k == "S1" else v
spec = [None, None,
 ("Deforestasi kumulatif (ha)", lambda k: f(R[k][D])),
 ("Deforestasi dihindari vs S1 (ha)", lambda k: dash(k, f(N.av(k)))),
 ("Emisi dihindari vs S1 (ribu tCO₂e)", lambda k: dash(k, f(N.em(k) / 1000))),
 ("Hutan tahun 2087 (ha)", lambda k: f(R[k]["Hutan 2087 (ha)"])),
 None,
 ("Kredit model (ribu tCO₂e)", lambda k: "–" if k in ("S1", "S2") else f(R[k]["Kredit REDD model diajukan (tCO2e)"] / 1000, 1)),
 ("Penerimaan kotor karbon (Rp miliar)", lambda k: "–" if k in ("S1", "S2") else f(R[k]["Penerimaan kotor karbon 2024-2086 (Rp)"] / 1e9, 1)),
 ("Biaya MRV, transaksi, pajak (Rp miliar)", lambda k: "–" if k in ("S1", "S2") else f(R[k]["Biaya MRV, transaksi, pajak 2024-2086 (Rp)"] / 1e9, 1)),
 ("Dana kolektif LPHD (Rp miliar)", lambda k: "–" if k in ("S1", "S2") else f(R[k]["Dana LPHD diterima 2024-2086 (Rp)"] / 1e9, 1)),
 ("NPV proyek 10 % (Rp miliar)", lambda k: "–" if k == "S1" else f(R[k]["NPV proyek 10% (Rp)"] / 1e9, 2).replace("-", "−")),
 None,
 ("Kesenjangan kebutuhan minimum LPHD (Rp miliar/th)", lambda k: dash(k, f(R[k]["Kesenjangan pembiayaan minimum rerata (Rp/th)"] / 1e9, 2))),
 ("Intensitas perlindungan (0–1)", lambda k: f(R[k]["Intensitas perlindungan rerata 2030-2055"], 2)),
 ("Pekerja setara penuh (orang)", lambda k: f(R[k]["FTE rerata"], 1)),
 ("Penerimaan anggota KUPS (Rp juta/th)", lambda k: f(R[k]["Penerimaan anggota KUPS rerata (Rp/th)"] / 1e6, 1)),
 ("Pendapatan rata-rata RT (Rp juta/RT/th)", lambda k: f(R[k]["Pendapatan bersih per RT bergantung (Rp/RT/th)"] / 1e6, 2))]
for i, s in enumerate(spec):
    if s is None: continue
    row = t4.rows[i]; cell_set(row.cells[0], s[0])
    for j, k in enumerate(cols): cell_set(row.cells[j + 1], s[1](k))
d.save(OUT)
# ganti gambar: rId17..22 -> image6..image11
M = {"image6.png": "fig/gambar2.png", "image7.png": "fig/gambar3.png", "image8.png": "fig/gambar4.png", "image9.png": "fig/gambar5.png", "image10.png": "fig/gambar6.png", "image11.png": "fig/gambar7.png"}
tmp = OUT + ".tmp"; zin = zipfile.ZipFile(OUT); zout = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
rels = zin.read("word/_rels/document.xml.rels").decode()
rid = {m.group(2): m.group(1) for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels)}
doc = zin.read("word/document.xml").decode()
for img, src in M.items():
    w, h = Image.open(src).size; r = rid[img]
    m = re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"/>((?:(?!<wp:extent).)*?r:embed="' + r + '")', doc, re.S)
    cx = int(m.group(1)); cy = int(cx * h / w)
    seg = m.group(0).replace(f'cy="{m.group(2)}"', f'cy="{cy}"', 1)
    seg = re.sub(r'<a:ext cx="' + str(cx) + r'" cy="\d+"/>', f'<a:ext cx="{cx}" cy="{cy}"/>', seg)
    doc = doc.replace(m.group(0), seg)
for it in zin.infolist():
    if it.filename == "word/document.xml": zout.writestr(it, doc)
    elif it.filename.startswith("word/media/") and it.filename.split("/")[-1] in M: zout.writestr(it, open(M[it.filename.split("/")[-1]], "rb").read())
    else: zout.writestr(it, zin.read(it.filename))
zin.close(); zout.close(); os.replace(tmp, OUT); print("ok", OUT)
