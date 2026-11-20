#!/usr/bin/env python3
"""Versão 2 do guia: hero em imagem, menu moderno, abas separadas (aéreo/trens),
tabelas com valor unitário, subtotal e rateio por pessoa."""
import base64
import importlib.util
import io
import json
import os

from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz do repo
IMG = os.path.join(BASE, "img")
DATA = os.path.join(BASE, "data")

EXTRA_CSS = """
td.lk{white-space:normal}
a.btn.mini{padding:6px 10px;font-size:12px;margin:2px 4px 2px 0;border-radius:8px}

/* ---------- mala ---------- */
.gridmala{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:14px;margin:8px 0 4px}
.malacol{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 18px;box-shadow:0 1px 2px rgba(15,23,42,.03)}
.mhead{display:flex;align-items:baseline;justify-content:space-between;gap:10px;border-bottom:1px solid var(--line);padding-bottom:9px;margin-bottom:6px}
.mhead h3{margin:0;font-size:16.5px}
.prog{font-size:12px;color:var(--muted);font-weight:600;white-space:nowrap}
.mgrupo h4{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:12px 0 3px}
.item{display:flex;gap:9px;align-items:flex-start;padding:5px 0;font-size:14px;cursor:pointer;line-height:1.4}
.item input{width:18px;height:18px;accent-color:#e2562b;margin:1px 0 0;flex:0 0 auto;cursor:pointer}
.item input:checked + span{color:#9aa5b1;text-decoration:line-through}
.malabar{display:flex;gap:14px;align-items:center;justify-content:space-between;margin:14px 0 6px;flex-wrap:wrap}

/* ---------- clima ---------- */
.clima{margin:10px 0 4px;padding:9px 12px;border-radius:10px;background:#f4f7fa;border:1px solid #e3eaf1;
  font-size:13px;color:#334155;display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center}
.clima b{font-weight:700;color:var(--ink)}
.clima .ico{font-size:15px}
.clima .src{font-size:11px;color:#94a3b8}
.clima.erro{background:#fdf3f0;border-color:#f2d9d1;color:#9a3412}
.quick{margin-top:14px}
.quick .chipf{margin:0 6px 8px 0}
.vazio-embed{background:#0f172a;display:flex;align-items:center;justify-content:center}
.vexp{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:34px;opacity:.55}

/* ---------- conversor ---------- */
.conv{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px;max-width:520px;box-shadow:0 1px 2px rgba(15,23,42,.03)}
.convrow{display:block}
.convrow label{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:700;margin-bottom:10px}
.convrow input{display:block;width:100%;margin-top:5px;padding:12px 14px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:18px;font-weight:600;background:#fff}
.convrow input:focus{outline:2px solid #cfe0ee;border-color:#9fc3e0}
.convrow .arrow{display:block;text-align:center;color:#9aa1ab;font-size:18px;margin:6px 0}
.rate{font-size:15px;font-weight:700;margin:12px 0 2px}
/* ---------- vídeos ---------- */
.vembed{position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;margin-bottom:14px;background:#000}
.vembed iframe{position:absolute;top:0;left:0;width:100%;height:100%;border:0}
h4.dest{font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:10px 0 2px}

/* ---------- topbar + drawer ---------- */
.topbar{position:sticky;top:0;z-index:900;background:rgba(255,255,255,.92);backdrop-filter:saturate(1.4) blur(12px);border-bottom:1px solid var(--line)}
.tbinner{display:flex;align-items:center;justify-content:space-between;height:58px}
.brand{font-weight:800;letter-spacing:-.01em;color:var(--ink);text-decoration:none;font-size:15px;white-space:nowrap}
.burger{width:44px;height:40px;border:0;background:transparent;cursor:pointer;display:flex;flex-direction:column;justify-content:center;gap:5px;align-items:flex-end;padding:0}
.burger span{display:block;height:2px;width:22px;background:var(--ink);border-radius:2px;transition:.2s}
.burger span:nth-child(2){width:16px}
.burger span:nth-child(3){width:20px}
.burger:hover span{width:22px}
.scrim{position:fixed;inset:0;background:rgba(8,15,26,.45);opacity:0;pointer-events:none;transition:.22s;z-index:940}
.scrim.on{opacity:1;pointer-events:auto}
.drawer{position:fixed;top:0;right:0;height:100%;width:min(340px,86vw);background:#fff;z-index:950;
  transform:translateX(105%);transition:transform .26s cubic-bezier(.3,.8,.3,1);box-shadow:-12px 0 40px rgba(8,15,26,.18);
  display:flex;flex-direction:column;padding:18px 0 24px}
.drawer.on{transform:translateX(0)}
.dhead{display:flex;align-items:center;justify-content:space-between;padding:0 20px 12px;border-bottom:1px solid var(--line);
  font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700}
.dclose{border:0;background:transparent;font-size:26px;line-height:1;color:var(--muted);cursor:pointer}
.drawer nav{display:block;padding:10px 0;overflow-y:auto}
.drawer nav a{display:block;padding:11px 20px;text-decoration:none;color:var(--ink-2);font-weight:600;font-size:15px;border-left:3px solid transparent}
.drawer nav a span{display:block;font-weight:400;font-size:12px;color:var(--muted);margin-top:2px}
.drawer nav a:hover{background:#f6f8fa}
.drawer nav a[aria-selected="true"]{border-left-color:var(--accent);background:#fbfcfd}
.drawer nav a[aria-selected="true"] span{color:var(--accent)}

/* ---------- calendário ---------- */
.calfull{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;margin:16px 0 8px;box-shadow:0 1px 2px rgba(15,23,42,.03)}
.calfull h3{margin:0 0 2px;font-size:16px}
.scen{display:block;margin:10px 0 14px}
.calwrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px 26px;margin-bottom:6px}
.cal{margin:0}
.cal h4{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin:0 0 7px;font-weight:700}
.calgrid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px}
.calgrid .wd{font-size:9.5px;text-transform:uppercase;color:#9aa1ab;text-align:center;padding:1px 0;font-weight:700;letter-spacing:.03em}
.cday{min-width:0;min-height:46px;border-radius:9px;background:#f3f5f8;display:flex;flex-direction:column;
  align-items:center;justify-content:center;font-size:11.5px;color:#8f99a5;padding:3px 2px;text-align:center;
  line-height:1.05;overflow:hidden}
.cday.blank{background:transparent;min-height:0;height:auto}
.cday.notrip{background:#f7f8fa;color:#b6bfc9}
.cday.trip{color:#fff;cursor:pointer;font-weight:700;box-shadow:inset 0 0 0 1px rgba(255,255,255,.18)}
.cday.trip .cn-long{display:none}
.cday.trip .cn-short{display:inline}
.cday.trip .cn{font-size:8.5px;font-weight:500;opacity:.95;margin-top:2px;max-width:100%;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap;letter-spacing:.01em}
.cday.trip:hover{filter:brightness(1.1)}
.cday.today{outline:2px solid var(--accent);outline-offset:1px}
.leg{display:block;font-size:12px;color:var(--muted)}
.leg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin:0 5px 0 0;vertical-align:-1px}
.leg span{display:inline-block;margin:0 12px 6px 0}
.sanf{margin-top:30px}

/* ---------- sanfona do dia a dia ---------- */
details.daycard{background:#fff;border:1px solid var(--line);border-radius:18px;margin:12px 0;overflow:hidden;box-shadow:0 1px 2px rgba(15,23,42,.03)}
details.daycard>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:10px;padding:16px 18px;font-weight:700;font-size:16px}
details.daycard>summary::-webkit-details-marker{display:none}
details.daycard>summary:hover{background:#fcfcfd}
details.daycard>summary .dt{flex:1 1 auto}
details.daycard[open]>summary{border-bottom:1px solid var(--line)}
.dbody{padding:16px 18px}

.daycard{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;margin:14px 0;box-shadow:0 1px 2px rgba(15,23,42,.03)}
.daycard .dh{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.daycard .dh h3{margin:0;font-size:18px}
.daycard .dh .pill{font-size:12px;font-weight:600;color:var(--muted);background:#f1f3f6;border-radius:999px;padding:4px 10px}
.dphoto{width:100%;height:210px;object-fit:cover;object-position:center 62%;border-radius:12px;display:block;margin-bottom:12px}
.dres{color:#374151;margin:0 0 12px}
.daycard h4{font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:14px 0 4px}
h2.sep{margin-top:44px}
.trad-top{display:block;margin:6px 0 12px}
#busca,#livre{display:inline-block;width:100%;max-width:520px;padding:11px 14px;border:1px solid var(--line);border-radius:10px;font:inherit;background:#fff;margin:0 8px 8px 0;vertical-align:middle}
#busca:focus,#livre:focus{outline:2px solid #cfe0ee;border-color:#9fc3e0}
.chipsf{display:block;margin-bottom:12px}
.chipf{display:inline-block;text-decoration:none;border:1px solid var(--line);background:#fff;color:var(--muted);font-size:12.5px;font-weight:600;padding:6px 12px;border-radius:999px;cursor:pointer;margin:0 6px 6px 0}
.chipf.on{background:var(--ink);color:#fff;border-color:var(--ink)}
table.trad td.zh{font-size:17px;font-weight:600;white-space:nowrap}
table.trad td.py{color:var(--muted);font-size:13px}
table.trad tbody tr{cursor:pointer}
table.trad tbody tr:hover td{background:#f4f8fb}
.livre{display:block;margin-top:14px}
.livre .btn{margin:0;cursor:pointer;border:0;font-family:inherit}
#overlay{position:fixed;inset:0;background:rgba(8,15,26,.94);color:#fff;display:none;align-items:center;justify-content:center;z-index:2000;padding:24px;text-align:center}
#overlay.on{display:flex}
#overlay .big{font-size:clamp(48px,14vw,120px);line-height:1.1;font-weight:700;letter-spacing:.02em}
#overlay .py{font-size:clamp(16px,3.4vw,24px);color:#9fc3e0;margin-top:14px}
#overlay .pt{font-size:clamp(14px,2.6vw,18px);color:#cbd5e1;margin-top:10px}
#overlay .fechar{position:absolute;top:18px;right:22px;font-size:26px;color:#fff;background:none;border:0;cursor:pointer}
.vazio{background:#fff;border:1px dashed #c9d2dc;border-radius:14px;padding:20px}
.vazio b{display:block;font-size:15px;margin-bottom:6px}
.vcard{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.vcard h3{margin:0 0 2px;font-size:16px}
@media(max-width:620px){
  .dphoto{height:170px}
  .cday{min-height:44px;font-size:11px;border-radius:8px}
  .calgrid{gap:3px}
  .cday.trip .cn{font-size:7.5px}
}
@media(min-width:700px){
  .cday.trip .cn-long{display:inline}
  .cday.trip .cn-short{display:none}
  .cday.trip .cn{font-size:8px}
  .cday{min-height:52px}
}
"""

