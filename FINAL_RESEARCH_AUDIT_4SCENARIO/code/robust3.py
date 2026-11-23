"""Uji sensitivitas OAT tambahan untuk butir matriks leveling yang belum diuji (DIAGNOSTIK AUDIT).
Tidak mengubah .mdl; parameter ditimpa saat run (PySD params). Metrik identik dengan robust2.py."""
import sys, pysd, pandas as pd, numpy as np, warnings
from multiprocessing import Pool
warnings.filterwarnings('ignore')
DT = 0.0625; ts = list(np.arange(2024, 2087 + 1e-9, DT))
FILES = {'S1': 'DKP_25HD_A1_S1_TANPA_INTERVENSI_PS_rapi', 'S2': 'DKP_25HD_A1_S2_PS_REGULER_rapi', 'S3': 'DKP_25HD_A1_S3_PEMBIAYAAN_AWAL_rapi',
         'S4USD10': 'DKP_25HD_A1_S4_USD10_rapi', 'S4USD20': 'DKP_25HD_A1_S4_USD20_rapi'}
COLS = ['Deforestasi Total', 'Pendapatan Kotor Penjualan Kredit', 'Biaya Transaksi dan MRV', 'Realisasi Pembiayaan Awal', 'Penggunaan Dana Pengelolaan',
        'Kebutuhan Dana Minimum', 'Kredit REDD Diajukan', 'Pendapatan Bersih per RT Bergantung', 'Total Emisi Bersih']
BAU = {'Laju HMS menjadi NonHutan BAU': 0.00261092, 'Laju HRS menjadi NonHutan BAU': 0.00955847}
def price_path(p0, kind):
    t = np.array(ts)
    if kind == 'turun': v = np.where(t < 2034, p0 * (1 - 0.4 * (t - 2024) / 10), 0.6 * p0)
    else: v = np.where(t < 2050, p0 * (1 + (t - 2024) / 26), 2 * p0)
    return pd.Series(v, index=t)
