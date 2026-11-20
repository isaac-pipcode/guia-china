
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
    pequim:['Pequim','#12263a'], datong:['Datong','#4b5d6e'], pingyao:['Pingyao','#b3402a'],
    xian:["Xi'an",'#b5741f'], chongqing:['Chongqing','#0f766e'], changsha:['Changsha','#c2410c'],
    zhangjiajie:['Zhangjiajie','#2f6b4f'], guilin:['Guilin','#1f6f8b'], xangai:['Xangai','#3730a3'],
    hangzhou:['Hangzhou','#15803d'], huangshan:['Huangshan','#7a4b2a'], nanjing:['Nanjing','#6b21a8']
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
    let html = '';
    MESES.forEach(([ano, mes, nome]) => {
      const primeiro = new Date(Date.UTC(ano, mes, 1));
      const dias = new Date(Date.UTC(ano, mes + 1, 0)).getUTCDate();
      html += '<div class="cal"><h4>' + nome + '</h4><div class="calgrid">';
      html += WD.map(w => '<div class="wd">' + w + '</div>').join('');
      for (let i = 0; i < primeiro.getUTCDay(); i++) html += '<div></div>';
      for (let d = 1; d <= dias; d++) {
        const atual = iso(new Date(Date.UTC(ano, mes, d)));
        const cid = cidade(atual, cen);
        if (cid) {
          const [nomeCid, cor] = CID[cid];
          html += '<div class="cday trip" style="background:' + cor + '" data-cid="' + cid + '" title="' + nomeCid + '">'
                + d + '<span class="cn">' + nomeCid + '</span></div>';
        } else {
          html += '<div class="cday notrip">' + d + '</div>';
        }
      }
      html += '</div></div>';
    });
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
      .map(([cid, [nome, cor]]) => '<span><i style="background:' + cor + '"></i>' + nome + '</span>').join('');
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
