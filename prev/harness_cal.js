const store = {};
function fakeEl(id){
  return store[id] || (store[id] = {id, innerHTML:'', dataset:{}, value:'',
    addEventListener(){}, appendChild(){}, setAttribute(){}, querySelector(){return {textContent:''}},
    querySelectorAll(){return {forEach(){}}}, classList:{add(){},remove(){},contains(){return false}}});
}
global.document = {
  getElementById: id => fakeEl(id),
  querySelectorAll: () => ({forEach(){}}),
  addEventListener(){},
  createElement: () => fakeEl('tmp'+Math.random()),
  body: {appendChild(){}}
};
global.window = {open(){}};
const src = require('fs').readFileSync('prev/L1.js','utf8');
eval(src);
const html = store['cal'].innerHTML;
const trips = (html.match(/class="cday trip"/g)||[]).length;
console.log('dias de viagem marcados:', trips);
const blocos = [...html.matchAll(/data-cid="([^"]+)"/g)].map(m=>m[1]);
console.log('primeiros 12:', blocos.slice(0,12).join(' '));
console.log('ultimos 6:', blocos.slice(-6).join(' '));
console.log('meses presentes:', html.includes('Dezembro 2026'), html.includes('Janeiro 2027'));
console.log('legenda:', (store['calleg'].innerHTML||'').slice(0,160));
