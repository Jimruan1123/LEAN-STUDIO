(function(root){
'use strict';
const G=typeof module==='object'&&module.exports?require('./graph.js'):root.LeanGraph;
const ID='WORKDESK-4040-001',params=[{key:'length_mm',label:'外部长度 X',min:380,max:3080},{key:'depth_mm',label:'外部宽度 Y',min:380,max:3080},{key:'frame_height_mm',label:'框架高度 Z',min:403,max:1203}],defaults={length_mm:1500,depth_mm:750,frame_height_mm:870};
function list(){return [{id:ID,name:'四立柱工作桌框架',category:'工作台',family:'NOPS-E4040t-probe-v1',defaults:{...defaults},parameters:params.map(p=>({...p})),status:'NEEDS_REVIEW'}]}
function create(id,p){if(id!==ID||!p||Object.keys(p).length!==3||!params.every(x=>Number.isInteger(p[x.key])&&p[x.key]>=x.min&&p[x.key]<=x.max))throw Error('模型或尺寸超出研究范围');const L=p.length_mm-80,D=p.depth_mm-80,H=p.frame_height_mm-3,g=G.empty(),posts={};
for(let i=0;i<2;i++)for(let j=0;j<2;j++){const post=G.insert(g,H,'Z',i*(L+40),j*(D+40),3);posts[i+''+j]=post.id;G.cap(g,post.id,'a');}
for(const level of ['top','bottom']){const z=3+(level==='top'?H-20:20);for(let j=0;j<2;j++){if(level==='bottom'&&j===0)continue;const b=G.insert(g,L,'X',20,j*(D+40),z);for(let i=0;i<2;i++)G.attach(g,posts[i+''+j],b.id,i?'right':'left',level);}for(let i=0;i<2;i++){const b=G.insert(g,D,'Y',i*(L+40),20,z);for(let j=0;j<2;j++)G.attach(g,posts[i+''+j],b.id,j?'right':'left',level);}}
g.mode='template';g.template={type:'workdesk',model_id:ID,model_revision:1,parameters:{...p},beam_mm:L,depth_mm:D,post_mm:H};return G.validate(g);}
function configure(g,p){if(g.mode!=='template'||g.template?.model_id!==ID||g.template.model_revision!==1)throw Error('当前不是可配置的标准工作桌');const base=create(ID,g.template.parameters);for(const k of ['parts','joints','connections'])if(JSON.stringify(g[k])!==JSON.stringify(base[k]))throw Error('已有非标变更：拒绝覆盖，请转自由设计');return create(ID,p);}
function selectedParameter(g,id){if(g.template?.model_id!==ID)return null;const p=g.parts.find(x=>x.id===id);if(p?.kind!=='profile')return null;return params.find(x=>x.key===(p.rotation[0][2]===1?'length_mm':p.rotation[1][2]===1?'depth_mm':'frame_height_mm'))||null;}
const api={list,create,configure,selectedParameter};if(typeof module==='object'&&module.exports){module.exports=api;return;}root.LeanModels=api;
const $=id=>document.getElementById(id),model=list()[0];
$('model-load').onclick=()=>root.leanApplyModel(()=>create(ID,model.defaults),'已调用工作桌模型；撤销可恢复原设计');
function update(){const g=root.leanState(),active=g.mode==='template'&&g.template?.model_id===ID,sel=selectedParameter(g,root.leanSelection());$('model-load').disabled=active;$('model-load').setAttribute('aria-pressed',String(active));$('model-config').hidden=!active;$('legacy-template-controls').hidden=active;if(!active)return;for(const p of params)$('model-'+p.key).value=g.template.parameters[p.key];$('model-group').hidden=!sel;if(sel){$('model-group-label').textContent='选中部位联动：'+sel.label;$('model-group-value').value=g.template.parameters[sel.key];$('model-group-value').min=sel.min;$('model-group-value').max=sel.max;}}
$('model-update').onclick=()=>root.leanApplyModel(g=>configure(g,Object.fromEntries(params.map(p=>[p.key,Number($('model-'+p.key).value)]))),'工作桌尺寸与BOM已联动');
$('model-group-update').onclick=()=>root.leanApplyModel(g=>{const p=selectedParameter(g,root.leanSelection());if(!p)throw Error('请选中型材');return configure(g,{...g.template.parameters,[p.key]:Number($('model-group-value').value)});},'选中部位所属尺寸已联动');
root.addEventListener('lean-update',update);update();
})(globalThis);
