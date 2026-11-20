const store = {};
const progs = {};
function box(id){ return {id, checked:false, _l:{}, addEventListener(e,f){this._l[e]=f}}; }
const boxes = [];
['m','f','c'].forEach(p => { for (let g=0; g<3; g++) for (let i=0; i<2; i++) boxes.push(box(`${p}-${g}-${i}`)); });
global.document = {
  querySelectorAll: sel => sel.includes('checkbox') ? boxes : {forEach(){}},
  getElementById: id => store[id] || (store[id] = {textContent:'', innerHTML:'', dataset:{}, value:'', addEventListener(e,f){this._l=this._l||{};this._l[e]=f}, querySelectorAll(){return {forEach(){}}}, appendChild(){}, setAttribute(){}, querySelector(){return {textContent:''}}, classList:{add(){},remove(){},contains(){return false}}}),
  addEventListener(){}, createElement: () => (store['tmp'+Math.random()] = {textContent:'', innerHTML:'', dataset:{}, value:'', style:{}, addEventListener(e,f){this._l=this._l||{};this._l[e]=f}, querySelectorAll(){return {forEach(){}}}, appendChild(){}, setAttribute(){}, querySelector(){return {textContent:''}}, classList:{add(){},remove(){},contains(){return false}}}), body:{appendChild(){}}
};
global.window = {open(){}};
global.localStorage = {_d:{}, getItem(k){return this._d[k]||null}, setItem(k,v){this._d[k]=v}, removeItem(k){delete this._d[k]}};
eval(require('fs').readFileSync('prev/T1.js','utf8'));
console.log('total inicial:', store['mala-total'].textContent);
boxes[0].checked = true; boxes[0]._l.change();
boxes[1].checked = true; boxes[1]._l.change();
console.log('após 2 marcas:', store['mala-total'].textContent);
console.log('salvo no storage:', JSON.parse(localStorage.getItem('mala_v1')));
