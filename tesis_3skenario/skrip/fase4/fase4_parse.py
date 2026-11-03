import re
def parse(path):
    txt = open(path, encoding="utf-8").read().split("\\\\\\---///")[0]; E = {}
    for blk in txt.split("|\n"):
        m = re.match(r"\s*(.+?)(\(\s*\n|=)\s*\n?\t?(.*?)\n\t~\t(.*?)\n", blk, re.S)
        if m: E[m.group(1).replace("{UTF-8}", "").strip()] = (re.sub(r"\s+", " ", m.group(3).replace("\\\n"," ").strip()), m.group(4).strip())
    return E
