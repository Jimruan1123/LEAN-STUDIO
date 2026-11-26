"""Offline research probe. GPL-3.0-or-later profile adaptation; see README.
Bracket uses upstream dimensions; hardware simplified independently, no threads or spring ball.
"""
import json, subprocess, pathlib, hashlib, tempfile
import numpy as np
import trimesh as tm
import cadquery as cq
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
R=pathlib.Path(__file__).parent
F='NOPS-E4040t-probe-v1'

def profile(l):
 p=R/f'profile-{l}.stl';subprocess.run(['openscad','-o',str(p),'-D',f'length={l}',str(R/'profile.scad')],check=True,capture_output=True)
 m=tm.load_mesh(p);assert m.is_watertight and len(m.split())==1 and np.allclose(m.extents,[40,40,l],atol=.001)
 cut=m.section(plane_origin=[0,0,l/2],plane_normal=[0,0,1]);rings=sorted([Polygon(a[:,:2]) for a in cut.discrete],key=lambda p:p.area,reverse=True);s=rings[0].difference(unary_union(rings[1:]));assert s.is_valid
 return m,s

def b(x,y,z,a,b,c):return cq.Solid.makeBox(a,b,c,cq.Vector(x,y,z))
def cyl(r,l,p,d):return cq.Solid.makeCylinder(r,l,cq.Vector(*p),cq.Vector(*d))
def mesh(shape):
 assert shape.isValid() and len(shape.Solids())==1
 with tempfile.TemporaryDirectory() as td:
  p=pathlib.Path(td)/'m.stl';cq.exporters.export(shape,str(p),tolerance=.08,angularTolerance=.12);m=tm.load_mesh(p)
 assert m.is_watertight and m.volume>0
 return m

def bracket():
 # 40 x 40 legs, 35 width, 2 mm base, 3 mm gussets, hole center 19.5.
 s=b(0,-17.5,0,40,35,2).fuse(b(0,-17.5,0,2,35,40))
 for y in (-17.5,14.5):
  w=cq.Wire.makePolygon([cq.Vector(x,y,z) for x,z in [(0,0),(40,0),(0,40),(0,0)]])
  s=s.fuse(cq.Solid.extrudeLinear(w,[],cq.Vector(0,3,0)))
 # slotted hole, 8.6 clearance; 3 mm travel, same on both legs
 for a in (18,21):
  s=s.cut(cyl(4.3,4,(a,0,-1),(0,0,1))).cut(cyl(4.3,4,(-1,0,a),(1,0,0)))
 s=s.cut(b(18,-4.3,-1,3,8.6,4)).cut(b(-1,-4.3,18,4,8.6,3))
 return s.clean()

def nut(): # independent simplified block, upstream nominal length/width/thickness; no ball or thread
 return b(-10.7,-6.75,-11,6.7,13.5,22).cut(cyl(4.05,8,(-11,0,0),(1,0,0))).clean()
def screw(): # M8 x 12 demo; no thread/socket geometry; head OD 13, h8
 return cyl(4,12,(-10,0,0),(1,0,0)).fuse(cyl(6.5,8,(2,0,0),(1,0,0))).clean()
def cap():return b(-20,-20,0,40,40,3) # visual-only flat cap, no retention feature

def tf(Rot,p):
 t=np.eye(4);t[:3,:3]=Rot;t[:3,3]=p;return t
I=np.eye(3);Y90=np.array([[0,0,1],[0,1,0],[-1,0,0]])
SWAP=np.array([[0,0,1],[0,-1,0],[1,0,0]]) # +x -> +z, proper rotation
GL=np.array([[.001,0,0,0],[0,0,.001,0],[0,-.001,0,0],[0,0,0,1]])
colors={'profile':[175,186,195,255],'bracket':[210,213,216,255],'nut':[87,98,108,255],'screw':[77,88,98,255],'cap':[40,48,56,255]}