EXTRA_JS = """
/* ---------- mala (checklist com memória) ---------- */
(function(){
  const KEY = 'mala_v1';
  const boxes = Array.from(document.querySelectorAll('.malacol input[type=checkbox]'));
  if (!boxes.length) return;
  let salvo = {};
  try { salvo = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(e) {}
  boxes.forEach(b => { if (salvo[b.id]) b.checked = true; });

  function atualiza(){
    const porCol = {};
    boxes.forEach(b => {
      const p = b.id.split('-')[0];
      porCol[p] = porCol[p] || [0, 0];
      porCol[p][1]++;
      if (b.checked) porCol[p][0]++;
    });
    document.querySelectorAll('[data-prog]').forEach(el => {
      const [n, t] = porCol[el.dataset.prog] || [0, 0];
      el.textContent = n + ' de ' + t + (n === t && t > 0 ? ' ✓' : '');
    });
    const n = boxes.filter(b => b.checked).length;
    const tot = document.getElementById('mala-total');
    if (tot) tot.textContent = n + ' de ' + boxes.length + ' itens marcados';
  }
  boxes.forEach(b => b.addEventListener('change', () => {
    salvo[b.id] = b.checked;
    try { localStorage.setItem(KEY, JSON.stringify(salvo)); } catch(e) {}
    atualiza();
  }));
  const rst = document.getElementById('mala-reset');
  if (rst) rst.addEventListener('click', ev => {
    ev.preventDefault();
    boxes.forEach(b => { b.checked = false; });
    salvo = {};
    try { localStorage.removeItem(KEY); } catch(e) {}
    atualiza();
  });
  atualiza();
})();

/* ---------- clima (Open-Meteo: atual + média histórica das datas) ---------- */
(function(){
  const alvos = Array.from(document.querySelectorAll('.clima'));
  if (!alvos.length) return;
  const cache = new Map();
  const TTL = 3 * 60 * 60 * 1000; // 3h
  const ICO = {0:'☀️',1:'🌤️',2:'⛅',3:'☁️',45:'🌫️',48:'🌫️',51:'🌦️',53:'🌦️',55:'🌧️',
               61:'🌧️',63:'🌧️',65:'🌧️',71:'🌨️',73:'🌨️',75:'❄️',77:'❄️',80:'🌦️',81:'🌧️',
               82:'⛈️',85:'🌨️',86:'🌨️',95:'⛈️',96:'⛈️',99:'⛈️'};

  function dentroDoIntervalo(md, d1, d2){
    return (d1 <= d2) ? (md >= d1 && md <= d2) : (md >= d1 || md <= d2);
  }
  function lerCache(chave){
    try {
      const bruto = localStorage.getItem('clima:' + chave);
      if (!bruto) return null;
      const o = JSON.parse(bruto);
      if (Date.now() - o.ts > TTL) return null;
      return o.dados;
    } catch(e) { return null; }
  }
  function gravarCache(chave, dados){
    try { localStorage.setItem('clima:' + chave, JSON.stringify({ts: Date.now(), dados})); } catch(e) {}
  }

  async function buscar(lat, lon, d1, d2){
    const chave = lat + ',' + lon + ',' + d1 + ',' + d2;
    if (cache.has(chave)) return cache.get(chave);
    const salvo = lerCache(chave);
    if (salvo) { cache.set(chave, salvo); return salvo; }

    const p = (async () => {
      const urlAtual = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lon +
                       '&current=temperature_2m,weather_code&timezone=auto';
      const urlHist  = 'https://archive-api.open-meteo.com/v1/archive?latitude=' + lat + '&longitude=' + lon +
                       '&start_date=2015-12-01&end_date=2025-01-31&daily=temperature_2m_max,temperature_2m_min&timezone=auto';
      const [atual, hist] = await Promise.all([
        fetch(urlAtual).then(r => r.json()).catch(() => null),
        fetch(urlHist).then(r => r.json()).catch(() => null)
      ]);
      let max = null, min = null, dias = 0;
      if (hist && hist.daily && hist.daily.time) {
        const t = hist.daily.time, mx = hist.daily.temperature_2m_max, mn = hist.daily.temperature_2m_min;
        let smx = 0, smn = 0, n = 0;
        for (let i = 0; i < t.length; i++) {
          const md = t[i].slice(5);
          if (dentroDoIntervalo(md, d1, d2) && mx[i] !== null && mn[i] !== null) { smx += mx[i]; smn += mn[i]; n++; }
        }
        if (n) { max = smx / n; min = smn / n; dias = Math.round(n / 10); }
      }
      const dados = {
        agora: (atual && atual.current) ? atual.current.temperature_2m : null,
        code: (atual && atual.current) ? atual.current.weather_code : null,
        max: max, min: min, dias: dias
      };
      gravarCache(chave, dados);
      return dados;
    })();
    cache.set(chave, p);
    return p;
  }

  function pintar(el, d){
    const r = v => Math.round(v);
    const partes = [];
    if (d.agora !== null && d.agora !== undefined) {
      partes.push('<span class="ico">' + (ICO[d.code] || '🌡️') + '</span><span>agora <b>' + r(d.agora) + ' °C</b></span>');
    }
    if (d.max !== null && d.min !== null) {
      partes.push('<span>na viagem: <b>máx ' + r(d.max) + ' °C</b> / <b>mín ' + r(d.min) + ' °C</b></span>');
      partes.push('<span class="src">média de 10 anos nas mesmas datas · Open-Meteo</span>');
    } else if (d.agora === null) {
      el.className = 'clima erro';
      el.textContent = 'clima indisponível (sem conexão com o Open-Meteo)';
      return;
    }
    el.innerHTML = partes.join('');
  }

  function carregar(el){
    if (el.dataset.carregado) return;
    el.dataset.carregado = '1';
    const [lat, lon, d1, d2] = el.dataset.clima.split(',');
    buscar(lat, lon, d1, d2).then(d => {
      if (d && (d.agora !== null || d.max !== null)) pintar(el, d);
      else { el.className = 'clima erro'; el.textContent = 'clima indisponível agora'; }
    }).catch(() => {
      el.className = 'clima erro'; el.textContent = 'clima indisponível agora';
    });
  }

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entradas => {
      entradas.forEach(e => { if (e.isIntersecting) { carregar(e.target); io.unobserve(e.target); } });
    }, {rootMargin: '250px'});
    alvos.forEach(el => io.observe(el));
  } else {
    alvos.forEach(carregar);
  }
})();

/* ---------- conversor de moeda ---------- */
(function(){
  const el = id => document.getElementById(id);
  const cny = el('cny'), brl = el('brl'), rt = el('rate'), src = el('rate-src'), bt = el('rate-refresh');
  if (!cny || !brl) return;
  let taxa = 0.776;
  let origem = 'referência fixa de 05/10/2026';

  function pintar(){
    brl.value = (parseFloat(cny.value || '0') * taxa).toFixed(2);
    rt.textContent = '1 ¥ = R$ ' + taxa.toFixed(4) + '   ·   R$ 1 = ' + (1/taxa).toFixed(2) + ' ¥';
    src.textContent = origem;
    pintaRef();
  }
  async function atualizar(){
    src.textContent = 'buscando cotação…';
    try {
      const r = await fetch('https://open.er-api.com/v6/latest/CNY', {cache:'no-store'});
      const j = await r.json();
      if (j && j.rates && j.rates.BRL) {
        taxa = j.rates.BRL;
        origem = 'open.er-api.com · atualizado em ' + (j.time_last_update_utc || '').replace(' 00:00:01 +0000','');
        pintar(); return;
      }
    } catch (e) {}
    try {
      const r2 = await fetch('https://api.frankfurter.app/latest?from=CNY&to=BRL', {cache:'no-store'});
      const j2 = await r2.json();
      if (j2 && j2.rates && j2.rates.BRL) {
        taxa = j2.rates.BRL;
        origem = 'frankfurter.app (BCE) · ' + j2.date;
        pintar(); return;
      }
    } catch (e) {}
    origem = 'referência fixa de 05/10/2026 (sem conexão com as APIs)';
    pintar();
  }
  cny.addEventListener('input', pintar);
  brl.addEventListener('input', () => {
    const v = parseFloat(brl.value || '0');
    cny.value = (v / taxa).toFixed(2);
    rt.textContent = '1 ¥ = R$ ' + taxa.toFixed(4) + '   ·   R$ 1 = ' + (1/taxa).toFixed(2) + ' ¥';
  });
  if (bt) bt.addEventListener('click', ev => { ev.preventDefault(); atualizar(); });

  /* atalhos de valor e tabela de referência */
  function pintaRef(){
    const par = (a, b) => 'R$ ' + (a*taxa).toFixed(0) + ' – ' + (b*taxa).toFixed(0);
    const m = (id, txt) => { const e = document.getElementById(id); if (e) e.textContent = txt; };
    m('ref1', par(3, 7)); m('ref2', par(25, 50)); m('ref3', par(50, 150));
    m('ref4', par(150, 450)); m('ref5', par(400, 800));
  }
  document.querySelectorAll('[data-cny]').forEach(ch => ch.addEventListener('click', ev => {
    ev.preventDefault();
    cny.value = ch.dataset.cny;
    pintar();
  }));
  pintar();
  atualizar();
})();

/* ---------- menu hambúrguer ---------- */
(function(){
  const burger = document.getElementById('burger');
  const drawer = document.getElementById('drawer');
  const scrim  = document.getElementById('scrim');
  const closeB = document.getElementById('dclose');
  function abrir(){ drawer.classList.add('on'); scrim.classList.add('on'); burger.setAttribute('aria-expanded','true'); drawer.setAttribute('aria-hidden','false'); }
  function fechar(){ drawer.classList.remove('on'); scrim.classList.remove('on'); burger.setAttribute('aria-expanded','false'); drawer.setAttribute('aria-hidden','true'); }
  if (burger) burger.addEventListener('click', () => drawer.classList.contains('on') ? fechar() : abrir());
  if (closeB) closeB.addEventListener('click', fechar);
  if (scrim)  scrim.addEventListener('click', fechar);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') fechar(); });
  document.querySelectorAll('.drawer nav a, .brand').forEach(a => a.addEventListener('click', fechar));
})();

/* ---------- calendário ---------- */
(function(){
  const CID = {
    pequim:['Pequim','PEQ','#12263a'], datong:['Datong','DAT','#4b5d6e'], pingyao:['Pingyao','PIN','#b3402a'],
    xian:["Xi'an",'XIA','#b5741f'], chongqing:['Chongqing','CQ','#0f766e'], changsha:['Changsha','CS','#c2410c'],
    zhangjiajie:['Zhangjiajie','ZJJ','#2f6b4f'], guilin:['Guilin','GUI','#1f6f8b'], xangai:['Xangai','XAN','#3730a3'],
    hangzhou:['Hangzhou','HZH','#15803d'], huangshan:['Huangshan','HS','#7a4b2a'], nanjing:['Nanjing','NJ','#6b21a8']
  };
  const CEN = {
    A:[[ '2026-12-30','2027-01-06','pequim'],['2027-01-06','2027-01-08','datong'],['2027-01-08','2027-01-10','pingyao'],
       ['2027-01-10','2027-01-13','xian'],['2027-01-13','2027-01-15','chongqing'],['2027-01-15','2027-01-18','zhangjiajie'],
       ['2027-01-18','2027-01-20','changsha'],['2027-01-20','2027-01-23','xangai'],['2027-01-23','2027-01-24','hangzhou'],
       ['2027-01-24','2027-01-25','nanjing'],['2027-01-25','2027-01-26','pequim']],
    B:[[ '2026-12-30','2027-01-06','pequim'],['2027-01-06','2027-01-08','datong'],['2027-01-08','2027-01-10','pingyao'],
       ['2027-01-10','2027-01-13','xian'],['2027-01-13','2027-01-15','chongqing'],['2027-01-15','2027-01-17','changsha'],
       ['2027-01-17','2027-01-20','guilin'],['2027-01-20','2027-01-23','xangai'],['2027-01-23','2027-01-24','hangzhou'],
       ['2027-01-24','2027-01-25','nanjing'],['2027-01-25','2027-01-26','pequim']],
    C:[[ '2026-12-30','2027-01-06','pequim'],['2027-01-06','2027-01-08','datong'],['2027-01-08','2027-01-10','pingyao'],
       ['2027-01-10','2027-01-13','xian'],['2027-01-13','2027-01-15','chongqing'],['2027-01-15','2027-01-17','changsha'],
       ['2027-01-17','2027-01-22','xangai'],['2027-01-22','2027-01-23','hangzhou'],['2027-01-23','2027-01-24','huangshan'],
       ['2027-01-24','2027-01-25','nanjing'],['2027-01-25','2027-01-26','pequim']]
  };
  const MESES = [[2026,11,'Dezembro 2026'],[2027,0,'Janeiro 2027']];
  const WD = ['D','S','T','Q','Q','S','S'];
  const iso = d => d.toISOString().slice(0,10);
  function cidade(isoStr, cen){
    for (const [ini, fim, cid] of CEN[cen]) { if (isoStr >= ini && isoStr < fim) return cid; }
    return null;
  }
  function render(cen){
    const alvo = document.getElementById('cal');
    if (!alvo) return;
    let html = '<div class="calwrap">';
    MESES.forEach(([ano, mes, nome]) => {
      const primeiro = new Date(Date.UTC(ano, mes, 1));
      const dias = new Date(Date.UTC(ano, mes + 1, 0)).getUTCDate();
      html += '<div class="cal"><h4>' + nome + '</h4><div class="calgrid">';
      html += WD.map(w => '<div class="wd">' + w + '</div>').join('');
      for (let i = 0; i < primeiro.getUTCDay(); i++) html += '<div class="cday blank"></div>';
      for (let d = 1; d <= dias; d++) {
        const atual = iso(new Date(Date.UTC(ano, mes, d)));
        const cid = cidade(atual, cen);
        if (cid) {
          const [nomeCid, sigla, cor] = CID[cid];
          html += '<div class="cday trip" style="background:' + cor + '" data-cid="' + cid + '" title="' + nomeCid + '">'
                + d + '<span class="cn cn-long">' + nomeCid + '</span>'
                + '<span class="cn cn-short">' + sigla + '</span></div>';
        } else {
          html += '<div class="cday notrip">' + d + '</div>';
        }
      }
      html += '</div></div>';
    });
    html += '</div>';
    alvo.innerHTML = html;
    alvo.querySelectorAll('.cday.trip').forEach(el => el.addEventListener('click', () => {
      const d = document.getElementById('dia-' + indiceCidade(el.dataset.cid));
      if (d) { d.open = true; d.scrollIntoView({behavior:'smooth', block:'start'}); }
    }));
    // legenda
    const usadas = new Map();
    CEN[cen].forEach(([, , cid]) => { if (!usadas.has(cid)) usadas.set(cid, CID[cid]); });
    const leg = document.getElementById('calleg');
    if (leg) leg.innerHTML = Array.from(usadas.entries())
      .map(([cid, [nome, sigla, cor]]) => '<span><i style="background:' + cor + '"></i>' + nome + '</span>').join('');
  }
  const ORDEM = ['pequim','datong','pingyao','xian','chongqing','zhangjiajie','guilin','changsha','xangai','hangzhou','huangshan','nanjing','pequim'];
  function indiceCidade(cid){
    // mapeia id da cidade para o índice do cartão (0..4 comuns, 100+ variantes, 200+ finais)
    const comuns = ['pequim','datong','pingyao','xian','chongqing'];
    if (comuns.indexOf(cid) >= 0) return comuns.indexOf(cid);
    const varA = {zhangjiajie:100}, varB = {guilin:101}, varC = {huangshan:102};
    if (cid === 'zhangjiajie') return 100;
    if (cid === 'guilin') return 101;
    if (cid === 'huangshan') return 102;
    if (cid === 'changsha') return 200;
    if (cid === 'xangai') return 201;
    if (cid === 'hangzhou') return 202;
    if (cid === 'nanjing') return 203;
    return 0;
  }
  document.querySelectorAll('[data-scen]').forEach(b => b.addEventListener('click', ev => {
    ev.preventDefault();
    document.querySelectorAll('[data-scen]').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
    render(b.dataset.scen);
  }));
  render('A');
})();

(function(){
  const overlay = document.createElement('div');
  overlay.id = 'overlay';
  overlay.innerHTML = '<button class="fechar" aria-label="fechar">&times;</button><div><div class="big"></div><div class="py"></div><div class="pt"></div></div>';
  document.body.appendChild(overlay);
  overlay.addEventListener('click', () => overlay.classList.remove('on'));

  document.querySelectorAll('table.trad tbody tr').forEach(tr => {
    tr.addEventListener('click', () => {
      overlay.querySelector('.big').textContent = tr.dataset.zh;
      overlay.querySelector('.py').textContent = tr.dataset.py;
      overlay.querySelector('.pt').textContent = tr.dataset.pt;
      overlay.classList.add('on');
    });
  });

  const busca = document.getElementById('busca');
  const chipEls = document.querySelectorAll('.chipf');
  let catAtiva = null;
  function filtrar(){
    const q = (busca.value || '').toLowerCase().trim();
    document.querySelectorAll('table.trad tbody tr').forEach(tr => {
      const okTexto = !q || tr.dataset.busca.includes(q);
      const okCat = !catAtiva || tr.dataset.cat === catAtiva;
      tr.style.display = (okTexto && okCat) ? '' : 'none';
    });
  }
  if (busca) busca.addEventListener('input', filtrar);
  chipEls.forEach(b => b.addEventListener('click', (ev) => {
    ev.preventDefault();
    const c = b.dataset.cat;
    catAtiva = (catAtiva === c) ? null : c;
    chipEls.forEach(x => x.classList.toggle('on', x.dataset.cat === catAtiva));
    filtrar();
  }));

  const btn = document.getElementById('btn-livre');
  if (btn) btn.addEventListener('click', (ev) => {
    ev.preventDefault();
    const t = document.getElementById('livre').value.trim();
    const url = 'https://translate.google.com/?sl=pt&tl=zh-CN&text=' + encodeURIComponent(t) + '&op=translate';
    window.open(url, '_blank');
  });
})();
"""

