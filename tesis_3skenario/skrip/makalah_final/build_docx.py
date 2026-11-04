"""Bangun DOCX makalah final dari Markdown, memakai tata letak makalah Seminar Hasil asli.

Pemakaian: python build_docx.py <docx_sumber_tata_letak> <md> <docx_keluaran>
Elemen identitas (judul, penulis + catatan kaki afiliasi, ABSTRACT, Keywords),
gaya paragraf, margin, dan pengaturan halaman diambil dari docx sumber; isi lama dihapus.
"""
import copy
import os
import re
import sys

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from docx.text.paragraph import Paragraph

SRC, MD, OUT = sys.argv[1:4]
BASE = os.path.dirname(os.path.abspath(MD))
d = docx.Document(SRC)
body = d.element.body
els = list(body.iterchildren())
T = {k: copy.deepcopy(els[i]) for k, i in
     dict(h1=6, h2=12, par=7, cap=15, ttitle=16, tnote=18, ref=70).items()}
TBL = copy.deepcopy(d.tables[2]._tbl)


def clear_runs(p):
    for r in list(p):
        if r.tag in (qn("w:r"), qn("w:hyperlink"), qn("w:bookmarkStart"), qn("w:bookmarkEnd")):
            p.remove(r)


def rpr_of(tmpl):
    r = tmpl.find(qn("w:r"))
    rp = r.find(qn("w:rPr")) if r is not None else None
    return copy.deepcopy(rp) if rp is not None else OxmlElement("w:rPr")


def add_run(p, text, rpr, italic=False, bold=False):
    r = OxmlElement("w:r")
    rp = copy.deepcopy(rpr)
    for tag, on in (("w:i", italic), ("w:b", bold)):
        if on and rp.find(qn(tag)) is None:
            rp.insert(0, OxmlElement(tag))
    r.append(rp)
    t = OxmlElement("w:t"); t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    r.append(t); p.append(r)


def segments(text):
    """**tebal** dan *miring* sederhana."""
    out = []
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not part:
            continue
        if part.startswith("**"):
            out.append((part[2:-2], False, True))
        elif part.startswith("*"):
            out.append((part[1:-1], True, False))
        else:
            out.append((part, False, False))
    return out


def new_par(kind, text, where=None):
    tmpl = T[kind]
    p = copy.deepcopy(tmpl); rpr = rpr_of(tmpl); clear_runs(p)
    for s, it, bd in segments(text):
        add_run(p, s, rpr, it, bd)
    (where if where is not None else ANCHOR).addprevious(p)
    return p


def set_par(el, text, keep_first=False):
    runs = el.findall(qn("w:r"))
    if keep_first:
        tgt = runs[1]
        for r in runs[2:]:
            el.remove(r)
    else:
        tgt = runs[0]
        for r in runs[1:]:
            el.remove(r)
    tt = tgt.findall(qn("w:t"))
    tt[0].text = text
    for x in tt[1:]:
        tgt.remove(x)


# --- baca Markdown
lines = open(MD, encoding="utf-8").read().split("\n")
lines = lines[: lines.index("---")] if "---" in lines else lines
title = lines[0][2:].strip()
title_en = next(l for l in lines if l.startswith("*") and not l.startswith("**")).strip("*")
i_abs = lines.index("## ABSTRACT")
abstract = next(l for l in lines[i_abs + 1:] if l.strip())
kw = next(l for l in lines if l.startswith("**Keywords:**")).replace("**Keywords:**", "").strip()
i_body = lines.index("## PENDAHULUAN")

# --- identitas
set_par(els[0], title)
set_par(els[1], title_en)
set_par(els[4], abstract)
set_par(els[5], kw, keep_first=True)
# hapus isi lama (6 .. sebelum sectPr)
for el in els[6:]:
    if el.tag != qn("w:sectPr"):
        body.remove(el)
ANCHOR = body.find(qn("w:sectPr"))


