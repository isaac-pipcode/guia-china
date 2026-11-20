const els = {};
function el(id){ return els[id] || (els[id] = {id, value:'', textContent:'', _l:{}, addEventListener(ev,fn){this._l[ev]=fn;}, classList:{add(){},remove(){}}, querySelectorAll(){return {forEach(){}}}, appendChild(){}, setAttribute(){}, querySelector(){return {textContent:''}} }); }
global.document = { getElementById: el, querySelectorAll: () => ({forEach(){}}), addEventListener(){}, createElement: () => el('t'+Math.random()), body:{appendChild(){}} };
global.window = {open(){}};
global.fetch = async (url) => {
  if (url.includes('er-api')) return { json: async () => ({ result:'success', time_last_update_utc:'Fri, 20 Nov 2026 00:02:32 +0000', rates:{ BRL: 0.882223 } }) };
  throw new Error('sem rede');
};
el('cny').value = '100';
eval(require('fs').readFileSync('prev/N1.js','utf8'));
setTimeout(() => {
  console.log('100 CNY =>', els['brl'].value, '(esperado 88.22)');
  console.log('taxa:', els['rate'].textContent);
  console.log('fonte:', els['rate-src'].textContent);
  els['brl'].value = '500';
  if (els['brl']._l.input) els['brl']._l.input();
  else console.log('sem listener de input em brl');
  setTimeout(()=>console.log('500 BRL =>', els['cny'].value, 'CNY (esperado 566.75)'), 20);
}, 150);
