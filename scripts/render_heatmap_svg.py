import json, math
from pathlib import Path
from datetime import datetime

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
WIDTH, HEIGHT = 860, 190
CELL, GAP = 11, 4
LEFT, TOP = 22, 48
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

data = json.loads(DATA.read_text(encoding="utf-8"))
days = data["days"]
# GitHub returns chronological cells. Pad to Sunday and arrange 7 rows.
if days:
    from datetime import date, timedelta
    first = date.fromisoformat(days[0]["date"])
    pad = first.weekday() + 1  # Monday=0; convert to Sunday=0
    pad = (first.weekday() + 1) % 7
    cells = [{"count":0,"level":0,"date":""}] * pad + days
else:
    cells=[]
weeks = math.ceil(len(cells) / 7)
max_level = 5
rects=[]
for i, d in enumerate(cells):
    col, row = i // 7, i % 7
    x, y = LEFT + col*(CELL+GAP), TOP + row*(CELL+GAP)
    level = max(0, min(max_level, int(d.get("level",0))))
    delay = (col + row) * 0.018
    rects.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[level]}" opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.28s" begin="{delay:.3f}s" fill="freeze"/></rect>')

# cap visual width to 860
stats=data.get("stats",{})
total=stats.get("total",0)
streak=stats.get("current_streak",0)
best=stats.get("best_day",0)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/>
<style>text{{font-family:monospace}}</style>
<text x="22" y="27" fill="#c9d1d9" font-size="14">AayushM0 · contribution activity</text>
<text x="{WIDTH-22}" y="27" fill="#8b949e" font-size="12" text-anchor="end">updated {data.get('updated','')}</text>
{''.join(rects)}
<text x="22" y="177" fill="#8b949e" font-size="11">{total:,} contributions · {streak} day current streak · best day {best}</text>
<text x="{WIDTH-22}" y="177" fill="#8b949e" font-size="11" text-anchor="end">Less</text>
{''.join(f'<rect x="{WIDTH-100+i*15}" y="168" width="10" height="10" rx="2" fill="{c}"/>' for i,c in enumerate(PALETTE))}
<text x="{WIDTH-22}" y="160" fill="#8b949e" font-size="11" text-anchor="end">More</text>
</svg>'''
OUT.write_text(svg,encoding="utf-8")
print(f"Wrote {OUT}")