spec = importlib.util.spec_from_file_location("bg", os.path.join(BASE, "src", "build_guia.py"))
bg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bg)

CIDADES = bg.CIDADES
DATA_IN, DATA_OUT = bg.DATA_IN, bg.DATA_OUT
svg_schema = bg.svg_schema
gmaps = bg.gmaps



CLIMA = {
    "pequim":     (39.9042, 116.4074, "12-30", "01-06"),
    "datong":     (40.0900, 113.3000, "01-06", "01-08"),
    "pingyao":    (37.2000, 112.1800, "01-08", "01-10"),
    "xian":       (34.3416, 108.9398, "01-10", "01-13"),
    "chongqing":  (29.5630, 106.5516, "01-13", "01-15"),
    "changsha":   (28.2282, 112.9388, "01-18", "01-20"),
    "xangai":     (31.2304, 121.4737, "01-20", "01-23"),
    "hangzhou":   (30.2741, 120.1551, "01-23", "01-24"),
    "nanjing":    (32.0603, 118.7969, "01-24", "01-25"),
    "zhangjiajie":(29.1170, 110.4790, "01-15", "01-18"),
    "guilin":     (25.2736, 110.2900, "01-17", "01-20"),
    "huangshan":  (30.1340, 118.1610, "01-23", "01-24"),
}

def norm_id(titulo):
    import unicodedata, re as _re
    t = _re.sub(r"[^A-Za-zÀ-ÿ /]", "", titulo).split("/")[0].strip().lower()
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = t.replace(" ", "").replace("'", "")
    # variantes e fechamento
    if "opcaoazhangjiajie" in t or "zhangjiajie" in t: return "zhangjiajie"
    if "guilin" in t or "yangshuo" in t: return "guilin"
    if "huangshan" in t: return "huangshan"
    if t.startswith("pequim"): return "pequim"
    mapa = {"pequim":"pequim","datong":"datong","pingyao":"pingyao","xian":"xian",
            "chongqing":"chongqing","changsha":"changsha","xangai":"xangai",
            "hangzhou":"hangzhou","nanjing":"nanjing","zhangjiajie":"zhangjiajie",
            "guilin":"guilin","huangshan":"huangshan"}
    return mapa.get(t, t)

def clima_div(cid):
    if cid not in CLIMA:
        return ""
    lat, lon, d1, d2 = CLIMA[cid]
    return f'<div class="clima" data-clima="{lat},{lon},{d1},{d2}">carregando clima…</div>'


MALA = {
  "Masculino": [
    ("Camadas de baixo", [("3 camisetas segunda pele manga longa",1),("1 camiseta manga curta (dentro de hotel)",1),
                          ("3 cuecas boxer (merino ou sintético)",1),("2 meias finas",1),("2 meias de lã grossa",1)]),
    ("Camada do meio", [("1 fleece ou pluma fina",1),("1 camisa social leve",1),("2 camisetas para jantar",1)]),
    ("Casaco", [("1 parka de pluma com capuz e capa impermeável",1)]),
    ("Pernas", [("1 calça softshell ou impermeável",1),("1 jeans escuro",1),("1 calça de moletom (voo e dormir)",1)]),
    ("Extremidades", [("Luvas touchscreen",1),("1 par de luvas grossas",1),("Gorro de lã",1),("Buff / cachecol",1)]),
    ("Pés", [("Bota impermeável de cano médio",1),("Tênis leve",1),("Chinelo",1)]),
    ("Extra", [("Sunga (o Ascott tem piscina)",1),("Pijama leve",1)]),
  ],
  "Feminino": [
    ("Camadas de baixo", [("2 segunda pele manga longa",1),("1 segunda pele manga curta",1),
                          ("3 leggings térmicas",1),("2 sutiãs esportivos + 1 normal",1),
                          ("2 meias finas",1),("2 meias de lã grossa",1),("1 meia-calça grossa",1)]),
    ("Camada do meio", [("1 fleece fino",1),("2 blusas de lã fina",1),("1 vestido ou conjunto para jantar",1)]),
    ("Casaco", [("1 parka de pluma longa com capuz",1)]),
    ("Pernas", [("1 calça impermeável",1),("1 jeans",1),("1 calça de moletom",1)]),
    ("Extremidades", [("Luvas",1),("Luvas internas finas",1),("Gorro",1),("Lenço grande que serve de xale",1)]),
    ("Pés", [("Bota impermeável de cano médio",1),("Sapatilha ou tênis",1),("Chinelo",1)]),
    ("Extra", [("Maiô (piscina do hotel)",1),("Nécessaire enxuto",1)]),
  ],
  "Comum aos quatro": [
    ("Documentos", [("Passaporte + cópia digital",1),("Seguro viagem contratado",1),("Reservas salvas offline",1)]),
    ("Saúde e pele", [("Remédios de uso próprio com receita",1),("Hidratante labial",1),
                      ("Hidratante corporal (ar seco do aquecimento)",1),("Protetor solar",1),("Analgésico",1)]),
    ("Tecnologia", [("Adaptador tipo A/I",1),("Power bank",1),("Carregadores",1),("Fone",1)]),
    ("Dia a dia", [("Saco de lavanderia",1),("Sabão de barra para lavar à mão",1),
                   ("Garrafa térmica pequena",1),("Máscara PFF2 (poluição em janeiro)",1)]),
    ("Comprar na China", [("Segunda pele Heattech (Uniqlo)",1),("Pluma / parka",1),
                          ("Luvas, gorro e cachecol",1),("Crampon, se forem de Huangshan",1)]),
  ],
}


DECA = [
    ("Segunda pele (parte de cima)", "/roupas/superiores/segunda-pele",
     "Gramatura 150–200 g/m²; poliéster ou merino, nunca algodão"),
    ("Segunda pele (parte de baixo)", "/roupas/inferiores/segunda-pele",
     "Legging térmica fina, para usar sob a calça"),
    ("Fleece / polar", "/roupas/superiores/agasalhos-e-fleeces",
     "Perto de 200 g/m², com zíper no peito"),
    ("Doudoune / jaqueta de pluma", "/roupas/superiores/jaquetas",
     "Veja a temperatura de conforto na descrição do produto"),
    ("Parka / capa corta-vento", "/roupas/superiores/capas-de-chuva",
     "Impermeável, sem isolamento, folgada para caber as camadas"),
    ("Calça impermeável / softshell", "/roupas/inferiores/calcas-e-leggings",
     "Que não faça barulho de plástico e vista sobre a segunda pele"),
    ("Bota impermeável", "/calcados/calcados/botas",
     "Cano médio, solado com cravos, meio número acima"),
    ("Meias", "/calcados/meias/meias",
     "Lã merino ou sintética; uma grossa e uma fina"),
    ("Luvas", "/acessorios/trajes/luvas",
     "Par fino touchscreen + par impermeável"),
    ("Gorro", "/acessorios/trajes/gorros",
     "Que cubra a orelha"),
    ("Cachecol", "/acessorios/trajes/cachecois",
     "Grande o bastante para virar xale"),
]

