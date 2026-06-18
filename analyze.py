#!/usr/bin/env python3
"""
KuCoin grid-bot backtest analysis — top 25 coins by market cap.
CSV-DRIVEN so new months are a simple append. See README.md for the monthly steps.

Reads
  coins.csv    universe + latest-month metadata  (ticker,name,rank,mcap,mcap_b,cat)
  returns.csv  long format, one row per coin per month  (date,label,ticker,r12)
Writes
  data.json    consumed by build_html.py

"12-Mo %" (r12)   = trailing-12-month backtested bot return (annual, simple)
"Avg Mo. %"       = r12 / 12  ;  "Weekly %" = r12 / 52
"""
import json, csv, datetime

# ---- universe + metadata (row order = market-cap order) ----
coins_meta = []
with open("coins.csv", newline="") as f:
    for r in csv.DictReader(f):
        coins_meta.append({"ticker":r["ticker"], "name":r["name"], "rank":int(r["rank"]),
                           "mcap":r["mcap"], "mcap_b":float(r["mcap_b"]), "cat":r["cat"]})

# ---- returns (long) ----
rows = list(csv.DictReader(open("returns.csv", newline="")))
month_pairs = sorted({(r["date"], r["label"]) for r in rows})   # chronological by YYYY-MM
DATES  = [d for d, _ in month_pairs]
MONTHS = [l for _, l in month_pairs]
R = {(r["ticker"], r["date"]): float(r["r12"]) for r in rows}

def avg(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs)/len(xs) if xs else None

coins = []
for m in coins_meta:
    tk = m["ticker"]
    series = [R.get((tk, d)) for d in DATES]
    present = [x for x in series if x is not None]
    if not present:
        continue                                   # coin has no data yet — skip
    a9 = avg(series)
    latest = next(x for x in reversed(series) if x is not None)
    first  = next(x for x in series if x is not None)
    coins.append({**m, "series":series, "latest":latest, "avg9":round(a9,2),
                  "min":min(present), "max":max(present), "n":len(present),
                  "chg":round(latest-first,2),
                  "wk_latest":round(latest/52,3), "wk_avg":round(a9/52,3)})

# ---- portfolio (equal-weight) per month over coins present that month ----
port_series, port_n = [], []
for i in range(len(DATES)):
    vals = [c["series"][i] for c in coins if c["series"][i] is not None]
    port_series.append(round(sum(vals)/len(vals), 2) if vals else None)
    port_n.append(len(vals))

port_latest = next(x for x in reversed(port_series) if x is not None)
port_first  = next(x for x in port_series if x is not None)
port_avg9   = round(sum(c["avg9"] for c in coins)/len(coins), 2)
lat_sorted  = sorted(c["latest"] for c in coins)
median_latest = lat_sorted[len(lat_sorted)//2]

meta = {
    "source":"KuCoin tab — BA monthly backtest snapshots",
    "window":f"{MONTHS[0]} – {MONTHS[-1]} ({len(MONTHS)} monthly readings)",
    "generated":datetime.date.today().isoformat(),
    "n_coins":len(coins),
    "port_latest":port_latest, "port_first":port_first, "port_avg9":port_avg9,
    "port_change_pct":round((port_latest-port_first)/port_first*100, 1),
    "median_latest":round(median_latest, 2),
    "btc_latest":coins[0]["latest"], "eth_latest":coins[1]["latest"],
}

payload = {"coins":coins, "months":MONTHS, "port_series":port_series, "port_n":port_n, "meta":meta}

# ---- console summary ----
print(f"Months loaded: {MONTHS[0]} -> {MONTHS[-1]}  ({len(MONTHS)})   Coins: {len(coins)}")
print("Portfolio equal-weight avg trailing-12-mo return by month:")
for m, v, n in zip(MONTHS, port_series, port_n):
    print(f"  {m}: {v:6.2f}%  (n={n})")
print(f"Latest {port_latest:.2f}%  |  through-cycle {port_avg9:.2f}%  |  "
      f"change {meta['port_change_pct']}%  |  median latest {meta['median_latest']:.2f}%")

with open("data.json", "w") as f:
    json.dump(payload, f, indent=2)
print("wrote data.json")
