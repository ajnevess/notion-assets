#!/usr/bin/env python3
"""Notion assets — Central + 13 paginas. Didot, nome inteiro, letras em italico rosa.

{x} marca a letra que vira italico na cor de acento. Duas palavras -> duas linhas no icone.
Render: python3 gen.py && ./render.sh
"""
import json
import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))

CAFE  = "#351C06"
ROSA  = "#D29C9A"
ROSAF = "#AB7477"
BRUMA = "#A0BCD0"
LIMA  = "#DCE764"
OSSO  = "#F1EDE4"
FUMO  = "#6E6055"

GROUP = {
    "hub":    dict(bg=CAFE,  fg=OSSO, dim="#A8907F", accent=ROSA),
    "work":   dict(bg=OSSO,  fg=CAFE, dim=FUMO,      accent=ROSAF),
    "life":   dict(bg=BRUMA, fg=CAFE, dim="#55707F", accent=ROSAF),
    "system": dict(bg=LIMA,  fg=CAFE, dim="#7B8434", accent=ROSAF),
    "quick":  dict(bg=CAFE,  fg=OSSO, dim="#A8907F", accent=ROSA),
}

PAGES = [
    ("central",        "3a96794f3a5581f78896f5d7aa1230d3", "C{e}ntr{a}l",           "hub",    "work · life · system"),
    ("anas-office",    "3a96794f3a55811683caffdc43e05139", "An{a}’s Off{i}ce",      "work",   "portfólio · cases · LinkedIn · marca pessoal"),
    ("marketing-study","a9cc67fe73214ad5b876c473ce1fc410", "Mark{et}ing St{u}dy",   "work",   "creative strategy · copy · ads · branding"),
    ("luccas-office",  "7b7a3ec33c204ef6ac837103a4bf4cf3", "Lu{cc}a’s Off{i}ce",    "work",   "recrutadores · respostas · follow-ups"),
    ("graduation",     "3a96794f3a5581f79de5faae640931af", "Gradu{a}ti{o}n",        "work",   "FIAP · marketing"),
    ("personal",       "3a96794f3a5581b29ef1e059143626c6", "Pers{o}n{a}l",          "life",   "rotinas · finanças · mudança · planejamento"),
    ("health-inbox",   "f31e7fb100f843d9bcec8fb3151463e4", "He{a}lth Inb{o}x",      "life",   "exames · laudos · receitas · plano"),
    ("central-ops",    "3a96794f3a5581df9405c8de1fa4b415", "Ce{n}tral {O}ps",       "system", "páginas · databases · views · mini me"),
    ("library",        "3a96794f3a558102b38ffd323245b42d", "Li{b}r{a}ry",           "system", "referências · notas · cursos"),
    ("prompt-library", "2096794f3a558327a70481547042e517", "Pr{o}mpt Libr{a}ry",    "system", "prompts salvos · reutilizáveis"),
    ("automation-lab", "3a96794f3a558155b233c0b491ea090c", "Aut{o}mati{o}n L{a}b",  "system", "workflows · automações"),
    ("today",          "3a96794f3a55817d8c64c93e598438b6", "T{o}d{a}y",             "quick",  None),
    ("inbox",          "3a96794f3a55812a8503f544bedeb477", "I{n}b{o}x",             "quick",  None),
    ("archive",        "3a96794f3a5581d195bcc015527457cc", "Ar{c}h{i}ve",           "quick",  None),
]

HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;}}
body{{background:{bg};color:{fg};font-family:"Helvetica Neue",Helvetica,sans-serif;-webkit-font-smoothing:antialiased;}}
.disp{{font-family:"Didot","Bodoni 72",Georgia,serif;font-weight:700;letter-spacing:-.005em;line-height:.95;}}
.disp .it{{font-style:italic;font-weight:400;color:{accent};}}
.mono{{font-family:"Menlo",monospace;letter-spacing:.2em;text-transform:uppercase;}}
.low{{text-transform:none;letter-spacing:.1em;}}
</style></head><body>{body}</body></html>"""


def plain(marked):
    return re.sub(r"[{}]", "", marked)


def rich(marked):
    return re.sub(r"\{([^}]+)\}", r'<i class="it">\1</i>', marked)


def write(name, html):
    os.makedirs(os.path.join(OUT, "html"), exist_ok=True)
    open(os.path.join(OUT, "html", name), "w").write(html)


def icon(slug, marked, g):
    lines = marked.split(" ")
    maxlen = max(len(plain(l)) for l in lines)
    fs = min(80, int(218 / (0.5 * maxlen)))
    rows = "".join(f'<div class="disp" style="font-size:{fs}px">{rich(l)}</div>' for l in lines)
    body = f"""<div style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{int(fs*0.08)}px;color:{g['fg']}">{rows}</div>"""
    write(f"icon-{slug}.html", HEAD.format(w=280, h=280, bg=g["bg"], fg=g["fg"], accent=g["accent"], body=body))


def strata(colors, widths):
    bars = "".join(f'<i style="display:block;height:6px;background:{c};width:{w}px"></i>' for c, w in zip(colors, widths))
    return f'<div style="display:flex;flex-direction:column;gap:6px">{bars}</div>'


def cover(slug, marked, g, items):
    n = len(plain(marked))
    fs = min(160, int(1150 / (0.5 * n)))
    body = f"""<div style="width:100%;height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:64px">
  <div style="display:flex;justify-content:space-between"><span class="mono" style="font-size:14px;color:{g['dim']}">AJN</span><span class="mono" style="font-size:14px;color:{g['dim']}">Central</span></div>
  <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:60px">
    <div class="disp" style="font-size:{fs}px;color:{g['fg']}">{rich(marked)}</div>
    {strata([g['accent'], g['dim'], g['dim']], [96, 62, 30])}
  </div>
  <div style="display:flex;justify-content:space-between;align-items:center">
    <span class="mono low" style="font-size:15px;color:{g['dim']}">{items}</span>
    <span style="display:block;width:150px;height:4px;background:{g['accent']}"></span>
  </div>
</div>"""
    write(f"cover-{slug}.html", HEAD.format(w=1500, h=600, bg=g["bg"], fg=g["fg"], accent=g["accent"], body=body))


def hub_cover(marked, g):
    rows = "".join(
        f'<div style="display:flex;gap:22px;align-items:baseline;margin-top:{0 if n==0 else 13}px">'
        f'<span class="mono" style="font-size:12px;color:{ROSA};width:34px">{num}</span>'
        f'<span style="font-size:25px;color:{OSSO};letter-spacing:-.01em">{name}</span></div>'
        for n, (num, name) in enumerate([("I", "Work"), ("II", "Life"), ("III", "System")])
    )
    body = f"""<div style="width:100%;height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:64px">
  <div style="display:flex;justify-content:space-between"><span class="mono" style="font-size:14px;color:{g['dim']}">AJN · Personal Hub</span><span class="mono" style="font-size:14px;color:{g['dim']}">3 Groups</span></div>
  <div style="display:flex;align-items:flex-end;gap:78px">
    <div class="disp" style="font-size:176px;color:{OSSO}">{rich(marked)}</div>
    <div style="border-left:1px solid {g['dim']};padding-left:44px;padding-bottom:14px">{rows}</div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end">
    {strata([ROSA, BRUMA, LIMA], [120, 76, 38])}
    <span class="mono low" style="font-size:15px;color:{g['dim']}">café &amp; rosa</span>
  </div>
</div>"""
    write("cover-central.html", HEAD.format(w=1500, h=600, bg=CAFE, fg=OSSO, accent=g["accent"], body=body))


manifest = []
for slug, pid, marked, group, items in PAGES:
    g = GROUP[group]
    icon(slug, marked, g)
    entry = dict(slug=slug, page_id=pid, title=plain(marked), group=group, icon=f"icon-{slug}.png", cover=None)
    if items is not None:
        hub_cover(marked, g) if group == "hub" else cover(slug, marked, g, items)
        entry["cover"] = f"cover-{slug}.png"
    manifest.append(entry)

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2, ensure_ascii=False)
print(f"{len(manifest)} paginas · {sum(1 for m in manifest if m['cover'])} capas")