# (id, label, sumber rentang, params atau fungsi(model_key)->params)
V = [
 ('DASAR', 'Dasar (tanpa perubahan)', '–', {}),
 ('D05', 'Laju BAU ×0,654 (tanpa pengali pulsa)', 'Dok. .mdl: pengali pulsa 1,5296', {k: v / 1.5296 for k, v in BAU.items()}),
 ('D05', 'Laju BAU ×1,5', 'UJI AUDIT (mendekati lonjakan Hansen 2015–2024)', {k: v * 1.5 for k, v in BAU.items()}),
 ('D07', 'Harga turun 40 % dalam 10 th lalu tetap', 'UJI AUDIT (lintasan)', 'turun'),
 ('D07', 'Harga naik 2× sampai 2050 lalu tetap', 'UJI AUDIT (lintasan)', 'naik'),
 ('D08', 'Tahun kering ekstrem aktif', 'Dok. .mdl: Switch Tahun Kering Ekstrem (uji struktur)', {'Switch Tahun Kering Ekstrem': 1}),
 ('D08', 'Alokasi pengendalian kebakaran 0,20', 'UJI AUDIT (dasar 0,10)', {'Proporsi Alokasi Pengendalian Kebakaran': 0.2}),
 ('D09', 'Biaya operasional LPHD Rp 25 juta', 'Dok. .mdl: rentang uji 25–100 juta', {'Biaya Operasional per LPHD per Tahun': 25e6}),
 ('D09', 'Biaya operasional LPHD Rp 100 juta', 'Dok. .mdl: rentang uji 25–100 juta', {'Biaya Operasional per LPHD per Tahun': 100e6}),
 ('D10', 'Biaya patroli/hari Rp 195.000 (−25 %)', 'UJI AUDIT', {'Biaya per Hari Patroli': 195000}),
 ('D10', 'Biaya patroli/hari Rp 325.000 (+25 %)', 'UJI AUDIT', {'Biaya per Hari Patroli': 325000}),
 ('D11', 'Efek izin PS −0,15', 'Dok. .mdl: rentang −0,15 s.d. 0,169', {'Efek Izin PS terhadap Deforestasi': -0.15}),
 ('D11', 'Efek izin PS 0,169', 'Dok. .mdl: rentang −0,15 s.d. 0,169', {'Efek Izin PS terhadap Deforestasi': 0.169}),
 ('D12', 'RT bergantung 2.144', 'Dok. .mdl: rentang uji 2.144–19.038', {'Masyarakat Bergantung pada Hutan Awal': 2144}),
 ('D12', 'RT bergantung 19.038', 'Dok. .mdl: rentang uji 2.144–19.038', {'Masyarakat Bergantung pada Hutan Awal': 19038}),
 ('D14', 'Bagi hasil masyarakat 50 %', 'UJI AUDIT (dasar 60 %)', {'Proporsi Manfaat Masyarakat': 0.5}),
 ('D14', 'Bagi hasil masyarakat 70 %', 'UJI AUDIT (dasar 60 %)', {'Proporsi Manfaat Masyarakat': 0.7}),
 ('D19', 'Atribusi patroli 2024 ke pembiayaan awal = 0', 'Dok. .mdl: 0 = seluruhnya swadaya', {'Porsi Kenaikan Patroli 2024 dari Pembiayaan Awal': 0}),
 ('D19', 'Atribusi patroli 2024 ke pembiayaan awal = 0,5', 'UJI AUDIT', {'Porsi Kenaikan Patroli 2024 dari Pembiayaan Awal': 0.5}),
 ('D22', 'Densitas biomassa ×0,8', 'UJI AUDIT', {'Densitas Biomassa HMS': 81.6202 * 0.8, 'Densitas Biomassa HRS': 123.69 * 0.8}),
 ('D22', 'Densitas biomassa ×1,2', 'UJI AUDIT', {'Densitas Biomassa HMS': 81.6202 * 1.2, 'Densitas Biomassa HRS': 123.69 * 1.2}),
 ('D24', 'Pertumbuhan penduduk 1,37 %', 'Dok. .mdl: L 0,0137', {'Laju Pertumbuhan Penduduk': 0.0137}),
 ('D24', 'Pertumbuhan penduduk 1,91 %', 'Dok. .mdl: H 0,0191', {'Laju Pertumbuhan Penduduk': 0.0191}),
]
def run_one(arg):
    idx = arg; vid, lab, src, par = V[idx]
    R = {}
    for k, f in FILES.items():
        m = pysd.load(f + '.py')
        if isinstance(par, str):
            p = {} if not k.startswith('S4') else {'Harga Karbon': price_path(10.0 if k == 'S4USD10' else 20.0, par)}
        else: p = par
        df = m.run(params=p, return_timestamps=ts, return_columns=COLS, progress=False)
        s = df.loc[df.index < 2087 - 1e-9]
        d = 1.1 ** (-(s.index.values - 2024)); pv = lambda c: float((s[c].values * d).sum() * DT)
        defor = float(df.loc[(df.index >= 2025 - 1e-9) & (df.index < 2087 - 1e-9), 'Deforestasi Total'].sum() * DT)
        w = df.loc[(df.index >= 2030) & (df.index < 2056)]
        R[k] = dict(defor=defor, npv=pv('Pendapatan Kotor Penjualan Kredit') - pv('Biaya Transaksi dan MRV') - pv('Realisasi Pembiayaan Awal') - pv('Penggunaan Dana Pengelolaan'),
                    cov=float(w['Penggunaan Dana Pengelolaan'].mean() / max(w['Kebutuhan Dana Minimum'].mean(), 1)), kredit=float(s['Kredit REDD Diajukan'].sum() * DT),
                    rt=float(w['Pendapatan Bersih per RT Bergantung'].mean()), em=float(df.loc[(df.index >= 2025 - 1e-9) & (df.index < 2087 - 1e-9), 'Total Emisi Bersih'].sum() * DT))
    return {'id': vid, 'variant': lab, 'sumber_rentang': src, 'S2-S1 ha': R['S1']['defor'] - R['S2']['defor'], 'S3-S2 ha': R['S2']['defor'] - R['S3']['defor'],
            'S4-S3 USD10 ha': R['S3']['defor'] - R['S4USD10']['defor'], 'S4-S3 USD20 ha': R['S3']['defor'] - R['S4USD20']['defor'],
            'NPV USD10 (Rp M)': R['S4USD10']['npv'] / 1e9, 'NPV USD20 (Rp M)': R['S4USD20']['npv'] / 1e9, 'Cakupan USD20 (%)': 100 * R['S4USD20']['cov'],
            'Kredit USD10 (ribu)': R['S4USD10']['kredit'] / 1e3, 'dRT S4-S3 USD10 (Rp)': R['S4USD10']['rt'] - R['S3']['rt'], 'dRT S4-S3 USD20 (Rp)': R['S4USD20']['rt'] - R['S3']['rt'], 'Emisi bersih kum S4 USD10 (juta tCO2e)': R['S4USD10']['em'] / 1e6, 'Emisi dihindari S4 USD10 vs S1 (ribu tCO2e)': (R['S1']['em'] - R['S4USD10']['em']) / 1e3}
if __name__ == '__main__':
    out = sys.argv[1]
    idxs = list(range(len(V))) if len(sys.argv) < 3 else [int(x) for x in sys.argv[2].split(',')]
    with Pool(4) as pool:
        res = pool.map(run_one, idxs)
    pd.DataFrame(res).to_csv(out, index=False); print(pd.DataFrame(res).iloc[:, [0, 1, 3, 5, 7, 11]].to_string())
