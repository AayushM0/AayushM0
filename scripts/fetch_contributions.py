import json, re
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = "AayushM0"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path("data/contributions.json")

html = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

cells = soup.select("td.ContributionCalendar-day") or soup.select("td[data-date]")
if not cells:
    raise RuntimeError("Could not find GitHub contribution cells; GitHub may have changed its HTML.")

days = []
for cell in cells:
    d = cell.get("data-date")
    level = cell.get("data-level")
    if not d:
        continue
    count = None
    label = cell.get("aria-label", "")
    m = re.search(r"(\d[\d,]*) contribution", label)
    if m:
        count = int(m.group(1).replace(",", ""))
    if count is None:
        title = cell.find("title")
        txt = title.get_text(" ", strip=True) if title else ""
        m = re.search(r"(\d[\d,]*) contribution", txt)
        count = int(m.group(1).replace(",", "")) if m else 0
    days.append({"date": d, "count": count or 0, "level": int(level or 0)})

days.sort(key=lambda x: x["date"])
counts = [x["count"] for x in days]

def streak_from(seq):
    best = cur = 0
    for x in seq:
        if x > 0: cur += 1; best = max(best, cur)
        else: cur = 0
    return best

current = 0
for x in reversed(counts):
    if x > 0: current += 1
    else: break

result = {
    "username": USERNAME,
    "updated": date.today().isoformat(),
    "days": days,
    "stats": {
        "total": sum(counts),
        "current_streak": current,
        "longest_streak": streak_from(counts),
        "best_day": max(counts) if counts else 0,
    },
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(f"Wrote {OUT} with {len(days)} days and {result['stats']['total']} contributions")
