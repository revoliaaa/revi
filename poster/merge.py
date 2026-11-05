"""Tumpuk lapisan ilustrasi di atas poster asli tanpa mengubah konten aslinya.
Pakai: python3 merge.py <poster_asli.pdf> <keluaran.pdf>"""
import sys
from pypdf import PdfReader, PdfWriter
src, out = sys.argv[1], sys.argv[2]
base = PdfReader(src).pages[0]
ov = PdfReader('build/overlay.pdf').pages[0]
print('base', base.mediabox, 'overlay', ov.mediabox)
base.merge_page(ov)
w = PdfWriter(); w.add_page(base)
w.add_metadata(PdfReader(src).metadata or {})
w.write(out)
