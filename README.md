# KuCoin Grid-Bot Returns — by Market Cap

A self-contained HTML report + investment/tax calculator built from the **KuCoin tab** of the
monthly "BA" grid-bot backtest snapshots. Designed to be updated **once a month** as a new
snapshot is published.

**Live:** https://speaktothewind.github.io/kucoin-bot-returns/ (GitHub Pages, auto-deploys on push)
**Local:** [`KuCoin-Top25-Bot-Returns.html`](KuCoin-Top25-Bot-Returns.html) — double-click it; no server needed.

Styling follows the shared **Session Ledger theme** (slate panels, Archivo + IBM Plex Mono, teal/orange
signals, yellow accent) — same design language as the NAS100 P&L tracker. The theme lives in
`build_html.py`; regenerating keeps it.

A picker at the top switches the whole page between **Top 25 / 30 / 45 / 50 / All** coins by market cap, or
**My coins** — your own pick of up to 30 (ticked in the table, remembered in your browser). It opens on Top 25.

It shows, for the chosen coins:
- Latest trailing-12-month bot return, the through-cycle average, and a per-coin trend sparkline.
- An equal-weight portfolio trend chart (the average has been compressing as the bear market deepens). The
  "Change" figure compares like-for-like — only coins with a reading in both months — and says how many.
- A live filter to **exclude coins below a chosen % return** (rebalances the cards, chart and calculator).
- A calculator: amount × return % × tax → **after-tax weekly / monthly / annual income**, plus a reverse
  "capital needed for a weekly target".

---

## What the numbers mean
- `r12` / **"12-Mo %"** = trailing-12-month **backtested** bot return (annual, simple sum of monthly returns).
- **"Avg Mo. %"** = r12 ÷ 12 · **"Weekly %"** = r12 ÷ 52.
- Source = **KuCoin tab only** (the tab containing KCS). Stablecoins and memecoins are excluded by the source
  sheet, so "top 25 by market cap" = the 25 largest tradeable coins on that tab.
- Every coin on the tab is kept, Sep 2025 onwards (filled in from the monthly sheets on 08/10/2026), so a coin's
  history doesn't start the month it entered the top 25.

## Files
| File | Role |
|---|---|
| `coins.csv` | The universe — every tested coin with **latest-month** metadata (ticker, name, rank, market cap, category). Row order = market-cap order; "Top N" on the page = the first N rows. |
| `returns.csv` | Long-format history — one row per coin per month: `date,label,ticker,r12,rank` (rank = that month's market-cap rank). **This is what you append each month.** |
| `analyze.py` | Reads the two CSVs → computes averages/series → writes `data.json`. |
| `build_html.py` | Reads `data.json` → writes the self-contained `KuCoin-Top25-Bot-Returns.html`. |
| `KuCoin-Top25-Bot-Returns.html` | The deliverable (data embedded inline). |

`data.json` is a generated artifact (git-ignored).

---

## Monthly update runbook

When the new month's **BA <Month>** sheet is in Google Drive:

1. **Read the new KuCoin tab** (Tab 1 — the one with KCS) for that month. (Claude does this via the Google
   Drive integration; ask: *"pull the new BA <month> KuCoin tab and update the report".*)
2. **Append to `returns.csv`** — one row per coin on the tab:
   `YYYY-MM,<Mon YY>,<TICKER>,<12-mo %>,<rank>`  (e.g. `2026-06,Jun 26,BTC,5.6,1`). Omit a coin only if it's
   absent that month.
3. **Refresh `coins.csv`** from the same tab: rank/market cap for every coin, new entrants added, anything that
   fell off the tab dropped. Keep rows in market-cap order.
4. **Rebuild:**
   ```bash
   python3 analyze.py && python3 build_html.py
   ```
5. Open `KuCoin-Top25-Bot-Returns.html` to confirm, then commit & push:
   ```bash
   git add -A && git commit -m "Add <Mon YY> snapshot" && git push
   ```

The HTML, chart, table and calculator all regenerate automatically from the CSVs — nothing else to edit.
