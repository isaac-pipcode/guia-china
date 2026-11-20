const els = {};
function el(id){ return els[id] || (els[id] = {id, value:'', textContent:'', _l:{}, dataset:{},
  addEventListener(ev,fn){this._l[ev]=fn;}, classList:{add(){},remove(){},contains(){return false}},
  querySelectorAll(){return {forEach(){}}}, appendChild(){}, setAttribute(){}, querySelector(){return {textContent:''}} }); }
global.document = { getElementById: el, querySelectorAll: () => ({forEach(){}}), addEventListener(){},
  createElement: () => el('t'+Math.random()), body:{appendChild(){}} };
global.window = {open(){}};
global.fetch = async () => ({ json: async () => ({ time_last_update_utc:'Fri, 20 Nov 2026 00:02:32 +0000', rates:{ BRL: 0.882223 } }) });
el('cny').value = '100';
eval(require('fs').readFileSync('prev/P1.js','utf8'));
setTimeout(()=>{
  console.log('100 CNY =', els['brl'].value);
  ['ref1','ref2','ref3','ref4','ref5'].forEach(k=>console.log(k, '=>', els[k].textContent));
}, 200);