def graph(L,H=500):
 parts=[];edges=[]
 def add(id,k,T,l=None):
  parts.append(dict(id=id,part_id={'profile':'NOPS-E4040t','bracket':'DEMO-E40-GUSSET','nut':'DEMO-M8-SLOT-NUT','screw':'DEMO-M8x12','cap':'DEMO-40-CAP'}[k],revision='1',kind=k,length_mm=l,pose_mm=T.tolist(),family=F))
 for id,x in [('left',0),('right',L+40)]:
  add(id,'profile',tf(I,[x,0,0]),H)
  add(id+'-cap-top','cap',tf(I,[x,0,H]));add(id+'-cap-bottom','cap',tf(np.diag([1,-1,-1]),[x,0,0]));edges.extend([dict(a=id,b=id+'-cap-top',type='end_cap',interface='end_b'),dict(a=id,b=id+'-cap-bottom',type='end_cap',interface='end_a')])
 for id,z in [('bottom',20),('top',H-20)]:add(id,'profile',tf(Y90,[20,0,z]),L)
 for side,sx,x in [('left',1,20),('right',-1,L+20)]:
  for level,sz,z in [('bottom',1,40),('top',-1,H-40)]:
   name=f'{side}-{level}';T=tf(np.diag([sx,sx*sz,sz]),[x,0,z]);add(name+'-bracket','bracket',T)
   for k,host,loc in [('v',side,tf(I,[0,0,19.5])),('h',level,tf(SWAP,[19.5,0,0]))]:
    add(name+'-'+k+'-nut','nut',T@loc);add(name+'-'+k+'-screw','screw',T@loc)
    edges.extend([dict(a=host,b=name+'-bracket',type='slot_face_mate',port=k),dict(a=host,b=name+'-'+k+'-nut',type='slot_insert',port=k),dict(a=name+'-bracket',b=name+'-'+k+'-screw',type='clearance_hole',port=k),dict(a=name+'-'+k+'-nut',b=name+'-'+k+'-screw',type='thread_proxy',port=k)])
 from collections import Counter
 counts=Counter((p['part_id'],p['length_mm'] or 0) for p in parts)
 return dict(schema_version='0.2-probe',engineering_status='NEEDS_REVIEW',width_mm=L+80,height_mm=H+6,beam_length_mm=L,parts=parts,joints=edges,bom=[dict(part_id=k,length_mm=l or None,qty=q) for (k,l),q in sorted(counts.items())])

def scene(g,meshes):
 s=tm.Scene()
 for p in g['parts']:
  m=meshes[(p['kind'],p['length_mm'])].copy();m.visual.face_colors=colors[p['kind']];m.apply_transform(np.array(p['pose_mm']));m.apply_transform(GL);s.add_geometry(m,node_name=p['id'],geom_name=p['id'])
 return s

