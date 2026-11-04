import sys; sys.path.insert(0, "fase3"); import common
from common import *
common.MDL = "fase4/MODEL_FINAL_DUA_SKENARIO_PWD_v2.mdl"
X = ["Kredit ARR Terbit", "Kredit Karbon Terbit", "Kredit Karbon Diajukan", "Kredit Karbon Terjual", "Realisasi Pembiayaan Jembatan", "Hari Patroli Didanai Jembatan", "Pendanaan Awal Belum Terpulihkan",
     "Pemulihan Pendanaan Awal", "Arus Kas Mitra", "Arus Kas Proyek Keseluruhan", "Arus Kas Proyek Karbon", "Defisit Biaya Bersama Belum Dipulihkan", "Pokok Talangan Kumulatif",
     "Kumulatif Pembiayaan Jembatan", "PV Pembiayaan Jembatan", "Efek Pengelolaan PS Tanpa Karbon", "Biaya Modal Pendanaan Awal Rp", "Biaya Modal Kumulatif", "Penghapusan Talangan",
     "Kerugian Mitra dari Penghapusan Talangan", "Check Identitas Arus Kas", "Check Identitas Patroli", "Hari Patroli Tambahan Dibutuhkan", "Kapasitas Hari Patroli Anggota",
     "Total Hutan Referensi S1", "Emisi Deforestasi Biomassa Referensi S1", "Emisi Bersih Biomassa Referensi S1", "Emisi Bersih Biomassa", "Check Referensi S1 Hutan",
     "Pengurangan Emisi REDD Bruto Referensi S1", "Pengurangan Emisi ARR Bruto Referensi S1", "Pengurangan Emisi Biomassa Referensi S1", "Potensi Kredit REDD terhadap BAU", "Potensi Kredit REDD Referensi S1",
     "Status Proyek Karbon Aktif", "Biaya MRV Tetap", "Biaya Monitoring MRV", "Biaya Verifikasi Tahunan", "Stok Kredit REDD Belum Terjual", "Stok Kredit ARR Belum Terjual", "Kredit REDD Kedaluwarsa", "Kredit ARR Kedaluwarsa",
     "Upah Patroli Berbayar", "Upah Patroli dari Kas LPHD", "Upah Pengendalian Kebakaran", "Upah Penanaman Didanai Karbon", "Upah Penanaman Program Non Karbon", "Upah Dibayar dari Kas LPHD",
     "Nilai Kontribusi Tenaga Non Tunai", "Nilai Logistik Non Tunai Patroli", "Biaya Operasional Patroli Sukarela per Anggota per Tahun", "Kesempatan Kerja PS", "Kumulatif Realisasi Pembiayaan Awal",
     "HOK Penanaman Berupah", "HOK Penanaman Sukarela", "HOK Pengendalian Kebakaran", "Pendapatan Hutan per RT Bergantung", "Pendapatan Non Hutan per RT Bergantung", "RT Terdampak Akses", "Pendapatan Dasar RT Bergantung",
     "Check Total Kawasan", "Check Konservasi Karbon", "Check Total Kawasan Referensi S1", "Saldo Dana LPHD dari Karbon", "Dana Desa Tersedia", "Indeks Intensitas Perlindungan Tanpa Karbon", "Saldo Mitigasi REDD Belum Dikreditkan", "Reversal Belum Terkompensasi", "Kumulatif Buffer REDD", "Mitigasi REDD Eligible Bersih Proyek", "Kredit REDD Referensi S1 Bersih", "Kredit Pengganti Reversal Kumulatif", "Biaya Penggantian Reversal", "Buffer REDD Tersedia", "Penggunaan Buffer Reversal", "Pembatalan Stok Kredit Reversal", "Kumulatif Penggunaan Buffer Reversal", "Kumulatif Pembatalan Stok Kredit Reversal", "Kewajiban Reversal Belum Diselesaikan", "Pulsa Verifikasi Reversal", "Kontribusi Buffer REDD", "Hari Patroli Didanai Kas Non Karbon",
     "Penggunaan Dana Perlindungan Total", "Realisasi Belanja Perlindungan"]
COLS = list(dict.fromkeys(V + X))
def runc(p, cols=None, ts=None):
    m = model(); m.reload(); return m.run(params=p, return_timestamps=ts or TS, return_columns=cols or COLS, progress=False)
