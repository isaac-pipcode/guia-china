const store = {};
function fakeEl(id){
  return store[id] || (store[id] = {id, innerHTML:'', dataset:{}, value:'',
    addEventListener(){}, appendChild(){}, setAttribute(){}, querySelector(){return {textContent:''}},
    querySelectorAll(){return {forEach(){}}}, classList:{add(){},remove(){},contains(){return false}}});
}
global.document = { getElementById: id => fakeEl(id), querySelectorAll: () => ({forEach(){}}),
  addEventListener(){}, createElement: () => fakeEl('t'+Math.random()), body:{appendChild(){}} };
global.window = {open(){}};
eval(require('fs').readFileSync('prev/L1.js','utf8'));
require('fs').writeFileSync('prev/cal_inner.html', store['cal'].innerHTML);
require('fs').writeFileSync('prev/cal_leg.html', store['calleg'].innerHTML);
console.log('gerado', store['cal'].innerHTML.length, 'chars');
