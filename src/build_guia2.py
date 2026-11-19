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

spec = importlib.util.spec_from_file_location("bg", os.path.join(BASE, "src", "build_guia.py"))
bg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bg)

CIDADES = bg.CIDADES
DATA_IN, DATA_OUT = bg.DATA_IN, bg.DATA_OUT
svg_schema = bg.svg_schema
gmaps = bg.gmaps


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
    ("Chongqing → bloco de natureza", "15/01", "4h30", "~01/01/2027"),
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

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>China em 30 dias · guia da viagem</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>{CSS}</style>
</head>
<body>

<div class="hero">
  <img src="{hero}" alt="Grande Muralha sob a neve">
  <div class="wrap cap-hero">
    <h1>China em 30 dias</h1>
    <div class="sub">Um trajeto só, do norte imperial ao delta do Yangtzé</div>
  </div>
  <div class="credit">Badaling sob a neve · {credito['autor']} / Wikimedia ({credito['licenca']})</div>
</div>

<div class="navwrap">
  <div class="wrap">
    <nav class="tabs" role="tablist">
      <a role="tab" href="#roteiro" data-tab="roteiro" aria-selected="true">Roteiro</a>
      <a role="tab" href="#aereo" data-tab="aereo" aria-selected="false">Passagens aéreas</a>
      <a role="tab" href="#trens" data-tab="trens" aria-selected="false">Trens</a>
      <a role="tab" href="#hoteis" data-tab="hoteis" aria-selected="false">Hospedagens</a>
      <a role="tab" href="#passeios" data-tab="passeios" aria-selected="false">Passeios</a>
      <a role="tab" href="#preparo" data-tab="preparo" aria-selected="false">Preparo</a>
    </nav>
  </div>
</div>

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
  document.querySelectorAll('nav.tabs a').forEach(b => b.setAttribute('aria-selected', b.dataset.tab === nome ? 'true' : 'false'));
  document.querySelectorAll('section[role=tabpanel]').forEach(s => s.classList.toggle('on', s.id === 'tab-' + nome));
  if (nome === 'roteiro') setTimeout(() => map.invalidateSize(), 60);
}}
document.querySelectorAll('nav.tabs a').forEach(btn => btn.addEventListener('click', () => {{
  trocarAba(btn.dataset.tab);
  window.scrollTo({{top: 0, behavior:'smooth'}});
}}));
{JS}
</script>
</body>
</html>"""

    out = os.path.join(BASE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("salvo:", out, round(os.path.getsize(out) / 1024 / 1024, 2), "MB")


if __name__ == "__main__":
    main()
