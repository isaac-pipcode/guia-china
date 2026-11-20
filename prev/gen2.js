const store={};
function el(id){ return store[id]||(store[id]={id,innerHTML:'',textContent:'',dataset:{},value:'',style:{},
  addEventListener(){},appendChild(){},setAttribute(){},querySelector(){return{textContent:''}},
  querySelectorAll(){return{forEach(){}}},classList:{add(){},remove(){},contains(){return false}}}); }
global.document={getElementById:el,querySelectorAll:()=>({forEach(){}}),addEventListener(){},
  createElement:()=>el('t'+Math.random()),body:{appendChild(){}}};
global.window={open(){}}; global.localStorage={getItem(){return null},setItem(){},removeItem(){}};
global.IntersectionObserver=class{constructor(cb){this.cb=cb}observe(){}unobserve(){}};
eval(require('fs').readFileSync('prev/W1.js','utf8'));
require('fs').writeFileSync('prev/cal2.html', store['cal'].innerHTML);
require('fs').writeFileSync('prev/leg2.html', store['calleg'].innerHTML);
console.log('ok', store['cal'].innerHTML.length);
