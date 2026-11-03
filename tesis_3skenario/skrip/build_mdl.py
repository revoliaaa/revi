"""Rekonstruksi berkas .mdl dari REGISTER_VARIABEL_PER_VIEW_A1.xlsx (lembar '2 Semua variabel')."""
import json, sys, re
def build(recs, out, overrides=None, extra=None, header_comment=""):
    import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
    overrides = overrides or {}
    lines = ["{UTF-8}"]
    ctrl = []
    for r in recs + (extra or []):
        name, view, kind, eq, unit = r[0], r[1], r[3], r[4], r[6]
        com = r[22] if len(r) > 22 and r[22] not in (None, "None") else (r[14] if len(r)>14 else "")
        if name in overrides:
            eq, c2 = overrides[name]
            com = (c2 + " || Sebelumnya: " + str(r[4])) if c2 else com
        eq = str(eq)
        unit = "" if unit in (None, "None") else str(unit)
        com = "" if com in (None, "None") else str(com).replace("~", "-").replace("|", "/")
        if kind == "Tabel lookup":
            block = f"{name}(\n\t{eq.strip()[1:-1].strip() if eq.strip().startswith('(') else eq})"
        else:
            block = f"{name}=\n\t{eq}"
        txt = f"{block}\n\t~\t{unit}\n\t~\t{com}\n\t|\n"
        (ctrl if kind == "Kontrol waktu" else lines).append(txt)
    lines.append("********************************************************\n\t.Control\n********************************************************~\n\t\tSimulation Control Parameters\n\t|\n")
    lines += ctrl
    from sketch import sketch
    allrecs = [list(r) for r in recs + (extra or [])]
    for r in allrecs:
        if r[0] in overrides: r[4] = overrides[r[0]][0]
    lines.append(sketch(allrecs))
    open(out, "w", encoding="utf-8").write("\n".join(lines))
if __name__ == "__main__":
    build(json.load(open(sys.argv[1]))[1:], sys.argv[2])
