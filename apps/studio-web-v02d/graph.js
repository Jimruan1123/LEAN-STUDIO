// LEAN-STUDIO V0.2-D | constrained 4040t assembly research probe
// Geometry assets are generated independently; engineering review is mandatory.
(function(root){
const FAMILY='NOPS-E4040t-probe-v1', IDs={profile:'NOPS-E4040t',bracket:'DEMO-E40-GUSSET',nut:'DEMO-M8-SLOT-NUT',screw:'DEMO-M8x12',cap:'DEMO-40-CAP'};
const I=[[1,0,0],[0,1,0],[0,0,1]],Y=[[0,0,1],[0,1,0],[-1,0,0]],S=[[0,0,1],[0,-1,0],[1,0,0]],Q=[[0,-1,0],[1,0,0],[0,0,1]];
const clone=x=>JSON.parse(JSON.stringify(x)), diag=(x,y,z)=>[[x,0,0],[0,y,0],[0,0,z]], add=(a,b)=>a.map((x,i)=>x+b[i]), mul=(r,v)=>r.map(a=>a.reduce((s,x,i)=>s+x*v[i],0)), mm=(a,b)=>a.map(r=>b[0].map((_,j)=>r.reduce((s,x,i)=>s+x*b[i][j],0))), point=(p,v)=>add(p.position,mul(p.rotation,v));
function length(v){v=Number(v);if(!Number.isFinite(v)||v<100||v>3000||!Number.isInteger(v))throw Error('长度必须为 100–3000 的整数 mm');return v}
function empty(){return {schema_version:'0.2-D',engineering_status:'NEEDS_REVIEW',family:FAMILY,mode:'free',seq:1,parts:[],joints:[],connections:[],template:null}}
function part(g,id,kind,pos,rot=I,l=null){if(g.parts.some(p=>p.id===id)||!IDs[kind])throw Error('零件 ID 重复或类型未知');let p={id,kind,part_id:IDs[kind],revision:'1',family:FAMILY,position:pos,rotation:clone(rot),length_mm:kind==='profile'?length(l):null};g.parts.push(p);return p}
function find(g,id){let p=g.parts.find(x=>x.id===id);if(!p)throw Error('零件不存在');return p}
function edge(g,a,b,type,port){g.joints.push({a,b,type,port})}
function corner(g,id,vertical,horizontal,side,level){
 let v=find(g,vertical),h=find(g,horizontal);if(v.kind!=='profile'||h.kind!=='profile'||v.family!==h.family||v.family!==FAMILY)throw Error('不兼容型材');
 let sx=side==='left'?1:-1,sz=level==='bottom'?1:-1;
 // Rotate the existing XZ fixture by 90 degrees about Z for YZ; full collision checks pending.
 const yAxis=h.rotation[1][2]===1, A=yAxis?Q:I, axis=yAxis?1:0, cross=yAxis?0:1;
 if(JSON.stringify(v.rotation)!==JSON.stringify(I)||JSON.stringify(h.rotation)!==JSON.stringify(yAxis?mm(Q,Y):Y))throw Error('请选择竖柱与 X/Y 向横梁');
 let z=h.position[2]+20*sz,x=v.position[axis]+20*sx,expected=sx===1?h.position[axis]:h.position[axis]+h.length_mm;
 if(Math.abs(x-expected)>1e-6||v.position[cross]!==h.position[cross]||z+19.5*sz<v.position[2]||z+19.5*sz>v.position[2]+v.length_mm||h.length_mm<40)throw Error('端面/槽口未对齐或超出有效范围');
 if(g.connections.some(c=>c.vertical===vertical&&c.horizontal===horizontal&&c.side===side&&c.level===level))throw Error('此接口已安装角码');
 let T=mm(A,diag(sx,sx*sz,sz)),pos=v.position.slice();pos[axis]=x;pos[2]=z;let b=part(g,id+'-bracket','bracket',pos,T);
 for(const [port,host,off,R] of [['v',vertical,[0,0,19.5],I],['h',horizontal,[19.5,0,0],S]]){let pos=point(b,off),rot=mm(T,R);part(g,id+'-'+port+'-nut','nut',pos,rot);part(g,id+'-'+port+'-screw','screw',pos,rot);edge(g,host,b.id,'slot_face_mate',port);edge(g,host,id+'-'+port+'-nut','slot_insert',port);edge(g,b.id,id+'-'+port+'-screw','clearance_hole',port);edge(g,id+'-'+port+'-nut',id+'-'+port+'-screw','thread_proxy',port)}
 g.connections.push({id,vertical,horizontal,side,level});
}
function cap(g,id,end){let p=find(g,id);if(p.kind!=='profile'||!['a','b'].includes(end))throw Error('端盖仅支持型材端面');let name=id+'-cap-'+end;part(g,name,'cap',point(p,[0,0,end==='b'?p.length_mm:0]),mm(p.rotation,end==='b'?I:diag(1,-1,-1)));edge(g,id,name,'end_cap',end)}
function frame(L=500,H=500){L=length(L);H=length(H);if(H<120)throw Error('框架高度至少120 mm');let g=empty();g.mode='template';g.template={beam_mm:L,post_mm:H};part(g,'left','profile',[0,0,0],I,H);part(g,'right','profile',[L+40,0,0],I,H);part(g,'bottom','profile',[20,0,20],Y,L);part(g,'top','profile',[20,0,H-20],Y,L);for(const v of ['left','right']){cap(g,v,'a');cap(g,v,'b');for(const h of ['bottom','top'])corner(g,v+'-'+h,v,h,v,h)}return g}
function frame3d(L=500,D=400,H=500){
 L=length(L);D=length(D);H=length(H);if(H<120)throw Error('框架高度至少120 mm');let g=empty();g.mode='template';g.template={type:'space',beam_mm:L,depth_mm:D,post_mm:H};
 for(let i=0;i<2;i++)for(let j=0;j<2;j++){let id='post-'+i+j;part(g,id,'profile',[i*(L+40),j*(D+40),0],I,H);cap(g,id,'a');cap(g,id,'b')}
 for(const level of ['bottom','top']){let z=level==='bottom'?20:H-20;for(let j=0;j<2;j++){let id='x-'+j+'-'+level;part(g,id,'profile',[20,j*(D+40),z],Y,L);for(let i=0;i<2;i++)corner(g,id+'-'+i,'post-'+i+j,id,i===0?'left':'right',level)}for(let i=0;i<2;i++){let id='y-'+i+'-'+level;part(g,id,'profile',[i*(L+40),20,z],mm(Q,Y),D);for(let j=0;j<2;j++)corner(g,id+'-'+j,'post-'+i+j,id,j===0?'left':'right',level)}}return g
}
function resizeFrame(g,L,H,D){if(g.mode!=='template')throw Error('仅标准框架支持整体尺寸修改');if(g.template?.type==='workdesk')throw Error('请使用工作桌模型参数');return g.template?.type==='space'?frame3d(L,D??g.template.depth_mm,H):frame(L,H)}
function toFree(g){if(g.mode!=='template')throw Error('当前已是自由模式');g.mode='free';g.template=null;return g}
function detach(g,id){if(g.mode!=='free')throw Error('请先转为自由设计');if(!g.connections.some(c=>c.id===id))throw Error('未选择连接');let dead=new Set(g.parts.filter(p=>p.id.startsWith(id+'-')).map(p=>p.id));g.parts=g.parts.filter(p=>!dead.has(p.id));g.joints=g.joints.filter(j=>!dead.has(j.a)&&!dead.has(j.b));g.connections=g.connections.filter(c=>c.id!==id)}
function componentWithout(g,start,excluded){const ids=new Set([start]),todo=[start];while(todo.length){let id=todo.pop();for(const e of g.joints){let next=e.a===id?e.b:e.b===id?e.a:null;if(next&&next!==excluded&&!ids.has(next)){ids.add(next);todo.push(next)}}}return ids}
function insert(g,l,orientation,x,y,z){if(g.mode!=='free')throw Error('切换至自由设计以新增零件');if(!['X','Y','Z'].includes(orientation))throw Error('方向无效');const p=[x,y,z].map(Number);if(!p.every(Number.isFinite))throw Error('坐标无效');return part(g,'P'+g.seq++,'profile',p,orientation==='X'?Y:orientation==='Y'?mm(Q,Y):I,l)}
function attach(g,vertical,horizontal,side,level,centerOffset){
 if(g.mode!=='free')throw Error('标准框架已配置角码');let h=find(g,horizontal),v=find(g,vertical);if(v.kind!=='profile'||h.kind!=='profile'||v.id===h.id||v.rotation[2][2]!==1||h.rotation[2][2]!==0)throw Error('请选择竖柱与 X/Y 向横梁');if(!['left','right'].includes(side)||!['bottom','top'].includes(level))throw Error('接口无效');
 let prior=g.connections.filter(c=>c.horizontal===horizontal);if(prior.some(c=>c.side===side))throw Error('该横梁端已连接，请先解除连接');const axis=h.rotation[1][2]===1?1:0,goal=v.position.slice();goal[axis]+=side==='left'?20:-20-h.length_mm;const offset=centerOffset===undefined?(level==='bottom'?20:v.length_mm-20):centerOffset;
 if(centerOffset!==undefined&&(!Number.isInteger(offset)||offset<(level==='bottom'?20:60)||offset>v.length_mm-(level==='bottom'?60:20)))throw Error('连接高度超出立柱和角码安装范围');
 goal[2]+=offset;
 if(prior.length){if(!goal.every((n,i)=>Math.abs(n-h.position[i])<1e-6))throw Error('第二端未对齐：请先移动未连接立柱或调整横梁长度');}else h.position=goal;
 corner(g,'C'+g.seq++,vertical,horizontal,side,level);if(centerOffset!==undefined)g.connections[g.connections.length-1].center_offset_mm=offset;updateCaps(g,h)
}
function resizeFree(g,id,L){L=length(L);if(g.mode!=='free')throw Error('标准框架请使用整体尺寸');let p=find(g,id);if(p.kind!=='profile')throw Error('固定件不能拉伸');if(L===p.length_mm)return;if(g.connections.some(c=>c.vertical===id))throw Error('关联立柱高度请使用标准框架参数或先解除连接');let cs=g.connections.filter(c=>c.horizontal===id),delta=L-p.length_mm,axis=p.rotation[1][2]===1?1:0;
 if(cs.length===2){let left=cs.find(c=>c.side==='left'),right=cs.find(c=>c.side==='right');if(!left||!right)throw Error('端点约束无效');let moving=componentWithout(g,right.vertical,id);if(moving.has(left.vertical))throw Error('闭环约束冲突：请用标准框架尺寸或先解除一个连接');for(const part of g.parts)if(moving.has(part.id))part.position[axis]+=delta;
 }else if(cs.length===1&&cs[0].side==='right')p.position[axis]-=delta;
 p.length_mm=L;updateCaps(g,p)
}
function updateCaps(g,p){for(const e of ['a','b']){const q=g.parts.find(x=>x.id===p.id+'-cap-'+e);if(q)q.position=point(p,[0,0,e==='b'?p.length_mm:0])}}
function canMove(g,id){return g.mode==='free'&&g.parts.some(p=>p.id===id&&p.kind==='profile')&&!g.connections.some(c=>c.vertical===id||c.horizontal===id)}
function move(g,id,pos,snap=false){if(!canMove(g,id))throw Error('仅未连接型材可移动；关联件请调整长度或先删除连接');if(!Array.isArray(pos)||pos.length!==3||!pos.every(Number.isFinite))throw Error('坐标无效');let p=find(g,id);p.position=pos.map(v=>Math.round(v));updateCaps(g,p);if(!snap||p.rotation[2][2]===1)return false;let axis=p.rotation[1][2]===1?1:0,candidates=[];for(const v of g.parts.filter(q=>q.kind==='profile'&&q.rotation[2][2]===1&&q.id!==id)){for(const side of ['left','right'])for(const level of ['bottom','top']){let goal=v.position.slice();goal[axis]+=side==='left'?20:-20-p.length_mm;goal[2]+=level==='bottom'?20:v.length_mm-20;let d=Math.hypot(...goal.map((n,i)=>n-p.position[i]));if(d<=30)candidates.push({v,side,level,d})}}candidates.sort((a,b)=>a.d-b.d);if(candidates.length&&(!candidates[1]||candidates[1].d-candidates[0].d>0.001)){let c=candidates[0];attach(g,c.v.id,id,c.side,c.level);return true}return false}
function remove(g,id){if(g.mode!=='free')throw Error('标准模板不支持单件删除');let p=find(g,id);if(p.kind!=='profile')throw Error('本轮仅删除型材及关联组件');let dead=new Set([id]);for(const c of g.connections.filter(c=>c.vertical===id||c.horizontal===id))for(const p of g.parts)if(p.id.startsWith(c.id+'-'))dead.add(p.id);for(const p of g.parts)if(p.id.startsWith(id+'-cap-'))dead.add(p.id);g.parts=g.parts.filter(p=>!dead.has(p.id));g.joints=g.joints.filter(e=>!dead.has(e.a)&&!dead.has(e.b));g.connections=g.connections.filter(c=>c.vertical!==id&&c.horizontal!==id)}
function bom(g){let m=new Map();for(const p of g.parts){let k=p.part_id+'|'+(p.length_mm??'');if(!m.has(k))m.set(k,{part_id:p.part_id,kind:p.kind,length_mm:p.length_mm,qty:0});m.get(k).qty++}return [...m.values()].sort((a,b)=>a.part_id.localeCompare(b.part_id)||(a.length_mm??0)-(b.length_mm??0))}
function validate(g){if(g.schema_version!=='0.2-D'||g.family!==FAMILY||!['free','template'].includes(g.mode)||!Array.isArray(g.parts)||!Array.isArray(g.joints)||!Array.isArray(g.connections)||!Number.isInteger(g.seq)||g.seq<1)throw Error('文件版本或结构无效');let ids=new Set();for(const p of g.parts){if(typeof p.id!=='string'||!/^[A-Za-z0-9_-]+$/.test(p.id)||ids.has(p.id)||p.family!==FAMILY||p.part_id!==IDs[p.kind]||p.revision!=='1'||!Array.isArray(p.position)||p.position.length!==3||!p.position.every(Number.isFinite)||!Array.isArray(p.rotation)||p.rotation.length!==3||!p.rotation.every(r=>Array.isArray(r)&&r.length===3&&r.every(x=>[-1,0,1].includes(x)))||JSON.stringify(mm(p.rotation,p.rotation[0].map((_,i)=>p.rotation.map(r=>r[i]))))!==JSON.stringify(I))throw Error('零件数据无效');if(p.kind==='profile')length(p.length_mm);else if(p.length_mm!==null)throw Error('固定件参数无效');ids.add(p.id)}for(const j of g.joints)if(!ids.has(j.a)||!ids.has(j.b))throw Error('装配边存在失效 ID');for(const c of g.connections)if(!ids.has(c.vertical)||!ids.has(c.horizontal)||!ids.has(c.id+'-bracket'))throw Error('连接记录失效');g.engineering_status='NEEDS_REVIEW';return g}
const api={empty,frame,frame3d,toFree,detach,resizeFrame,insert,attach,cap,resizeFree,remove,bom,validate,clone,find,point,canMove,move};if(typeof module!=='undefined')module.exports=api;else root.LeanGraph=api;
})(globalThis);
