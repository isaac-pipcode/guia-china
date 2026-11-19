
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
