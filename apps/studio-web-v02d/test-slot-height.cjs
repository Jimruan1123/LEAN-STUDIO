const a=require('node:assert/strict'),G=require('./graph.js'),A=require('./design-actions.cjs');
const g=G.empty(),l=G.insert(g,867,'Z',0,0,3),r=G.insert(g,867,'Z',1460,0,3),b=G.insert(g,1420,'X',20,0,203);
G.attach(g,l.id,b.id,'left','bottom',200);G.attach(g,r.id,b.id,'right','bottom',200);a.equal(b.position[2],203);a.equal(g.parts.length,13);a.equal(g.joints.length,16);a.equal(g.connections[1].center_offset_mm,200);a.equal(G.find(g,'C4-bracket').position[2],223);console.log('PASS custom height and dual-end hardware');
a.deepEqual(G.validate(JSON.parse(JSON.stringify(g))),g);console.log('PASS JSON roundtrip');
const f=G.empty(),v=G.insert(f,500,'Z',0,0,0),h=G.insert(f,400,'Y',0,20,0),before=G.clone(f);a.throws(()=>G.attach(f,v.id,h.id,'left','bottom',480));a.deepEqual(f,before);console.log('PASS reject out of range before mutation');
const req={contract:A.CONTRACT,actions:[{op:'connect_at',args:{vertical:v.id,horizontal:h.id,side:'left',level:'top',center_offset_mm:200}}]};const out=A.preview(f,req);a.equal(out.ok,true,JSON.stringify(out));a.equal(G.find(out.graph,h.id).position[2],200);a.deepEqual(f,before);console.log('PASS AI preview custom height');
const prev=G.clone(g);a.throws(()=>G.attach(g,r.id,b.id,'right','top',200));a.deepEqual(g,prev);console.log('PASS duplicate endpoint rejected');