COMPRAS = [
    ("Segunda pele (Heattech)", "China · ¥99–149 na Uniqlo",
     "No Brasil em dezembro é fora de estação e custa R$ 150+",
     [("Uniqlo China", "https://www.uniqlo.cn/")]),
    ("Pluma / parka", "China · Bosideng ou Uniqlo",
     "Estoque de inverno pleno; aqui seria caro e escasso",
     [("Bosideng", "https://www.bosideng.com/"), ("Uniqlo China", "https://www.uniqlo.cn/")]),
    ("Bota impermeável", "Brasil · Decathlon",
     "Pé brasileiro é mais largo que a forma chinesa; numeração acima de 44 é rara lá",
     [("Decathlon · botas", "https://www.decathlon.com.br/calcados/calcados/botas")]),
    ("Luvas, gorro, cachecol", "China · ¥20–60",
     "Você escolhe a espessura vendo",
     [("Taobao", "https://www.taobao.com/"), ("Uniqlo China", "https://www.uniqlo.cn/")]),
    ("Crampon (microspike)", "China · ¥30–50",
     "Só se Huangshan entrar no roteiro",
     [("Taobao", "https://www.taobao.com/")]),
    ("Meias de lã", "Brasil · Decathlon",
     "As chinesas são finas demais",
     [("Decathlon · meias", "https://www.decathlon.com.br/calcados/meias/meias")]),
]
def b64(nome, largura=900, qualidade=70):
    im = Image.open(os.path.join(IMG, nome)).convert("RGB")
    if im.width > largura:
        im = im.resize((largura, int(im.height * largura / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=qualidade, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


TRENS = [
    ("Pequim → Datong", "06/01", "1h45", "~21/12/2026"),
    ("Datong → Pingyao", "08/01", "3h", "~24/12/2026"),
    ("Pingyao → Xi'an", "10/01", "3h", "~26/12/2026"),
    ("Xi'an → Chongqing", "13/01", "5h", "~29/12/2026"),
    ("Chongqing → bloco de natureza", "15/01", "~3h (linha nova)", "~01/01/2027"),
    ("Changsha → Xangai", "20/01", "4h30", "~05/01/2027"),
    ("Xangai → Hangzhou", "23/01", "1h", "~08/01/2027"),
    ("Nanjing → Pequim", "25/01", "3h30", "~10/01/2027"),
]

CSS = """
:root{
  --ink:#0b1220; --ink-2:#1f2937; --muted:#64748b; --line:#e6e8ec;
  --bg:#f6f7f9; --surface:#fff; --accent:#e2562b; --accent-soft:#fff1ec;
  --teal:#0f766e; --green:#2f6b4f; --brown:#7a4b2a; --radius:18px;
  --shadow:0 1px 2px rgba(15,23,42,.04),0 8px 24px -12px rgba(15,23,42,.18);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-size:15.5px;line-height:1.6;-webkit-font-smoothing:antialiased}
img{max-width:100%}
.wrap{max-width:1140px;margin:0 auto;padding:0 20px}

/* ---------- hero ---------- */
.hero{position:relative;height:clamp(280px,52vh,520px);display:flex;align-items:flex-end;overflow:hidden}
.hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,15,26,.15) 0%,rgba(8,15,26,.05) 45%,rgba(8,15,26,.72) 100%)}
.hero .cap-hero{position:relative;z-index:2;color:#fff;padding:0 0 26px}
.hero h1{font-size:clamp(30px,6vw,58px);line-height:1.02;margin:0;font-weight:800;letter-spacing:-.02em;text-shadow:0 2px 24px rgba(0,0,0,.35)}
.hero .sub{font-size:clamp(13px,1.6vw,16px);color:rgba(255,255,255,.9);margin-top:8px;font-weight:500}
.credit{position:absolute;right:12px;bottom:8px;z-index:3;font-size:10.5px;color:rgba(255,255,255,.75)}

/* ---------- nav ---------- */
.navwrap{position:sticky;top:0;z-index:800;background:rgba(255,255,255,.88);
  backdrop-filter:saturate(1.4) blur(12px);border-bottom:1px solid var(--line)}
nav.tabs{display:block;padding:10px 0}
nav.tabs::-webkit-scrollbar{display:none}
nav.tabs a{display:inline-block;text-decoration:none;background:transparent;color:var(--muted);font-weight:600;
  font-size:14px;padding:9px 15px;border-radius:999px;cursor:pointer;transition:.18s;white-space:nowrap;margin:0 6px 6px 0}
nav.tabs a:hover{background:#f1f3f6;color:var(--ink)}
nav.tabs a[aria-selected="true"]{background:var(--ink);color:#fff}

/* ---------- tipografia ---------- */
h2{font-size:clamp(21px,3vw,29px);letter-spacing:-.02em;margin:38px 0 6px;font-weight:800}
h2:first-of-type{margin-top:26px}
.sub{display:block;font-size:14px;font-weight:400;color:var(--muted);margin-top:6px;letter-spacing:0}
h3{font-size:15.5px;margin:20px 0 6px;font-weight:700}
p{margin:0 0 14px}
.fine{font-size:12px;color:var(--muted)}
section[role=tabpanel]{display:none;padding:26px 0 70px}
section[role=tabpanel].on{display:block}

/* ---------- mapa ---------- */
#map{height:470px;border-radius:var(--radius);border:1px solid var(--line);box-shadow:var(--shadow);z-index:0}
.leaflet-popup-content{font-size:13px}

/* ---------- cards / sanfona ---------- */
details{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);margin:10px 0;
  box-shadow:0 1px 2px rgba(15,23,42,.03);overflow:hidden}
details summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:12px;padding:16px 18px;
  font-weight:700;font-size:16px}
details summary::-webkit-details-marker{display:none}
details summary:hover{background:#fcfcfd}
details[open] summary{border-bottom:1px solid var(--line)}
.pill{font-size:12px;font-weight:600;color:var(--muted);background:#f1f3f6;border-radius:999px;padding:4px 10px;white-space:nowrap}
.chev{margin-left:auto;color:#9aa1ab;font-size:12px;transition:transform .18s}
details[open] .chev{transform:rotate(90deg)}
details .inner{padding:18px}
details img.photo{width:100%;height:220px;object-fit:cover;object-position:center 60%;border-radius:12px;display:block}
figure{margin:0}
figcaption{font-size:11.5px;color:var(--muted);margin-top:6px}

/* ---------- tabelas ---------- */
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:14px;margin:12px 0;background:var(--surface)}
.tw table{min-width:620px}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{background:#f8f9fb;text-align:left;padding:10px 12px;font-size:11.5px;letter-spacing:.04em;
  text-transform:uppercase;color:var(--muted);font-weight:700;border-bottom:1px solid var(--line)}
td{padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover td{background:#fcfcfd}
.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}

/* ---------- inputs de valor ---------- */
input.money{width:110px;padding:7px 9px;border:1px solid var(--line);border-radius:9px;font:inherit;
  font-size:13.5px;text-align:right;background:#fff;color:var(--ink)}
input.money:focus{outline:2px solid #cfe0ee;border-color:#9fc3e0}
input.qty{width:62px;padding:7px 9px;border:1px solid var(--line);border-radius:9px;font:inherit;
  font-size:13.5px;text-align:center;background:#fff}
.subtotal{font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.perperson{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
.totbar{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;
  background:var(--ink);color:#fff;border-radius:14px;padding:14px 18px;margin:14px 0 4px}
.totbar b{font-size:17px;font-variant-numeric:tabular-nums}
.totbar .lbl{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#9fb3c8}
.hint{background:var(--accent-soft);border-left:3px solid var(--accent);border-radius:10px;padding:10px 14px;font-size:13px;margin:10px 0}

/* ---------- diversos ---------- */
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 18px;box-shadow:0 1px 2px rgba(15,23,42,.03)}
.card b{display:block;font-size:14.5px;margin-bottom:2px}
.card span{font-size:13px;color:var(--muted)}
a{color:#0b5f86}
a.btn{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;padding:10px 16px;
  border-radius:10px;font-size:13.5px;font-weight:600;margin:8px 8px 0 0;transition:.18s}
a.btn:hover{transform:translateY(-1px)}
a.btn.ghost{background:#fff;color:var(--ink);border:1px solid var(--line)}
ul.tight{margin:8px 0 12px;padding-left:20px;font-size:14px}
ul.tight li{margin:6px 0}
.tag{display:inline-block;font-size:11.5px;background:#f1f3f6;color:#37414d;border-radius:999px;padding:3px 9px;margin:0 4px 4px 0}
footer{margin-top:44px;padding:26px 0 40px;border-top:1px solid var(--line);font-size:11.5px;color:var(--muted)}
@media(max-width:620px){
  body{font-size:15px}
  #map{height:360px}
  details img.photo{height:180px}
  .tw table{min-width:520px}
  input.money{width:92px}
}
"""

JS = """
const fmt = n => (n||0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
const $ = id => document.getElementById(id);
const KEY = 'china_guia_valores_v1';

function travelers(){
  const v = parseInt($('travelers')?.value || '4', 10);
  return Number.isFinite(v) && v > 0 ? v : 4;
}

function recalc(){
  const n = travelers();
  const totais = {aereo:0, trens:0, hoteis:0};
  document.querySelectorAll('input.money').forEach(inp => {
    const unit = parseFloat(inp.value) || 0;   // inputs são type=number
    const tab = inp.dataset.tab || 'hoteis';
    let sub = unit;
    if (inp.dataset.mode === 'travelers') sub = unit * n;
    if (inp.dataset.mode === 'nights') sub = unit * (+inp.dataset.nights || 1) * (+inp.dataset.rooms || 1);
    const cel = $('sub-' + inp.dataset.id);
    if (cel) cel.textContent = fmt(sub);
    const per = $('per-' + inp.dataset.id);
    if (per) per.textContent = 'R$ ' + (sub / n).toLocaleString('pt-BR',{minimumFractionDigits:2, maximumFractionDigits:2}) + ' /pessoa';
    totais[tab] = (totais[tab] || 0) + sub;
  });
  ['tot-aereo','tot-aereo2'].forEach(id => { if ($(id)) $(id).textContent = fmt(totais.aereo); });
  ['tot-trens','tot-trens2'].forEach(id => { if ($(id)) $(id).textContent = fmt(totais.trens); });
  ['tot-hoteis','tot-hoteis2'].forEach(id => { if ($(id)) $(id).textContent = fmt(totais.hoteis); });
  const geral = totais.aereo + totais.trens + totais.hoteis;
  if ($('tot-geral')) $('tot-geral').textContent = fmt(geral);
  if ($('tot-geral-pessoa')) $('tot-geral-pessoa').textContent = fmt(geral / n) + ' por pessoa';
  save();
}

function save(){
  const dados = {};
  document.querySelectorAll('input.money, input.qty').forEach(i => { if (i.id) dados[i.id] = i.value; });
  try { localStorage.setItem(KEY, JSON.stringify(dados)); } catch(e) {}
}
function load(){
  try {
    const dados = JSON.parse(localStorage.getItem(KEY) || '{}');
    Object.entries(dados).forEach(([id, v]) => { const el = $(id); if (el) el.value = v; });
  } catch(e) {}
}

document.addEventListener('DOMContentLoaded', () => {
  load();
  document.querySelectorAll('input.money, input.qty').forEach(i => i.addEventListener('input', recalc));
  if ($('travelers')) $('travelers').addEventListener('input', recalc);
  recalc();
});
"""


def money_input(id_, tab, mode="travelers", nights=None, rooms=None, placeholder="0,00"):
    extra = ""
    if nights is not None:
        extra += f' data-nights="{nights}"'
    if rooms is not None:
        extra += f' data-rooms="{rooms}"'
    return (f'<input class="money" id="in-{id_}" data-id="{id_}" data-tab="{tab}" data-mode="{mode}"{extra} '
            f'type="number" min="0" step="0.01" inputmode="decimal" placeholder="{placeholder}">')



def html_mala():
    out = []
    for coluna, grupos in MALA.items():
        total = sum(len(itens) for _, itens in grupos)
        prefixo = {"Masculino": "m", "Feminino": "f"}.get(coluna, "c")
        blocos = []
        for gi, (grupo, itens) in enumerate(grupos):
            lis = "".join(
                f'<label class="item"><input type="checkbox" id="{prefixo}-{gi}-{ii}">'
                f'<span>{texto}</span></label>' for ii, (texto, _) in enumerate(itens))
            blocos.append(f'<div class="mgrupo"><h4>{grupo}</h4>{lis}</div>')
        out.append(f"""<div class="malacol">
      <div class="mhead"><h3>{coluna}</h3><span class="prog" data-prog="{prefixo}">0 de {total}</span></div>
      {''.join(blocos)}
    </div>""")
    return "".join(out)


def html_deca():
    linhas = []
    for peca, path, olhar in DECA:
        url = "https://www.decathlon.com.br" + path
        linhas.append(f"<tr><td><b>{peca}</b></td>"
                      f"<td class='lk'><a class='btn ghost mini' href='{url}' target='_blank' rel='noopener'>Decathlon</a></td>"
                      f"<td class='fine'>{olhar}</td></tr>")
    return "".join(linhas)

def html_compras():
    linhas = []
    for item, onde, porque, links in COMPRAS:
        ls = " ".join(f'<a class="btn ghost mini" href="{u}" target="_blank" rel="noopener">{t}</a>'
                      for t, u in links)
        linhas.append(f"<tr><td><b>{item}</b></td><td>{onde}</td>"
                      f"<td class='fine'>{porque}</td><td class='lk'>{ls}</td></tr>")
    return "".join(linhas)

def main():
    imgs = {c["id"]: b64(c["img"]) for c in CIDADES}
    hero = b64("muralha_inverno.jpg", largura=1700, qualidade=76)
    credito = json.load(open(os.path.join(IMG, "credito_hero.json"), encoding="utf-8"))

    # ---------- sanfona de cidades
    blocos = []
    for c in CIDADES:
        atr = "".join(
            f"<tr><td><b>{n}</b><br><span class='fine'>{obs}</span></td><td>{t}</td><td>{p}</td>"
            f"<td><a href='{gmaps(g)}' target='_blank' rel='noopener'>mapa</a></td></tr>"
            for n, t, p, obs, g in c["atracoes"])

        # hospedagem sugerida + campo de valor
        if c["hoteis"]:
            lista_html = "".join(f"<li><b>{n}</b> — {r} · <span class='fine'>{o}</span></li>" for n, r, o in c["hoteis"])
        else:
            dados = json.load(open(os.path.join(DATA, "hoteis_cidades.json"), encoding="utf-8"))
            chave = "Guilin" if "Guilin" in c["nome"] else c["nome"]
            lista_html = "".join(
                f"<li><b>{h['nome']}</b> — {h['estrelas']}★ · {h['nota']} ({h['avaliacoes']} avaliações)</li>"
                for h in bg.top3(dados.get(chave, []))) or "<li class='fine'>Ver no Booking.</li>"

        dicas = "".join(f"<li>{d}</li>" for d in c["dicas"])
        cid = c["id"]
        blocos.append(f"""
  <details id="city-{cid}">
    <summary>{c['emoji']} {c['nome']}<span class="pill">{c['noites']} noites · {c['datas']}</span><span class="chev">▶</span></summary>
    <div class="inner">
      <figure>
        <img class="photo" src="{imgs[cid]}" alt="{c['nome']}">
        <figcaption>{c['cap']} · Wikimedia Commons</figcaption>
      </figure>
      {clima_div(cid)}
      <p style="margin-top:14px">{c['resumo']}</p>

      <h3>O que fazer</h3>
      <div class="tw"><table><thead><tr><th>Atração</th><th>Tempo</th><th>Ingresso</th><th></th></tr></thead>
      <tbody>{atr}</tbody></table></div>

      <h3>Onde dormir</h3>
      <ul class="tight">{lista_html}</ul>

      <p class="fine">Valor da hospedagem e rateio por pessoa: na aba <b>Hospedagens</b>.</p>

      <h3>Programação e dicas</h3>
      <ul class="tight">{dicas}</ul>

      <a class="btn" href="https://www.booking.com/searchresults.pt-br.html?ss={c['nome'].replace(' ', '+')}%2C+China&checkin={DATA_IN[cid]}&checkout={DATA_OUT[cid]}&group_adults=4&no_rooms=2" target="_blank" rel="noopener">Ver hospedagem</a>
      <a class="btn ghost" href="{gmaps(c['nome'] + ' China')}" target="_blank" rel="noopener">No mapa</a>
    </div>
  </details>""")

    # ---------- trens com valores
    linhas_trem = []
    for i, (trecho, data, dur, venda) in enumerate(TRENS, start=1):
        rid = f"trem{i}"
        linhas_trem.append(f"""<tr>
          <td><b>{trecho}</b><br><span class="fine">venda abre {venda}</span></td>
          <td>{data}</td><td>{dur}</td>
          <td>{money_input(rid, 'trens', 'travelers')}</td>
          <td class="num subtotal" id="sub-{rid}">R$ 0,00</td>
          <td class="num perperson" id="per-{rid}">—</td>
        </tr>""")

    pontos_json = json.dumps([{k: c[k] for k in ("id", "nome", "lat", "lon", "noites", "datas", "emoji")}
                              for c in CIDADES], ensure_ascii=False)

    # ---------- roteiro dia a dia (enriquecido) ----------
    import conteudo
    DIA, DIA_VARIANTES, DIA_FINAL = conteudo.dados_dia()
    FRASES = conteudo.tradutor_dados()

    def bloco_dia(b, idx):
        linhas = "".join(
            f"<tr><td><b>{d}</b></td><td>{m}</td><td>{t}</td><td class='fine'>{o}</td></tr>"
            for d, m, t, o in b["dias"])
        dicas = "".join(f"<li>{x}</li>" for x in b["dicas"])
        return f"""  <details class="daycard" id="dia-{idx}">
    <summary><span class="dt">{b['titulo']}</span><span class="pill">{b['subt']}</span><span class="chev">▶</span></summary>
    <div class="dbody">
    <img class="dphoto" src="{b64(b['img'], 640, 62)}" alt="{b['titulo']}">
    {clima_div(norm_id(b['titulo']))}
    <p class="dres">{b['resumo']}</p>
    <div class="tw"><table>
      <thead><tr><th>Dia</th><th>Manhã</th><th>Tarde</th><th>Noite / observação</th></tr></thead>
      <tbody>{linhas}</tbody>
    </table></div>
    <h4>Dicas</h4>
    <ul class="tight">{dicas}</ul>
    </div>
  </details>
"""

    blocos_dia = "".join(bloco_dia(b, i) for i, b in enumerate(DIA))
    blocos_dia += '  <h2 class="sep">O bloco de natureza<span class="sub">Escolha uma das três: a rotina de cada uma, dia a dia.</span></h2>\n'
    blocos_dia += "".join(bloco_dia(b, 100 + i) for i, b in enumerate(DIA_VARIANTES))
    blocos_dia += '  <h2 class="sep">O fim da viagem<span class="sub">Do delta do Yangtzé de volta a Pequim, para o voo das 02:45.</span></h2>\n'
    blocos_dia += "".join(bloco_dia(b, 200 + i) for i, b in enumerate(DIA_FINAL))

    # ---------- tradutor ----------
    cats = []
    for c, pt, zh, py in FRASES:
        if c not in cats:
            cats.append(c)
    linhas_frases = []
    for c, pt, zh, py in FRASES:
        busca = f"{pt} {zh} {py} {c}".lower().replace("'", "")
        linhas_frases.append(
            f'<tr class="frase" data-cat="{c}" data-busca="{busca}" '
            f'data-zh="{zh}" data-py="{py}" data-pt="{pt}">'
            f'<td>{pt}</td><td class="zh">{zh}</td><td class="py">{py}</td></tr>')
    filtros = "".join(f'<a href="#" class="chipf" data-cat="{c}">{c}</a>' for c in cats)

    # ---------- referências ----------
    REFS = [

        dict(tipo="Artigo", titulo="Mairon pelo Mundo — diário de uma viagem com o mesmo trajeto",
             fonte="Mairon Giovani · posts de 2025–2026",
             data="lido e resumido por nós",
             url="https://maironpelomundo.com/china/",
             insights=[
                 "<b>O trajeto dele é quase o nosso</b>: Pequim → Pingyao → Xi'an → Chengdu → Guilin/Yangshuo, com posts detalhados de cada cidade. Serve como leitura de aprofundamento para as paradas que coincidem.",
                 "<b>Trens:</b> a China tem mais de <b>40 mil km</b> de malha de alta velocidade. A letra indica a categoria — <b>G é a mais rápida (350 km/h)</b>, D fica em 250 km/h. Sempre que houver escolha, pegar G.",
                 "<b>Assentos são estreitos:</b> a segunda classe é 3+2 pensando no biotipo asiático. Ele recomenda considerar a <b>primeira classe (2+2)</b> quando a diferença de preço é pequena — na China ela não custa o que custa em avião.",
                 "<b>Preço fixo, sem flutuação:</b> não existe tarifa promocional como em avião. O risco é esgotar e sobrar só primeira classe. A venda abre <b>14 dias antes</b> (nosso guia trabalha com ~15).",
                 "<b>Referência de custo:</b> Pequim → Xi'an sai por cerca de <b>¥575</b> (~R$ 445 na cotação de out/2026) para 4h cobrindo 1.200 km. Ajuda a calibrar a linha de trens do orçamento.",
                 "<b>A bordo:</b> não há vagão-restaurante, mas há quiosque e carrinho; café custa ~¥27 (preço europeu) e quase todo vagão tem dispensador de água quente — daí o hábito chinês do miojo instantâneo.",
                 "<b>Tomadas</b> são tipo A (pinos chatos) ou C (redondos), às vezes híbridas, normalmente embaixo do assento. Adaptador é obrigatório.",
                 "<b>Internet:</b> ele defende o <b>eSIM (Airalo, Holafly)</b> instalado antes de embarcar em vez de VPN comprada no Brasil — mesma conclusão do outro vídeo que resumimos.",
             ]),
        dict(tipo="Vídeo", titulo="CHINA 2026: tudo o que você precisa saber antes de viajar",
             fonte="Invista pra Viagem (Jennifer & João) · 22:59 · publicado em 15/11/2025",
             data="assistido e resumido por nós",
             url="https://www.youtube.com/watch?v=_VWAfpxWhPw",
             video_id="_VWAfpxWhPw",
             insights=[
                 "<b>Visto:</b> confirmam a isenção de 30 dias para brasileiros, renovada até dezembro de 2026 — a mesma regra que usamos (chegada até 31/12).",
                 "<b>Imigração em Pequim é automatizada:</b> máquina com digital e foto, sem contato com agente. Mas podem pedir a <b>passagem de saída</b> já no embarque no Brasil.",
                 "<b>Passaporte original sempre na mão:</b> é escaneado na Muralha, na Cidade Proibida, em tudo. Cópia não serve.",
                 "<b>Internet é o maior perrengue:</b> VPN comprada no Brasil pode chegar bloqueada; a que funcionou para eles foi a <b>Surfshark</b>. Google (inclusive Maps), WhatsApp, Instagram e Facebook não funcionam. Microsoft/Bing funcionam. Chip com VPN integrada resolve.",
                 "<b>Alipay</b> (mais usado que o WeChat) precisa ser instalado e ativado <b>antes de embarcar</b>, porque a ativação depende de SMS.",
                 "<b>Dinheiro quase não existe:</b> pagam-se até barracas de rua por QR code. Cadastrar um cartão multimoeda (Wise, Nomad) dentro do app evita IOF e spread do cartão comum.",
                 "<b>Custos que eles mediram:</b> refeição simples ≈ <b>R$ 10</b>; metrô/ônibus <b>R$ 2–3</b> (ônibus chegou a R$ 0,80); hotel muito bom <b>R$ 200–300</b> a diária. Confirma que o guia pode ser generoso em hospedagem.",
                 "<b>Não agende a Muralha numa segunda-feira:</b> é o dia em que os museus fecham, então todo mundo vai para a Muralha e as filas explodem. Nosso plano já põe a Muralha em 31/12, quinta.",
                 "<b>Não precisa de agência</b>, mas reservar os ingressos antes compensa — Cidade Proibida esgota em alta temporada.",
                 "<b>Idioma:</b> inglês é raro, mas eles são solícitos e usam tradutor na hora. Segurança nas ruas é alta.",
             ]),
        dict(tipo="Vídeo", titulo="Pequim no inverno",
             fonte="Cami Li Vo · 15:09 · publicado em 20/03/2024",
             data="assistido e resumido por nós",
             url="https://www.youtube.com/watch?v=8kMs2rlHMuU",
             video_id="8kMs2rlHMuU",
             insights=[
                 "<b>Neve em Pequim é rara e transforma a cidade</b> — a −4 °C / −10 °C ela mostra a Cidade Proibida, o Templo do Céu e os parques cobertos de branco. Em compensação, o chão fica escorregadio: sapato com sola boa importa.",
                 "<b>Cidade Proibida exige ingresso comprado com 5 a 7 dias de antecedência</b> — sem ele não se entra, e não há bilheteria para vender na hora. Elas descobriram isso na porta e ficaram do lado de fora.",
                 "<b>Dentro da Cidade Proibida o caminho é de mão única</b>, da entrada sul para a saída norte: não dá para voltar atrás.",
                 "<b>Templo do Céu custa ¥28 por pessoa</b> (o combinado com o complexo sai um pouco mais). Elas chegaram ao meio-dia e pegaram fila para foto — a lição que tiram é ir cedo, que é o que o nosso roteiro já faz.",
                 "<b>Museu Nacional de Arte da China (NAMOC)</b>: ¥30 para visitar, prédio cercado de água, perto da praça. Boa opção de arte para uma tarde fria — incluímos na lista de Pequim.",
                 "<b>Praça Tiananmen passa por várias checagens de segurança</b> antes de entrar: contar com fila e levar o passaporte.",
                 "<b>Ópera de Pequim no teatro do hotel Qianmen</b>: em 2024 estava sem espetáculos — vale checar a programação da temporada antes de contar com ela.",
                 "<b>Qianmen Street</b> é rua comercial turística, boa para lembranças, não para o roteiro principal.",
             ]),
        dict(tipo="Vídeo", titulo="Zhangjiajie: como visitar as Montanhas de Avatar na China",
             fonte="Rota do Deco · 20:05 · publicado em 29/09/2026",
             data="assistido e resumido por nós",
             url="https://www.youtube.com/watch?v=MO7G-Oky76w",
             video_id="MO7G-Oky76w",
             insights=[
                 "<b>Zhangjiajie não é uma coisa só:</b> é o nome da cidade (com o aeroporto e a estação), e dentro dela ficam três atrações independentes, cada uma com ingresso próprio — o <b>Parque Nacional em Wulingyuan</b> (as montanhas de Avatar), o <b>Monte Tianmen</b> (a Porta do Céu) e o <b>Grand Canyon com a ponte de vidro</b>.",
                 "<b>Como chegar:</b> a linha nova de <b>Chongqing leva ~2h30–3h</b> — e o vídeo é explícito: é a melhor porta de entrada. De Pequim ou Xangai são 7–10h de trem, o que não compensa. Isso confirma o nosso encaixe depois de Chongqing (corrigimos a duração no guia, que estava com 4h30).",
                 "<b>Ingresso do parque vale 4 dias</b>, com entradas e saídas ilimitadas. É a maior vantagem de dormir na região: se um dia amanhecer encoberto, volta-se no seguinte.",
                 "<b>Comprar antes no Trip.com</b>, cerca de 7 dias antes, e andar sempre com o passaporte — na China ele é o ingresso.",
                 "<b>Clima:</b> chove em média <b>200 dias por ano</b>. O inverno é a estação mais seca (menos chuva, mais chance de visibilidade), com o risco oposto: neve pode fechar setores. O autor considera outono o melhor período e evita feriados chineses a qualquer custo.",
                 "<b>Quanto tempo:</b> 1 dia inteiro para o parque é o mínimo (fora chegada e saída); 2 dias para uma visita completa; 3 a 4 para incluir Tianmen, ponte de vidro e Furong. Nossas 3 noites dão 2 dias cheios — dá para o parque e mais uma atração.",
                 "<b>Onde dormir:</b> <b>Wulingyuan</b>, não a cidade — a 30–40 min do aeroporto, mas permite entrar no parque às 6h–8h. Didi entre as duas leva ~30–40 min.",
                 "<b>Extras que o vídeo sugere:</b> <b>Furong</b> (a cidade na cachoeira, 30 min de trem, bom para um fim de tarde) e <b>Fenghuang</b> (40–50 min de trem); em Wulingyuan há o espetáculo <b>Charming Xiangxi</b>, de cultura Tujia e Miao, sem precisar de mandarim.",
                 "<b>Atenção:</b> o teleférico do Monte Tianmen estava <b>em reforma em 2026</b>, sem prazo divulgado — se estiver fechado na nossa data, o plano B é o elevador de Bailong e o segundo setor do parque.",
             ]),
        dict(tipo="Artigo", titulo="Onde ficar em Pequim: melhores bairros e hotéis",
             fonte="Mala de Aventuras (Nanda Hudson)", data="atualizado em 10/04/2025",
             url="https://www.maladeaventuras.com/onde-ficar-em-pequim/",
             insights=[
                 "Escolhe quatro bases: <b>Wangfujing</b> (melhor para primeira viagem, dá para ir a pé às atrações; ponto fraco é o movimento 24h), <b>Sanlitun</b> (vida noturna em Chaoyang, muitos estrangeiros, hotéis para todos os bolsos), <b>Qianmen</b> (a mais barata, arquitetura tradicional, ao sul do centro) e <b>CBD</b> (luxo).",
                 "Critério de seleção: nota <b>≥ 8 no Booking</b> — em outra escala da que usamos aqui (Google, 0–5). O Holiday Inn Express Dongzhimen aparece com <b>8,9/10</b>, coerente com o 4,4/5 que levantamos.",
                 "Confirma dois dos nossos finalistas: <b>Holiday Inn Express Dongzhimen</b> e <b>Ascott Raffles City</b> — mas os classifica como “Sanlitun”, porque ficam na borda leste, não no centro histórico.",
                 "Não trata de <b>Gulou/Shichahai</b> nem de <b>Dongzhimen</b> como base própria: é exatamente o recorte que interessa a quem quer hutong e comida, e não vida noturna.",
                 "Para 4 pessoas: a lista de “conforto” de Wangfujing (Grand Hyatt, Hilton Wangfujing, Beijing Hotel NUO) é a que resolve dois quartos no mesmo prédio, a pé da Cidade Proibida.",
             ]),
    ]

    def card_ref(r):
        itens = "".join(f"<li>{i}</li>" for i in r["insights"])
        vid = r.get("video_id")
        if vid:
            topo = (f'<div class="vembed"><iframe src="https://www.youtube.com/embed/{vid}" '
                    f'title="{r["titulo"]}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; '
                    f'encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')
            ico = "▶️"
        else:
            topo = ""
            ico = "📄"
        return f"""<article class="vcard">
      {topo}
      <h3>{ico} {r['titulo']}</h3>
      <p class="fine">{r['fonte']} · {r['data']}</p>
      <h4 class="dest">Destaques</h4>
      <ul class="tight">{itens}</ul>
      <a class="btn ghost" href="{r['url']}" target="_blank" rel="noopener">Abrir original</a>
    </article>"""

    cards_video = "".join(card_ref(r) for r in REFS)
    cards_video += """
    <article class="vcard">
      <div class="vembed vazio-embed"><div class="vexp">▶️</div></div>
      <h3>▶️ Vídeos do YouTube</h3>
      <p class="fine">aguardando os links</p>
      <h4 class="dest">Destaques</h4>
      <ul class="tight">
        <li>Mande a URL do vídeo. Eu assisto, extraio os pontos que interessam para esta viagem e publico aqui.</li>
        <li>O vídeo entra <b>incorporado</b> (embed), com o resumo dos destaques logo abaixo — como no cartão ao lado.</li>
        <li>Se preferir, mande só o título e o canal: eu localizo e confirmo antes de publicar.</li>
      </ul>
    </article>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>China em 30 dias · guia da viagem</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>{CSS}</style>
<style>{EXTRA_CSS}</style>\n</head>
<body>

<div class="hero">
  <img src="{hero}" alt="Grande Muralha sob a neve">
  <div class="wrap cap-hero">
    <h1>China em 30 dias</h1>
    <div class="sub">Um trajeto só, do norte imperial ao delta do Yangtzé</div>
  </div>
  <div class="credit">Badaling sob a neve · {credito['autor']} / Wikimedia ({credito['licenca']})</div>
</div>

<div class="topbar">
  <div class="wrap tbinner">
    <a class="brand" href="#" data-tab="roteiro">China em 30 dias</a>
    <button class="burger" id="burger" aria-label="Abrir menu" aria-expanded="false" aria-controls="drawer">
      <span></span><span></span><span></span>
    </button>
  </div>
</div>

<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-hidden="true">
  <div class="dhead">
    <span>Seções</span>
    <button class="dclose" id="dclose" aria-label="Fechar menu">&times;</button>
  </div>
  <nav role="tablist">
    <a role="tab" href="#roteiro" data-tab="roteiro" aria-selected="true">Roteiro<span>mapa e cidades</span></a>
    <a role="tab" href="#roteiro-dia" data-tab="roteiro-dia" aria-selected="false">Roteiro dia a dia<span>calendário e sanfona</span></a>
    <a role="tab" href="#aereo" data-tab="aereo" aria-selected="false">Passagens aéreas<span>voos e bagagem</span></a>
    <a role="tab" href="#trens" data-tab="trens" aria-selected="false">Trens<span>trechos internos</span></a>
    <a role="tab" href="#hoteis" data-tab="hoteis" aria-selected="false">Hospedagens<span>bairros e valores</span></a>
    <a role="tab" href="#passeios" data-tab="passeios" aria-selected="false">Passeios<span>ingressos e horários</span></a>
    <a role="tab" href="#mala" data-tab="mala" aria-selected="false">Mala<span>o que levar</span></a>
    <a role="tab" href="#tradutor" data-tab="tradutor" aria-selected="false">Tradutor<span>frases em chinês</span></a>
    <a role="tab" href="#conversor" data-tab="conversor" aria-selected="false">Conversor<span>yuan ⇄ real</span></a>
    <a role="tab" href="#videos" data-tab="videos" aria-selected="false">Referências<span>artigos e vídeos</span></a>
    <a role="tab" href="#preparo" data-tab="preparo" aria-selected="false">Preparo<span>custos e checklist</span></a>
  </nav>
</aside>

<div class="wrap">

<section role="tabpanel" id="tab-roteiro" class="on">
  <h2>O trajeto<span class="sub">Clique em uma cidade no mapa ou abra a sanfona. As linhas pontilhadas são as três variantes de natureza.</span></h2>
  <div id="map"></div>
  <p class="fine" style="margin-top:10px">Mapa: OpenStreetMap (precisa de internet). Sem conexão, use o esquema abaixo.</p>

  <details>
    <summary>🧭 Esquema de posições (funciona offline)<span class="chev">▶</span></summary>
    <div class="inner">{svg_schema()}</div>
  </details>

  <div class="grid" style="margin-top:16px">
    <div class="card"><b>✅ Passagens</b><span>Air China 5HAJHF · ida 29/12 · volta 27/01 02:45</span></div>
    <div class="card"><b>✅ Visto</b><span>Isento · 30/12 a 27/01 (28 dias)</span></div>
    <div class="card"><b>🟡 Roteiro</b><span>Três variantes em aberto: 🌄 🛶 ⛰️</span></div>
    <div class="card"><b>⬜ Trens e hotéis</b><span>Valores e reservas em aberto</span></div>
  </div>

  <h2>Cidades, uma por uma<span class="sub">Atrações, hospedagem, valor com rateio e programação sugerida.</span></h2>
  {"".join(blocos)}
</section>

<section role="tabpanel" id="tab-aereo">
  <h2>Passagens aéreas<span class="sub">Air China · localizador 5HAJHF · emitido em 13/10/2026</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Trecho</th><th>Voo</th><th>Horários</th><th>Duração</th></tr></thead>
    <tbody>
      <tr><td><b>IDA · 29/12</b><br>São Paulo → Pequim</td><td>CA898 · Boeing 787-900</td>
        <td>GRU 08:30 → Madri 22:35 <span class="tag">conexão 2h05 · T1</span><br>Madri 00:40 → PEK 18:45 (+1 dia)</td><td>23h15</td></tr>
      <tr><td><b>VOLTA · 27/01</b><br>Pequim → São Paulo</td><td>CA875 · A350-900<br>CA7105 (LATAM)</td>
        <td>PEK 02:45 → Paris 07:00 <span class="tag">conexão 5h05 · T1→T2A</span><br>Paris 12:05 → GRU 20:00</td><td>28h15</td></tr>
    </tbody>
  </table></div>

  <h3>Valores</h3>
  <div class="tw"><table>
    <thead><tr><th>Viajantes</th><th>Valor por pessoa</th><th class="num">Subtotal</th><th class="num">Por pessoa</th></tr></thead>
    <tbody>
      <tr>
        <td><input class="qty" id="travelers" type="number" min="1" max="9" step="1" value="4"></td>
        <td>{money_input('aereo', 'aereo', 'travelers')}</td>
        <td class="num subtotal" id="sub-aereo">R$ 0,00</td>
        <td class="num perperson" id="per-aereo">—</td>
      </tr>
    </tbody>
  </table></div>
  <div class="totbar"><span class="lbl">Total aéreo</span><b id="tot-aereo">R$ 0,00</b></div>
  <div class="hint">O recibo emitido para um dos passageiros mostra <b>USD 1.156,60</b> (tarifa 1.100 + taxas 56,60).
  Preencha aqui o valor em reais efetivamente pago por pessoa; o campo multiplica pelos viajantes.</div>

  <h3>Bagagem e assentos</h3>
  <div class="grid">
    <div class="card"><b>Bagagem</b><span>2 peças na ida, <b>1 peça na volta</b> — limite para as compras.</span></div>
    <div class="card"><b>Assentos</b><span>52A (GRU→PEK) e 54A (PEK→CDG). Paris→São Paulo sem assento.</span></div>
    <div class="card"><b>Saída de Pequim</b><span>Voo 02:45 · estar no aeroporto ~00:45 do dia 27.</span></div>
  </div>
  <a class="btn" href="https://www.airchina.com.br" target="_blank" rel="noopener">Air China · gestão da reserva</a>
  <a class="btn ghost" href="https://www.google.com/travel/flights?q=Flights%20from%20GRU%20to%20PEK%20on%202026-12-29%20through%202027-01-27&curr=BRL&hl=pt-BR" target="_blank" rel="noopener">Comparar no Google Flights</a>
</section>

<section role="tabpanel" id="tab-trens">
  <h2>Trens internos<span class="sub">Todos os trechos são de trem-bala. Comprar no Trip.com (aceita cartão internacional) ou no 12306.</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Trecho</th><th>Data</th><th>Duração</th><th>Por pessoa</th><th class="num">Subtotal (4)</th><th class="num">Por pessoa</th></tr></thead>
    <tbody>{"".join(linhas_trem)}</tbody>
  </table></div>
  <div class="totbar"><span class="lbl">Total trens</span><b id="tot-trens">R$ 0,00</b></div>
  <div class="hint">A venda abre cerca de <b>15 dias antes</b> de cada trecho. Em período de chunyun (a partir de ~20/01),
  comprar no primeiro dia — os trens esgotam.</div>
  <a class="btn" href="https://www.trip.com/trains/" target="_blank" rel="noopener">Trip.com · trens</a>
  <a class="btn ghost" href="https://www.12306.cn" target="_blank" rel="noopener">12306 (oficial)</a>
</section>

<section role="tabpanel" id="tab-hoteis">
  <h2>Hospedagens<span class="sub">Pequim em Dongzhimen; nas demais cidades, os 3 melhores da pesquisa por nota e volume de avaliações.</span></h2>

  <h3>Pequim · sugestões</h3>
  <div class="tw"><table>
    <thead><tr><th>Opção</th><th>Nota</th><th>Por que serve para 4</th></tr></thead>
    <tbody>
      <tr><td><b>Ascott Raffles City Beijing</b><br><span class="fine">Dongzhimen</span></td><td>5★ · 4,5 (70)</td>
        <td>Apartamento com cozinha, piscina e academia. Confirmar categoria de <b>dois dormitórios</b> — a de entrada pode ser estúdio.</td></tr>
      <tr><td><b>Holiday Inn Express Dongzhimen</b><br><span class="fine">Dongzhimen</span></td><td>4★ · 4,4 (229)</td>
        <td>Quartos twin e café da manhã; duas reservas (casal + twin) resolvem o grupo.</td></tr>
      <tr><td><b>Shichahai Shadow Art Hotel</b><br><span class="fine">Gulou</span></td><td>4★ · 4,6 (89)</td>
        <td>Hutong com teatro de sombras; quartos menores.</td></tr>
    </tbody>
  </table></div>

  <h3>Valores por cidade</h3>
  <p class="fine">Preencha a diária por quarto. O cálculo usa as noites de cada cidade e 2 quartos — o rateio é dividido pelo número de viajantes definido na aba Passagens aéreas.</p>
  <div class="tw"><table>
    <thead><tr><th>Cidade</th><th>Noites</th><th>Diária / quarto</th><th class="num">Subtotal</th><th class="num">Por pessoa</th></tr></thead>
    <tbody>
      {"".join(f'<tr><td><b>{c["emoji"]} {c["nome"]}</b></td><td>{c["noites"]}</td><td>{money_input("hot-" + c["id"], "hoteis", "nights", c["noites"], 2)}</td><td class="num subtotal" id="sub-hot-{c["id"]}">R$ 0,00</td><td class="num perperson" id="per-hot-{c["id"]}">R$ 0,00 /pessoa</td></tr>' for c in CIDADES)}
    </tbody>
  </table></div>
  <div class="totbar"><span class="lbl">Total hospedagem</span><b id="tot-hoteis">R$ 0,00</b></div>

  <a class="btn" href="https://www.booking.com/searchresults.pt-br.html?ss=Dongzhimen%2C+Pequim&checkin=2026-12-30&checkout=2027-01-06&group_adults=4&no_rooms=2" target="_blank" rel="noopener">Pequim · preços</a>
  <a class="btn ghost" href="https://www.airbnb.com.br/s/Beijing--China/homes?checkin=2026-12-30&checkout=2027-01-06&adults=4" target="_blank" rel="noopener">Apartamentos inteiros</a>
  <p class="fine" style="margin-top:10px">Em janeiro, dois critérios eliminam opções ruins: aquecimento funcionando e no máximo 10 minutos a pé do metrô.</p>
</section>

<section role="tabpanel" id="tab-passeios">
  <h2>Passeios<span class="sub">Ingressos em yuan, valores de referência para orçamento — confirmar no site ou na bilheteria.</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Cidade</th><th>Atração</th><th>Tempo</th><th>Ingresso</th><th>Horário / observação</th><th></th></tr></thead>
    <tbody>
      {"".join(f'<tr><td><b>{c["emoji"]} {c["nome"]}</b></td><td>{n}</td><td>{t}</td><td>{p}</td><td class="fine">{obs}</td><td><a href="{gmaps(g)}" target="_blank" rel="noopener">mapa</a></td></tr>' for c in CIDADES for n, t, p, obs, g in c["atracoes"])}
    </tbody>
  </table></div>

  <h3>Reservas que não podem escorregar</h3>
  <ul class="tight">
    <li><b>25/12/2026</b> — Cidade Proibida (visita 02/01), janela de 7 dias, com passaporte</li>
    <li><b>29/12/2026</b> — Museu Nacional (visita 05/01)</li>
    <li><b>~21/12/2026</b> — trem Pequim → Datong (06/01)</li>
    <li><b>~01/01/2027</b> — trem do bloco de natureza</li>
    <li><b>~10/01/2027</b> — trem Nanjing → Pequim (25/01)</li>
  </ul>
  <a class="btn" href="https://intl.dpm.org.cn" target="_blank" rel="noopener">Cidade Proibida</a>
  <a class="btn ghost" href="http://en.chnmuseum.cn" target="_blank" rel="noopener">Museu Nacional</a>
  <a class="btn ghost" href="https://www.trip.com/things-to-do/" target="_blank" rel="noopener">Trip.com · ingressos</a>
</section>

<section role="tabpanel" id="tab-conversor">
  <h2>Conversor de moeda<span class="sub">Cotação do yuan buscada no navegador a cada visita. Sem internet, usa a referência de 05/10/2026.</span></h2>
  <div class="conv">
    <div class="convrow">
      <label>Yuan (¥)<input id="cny" type="number" inputmode="decimal" step="0.01" value="100"></label>
      <span class="arrow">⇄</span>
      <label>Real (R$)<input id="brl" type="number" inputmode="decimal" step="0.01"></label>
    </div>
    <p class="rate" id="rate">1 ¥ = R$ —</p>
    <p class="fine" id="rate-src">buscando cotação…</p>
    <div class="quick">
      <a href="#" class="chipf" data-cny="10">¥10</a>
      <a href="#" class="chipf" data-cny="50">¥50</a>
      <a href="#" class="chipf" data-cny="100">¥100</a>
      <a href="#" class="chipf" data-cny="500">¥500</a>
      <a href="#" class="chipf" data-cny="1000">¥1.000</a>
      <a href="#" class="chipf" id="rate-refresh">Atualizar cotação</a>
    </div>
  </div>
  <h3>Para ter na cabeça</h3>
  <div class="tw"><table>
    <thead><tr><th>Item</th><th>Yuan</th><th>Real (na cotação atual)</th></tr></thead>
    <tbody>
      <tr><td>Metrô</td><td>¥3–7</td><td id="ref1">—</td></tr>
      <tr><td>Refeição popular</td><td>¥25–50</td><td id="ref2">—</td></tr>
      <tr><td>Ingresso de museu/templo</td><td>¥50–150</td><td id="ref3">—</td></tr>
      <tr><td>Trem-bala (3–5 h)</td><td>¥150–450</td><td id="ref4">—</td></tr>
      <tr><td>Hotel 4★ (quarto/noite)</td><td>¥400–800</td><td id="ref5">—</td></tr>
    </tbody>
  </table></div>
  <p class="fine">A tabela recalcula junto com a cotação sempre que a página carrega.</p>
</section>

<section role="tabpanel" id="tab-preparo">
  <h2>Resumo de custos<span class="sub">Somatório do que foi preenchido nas outras abas.</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Categoria</th><th class="num">Total</th></tr></thead>
    <tbody>
      <tr><td>Aéreo</td><td class="num subtotal" id="tot-aereo2">R$ 0,00</td></tr>
      <tr><td>Trens</td><td class="num subtotal" id="tot-trens2">R$ 0,00</td></tr>
      <tr><td>Hospedagem</td><td class="num subtotal" id="tot-hoteis2">R$ 0,00</td></tr>
      <tr><td><b>Total</b></td><td class="num subtotal"><b id="tot-geral">R$ 0,00</b></td></tr>
    </tbody>
  </table></div>
  <p class="fine" id="tot-geral-pessoa">R$ 0,00 por pessoa</p>

  <h2>Antes de embarcar</h2>
  <ul class="tight">
    <li>Passaporte válido cobrindo a estada, com página em branco</li>
    <li><b>Alipay</b> e <b>WeChat Pay</b> com cartão internacional, configurados no Brasil</li>
    <li><b>VPN</b> instalada e testada: Google, WhatsApp e Instagram são bloqueados</li>
    <li><b>eSIM</b> de dados + apps <b>Amap</b> (mapas) e <b>Didi</b> (táxi)</li>
    <li>Roupa de frio: −8 a −13 °C à noite no norte</li>
    <li>Dinheiro em espécie para mercados e templos</li>
  </ul>

  <h2>Ordem de grandeza no dia a dia</h2>
  <div class="tw"><table>
    <thead><tr><th>Item</th><th>Referência</th></tr></thead>
    <tbody>
      <tr><td>Refeição em restaurante popular</td><td>¥25–50 por pessoa</td></tr>
      <tr><td>Metrô</td><td>¥3–7 por viagem</td></tr>
      <tr><td>Trem-bala (3-5 h)</td><td>¥150–450</td></tr>
      <tr><td>Hotel 4★ (quarto/noite)</td><td>¥400–800</td></tr>
      <tr><td>Museus e templos</td><td>¥50–150 por dia</td></tr>
    </tbody>
  </table></div>
  <p class="fine">Cotação de referência em 05/10/2026: ¥1 = R$ 0,776.</p>
</section>

<section role="tabpanel" id="tab-roteiro-dia">
  <h2>Roteiro dia a dia<span class="sub">O plano hora a hora, com espaço deliberado para se perder. Cada linha tem uma tarde ou noite sem atração marcada.</span></h2>
  <p class="look">Este é o roteiro completo do circuito atual — 27 noites, entrada e saída por Pequim. Se o grupo decidir cortar cidades, os blocos de <b>Changsha</b>, <b>Hangzhou</b> e <b>Nanjing</b> são os primeiros candidatos, e a aba mostra exatamente o que se perde em cada um.</p>
  <div class="calfull"><h3>Calendário<span class="sub">Escolha a variante: os dias mudam de cor conforme a cidade onde vocês dormem.</span></h3>
    <div class="scen">
      <a href="#" class="chipf on" data-scen="A">A · Zhangjiajie</a>
      <a href="#" class="chipf" data-scen="B">B · Guilin</a>
      <a href="#" class="chipf" data-scen="C">C · Huangshan</a>
    </div>
    <div id="cal"></div>
    <div id="calleg" class="leg"></div>
  </div>

  <h3 class="sanf">Cidade por cidade<span class="sub">Abra a cidade que quiser ver — cada uma tem foto, tabela de dias e dicas.</span></h3>
  {blocos_dia}
</section>

<section role="tabpanel" id="tab-mala">
  <h2>Mala<span class="sub">Duas listas e uma comum. Marque o que já separou — fica salvo neste aparelho.</span></h2>
  <p class="look">A premissa é o contraste: <b>−13 °C em Datong</b> e <b>+14 °C em Guilin</b>, com hotéis aquecidos a 20–24 °C.
  Isso pede <b>camadas que se removem</b>, não uma peça grossa só. E como a volta permite <b>uma única peça de bagagem</b>,
  a regra é 3 conjuntos de segunda pele e lavanderia de hotel.</p>

  <div class="gridmala">{html_mala()}</div>

  <div class="malabar">
    <span id="mala-total" class="fine">0 de 0 itens</span>
    <a href="#" class="chipf" id="mala-reset">Limpar marcações</a>
  </div>

  <h2>Glossário<span class="sub">Três palavras que decidem a compra — e não são sinônimos.</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Termo</th><th>O que é</th><th>O que importa</th></tr></thead>
    <tbody>
      <tr><td><b>Pluma</b> (down)</td>
          <td>O <b>recheio</b>: tufos de penugem de ganso ou pato que prendem ar entre as fibras</td>
          <td>Mede-se em <b>fill power</b> (700, 800, 900): mais ar por grama = mais quente e mais leve.
              <b>Perde quase toda a eficácia se molhar</b></td></tr>
      <tr><td><b>Parka</b></td>
          <td>O <b>formato</b>, não o material: casaco comprido (até a metade da coxa), com capuz,
              vento bloqueado e bolsos</td>
          <td>O comprimento protege coxa e lombar, que é o que congela primeiro com vento.
              Pode ser de pluma, sintético ou lã</td></tr>
      <tr><td><b>Doudoune</b></td>
          <td>Jaqueta curta de pluma ou sintético, leve e compactável — franceses chamam assim
              a “puffer” fina</td>
          <td>É a peça perfeita de <b>camada do meio</b>: sozinha vai de 0 a −5 °C; sob um corta-vento
              vai bem abaixo disso</td></tr>
      <tr><td><b>Fleece</b> (polar)</td>
          <td>Malha sintética de poliéster com a superfície escovada, que prende ar entre as fibras —
              o substituto moderno da lã</td>
          <td>Aquece <b>mesmo molhado</b> e seca rápido, ao contrário do algodão e da pluma.
              Mas <b>não corta vento nenhum</b>: sozinho, é só uma camada do meio</td></tr>
      <tr><td><b>Hardshell</b></td>
          <td>Capa externa sem isolamento: só barra vento e água</td>
          <td>É o que transforma uma doudoune em roupa de −13 °C. Precisa ser <b>folgada</b></td></tr>
    </tbody>
  </table></div>

  <h2>O sistema de camadas<span class="sub">Quatro camadas, que se combinam conforme a cidade — de +14 °C em Guilin a −13 °C em Datong.</span></h2>
  <div class="tw"><table>
    <thead><tr><th>#</th><th>Camada</th><th>Função</th><th>Como escolher</th></tr></thead>
    <tbody>
      <tr><td>1</td><td><b>Segunda pele</b></td><td>Tirar o suor do corpo antes que esfrie</td>
          <td><b>Poliéster ou lã merino. Nunca algodão</b> — algodão molhado vira gelo.
              Ajustada ao corpo, manga longa</td></tr>
      <tr><td>2</td><td><b>Fleece</b></td><td>Reter calor mesmo úmido</td>
          <td>Polar de ~200 g/m², com zíper no peito para ventilar. Custa pouco e resolve muito</td></tr>
      <tr><td>3</td><td><b>Doudoune / pluma fina</b></td><td>Isolar</td>
          <td>Fill power 600–800. Tem que caber <b>sem comprimir</b> sob a camada 4</td></tr>
      <tr><td>4</td><td><b>Parka ou hardshell</b></td><td>Cortar vento e neve</td>
          <td>Capuz ajustável, punho elástico, zíper duplo. Comprida até a coxa</td></tr>
    </tbody>
  </table></div>
  <p class="fine"><b>Combinações por cidade:</b> Guilin +14 °C → camada 1 + 2 · Xangai e Chongqing → 1 + 2 (3 só à noite) ·
  Pequim, Xi'an, Pingyao → 1 + 2 + 3 · Datong e cume de Huangshan → 1 + 2 + 3 + 4, tudo junto.</p>

  <div class="hint" style="background:#f4f7fa;border-left-color:#1f6f8b"><b>Fleece não corta vento.</b>
  É a peça mais barata e mais versátil do conjunto (¥150–250 na Uniqlo, R$ 150–250 na Decathlon),
  mas sozinho ele só funciona parado e sem vento. Com vento de Pequim, ele precisa de uma capa por cima —
  é literalmente um cobertor de poliéster com zíper.</div>

  <div class="hint"><b>Sua doudoune da Decathlon entra como camada 3.</b> Sim — ela é exatamente a peça do meio.
  Duas condições: (1) a camada 4 precisa ser <b>folgada</b> o suficiente para ela não ficar comprimida;
  (2) pluma comprimida perde eficiência, então se você se abraçar e sentir aperto, o tamanho do casaco externo está errado.
  Sozinha, a doudoune cobre 0 a −5 °C. Com fleece por baixo e corta-vento por cima, encara Datong.
  Confira na etiqueta a <b>temperatura de conforto</b> que a Decathlon imprime — é o número que vale.</div>

  <h2>Como escolher cada peça<span class="sub">O critério que decide, e o erro comum.</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Peça</th><th>O que procurar</th><th>Erro comum</th></tr></thead>
    <tbody>
      <tr><td><b>Segunda pele</b></td>
          <td>Poliéster (Heattech) ou merino; ajustada; manga longa e decote alto</td>
          <td>Levar camiseta de algodão “porque é quentinha” — molhada, ela rouba calor</td></tr>
      <tr><td><b>Fleece</b></td>
          <td>Polar 200 g/m², com zíper no peito, gola alta</td>
          <td>Comprar um gigante e não conseguir vestir nada por cima</td></tr>
      <tr><td><b>Doudoune</b></td>
          <td>Fill power 600+, compactável, com capuz se possível</td>
          <td>Usar apertada sob o casaco: o aperto tira o ar, e o ar é o isolante</td></tr>
      <tr><td><b>Parka</b></td>
          <td>Comprida, capuz com ajuste, DWR na capa, zíper de dois sentidos, bolso interno</td>
          <td>Comprar justa “para não parecer grande” — tem que caber as camadas 1 a 3</td></tr>
      <tr><td><b>Bota</b></td>
          <td>Impermeável, cano médio, solado com cravos, meio número acima</td>
          <td>Bota de neve rígida para andar 10 km em cidade: calo garantido</td></tr>
      <tr><td><b>Meias</b></td>
          <td>Lã merino ou sintética; grossa para montanha, fina para cidade</td>
          <td>Só meia grossa: com bota justa, ela comprime o pé e esfria o dedo</td></tr>
      <tr><td><b>Luvas</b></td>
          <td>Par interno fino (toque em tela) + par externo impermeável</td>
          <td>Luva única e grossa: você tira para usar o celular e perde o calor</td></tr>
      <tr><td><b>Gorro e cachecol</b></td>
          <td>Gorro que cobre a orelha; lenço grande que vira xale</td>
          <td>Esquecer o pescoço: é por ali que sai a maior parte do calor</td></tr>
    </tbody>
  </table></div>

  <h2>A parka, em números<span class="sub">O que a peça precisa ter para encarar −13 °C em Datong e o vento da Muralha.</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Item</th><th>Especificação</th><th>Por quê</th></tr></thead>
    <tbody>
      <tr><td><b>Isolamento</b></td><td>Pluma <b>600–700 fill</b>, 200–300 g de pluma (ou sintético equivalente: HEATSEEKER, PrimaLoft)</td>
          <td>Abaixo de 550 fill a peça fica pesada para o calor que entrega</td></tr>
      <tr><td><b>Capa</b></td><td>Membrana impermeável (DryVent, Gore-Tex) ou DWR forte, com <b>costuras seladas</b></td>
          <td>Pluma molhada perde quase toda a eficácia</td></tr>
      <tr><td><b>Comprimento</b></td><td>Até a <b>metade da coxa</b></td>
          <td>Cobre coxa e lombar, o que congela primeiro com vento</td></tr>
      <tr><td><b>Capuz</b></td><td>Fixo ou removível, ajustável em 3 pontos, com isolamento próprio</td>
          <td>Capuz sem isolamento é enfeite</td></tr>
      <tr><td><b>Zíper</b></td><td>Dois sentidos, com aba (storm flap) por dentro</td>
          <td>Permite sentar e abrir por baixo sem expor o peito</td></tr>
      <tr><td><b>Punhos e barra</b></td><td>Punho elástico interno + ajuste externo; barra com cordão</td>
          <td>Vento entra por punho e barra, não pela capa</td></tr>
      <tr><td><b>Ajuste</b></td><td><b>Folgada</b> sobre as camadas 1–3</td>
          <td>Pluma comprimida não isola</td></tr>
      <tr><td><b>Peso</b></td><td>1,0–1,5 kg</td>
          <td>Abaixo disso é provável que falte isolamento</td></tr>
    </tbody>
  </table></div>
  <p class="fine"><b>Como provar na loja:</b> vista segunda pele + fleece + doudoune, levante os braços e se abrace.
  Se apertar nos ombros ou nas costas, suba um tamanho — o aperto é o que estraga o isolamento.</p>

  <h2>Modelos no Brasil<span class="sub">The North Face Brasil, preços de 20/11/2026 (semana de Black Friday, com desconto aplicado).</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Modelo</th><th>Isolamento e capa</th><th class="num">Preço</th><th>Para quem</th></tr></thead>
    <tbody>
      <tr><td><b>McMurdo</b> (masc.)<br><span class="fine">o mais longo da linha</span></td>
          <td>Pluma <b>600 fill</b> reciclada, DryVent impermeável e corta-vento</td>
          <td class="num"><b>R$ 4.199</b><br><span class="fine">de 4.590</span></td>
          <td>Quem quer <b>uma peça só</b> resolvendo tudo, sem camadas</td></tr>
      <tr><td><b>Mountain Range Down</b> (masc.)</td>
          <td>Pluma + HEATSEEKER, capa impermeável com costuras seladas, capuz isolado</td>
          <td class="num"><b>R$ 3.949</b><br><span class="fine">de 4.590</span></td>
          <td>Sistema de camadas, com ajuste folgado</td></tr>
      <tr><td><b>Arctic Summit</b> (fem.)</td>
          <td>Pluma <b>600 fill</b> reciclada, DryVent, comprimento alongado,
              capuz com pelo removível</td>
          <td class="num"><b>R$ 3.399</b><br><span class="fine">de 3.990</span></td>
          <td>É a que o texto descreve como “ajuste espaçoso para camadas”</td></tr>
      <tr><td><b>Hydrenalite City Down</b> (fem.)</td>
          <td>Pluma <b>700 fill</b>, tecido repelente à água, leve e compressível</td>
          <td class="num"><b>R$ 2.799</b><br><span class="fine">de 3.490 · esgotada em 2 cores</span></td>
          <td>Melhor fill power por real; menos comprida</td></tr>
      <tr><td><b>Antora Rain</b> (fem.)</td>
          <td>DryVent 2L <b>sem isolamento</b> — é capa pura</td>
          <td class="num"><b>R$ 1.149</b><br><span class="fine">de 1.399</span></td>
          <td><b>Quem já tem a doudoune:</b> esta é a camada 4 que falta</td></tr>
    </tbody>
  </table></div>
  <p class="fine">Links: <a href="https://www.thenorthface.com.br/parka-masculina-mcmurdo-woodland-green-5gjf-bri/p" target="_blank" rel="noopener">McMurdo</a> ·
  <a href="https://www.thenorthface.com.br/parka-masculina-mountain-range-down-tnf-black-88we-kx7/p" target="_blank" rel="noopener">Mountain Range Down</a> ·
  <a href="https://www.thenorthface.com.br/parka-feminina-arctic-summit-navy-84j2-8k2/p" target="_blank" rel="noopener">Arctic Summit</a> ·
  <a href="https://www.thenorthface.com.br/parka-feminina-hydrenalite-city-down-hooded-white-dune-8d3k-qli/p" target="_blank" rel="noopener">Hydrenalite</a> ·
  <a href="https://www.thenorthface.com.br/parka-feminina-antora-rain-tnf-black-8bkc-jk3/p" target="_blank" rel="noopener">Antora Rain</a></p>
  <div class="hint"><b>O que a busca mostrou:</b> a Decathlon Brasil está com catálogo de verão —
  não há parka de expedição hoje, só jaquetas puffer de moda. Quem tem inverno de verdade no Brasil
  é The North Face, Columbia e Trilhas &amp; Aventuras. Para o nosso caso, a <b>Antora Rain (R$ 1.149)</b>
  combinada com a sua doudoune resolve mais barato que a McMurdo — e é mais versátil, porque no sul
  vocês vão querer só a capa.</div>

  <h2>Comparar na Decathlon<span class="sub">Um link por peça, já na categoria certa — para comparar modelo e preço.</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Peça</th><th>Link</th><th>O que comparar</th></tr></thead>
    <tbody>{html_deca()}</tbody>
  </table></div>
  <p class="fine">Atenção ao calendário: em dezembro o Brasil está no verão e muitas dessas categorias ficam
  com estoque sazonal reduzido. Serve para comparar modelo e referência de preço — a compra de inverno pesado
  continua melhor na China.</p>

  <h2>Comprar aqui ou na China?<span class="sub">Dividir é o caminho — e há um motivo forte para cada escolha.</span></h2>
  <div class="tw"><table>
    <thead><tr><th>Item</th><th>Onde comprar</th><th>Por quê</th><th>Link</th></tr></thead>
    <tbody>{html_compras()}</tbody>
  </table></div>

  <h2>Os pés<span class="sub">Uma bota, um tênis leve, um chinelo. Nada além disso.</span></h2>
  <p>O problema não é neve nas calçadas de Pequim — elas são limpas. É <b>gelo nas escadarias</b> da Muralha e de Huangshan,
  <b>pedra polida</b> em Pingyao e chão molhado em Xangai. Tênis de São Paulo não resolve.</p>
  <ul class="tight">
    <li><b>Bota:</b> impermeável, cano médio, solado com cravos profundos, <b>meio número acima</b> para caber meia grossa</li>
    <li><b>Modelo:</b> trilha leve serve melhor que bota de neve, que é dura demais para cidade</li>
    <li><b>Tênis leve:</b> vocês passam 10 dias no sul ameno e dentro de hotéis aquecidos</li>
    <li><b>Crampon:</b> só se Huangshan entrar no roteiro — compra-se na China por ¥30–50</li>
  </ul>

  <h2>Plano de compra<span class="sub">Para não desembarcar a −7 °C sem nada.</span></h2>
  <ul class="tight">
    <li><b>Antes de viajar (Brasil):</b> bota impermeável e meias de lã — o que precisa de numeração e prova</li>
    <li><b>Chegar com:</b> uma segunda pele e um casaco razoável, para o trajeto do aeroporto até Dongzhimen</li>
    <li><b>Primeiro ou segundo dia em Pequim:</b> uma hora de Uniqlo resolve segunda pele, pluma e acessórios dos quatro</li>
    <li><b>Custo estimado do kit na China:</b> ¥800–1.500 por pessoa</li>
  </ul>
</section>

<section role="tabpanel" id="tab-tradutor">
  <h2>Tradutor<span class="sub">Frases de sobrevivência em chinês, com pinyin. Toque na frase para mostrar em tela cheia para a outra pessoa.</span></h2>
  <div class="trad-top">
    <input id="busca" type="search" placeholder="Buscar em português, 中文 ou pinyin…">
    <a class="btn" href="https://translate.google.com/?sl=pt&tl=zh-CN&op=translate" target="_blank" rel="noopener">Google Tradutor (PT ↔ 中文)</a>
  </div>
  <div class="chipsf">{filtros}</div>
  <div class="tw"><table class="trad">
    <thead><tr><th>Português</th><th>中文</th><th>Pinyin</th></tr></thead>
    <tbody>{"".join(linhas_frases)}</tbody>
  </table></div>
  <p class="fine">Funciona offline (é uma lista curada, não tradução automática). Para frases livres, use o Google Tradutor —
  o texto digitado abaixo já vai preenchido ao clicar.</p>
  <div class="livre">
    <input id="livre" type="text" placeholder="Digite uma frase em português para traduzir">
    <a href="#" class="btn" id="btn-livre">Traduzir no Google</a>
  </div>
</section>

<section role="tabpanel" id="tab-videos">
  <h2>Referências<span class="sub">Artigos e vídeos que lemos, com os insights que interessam para esta viagem.</span></h2>
  <div class="grid">{cards_video}</div>
</section>

<footer>
  <div class="wrap" style="padding:0">
    Guia gerado para o grupo. Fotografias do Wikimedia Commons sob licenças livres. Mapa: OpenStreetMap.
    O esquema de posições é ilustrativo, não está em escala. Valores digitados ficam salvos neste navegador.
  </div>
</footer>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const CIDADES = {pontos_json};
const anel = ["pequim","datong","pingyao","xian","chongqing","changsha","xangai","hangzhou","nanjing","pequim"];
const variantes = [
  {{cor:"#2f6b4f", ids:["chongqing","zhangjiajie","changsha"]}},
  {{cor:"#1f6f8b", ids:["changsha","guilin","xangai"]}},
  {{cor:"#7a4b2a", ids:["hangzhou","huangshan","nanjing"]}}
];
const byId = Object.fromEntries(CIDADES.map(c => [c.id, c]));
const map = L.map('map', {{scrollWheelZoom:false}}).setView([33.5, 113], 4);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{maxZoom:18, attribution:'&copy; OpenStreetMap'}}).addTo(map);
const coord = id => [byId[id].lat, byId[id].lon];
L.polyline(anel.map(coord), {{color:"#0b1220", weight:3}}).addTo(map);
variantes.forEach(v => L.polyline(v.ids.map(coord), {{color:v.cor, weight:2.5, dashArray:"7 6"}}).addTo(map));
CIDADES.forEach(c => {{
  const cor = c.id === "zhangjiajie" ? "#2f6b4f" : c.id === "guilin" ? "#1f6f8b" : c.id === "huangshan" ? "#7a4b2a" : "#0b1220";
  L.circleMarker([c.lat, c.lon], {{radius:8, color:cor, weight:3, fillColor:"#fff", fillOpacity:1}})
    .addTo(map)
    .bindPopup(`<b>${{c.emoji}} ${{c.nome}}</b><br>${{c.noites}} noites · ${{c.datas}}<br><a href="#" onclick="abrirCidade('${{c.id}}');return false;">ver detalhes →</a>`);
}});
function abrirCidade(id) {{
  trocarAba('roteiro');
  const d = document.getElementById('city-' + id);
  if (d) {{ d.open = true; d.scrollIntoView({{behavior:'smooth', block:'start'}}); }}
  map.closePopup();
}}
function trocarAba(nome) {{
  document.querySelectorAll('[data-tab]').forEach(b => b.setAttribute('aria-selected', b.dataset.tab === nome ? 'true' : 'false'));
  document.querySelectorAll('section[role=tabpanel]').forEach(s => s.classList.toggle('on', s.id === 'tab-' + nome));
  if (nome === 'roteiro') setTimeout(() => map.invalidateSize(), 60);
}}
document.querySelectorAll('[data-tab]').forEach(btn => btn.addEventListener('click', () => {{
  trocarAba(btn.dataset.tab);
  window.scrollTo({{top: 0, behavior:'smooth'}});
}}));
{JS}
</script>
<script>{EXTRA_JS}</script>\n</body>
</html>"""

    out = os.path.join(BASE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("salvo:", out, round(os.path.getsize(out) / 1024 / 1024, 2), "MB")


if __name__ == "__main__":
    main()
