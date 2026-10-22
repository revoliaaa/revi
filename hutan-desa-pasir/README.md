# Hutan Desa Pasir — Integrated Community Carbon Development Roadmap (Plan Vivo PV Climate)

| File | Isi |
|---|---|
| `Roadmap_HD_Pasir_PVClimate.pptx` | Slide 1: kerangka 8 tahap (Tahap 1–2 SETAPAK 4 → Tahap 3 pipeline & investasi → Tahap 4–8 sampai penjualan) · Slide 2: one-page integrated roadmap detail (Output 1) · Slide 3: timeline & critical path (Output 4) · Slide 4: Post-SETAPAK 4 roadmap (Output 3) · Slide 5: transition readiness checklist (Output 5) |
| `Milestone_Matrix_HD_Pasir_PVClimate.xlsx` | Project Monitoring Excel: Master_Matrix, Gantt_Step1, Tahapan, Participatory_Tools, Doc_Checklist, Risk_Register, Step2_Outlook, Transition_Checklist, Sources |
| `Roadmap_HD_Pasir_PVClimate.md` | Dokumen lengkap bagian A–F + referensi |

Semua output dibangun dari satu sumber data (`build/data.py`) agar kode milestone konsisten.

```bash
cd build
pip install python-pptx openpyxl
python3 build_pptx.py ../Roadmap_HD_Pasir_PVClimate.pptx
python3 build_xlsx.py ../Milestone_Matrix_HD_Pasir_PVClimate.xlsx
python3 build_md.py   ../Roadmap_HD_Pasir_PVClimate.md
```
