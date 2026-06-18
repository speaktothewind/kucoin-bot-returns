# KuCoin Grid-Bot Returns — Top 25 by Market Cap

A self-contained HTML report + investment/tax calculator built from the **KuCoin tab** of the
monthly "BA" grid-bot backtest snapshots. Designed to be updated **once a month** as a new
snapshot is published.

**Open:** [`KuCoin-Top25-Bot-Returns.html`](KuCoin-Top25-Bot-Returns.html) — double-click it; no server needed.

It shows, for the top 25 coins by market cap:
- Latest trailing-12-month bot return, the 9-month (through-cycle) average, and a per-coin trend sparkline.
- An equal-weight portfolio trend chart (the average has been compressing as the bear market deepens).
- A live filter to **exclude coins below a chosen % return** (rebalances the cards, chart and calculator).
- A calculator: amount × return % × tax → **after-tax weekly / monthly / annual income**, plus a reverse
  "capital needed for a weekly target".

---

## What the numbers mean
- `r12` / **"12-Mo %"** = trailing-12-month **backtested** bot return (annual, simple sum of monthly returns).
- **"Avg Mo. %"** = r12 ÷ 12 · **"Weekly %"** = r12 ÷ 52.
- Source = **KuCoin tab only** (the tab containing KCS). Stablecoins and memecoins are excluded by the source
  sheet, so "top 25 by market cap" = the 25 largest tradeable coins on that tab.

## Files
| File | Role |
|---|---|
| `coins.csv` | The universe — 25 coins with **latest-month** metadata (ticker, name, rank, market cap, category). Row order = market-cap order. |
| `returns.csv` | Long-format history — one row per coin per month: `date,label,ticker,r12`. **This is what you append each month.** |
| `analyze.py` | Reads the two CSVs → computes averages/series → writes `data.json`. |
| `build_html.py` | Reads `data.json` → writes the self-contained `KuCoin-Top25-Bot-Returns.html`. |
| `KuCoin-Top25-Bot-Returns.html` | The deliverable (data embedded inline). |

`data.json` is a generated artifact (git-ignored).

---

## Monthly update runbook

When the new month's **BA <Month>** sheet is in Google Drive:

1. **Read the new KuCoin tab** (Tab 1 — the one with KCS) for that month. (Claude does this via the Google
   Drive integration; ask: *"pull the new BA <month> KuCoin tab and update the report".*)
2. **Append to `returns.csv`** — one row per tracked coin:
   `YYYY-MM,<Mon YY>,<TICKER>,<12-mo %>`  (e.g. `2026-06,Jun 26,BTC,5.6`). Omit a coin only if it's absent
   that month.
3. **Refresh `coins.csv`** if the top-25-by-market-cap list or the metadata changed: update rank/market cap,
   add any new entrant (and backfill its earlier `returns.csv` rows if you want full history), drop anything
   that fell out. Keep rows in market-cap order.
4. **Rebuild:**
   ```bash
   python3 analyze.py && python3 build_html.py
   ```
5. Open `KuCoin-Top25-Bot-Returns.html` to confirm, then commit & push:
   ```bash
   git add -A && git commit -m "Add <Mon YY> snapshot" && git push
   ```

The HTML, chart, table and calculator all regenerate automatically from the CSVs — nothing else to edit.
