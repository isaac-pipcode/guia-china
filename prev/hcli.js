const store = {};
function mkEl(ds){ const e={dataset:Object.assign({},ds), innerHTML:'', textContent:'', className:'clima',
  addEventListener(){}, setAttribute(){}, querySelectorAll(){return {forEach(){}}}, appendChild(){},
  classList:{add(){},remove(){},contains(){return false}} }; return e; }
const alvos = [
  mkEl({clima:'39.9042,116.4074,12-30,01-06'}),
  mkEl({clima:'34.3416,108.9398,01-10,01-13'}),
  mkEl({clima:'31.2304,121.4737,01-20,01-23'}),
];
global.document = {
  querySelectorAll: sel => sel === '.clima' ? alvos : [],
  getElementById: id => store[id] || (store[id] = mkEl({})),
  addEventListener(){}, createElement: () => mkEl({}), body:{appendChild(){}}
};
global.window = {open(){}};
global.localStorage = {getItem(){return null;}, setItem(){}};
global.IntersectionObserver = class { constructor(cb){this.cb=cb;} observe(el){ this.cb([{isIntersecting:true,target:el}]); } unobserve(){} };
eval(require('fs').readFileSync('prev/S1.js','utf8'));
setTimeout(()=>{
  alvos.forEach((e,i)=>console.log((i+1)+':', e.innerHTML.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim() || e.textContent || '(vazio)'));
}, 9000);