def main():
 meshes={};secs={}
 for l in (500,800):meshes[('profile',l)],secs[l]=profile(l)
 for k,fn in [('bracket',bracket),('nut',nut),('screw',screw),('cap',cap)]:meshes[(k,None)]=mesh(fn())
 a,bg=graph(500),graph(800);p=secs[500];tests=[]
 def test(name,cond):assert cond,name;tests.append(name);print('PASS',name)
 test('E4040t section invariant 500 to 800',p.symmetric_difference(secs[800]).area<.01)
 # Local outer face x=20, rectangular nut envelope behind lip, screw through slot.
 test('nut cross-section envelope clear of profile',p.intersection(box(9.3,-6.75,16,6.75)).area<1e-6)
 test('M8 shank through slot envelope clear',p.intersection(box(10,-4,20,4)).area<1e-6)
 test('bracket clearance vs screw shank',bracket().intersect(screw().translate(cq.Vector(0,0,19.5))).Volume()<1e-6)
 test('nut hole vs screw shank proxy',nut().intersect(screw()).Volume()<1e-6)
 test('28 instances and 36 graph edges',len(a['parts'])==28 and len(a['joints'])==36)
 test('all graph endpoints exist',all(e['a'] in {q['id'] for q in a['parts']} and e['b'] in {q['id'] for q in a['parts']} for e in a['joints']))
 test('length update keeps IDs, joints and hardware counts',a['joints']==bg['joints'] and [q['id'] for q in a['parts']]==[q['id'] for q in bg['parts']] and len(a['parts'])==len(bg['parts']))

 for g in (a,bg):
  pp={q['id']:q for q in g['parts']}
  def point(q,v):return (np.array(q['pose_mm']) @ np.array([*v,1]))[:3]
  matches=[]
  for side in ('left','right'):
   for level in ('bottom','top'):
    name=f'{side}-{level}';br=pp[name+'-bracket']
    for port,host,v in [('v',pp[side],[0,0,19.5]),('h',pp[level],[19.5,0,0])]:
     pt=point(br,v);local=(np.linalg.inv(np.array(host['pose_mm'])) @ np.array([*pt,1]))[:3]
     matches.append(abs(abs(local[0])-20)<1e-6 and abs(local[1])<1e-6 and 0<=local[2]<=host['length_mm'] and np.allclose(pt,point(pp[name+'-'+port+'-nut'],[0,0,0])) and np.allclose(pt,point(pp[name+'-'+port+'-screw'],[0,0,0])))
  test(f'8 bracket/slot/fastener anchors match at {g["beam_length_mm"]}',len(matches)==8 and all(matches))
 test('right-side subtree follows +300 mm; left-side fixed',all(np.allclose(np.array(q2['pose_mm'])[:3,3]-np.array(q1['pose_mm'])[:3,3],[300 if q1['id'].startswith('right') else 0,0,0]) for q1,q2 in zip(a['parts'],bg['parts'])))
 for g in (a,bg):
  ss=scene(g,meshes);out=R/f'frame-{g["beam_length_mm"]}';out.mkdir(exist_ok=True);(out/'assembly.json').write_text(json.dumps(g,indent=2));(out/'assembly.glb').write_bytes(ss.export(file_type='glb'));load=tm.load(out/'assembly.glb',force='scene');test(f'GLB roundtrip {g["beam_length_mm"]} named instances and bounds',len(load.graph.nodes_geometry)==28 and np.allclose(load.extents,[g['width_mm']/1000,g['height_mm']/1000,.04],atol=1e-5))
  test(f'JSON roundtrip {g["beam_length_mm"]}',json.loads((out/'assembly.json').read_text())==g)
 # assets with ID, geometry hash, own local coordinates, minimal metadata
 assets=R/'parts';assets.mkdir(exist_ok=True)
 for (k,l),m in meshes.items():
  if k=='profile' and l!=500:continue
  pp=next(q for q in a['parts'] if q['kind']==k);folder=assets/pp['part_id'];folder.mkdir(exist_ok=True);v=m.copy();v.visual.face_colors=colors[k];v.apply_transform(GL);f=folder/'part.glb';f.write_bytes(v.export(file_type='glb'))
  interfaces={'profile':[{'id':'end_a','position':[0,0,0],'direction':[0,0,-1]},{'id':'end_b','position':[0,0,500],'position_rule':'[0,0,length_mm]','direction':[0,0,1]}]+[{'id':f'slot_{i}','type':'slot_line','position':pos,'direction':normal,'axis':[0,0,1]} for i,(pos,normal) in enumerate([([20,0,0],[1,0,0]),([-20,0,0],[-1,0,0]),([0,20,0],[0,1,0]),([0,-20,0],[0,-1,0])])],'bracket':[{'id':'face_v','position':[0,0,19.5],'direction':[-1,0,0]},{'id':'face_h','position':[19.5,0,0],'direction':[0,0,-1]}],'nut':[{'id':'bore','position':[0,0,0],'direction':[1,0,0]}],'screw':[{'id':'shaft','position':[2,0,0],'direction':[-1,0,0]}],'cap':[{'id':'base','position':[0,0,0],'direction':[0,0,-1]}]}[k]
  for q in interfaces:q['compatibility_family']=F
  meta=dict(schema_version='0.2-probe',part_id=pp['part_id'],revision='1',name=pp['part_id'],category=k,edit_mode='parametric' if k=='profile' else 'rigid',units='mm',coordinate_system='RH_Z_UP',local_origin=[0,0,0],dimensions=m.extents.tolist(),geometry_ref='part.glb',geometry_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),source='NopSCADlib adapted profile' if k=='profile' else 'upstream nominal dimensions; simplified self-authored geometry' if k!='cap' else 'self-authored visual-only cap',license_status='GPL-3.0-or-later research source; distribution review pending',parameters={'length_mm':{'default':500,'min':100,'max':3000}} if k=='profile' else {},interfaces=interfaces,procurement={'sku':None,'unit':'mm' if k=='profile' else 'pcs'},engineering_status='NEEDS_REVIEW');(folder/'part.json').write_text(json.dumps(meta,indent=2))
  if k=='profile':(folder/'section.json').write_text(json.dumps(dict(units='mm',outer=list(p.exterior.coords),holes=[list(r.coords) for r in p.interiors])))
 (R/'results.json').write_text(json.dumps(dict(passed=tests,count=len(tests),engineering_status='NEEDS_REVIEW',scope='offline fixed-frame geometry/pose probe; not generic snap solver, full collision or real hardware approval'),indent=2));return a,meshes
if __name__=='__main__':main()
