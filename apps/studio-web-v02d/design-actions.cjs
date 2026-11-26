'use strict';
// Offline AI-facing adapter probe. Not loaded by the public web UI.
const G=require('./graph.js');
const CONTRACT='lean-actions/0.1';
const int=(v,min,max)=>Number.isInteger(v)&&v>=min&&v<=max;
const size=v=>int(v,100,3000);
const xyz=v=>Array.isArray(v)&&v.length===3&&v.every(n=>int(n,-100000,100000));
const one=(v,choices)=>choices.includes(v);
const ref=v=>typeof v==='string'&&/^(\$?[A-Za-z0-9_-]{1,80})$/.test(v);
const alias=v=>typeof v==='string'&&/^\$[A-Za-z][A-Za-z0-9_-]{0,39}$/.test(v);
const rules={
  create_profile:{length_mm:size,axis:v=>one(v,['X','Y','Z']),position_mm:xyz,as:alias},
  connect:{vertical:ref,horizontal:ref,side:v=>one(v,['left','right']),level:v=>one(v,['bottom','top'])},
  move_part:{id:ref,position_mm:xyz,auto_snap:v=>typeof v==='boolean'},
  resize_part:{id:ref,length_mm:size},
  add_end_cap:{id:ref,end:v=>one(v,['a','b'])},
  detach:{id:ref},remove_part:{id:ref},
  convert_to_free:{},
  create_space_frame:{length_mm:size,depth_mm:size,height_mm:size,replace_existing:v=>typeof v==='boolean'},
  resize_frame:{length_mm:size,depth_mm:size,height_mm:size}
};
function diff(before,after){const a=new Map(before.parts.map(p=>[p.id,p])),b=new Map(after.parts.map(p=>[p.id,p]));return {added:[...b.keys()].filter(k=>!a.has(k)),removed:[...a.keys()].filter(k=>!b.has(k)),changed:[...b.keys()].filter(k=>a.has(k)&&JSON.stringify(a.get(k))!==JSON.stringify(b.get(k))),joint_delta:after.joints.length-before.joints.length};}
function preview(graph,request){let step=-1;try{
  if(!request||request.contract!==CONTRACT||!Array.isArray(request.actions)||request.actions.length<1||request.actions.length>200)throw Error('Invalid action contract or batch size');
  const before=G.validate(G.clone(graph));let g=G.clone(before),refs=new Map();
  const id=v=>{if(v.startsWith('$')){if(!refs.has(v))throw Error('Unknown alias '+v);return refs.get(v);}return v;};
  for(const a of request.actions){step++;if(!a||!Object.hasOwn(rules,a.op)||!a.args||typeof a.args!=='object'||Array.isArray(a.args))throw Error('Unsupported action');const r=rules[a.op],p=a.args;if(Object.keys(p).length!==Object.keys(r).length||Object.keys(r).some(k=>!Object.hasOwn(p,k)||!r[k](p[k])))throw Error('Invalid arguments for '+a.op);
    switch(a.op){
      case 'create_profile':if(refs.has(p.as))throw Error('Duplicate alias');refs.set(p.as,G.insert(g,p.length_mm,p.axis,...p.position_mm).id);break;
      case 'connect':G.attach(g,id(p.vertical),id(p.horizontal),p.side,p.level);break;
      case 'move_part':G.move(g,id(p.id),p.position_mm,p.auto_snap);break;
      case 'resize_part':G.resizeFree(g,id(p.id),p.length_mm);break;
      case 'add_end_cap':G.cap(g,id(p.id),p.end);break;
      case 'detach':G.detach(g,id(p.id));break;
      case 'remove_part':G.remove(g,id(p.id));break;
      case 'convert_to_free':G.toFree(g);break;
      case 'create_space_frame':if(g.parts.length&&!p.replace_existing)throw Error('Explicit replacement required');g=G.frame3d(p.length_mm,p.depth_mm,p.height_mm);refs.clear();break;
      case 'resize_frame':g=G.resizeFrame(g,p.length_mm,p.height_mm,p.depth_mm);break;
    }G.validate(g);
  }
  return {ok:true,contract:CONTRACT,preview_only:true,engineering_status:'NEEDS_REVIEW',graph:g,diff:diff(before,g),bom:G.bom(g),aliases:Object.fromEntries(refs)};
}catch(e){return {ok:false,contract:CONTRACT,preview_only:true,failed_action_index:step,error:String(e.message),engineering_status:'NEEDS_REVIEW'};}}
module.exports={CONTRACT,preview};
