"""Membuat bagian sketch Vensim (16 View) secara otomatis: variabel asli per View, bayangan (shadow) untuk masukan dari View lain, dan panah sebab-akibat."""
import re
VIEWS = ["01 Forest Land Cover","02 Carbon Baseline Forest","03 Peat Dynamics","04 Forest Patrol Protection","05 Fire Management","06 Forest Rehabilitation",
 "07 Demography and Employment","08 Forest Livelihood Dependence","09 KUPS Economy Membership","10 Household Income Welfare","11 LPHD Institutions",
 "12 Social Ecological Feedback","13 Carbon Finance Revenues","14 LPHD Finance Allocation","15 Carbon Emission Accounting","16 Scenario Controls"]
def inputs_of(eq, names_sorted):
    s = " " + str(eq) + " "; found = []
    for n in names_sorted:
        pat = r"(?<![A-Za-z0-9_])" + re.escape(n) + r"(?![A-Za-z0-9_])"
        if re.search(pat, s):
            found.append(n); s = re.sub(pat, " ", s)
    return found
def sketch(recs):
    names = [r[0] for r in recs if r[3] != "Kontrol waktu"]
    ns = sorted(names, key=len, reverse=True)
    kind = {r[0]: r[3] for r in recs}; view = {r[0]: (r[1] if r[1] in VIEWS else "16 Scenario Controls") for r in recs}
    inp = {r[0]: [x for x in inputs_of(r[4], ns) if x != r[0]] for r in recs if r[3] != "Kontrol waktu"}
    out = []
    for v in VIEWS:
        own = [n for n in names if view[n] == v]
        out.append("\\\\\\---/// Sketch information - do not modify anything except names\nV300  Do not put anything below this section - it will be ignored\n*" + v +
                   "\n$192-192-192,0,Times New Roman|12||0-0-0|0-0-0|0-0-255|-1--1--1|-1--1--1|96,96,100,0")
        ids = {}; nid = 1; cols = 6
        for i, n in enumerate(own):
            x, y = 150 + 260 * (i % cols), 80 + 90 * (i // cols)
            shape = 3 if kind[n] == "Stok" else 8
            w, h = (50, 25) if shape == 3 else (60, 18)
            out.append(f"10,{nid},{n},{x},{y},{w},{h},{shape},3,0,0,0,0,0,0"); ids[n] = nid; nid += 1
        ghosts = []
        for n in own:
            for s in inp.get(n, []):
                if s not in ids and s not in ghosts: ghosts.append(s)
        base_y = 80 + 90 * ((len(own) - 1) // cols + 2)
        for i, s in enumerate(ghosts):
            x, y = 150 + 260 * (i % cols), base_y + 70 * (i // cols)
            out.append(f"10,{nid},{s},{x},{y},60,18,8,2,0,3,-1,0,0,0,128-128-128,0-0-0,|12||128-128-128"); ids[s] = nid; nid += 1
        for n in own:
            for s in inp.get(n, []):
                if s in ids:
                    out.append(f"1,{nid},{ids[s]},{ids[n]},0,0,0,0,0,64,0,-1--1--1,,1|(0,0)|"); nid += 1
    out.append("///---\\\\\\\n:L<%^E!@\n1:Current.vdfx\n9:Current\n15:0,0,0,0,0,0\n19:100,0\n27:0,\n34:0,\n4:Time\n5:Total Hutan\n35:Date\n36:YYYY-MM-DD\n37:2024\n38:1\n39:1\n40:2\n41:0\n42:1\n24:2024\n25:2087\n26:2087\n")
    return "\n".join(out)
