
const CIDADES = [{"id": "pequim", "nome": "Pequim", "lat": 39.9042, "lon": 116.4074, "noites": 7, "datas": "30/12 – 06/01", "emoji": "🏯"}, {"id": "datong", "nome": "Datong", "lat": 40.09, "lon": 113.3, "noites": 2, "datas": "06 – 08/01", "emoji": "🗿"}, {"id": "pingyao", "nome": "Pingyao", "lat": 37.2, "lon": 112.18, "noites": 2, "datas": "08 – 10/01", "emoji": "🏮"}, {"id": "xian", "nome": "Xi'an", "lat": 34.3416, "lon": 108.9398, "noites": 3, "datas": "10 – 13/01", "emoji": "🏛️"}, {"id": "chongqing", "nome": "Chongqing", "lat": 29.563, "lon": 106.5516, "noites": 2, "datas": "13 – 15/01", "emoji": "🌉"}, {"id": "changsha", "nome": "Changsha", "lat": 28.2282, "lon": 112.9388, "noites": 2, "datas": "15 – 17/01 (A: 18 – 20/01)", "emoji": "🌶️"}, {"id": "xangai", "nome": "Xangai", "lat": 31.2304, "lon": 121.4737, "noites": 3, "datas": "20 – 23/01 (C: 17 – 22/01)", "emoji": "🏙️"}, {"id": "hangzhou", "nome": "Hangzhou", "lat": 30.2741, "lon": 120.1551, "noites": 1, "datas": "23 – 24/01", "emoji": "🍵"}, {"id": "nanjing", "nome": "Nanjing", "lat": 32.0603, "lon": 118.7969, "noites": 1, "datas": "24 – 25/01", "emoji": "🕯️"}, {"id": "zhangjiajie", "nome": "Zhangjiajie", "lat": 29.117, "lon": 110.479, "noites": 3, "datas": "15 – 18/01 (opção A)", "emoji": "🌄"}, {"id": "guilin", "nome": "Guilin / Yangshuo", "lat": 25.2736, "lon": 110.29, "noites": 3, "datas": "17 – 20/01 (opção B)", "emoji": "🛶"}, {"id": "huangshan", "nome": "Huangshan", "lat": 30.134, "lon": 118.161, "noites": 1, "datas": "23 – 24/01 (opção C)", "emoji": "⛰️"}];
const anel = ["pequim","datong","pingyao","xian","chongqing","changsha","xangai","hangzhou","nanjing","pequim"];
const variantes = [
  {cor:"#2f6b4f", ids:["chongqing","zhangjiajie","changsha"]},
  {cor:"#1f6f8b", ids:["changsha","guilin","xangai"]},
  {cor:"#7a4b2a", ids:["hangzhou","huangshan","nanjing"]}
];
const byId = Object.fromEntries(CIDADES.map(c => [c.id, c]));
const map = L.map('map', {scrollWheelZoom:false}).setView([33.5, 113], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:18, attribution:'&copy; OpenStreetMap'}).addTo(map);
const coord = id => [byId[id].lat, byId[id].lon];
L.polyline(anel.map(coord), {color:"#0b1220", weight:3}).addTo(map);
variantes.forEach(v => L.polyline(v.ids.map(coord), {color:v.cor, weight:2.5, dashArray:"7 6"}).addTo(map));
CIDADES.forEach(c => {
  const cor = c.id === "zhangjiajie" ? "#2f6b4f" : c.id === "guilin" ? "#1f6f8b" : c.id === "huangshan" ? "#7a4b2a" : "#0b1220";
  L.circleMarker([c.lat, c.lon], {radius:8, color:cor, weight:3, fillColor:"#fff", fillOpacity:1})
    .addTo(map)
    .bindPopup(`<b>${c.emoji} ${c.nome}</b><br>${c.noites} noites · ${c.datas}<br><a href="#" onclick="abrirCidade('${c.id}');return false;">ver detalhes →</a>`);
});
function abrirCidade(id) {
  trocarAba('roteiro');
  const d = document.getElementById('city-' + id);
  if (d) { d.open = true; d.scrollIntoView({behavior:'smooth', block:'start'}); }
  map.closePopup();
}
function trocarAba(nome) {
  document.querySelectorAll('nav.tabs a').forEach(b => b.setAttribute('aria-selected', b.dataset.tab === nome ? 'true' : 'false'));
  document.querySelectorAll('section[role=tabpanel]').forEach(s => s.classList.toggle('on', s.id === 'tab-' + nome));
  if (nome === 'roteiro') setTimeout(() => map.invalidateSize(), 60);
}
document.querySelectorAll('nav.tabs a').forEach(btn => btn.addEventListener('click', () => {
  trocarAba(btn.dataset.tab);
  window.scrollTo({top: 0, behavior:'smooth'});
}));

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

