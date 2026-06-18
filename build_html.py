#!/usr/bin/env python3
"""Build the self-contained HTML report from data.json."""
import json

with open("data.json") as f:
    DATA = json.load(f)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KuCoin Bot Returns — Top 25 by Market Cap</title>
<style>
  :root{
    --bg:#0b0e13; --panel:#141921; --panel2:#1b2230; --line:#252d3b;
    --txt:#e6edf3; --mut:#8b97a7; --dim:#5d6776;
    --accent:#2dd4a7; --accent2:#38bdf8; --warn:#f5a524; --bad:#f4607a;
    --shadow:0 1px 0 rgba(255,255,255,.02),0 12px 30px -12px rgba(0,0,0,.6);
  }
  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(1200px 600px at 70% -10%,#10212a 0%,var(--bg) 55%);
       color:var(--txt);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       -webkit-font-smoothing:antialiased;padding:32px 20px 80px}
  .wrap{max-width:1120px;margin:0 auto}
  h1{font-size:26px;margin:0 0 4px;letter-spacing:-.02em}
  h2{font-size:17px;margin:34px 0 14px;letter-spacing:-.01em;color:var(--txt)}
  .sub{color:var(--mut);font-size:13.5px}
  .pill{display:inline-block;padding:2px 9px;border:1px solid var(--line);border-radius:999px;
        color:var(--mut);font-size:12px;margin-right:6px;background:var(--panel)}
  .cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px;box-shadow:var(--shadow)}
  .card .k{color:var(--mut);font-size:12.5px;margin-bottom:8px;text-transform:uppercase;letter-spacing:.04em}
  .card .v{font-size:27px;font-weight:650;letter-spacing:-.02em}
  .card .v small{font-size:14px;color:var(--mut);font-weight:500}
  .card .note{color:var(--dim);font-size:12px;margin-top:5px}
  .up{color:var(--accent)} .down{color:var(--bad)} .neu{color:var(--accent2)}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px 22px;box-shadow:var(--shadow)}
  /* calculator */
  .calc{display:grid;grid-template-columns:1.05fr 1fr;gap:0;overflow:hidden;padding:0}
  .calc .inp{padding:22px 24px;border-right:1px solid var(--line)}
  .calc .out{padding:22px 24px;background:linear-gradient(180deg,#11202a,#0f1620)}
  label{display:block;color:var(--mut);font-size:12.5px;margin:14px 0 6px;letter-spacing:.02em}
  label:first-child{margin-top:0}
  input[type=number],select{width:100%;background:var(--panel2);border:1px solid var(--line);color:var(--txt);
        border-radius:10px;padding:11px 12px;font-size:15px;outline:none}
  input[type=number]:focus,select:focus{border-color:var(--accent2);box-shadow:0 0 0 3px rgba(56,189,248,.12)}
  .row{display:flex;gap:10px}
  .seg{display:flex;gap:6px;flex-wrap:wrap}
  .seg button,.preset{background:var(--panel2);border:1px solid var(--line);color:var(--mut);border-radius:8px;
        padding:7px 11px;font-size:12.5px;cursor:pointer;transition:.12s}
  .seg button.on{background:var(--accent2);border-color:var(--accent2);color:#04121b;font-weight:600}
  .seg button:hover,.preset:hover{border-color:var(--accent2);color:var(--txt)}
  .hero{font-size:42px;font-weight:720;letter-spacing:-.03em;color:var(--accent);line-height:1.05}
  .hero small{font-size:15px;color:var(--mut);font-weight:500}
  .outk{color:var(--mut);font-size:12.5px;text-transform:uppercase;letter-spacing:.04em}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px 18px;margin-top:18px}
  .stat .s{font-size:19px;font-weight:600} .stat .l{color:var(--mut);font-size:12px}
  .muted{color:var(--mut)} .small{font-size:12.5px}
  /* table */
  table{width:100%;border-collapse:collapse;font-size:13.5px}
  th,td{padding:9px 10px;text-align:right;border-bottom:1px solid var(--line);white-space:nowrap}
  th{color:var(--mut);font-weight:500;font-size:12px;cursor:pointer;user-select:none;position:sticky;top:0;background:var(--panel)}
  th:hover{color:var(--txt)}
  th.l,td.l{text-align:left}
  tbody tr{cursor:pointer}
  tbody tr:hover{background:var(--panel2)}
  .tk{font-weight:650} .nm{color:var(--mut);font-size:12px;margin-left:6px}
  .barwrap{display:inline-block;width:120px;vertical-align:middle}
  .tag{font-size:11px;color:var(--dim);border:1px solid var(--line);border-radius:6px;padding:1px 6px}
  .chartbox{position:relative}
  .leg{color:var(--mut);font-size:12px}
  .foot{color:var(--dim);font-size:12.5px;line-height:1.7;margin-top:8px}
  .foot b{color:var(--mut)}
  .fbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:13.5px;color:var(--mut)}
  .fbar input[type=number]{width:74px;padding:7px 9px}
  .fbar select{width:auto;padding:7px 9px}
  .fbar .chk{display:flex;align-items:center;gap:8px;color:var(--txt);cursor:pointer}
  .fbar input[type=checkbox]{width:16px;height:16px;accent-color:var(--accent);cursor:pointer}
  #fCount{font-size:12.5px;margin-left:2px}
  tbody tr.excl{opacity:.3} tbody tr.excl:hover{opacity:.6}
  a{color:var(--accent2)}
  @media(max-width:880px){.cards{grid-template-columns:repeat(2,1fr)}.calc{grid-template-columns:1fr}
    .calc .inp{border-right:none;border-bottom:1px solid var(--line)} .barwrap{width:74px}}
</style>
</head>
<body>
<div class="wrap">

  <h1>KuCoin Grid-Bot Returns — Top 25 by Market Cap</h1>
  <div class="sub" id="metaline"></div>

  <div class="panel fbar" style="margin-top:18px">
    <span class="chk"><input type="checkbox" id="fEnable"> Exclude coins that returned below</span>
    <input type="number" id="fThresh" value="10" min="0" step="1"> %
    <span>on</span>
    <select id="fBasis"><option value="latest">latest 12-mo %</option><option value="avg9">9-mo avg %</option></select>
    <span id="fCount"></span>
  </div>

  <div class="cards" id="cards"></div>

  <h2>The 12-month average is compressing as the bear market deepens</h2>
  <div class="panel chartbox">
    <div class="leg">Equal-weight average trailing-12-month bot return across the top 25 coins, by snapshot month.</div>
    <div id="chart"></div>
  </div>

  <h2>Investment &amp; weekly income calculator</h2>
  <div class="panel calc">
    <div class="inp">
      <label>Amount to invest (A$)</label>
      <input type="number" id="amount" value="1000" min="0" step="100">

      <label>Use return from</label>
      <select id="coinSel"></select>

      <label>Return basis &nbsp;<span class="muted small" id="basisHint"></span></label>
      <div class="seg" id="basis">
        <button data-b="annual" class="on">Annual (12-mo)</button>
        <button data-b="monthly">Monthly</button>
        <button data-b="weekly">Weekly</button>
      </div>

      <label>Return rate (%)</label>
      <div class="row">
        <input type="number" id="rate" value="0" step="0.1">
        <div class="seg">
          <button id="srcLatest" class="on" data-src="latest">Latest</button>
          <button id="srcAvg" data-src="avg9">9-mo avg</button>
        </div>
      </div>

      <label>Tax rate on profit (%)</label>
      <input type="number" id="tax" value="32" min="0" max="100" step="1">
      <div class="seg" style="margin-top:8px">
        <span class="muted small" style="align-self:center">AU marginal incl. Medicare:</span>
        <button class="preset" data-t="0">0</button>
        <button class="preset" data-t="18">18</button>
        <button class="preset" data-t="32">32</button>
        <button class="preset" data-t="39">39</button>
        <button class="preset" data-t="47">47</button>
      </div>
    </div>

    <div class="out">
      <div class="outk">Final output per week (after tax)</div>
      <div class="hero" id="weeklyNet">A$0.00<small> /week</small></div>

      <div class="grid2">
        <div class="stat"><div class="l">Weekly gross</div><div class="s" id="weeklyGross">A$0.00</div></div>
        <div class="stat"><div class="l">Weekly tax</div><div class="s down" id="weeklyTax">A$0.00</div></div>
        <div class="stat"><div class="l">Monthly net</div><div class="s" id="monthlyNet">A$0.00</div></div>
        <div class="stat"><div class="l">Annual net</div><div class="s" id="annualNet">A$0.00</div></div>
      </div>

      <div style="margin-top:18px;padding-top:16px;border-top:1px solid var(--line)">
        <div class="outk" style="margin-bottom:8px">Reverse: capital needed for a weekly target</div>
        <div class="row" style="align-items:center">
          <input type="number" id="target" value="200" step="10" style="max-width:130px">
          <span class="muted small">A$/week net &rarr;&nbsp;</span>
          <span class="s" id="needed" style="font-size:19px;font-weight:600"></span>
        </div>
      </div>
      <div class="foot small" id="calcnote"></div>
    </div>
  </div>

  <h2>Top 25 coins — KuCoin tab (click a row to load it into the calculator)</h2>
  <div class="panel" style="padding:8px 10px;overflow:auto">
    <table id="tbl">
      <thead><tr>
        <th class="l" data-s="rank">#</th>
        <th class="l" data-s="ticker">Coin</th>
        <th data-s="mcap_b">Mkt&nbsp;cap</th>
        <th class="l" data-s="cat">Category</th>
        <th data-s="latest">Latest 12-mo&nbsp;%</th>
        <th data-s="avg9">9-mo avg&nbsp;%</th>
        <th data-s="wk_latest">Weekly* %</th>
        <th class="l">Sep&rarr;May trend</th>
      </tr></thead>
      <tbody></tbody>
    </table>
  </div>
  <div class="foot">*Weekly % = Latest 12-mo % ÷ 52 (simple). Sparkline spans Sep 25 → May 26.</div>

  <h2>How to read this &amp; caveats</h2>
  <div class="panel">
    <div class="foot">
      <p><b>What the numbers are.</b> Each value is the <b>trailing-12-month backtested return</b> of running the bot
      on that coin's pair on <b>KuCoin</b> (the KuCoin tab only, per your instruction). "9-mo avg" is the mean of the nine
      monthly snapshots (Sept 2025 → May 2026) — a through-cycle figure that smooths out the bear-market compression.
      "Latest" is the May 2026 snapshot.</p>
      <p><b>Why the average is falling.</b> The trailing-12-month window now contains more of the bear market, so the
      portfolio average dropped from <b id="f1"></b> to <b id="f2"></b> (<b id="f3"></b>). Almost every coin's
      latest reading sits at or near its own 9-month low — returns are compressed right now, which is consistent with
      being near a cycle bottom.</p>
      <p><b>Volatility pays, size doesn't.</b> Grid bots earn from oscillation, so the mega-caps return little
      (BTC ~5%, TRX ~3%, BNB ~9%, ETH ~12%) while smaller, more volatile large-caps return far more
      (ZEC ~73%, TAO/HYPE ~34%, UNI/NEAR ~29%). ZEC is an outlier driven by a large directional run and may not repeat.</p>
      <p><b>For sizing your end-of-year deployment.</b> If you want a conservative plan, model with the
      <b>9-mo avg</b> (or even the recent low) rather than peak figures — returns this late in the bear are the
      compressed end of the range. Use the calculator with both "Latest" and "9-mo avg" to bracket a realistic weekly income.</p>
      <p><b>Caveats.</b> Backtested ≠ future; past bot performance assumes similar volatility and the same settings.
      A few source cells look like data glitches (e.g. Mantle Dec 25 = 1.76%) and are left raw — they don't change the
      conclusions. Returns are gross of trading fees and slippage. Tax: the calculator just applies a flat rate you enter —
      it is <b>not tax advice</b>; AU bot-trading profit is generally ordinary income, so confirm your marginal rate.</p>
    </div>
  </div>

</div>

<script>
const DATA = __DATA__;
const fmtMoney = n => "A$"+ n.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
const fmtBig = n => "A$"+ Math.round(n).toLocaleString();
const $ = id => document.getElementById(id);

/* meta line + insight cards */
const M = DATA.meta;
$("metaline").innerHTML =
  '<span class="pill">Source: '+M.source+'</span>'+
  '<span class="pill">Window: '+M.window+'</span>'+
  '<span class="pill">'+M.n_coins+' coins · top 25 by market cap</span>'+
  '<span class="pill">Generated '+M.generated+'</span>';

function renderCards(P){
  $("cards").innerHTML = [
    ['Portfolio avg — latest', P.latest.toFixed(1)+'<small>%</small>', 'neu', P.n+' coins · May 2026'],
    ['Through-cycle avg', P.avg9.toFixed(1)+'<small>%</small>', 'up', 'mean of 9 monthly snapshots'],
    ['Change Sep&rarr;May', (((P.latest-P.first)/P.first)*100).toFixed(1)+'<small>%</small>', 'down', P.first.toFixed(1)+'% &rarr; '+P.latest.toFixed(1)+'%'],
    ['Latest range', P.minLat.toFixed(1)+'&ndash;'+P.maxLat.toFixed(1)+'<small>%</small>', 'neu', 'lowest&ndash;highest included'],
  ].map(c=>'<div class="card"><div class="k">'+c[0]+'</div><div class="v '+c[2]+'">'+c[1]+'</div><div class="note">'+c[3]+'</div></div>').join('');
}

$("f1").textContent = M.port_first.toFixed(1)+'%';
$("f2").textContent = M.port_latest.toFixed(1)+'%';
$("f3").textContent = M.port_change_pct.toFixed(1)+'% relative';

/* ---- line chart of portfolio series ---- */
function drawChart(S){
  const w=1040,h=230,padL=42,padR=16,padT=18,padB=28;
  const s=S, mn=Math.min(...s), mx=Math.max(...s);
  const lo=Math.floor((mn-2)/2)*2, hi=Math.ceil((mx+2)/2)*2;
  const X=i=> padL + i*(w-padL-padR)/(s.length-1);
  const Y=v=> padT + (1-(v-lo)/(hi-lo))*(h-padT-padB);
  let grid='', axis='';
  for(let g=lo; g<=hi; g+=4){ const y=Y(g);
    grid+='<line x1="'+padL+'" y1="'+y+'" x2="'+(w-padR)+'" y2="'+y+'" stroke="#252d3b"/>';
    axis+='<text x="'+(padL-8)+'" y="'+(y+4)+'" fill="#5d6776" font-size="11" text-anchor="end">'+g+'%</text>';
  }
  let labels='';
  DATA.months.forEach((m,i)=> labels+='<text x="'+X(i)+'" y="'+(h-8)+'" fill="#8b97a7" font-size="11" text-anchor="middle">'+m+'</text>');
  const path=s.map((v,i)=>(i?'L':'M')+X(i)+' '+Y(v)).join(' ');
  const area=path+' L'+X(s.length-1)+' '+(h-padB)+' L'+X(0)+' '+(h-padB)+' Z';
  let dots='';
  s.forEach((v,i)=>{ dots+='<circle cx="'+X(i)+'" cy="'+Y(v)+'" r="3.5" fill="#0b0e13" stroke="#2dd4a7" stroke-width="2"/>'+
    '<text x="'+X(i)+'" y="'+(Y(v)-10)+'" fill="#e6edf3" font-size="11" text-anchor="middle">'+v.toFixed(1)+'</text>'; });
  $("chart").innerHTML='<svg viewBox="0 0 '+w+' '+h+'" width="100%" preserveAspectRatio="xMidYMid meet">'+
    '<defs><linearGradient id="g" x1="0" x2="0" y1="0" y2="1">'+
    '<stop offset="0" stop-color="#2dd4a7" stop-opacity=".28"/><stop offset="1" stop-color="#2dd4a7" stop-opacity="0"/></linearGradient></defs>'+
    grid+axis+'<path d="'+area+'" fill="url(#g)"/><path d="'+path+'" fill="none" stroke="#2dd4a7" stroke-width="2.5"/>'+dots+labels+'</svg>';
}

/* ---- sparkline helper ---- */
function spark(series){
  const vals=series.map(v=>v===null?null:v);
  const present=vals.filter(v=>v!==null);
  const mn=Math.min(...present), mx=Math.max(...present);
  const w=120,h=26,pad=3;
  const span=(mx-mn)||1;
  const pts=[]; vals.forEach((v,i)=>{ if(v===null)return;
    const x=pad+i*(w-2*pad)/(vals.length-1);
    const y=pad+(1-(v-mn)/span)*(h-2*pad); pts.push([x,y]); });
  const d=pts.map((p,i)=>(i?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' ');
  const last=pts[pts.length-1], first=pts[0];
  const col = series[series.length-1] >= series.find(v=>v!==null) ? '#2dd4a7' : '#f4607a';
  return '<svg class="barwrap" viewBox="0 0 '+w+' '+h+'" height="26">'+
    '<path d="'+d+'" fill="none" stroke="'+col+'" stroke-width="1.6"/>'+
    '<circle cx="'+last[0].toFixed(1)+'" cy="'+last[1].toFixed(1)+'" r="2.4" fill="'+col+'"/></svg>';
}

/* ---- table ---- */
let sortKey='rank', sortDir=1;
function renderTable(){
  const rows=[...DATA.coins].sort((a,b)=>{
    let x=a[sortKey],y=b[sortKey];
    if(typeof x==='string'){return sortDir*x.localeCompare(y);}
    return sortDir*(x-y);
  });
  const tb=document.querySelector('#tbl tbody');
  tb.innerHTML=rows.map(c=>{
    return '<tr data-tk="'+c.ticker+'">'+
      '<td class="l muted">'+c.rank+'</td>'+
      '<td class="l"><span class="tk">'+c.ticker+'</span><span class="nm">'+c.name+'</span></td>'+
      '<td>'+c.mcap+'</td>'+
      '<td class="l"><span class="tag">'+c.cat+'</span></td>'+
      '<td>'+c.latest.toFixed(2)+'%</td>'+
      '<td class="muted">'+c.avg9.toFixed(2)+'%</td>'+
      '<td>'+c.wk_latest.toFixed(3)+'%</td>'+
      '<td class="l">'+spark(c.series)+'</td>'+
    '</tr>';
  }).join('');
  tb.querySelectorAll('tr').forEach(tr=>tr.onclick=()=>{ $("coinSel").value=tr.dataset.tk; loadCoin(); });
  applyExcl();
}
document.querySelectorAll('#tbl th[data-s]').forEach(th=>th.onclick=()=>{
  const k=th.dataset.s; sortDir = (sortKey===k)? -sortDir : (typeof DATA.coins[0][k]==='string'?1:-1);
  sortKey=k; renderTable();
});

/* ---- calculator ---- */
const coinMap={}; DATA.coins.forEach(c=>coinMap[c.ticker]=c);
let basis='annual', src='latest';
(function fillSel(){
  let opts='<option value="__PORT_LATEST">Portfolio avg — latest ('+M.port_latest.toFixed(1)+'%)</option>'+
           '<option value="__PORT_AVG">Portfolio avg — 9-mo ('+M.port_avg9.toFixed(1)+'%)</option>'+
           '<option value="__CUSTOM">Custom rate…</option>'+
           '<optgroup label="Coins">';
  DATA.coins.forEach(c=> opts+='<option value="'+c.ticker+'">'+c.ticker+' — '+c.name+'</option>');
  $("coinSel").innerHTML=opts+'</optgroup>';
})();

function currentRate(){
  const v=$("coinSel").value;
  if(v==='__CUSTOM') return parseFloat($("rate").value)||0;
  if(v==='__PORT_LATEST') return PORT.latest;
  if(v==='__PORT_AVG') return PORT.avg9;
  const c=coinMap[v]; if(!c) return 0;
  return src==='avg9'? c.avg9 : c.latest;
}
function loadCoin(){
  const v=$("coinSel").value;
  if(v!=='__CUSTOM'){ basis='annual'; setBasisBtns();
    $("rate").value=currentRate().toFixed(2);
  }
  calc();
}
function setBasisBtns(){ document.querySelectorAll('#basis button').forEach(b=>b.classList.toggle('on',b.dataset.b===basis));
  $("basisHint").textContent = basis==='annual'?'(the sheet’s 12-mo figure)':basis==='monthly'?'(×12 → year)':'(×52 → year)';}

function calc(){
  const amt=parseFloat($("amount").value)||0;
  const r=(parseFloat($("rate").value)||0)/100;
  const tax=(parseFloat($("tax").value)||0)/100;
  let weeklyGross;
  if(basis==='annual') weeklyGross=amt*r/52;
  else if(basis==='monthly') weeklyGross=amt*r*12/52;
  else weeklyGross=amt*r;
  const weeklyTax=weeklyGross*tax, weeklyNet=weeklyGross-weeklyTax;
  $("weeklyNet").innerHTML=fmtMoney(weeklyNet)+'<small> /week</small>';
  $("weeklyGross").textContent=fmtMoney(weeklyGross);
  $("weeklyTax").textContent=fmtMoney(weeklyTax);
  $("monthlyNet").textContent=fmtMoney(weeklyNet*52/12);
  $("annualNet").textContent=fmtMoney(weeklyNet*52);
  // reverse
  const tgt=parseFloat($("target").value)||0;
  const netRateWk = basis==='annual'? r/52 : basis==='monthly'? r*12/52 : r;
  const eff = netRateWk*(1-tax);
  $("needed").textContent = eff>0 ? fmtBig(tgt/eff) : '—';
  $("calcnote").innerHTML='Using <b>'+(basis==='annual'?'annual':basis)+'</b> rate of <b>'+
     ($("rate").value||0)+'%</b> on <b>'+fmtBig(amt)+'</b> at <b>'+($("tax").value||0)+'%</b> tax. '+
     'Weekly = rate ÷ 52 (gross of fees/slippage).';
}

/* events */
$("coinSel").onchange=loadCoin;
document.querySelectorAll('#basis button').forEach(b=>b.onclick=()=>{basis=b.dataset.b;setBasisBtns();calc();});
[['srcLatest','latest'],['srcAvg','avg9']].forEach(()=>{});
$("srcLatest").onclick=()=>{src='latest';$("srcLatest").classList.add('on');$("srcAvg").classList.remove('on');loadCoin();};
$("srcAvg").onclick=()=>{src='avg9';$("srcAvg").classList.add('on');$("srcLatest").classList.remove('on');loadCoin();};
document.querySelectorAll('.preset').forEach(p=>p.onclick=()=>{$("tax").value=p.dataset.t;calc();});
['amount','rate','tax','target'].forEach(id=>$(id).addEventListener('input',()=>{ if(id==='rate')$("coinSel").value='__CUSTOM'; calc();}));

/* ---- filter + portfolio recompute (client-side, no re-pull) ---- */
let PORT=null;
function getIncluded(){
  if(!$("fEnable").checked) return DATA.coins.slice();
  const t=parseFloat($("fThresh").value)||0, b=$("fBasis").value;
  const r=DATA.coins.filter(c=> (b==='avg9'?c.avg9:c.latest) >= t);
  return r.length? r : DATA.coins.slice();   // never let the basket go empty
}
function computePort(list){
  const series=[], ns=[];
  for(let i=0;i<DATA.months.length;i++){
    const v=list.map(c=>c.series[i]).filter(x=>x!==null);
    series.push(v.length? v.reduce((a,b)=>a+b,0)/v.length : null);
    ns.push(v.length);
  }
  const avg9=list.reduce((a,c)=>a+c.avg9,0)/list.length;
  const lats=list.map(c=>c.latest);
  return {series, ns, latest:series[series.length-1], first:series.find(x=>x!==null),
          avg9, n:list.length, minLat:Math.min(...lats), maxLat:Math.max(...lats)};
}
function applyExcl(){
  const inc=new Set(getIncluded().map(c=>c.ticker));
  document.querySelectorAll('#tbl tbody tr').forEach(tr=>tr.classList.toggle('excl',!inc.has(tr.dataset.tk)));
}
function updatePortOptions(P){
  for(const op of $("coinSel").options){
    if(op.value==='__PORT_LATEST') op.textContent='Portfolio avg — latest ('+P.latest.toFixed(1)+'%)';
    if(op.value==='__PORT_AVG') op.textContent='Portfolio avg — 9-mo ('+P.avg9.toFixed(1)+'%)';
  }
}
function recompute(){
  const inc=getIncluded(), incSet=new Set(inc.map(c=>c.ticker));
  const excl=DATA.coins.filter(c=>!incSet.has(c.ticker)).map(c=>c.ticker);
  PORT=computePort(inc);
  drawChart(PORT.series);
  renderCards(PORT);
  updatePortOptions(PORT);
  applyExcl();
  $("fCount").innerHTML = $("fEnable").checked
    ? ('<span class="up">'+inc.length+'</span> of '+DATA.coins.length+' coins included'+(excl.length?' &middot; excluded: '+excl.join(', '):''))
    : ('all '+DATA.coins.length+' coins included');
  const v=$("coinSel").value;
  if(v==='__PORT_LATEST'||v==='__PORT_AVG') $("rate").value=currentRate().toFixed(2);
  calc();
}
['fThresh','fBasis'].forEach(id=>$(id).addEventListener('input',recompute));
$("fBasis").addEventListener('change',recompute);
$("fEnable").addEventListener('change',recompute);

renderTable(); setBasisBtns(); recompute();
$("coinSel").value='__PORT_AVG'; loadCoin();
</script>
</body>
</html>
"""

html = TEMPLATE.replace("__DATA__", json.dumps(DATA))
with open("KuCoin-Top25-Bot-Returns.html","w") as f:
    f.write(html)
print("wrote KuCoin-Top25-Bot-Returns.html  (%d bytes)" % len(html))