def add_table(rows, numeric):
    tbl = copy.deepcopy(TBL)
    for tr in tbl.findall(qn("w:tr")):
        tbl.remove(tr)
    grid = tbl.find(qn("w:tblGrid"))
    for gc in list(grid):
        grid.remove(gc)
    ncol = len(rows[0])
    widths = WIDTHS.get(ncol)
    for w in widths:
        gc = OxmlElement("w:gridCol"); gc.set(qn("w:w"), str(w)); grid.append(gc)
    tbl.find(qn("w:tblPr")).find(qn("w:tblW")).set(qn("w:w"), str(sum(widths)))
    for ri, row in enumerate(rows):
        tr = OxmlElement("w:tr")
        if ri == 0:
            trpr = OxmlElement("w:trPr"); th = OxmlElement("w:tblHeader"); trpr.append(th)
            tr.append(trpr)
        for ci, val in enumerate(row):
            tc = OxmlElement("w:tc"); tcpr = OxmlElement("w:tcPr")
            tw = OxmlElement("w:tcW"); tw.set(qn("w:w"), str(widths[ci])); tw.set(qn("w:type"), "dxa")
            tcpr.append(tw)
            if ri == 0:
                b = OxmlElement("w:tcBorders"); bt = OxmlElement("w:bottom")
                for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "0"), ("w:color", "auto")):
                    bt.set(qn(k), v)
                b.append(bt); tcpr.append(b)
            tc.append(tcpr)
            p = OxmlElement("w:p"); ppr = OxmlElement("w:pPr")
            sp = OxmlElement("w:spacing"); sp.set(qn("w:before"), "10"); sp.set(qn("w:after"), "10")
            sp.set(qn("w:line"), "220"); sp.set(qn("w:lineRule"), "auto"); ppr.append(sp)
            jc = OxmlElement("w:jc")
            jc.set(qn("w:val"), "left" if ci == 0 else ("right" if numeric and ri > 0 else "center" if numeric else "left"))
            ppr.append(jc); p.append(ppr)
            rpr = OxmlElement("w:rPr")
            fn = OxmlElement("w:rFonts")
            for a in ("w:ascii", "w:hAnsi", "w:cs"):
                fn.set(qn(a), "Times New Roman")
            rpr.append(fn)
            sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "18"); rpr.append(sz)
            szc = OxmlElement("w:szCs"); szc.set(qn("w:val"), "18"); rpr.append(szc)
            for s, it, bd in segments(val):
                add_run(p, s, rpr, it, bd or ri == 0)
            tc.append(p); tr.append(tc)
        tbl.append(tr)
    ANCHOR.addprevious(tbl)


TW = 8500
WIDTHS = {}
i = i_body
pending_rows = []
table_numeric = True
in_refs = False
while i < len(lines):
    l = lines[i].rstrip()
    if not l:
        i += 1; continue
    if l.startswith("## "):
        h = l[3:].strip(); new_par("h1", h); in_refs = h == "DAFTAR PUSTAKA"
    elif l.startswith("### "):
        new_par("h2", l[4:].strip())
    elif l.startswith("!["):
        m = re.match(r"!\[(.*)\]\((.*)\)", l)
        cap, path = m.group(1), m.group(2)
        p = new_par("cap", "")
        para = Paragraph(p, d)
        wcm = 8.0 if "Gambar1" in path else (11.0 if "Gambar2" in path else 13.2)
        para.add_run().add_picture(os.path.join(BASE, path), width=Cm(wcm))
        pf = p.find(qn("w:pPr"))
        kn = OxmlElement("w:keepNext"); pf.insert(0, kn) if pf is not None else None
        c = new_par("cap", cap.replace("Gambar ", "Gambar ", 1))
    elif l.startswith("**Tabel"):
        new_par("ttitle", l.strip("*"))
    elif l.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                rows.append(cells)
            i += 1
        n = len(rows[0])
        numeric = n >= 4
        if n == 3:
            WIDTHS[3] = [1500, 4800, 2200]
        elif n == 5:
            WIDTHS[5] = [3900, 1150, 1150, 1150, 1150]
        add_table(rows, numeric)
        continue
    elif l.startswith("Catatan:") or l.startswith("Sumber:"):
        new_par("tnote", l)
    elif in_refs:
        new_par("ref", l)
    else:
        new_par("par", l)
    i += 1

d.save(OUT)
print("OK", OUT)
