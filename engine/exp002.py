"""EXP-002: exact CAD via CadQuery; LCS mating inspired by Assembly4.
Self-authored illustrative geometry, not vendor parts or load-rated design.
"""
import cadquery as cq
import json
from pathlib import Path


def loc(z=0, flip=False):
    return cq.Location(cq.Vector(0,0,z), cq.Vector(1,0,0), 180 if flip else 0)


def mate(parent_pose, parent_port, child_port):
    # Oppose outward normals; use native CadQuery rigid transformations.
    return parent_pose * parent_port * loc(flip=True) * child_port.inverse


def build(lengths=(300,450), parent_pose=None):
    if any(l<=24 for l in lengths):
        raise ValueError('Illustrative overlap requires tube longer than 24 mm')
    parent_pose = parent_pose if parent_pose is not None else loc()
    sleeve = cq.Workplane('XY').workplane(offset=-25).circle(17).circle(14.2).extrude(50)
    asm = cq.Assembly(name='EXP002')
    asm.add(sleeve, name='sleeve', loc=parent_pose)
    solids=[sleeve.val().moved(parent_pose)]
    for name,l,port in zip(('pipe_a','pipe_b'),lengths,(loc(-1,True),loc(1))):
        tube=cq.Workplane('XY').circle(14).circle(13).extrude(l)
        pose=mate(parent_pose,port,loc(flip=True))
        asm.add(tube,name=name,loc=pose)
        solids.append(tube.val().moved(pose))
    bom=[{'part':'illustrative_28mm_tube','length_mm':l,'qty':lengths.count(l)} for l in sorted(set(lengths))]
    bom.append({'part':'illustrative_sleeve','qty':1})
    return asm,solids,bom


def run(out):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    asm,solids,bom=build()
    def check(test,condition):
        assert condition,test
        return {'test':test,'status':'PASS'}
    tests=[]
    tests.append(check('three valid native B-rep solids',len(solids)==3 and all(s.isValid() for s in solids)))
    bounds=[s.BoundingBox() for s in solids]
    tests.append(check('LCS auto placement with 2 mm axial gap',abs(bounds[1].zmax+1)<1e-6 and abs(bounds[2].zmin-1)<1e-6))
    tests.append(check('no positive-volume interferences',all(solids[i].intersect(solids[j]).Volume()<1e-6 for i in range(3) for j in range(i+1,3))))
    _,updated,bom2=build((300,600))
    tests.append(check('parameter resize and BOM update',abs(updated[2].BoundingBox().zmax-601)<1e-6 and bom2[1]['length_mm']==600))
    rotated=cq.Location(cq.Vector(100,20,30),cq.Vector(0,1,0),90)
    _,rotated_solids,_=build(parent_pose=rotated)
    tests.append(check('rigid transform propagation',abs(rotated_solids[2].BoundingBox().xmin-101)<1e-6 and abs(rotated_solids[2].BoundingBox().xmax-551)<1e-6))
    path=out/'EXP002.step'
    asm.export(str(path))
    loaded=cq.Assembly.load(str(path))
    tests.append(check('STEP assembly round trip named parts',all(n in loaded.objects for n in ('sleeve','pipe_a','pipe_b')) and len(loaded.toCompound().Solids())==3))
    result={'cadquery':cq.__version__,'tests':tests,'bom':bom,'engineering_status':'NEEDS_REVIEW','limits':'illustrative sleeve; no fasteners, real connector catalog, constraint solve or load verification'}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    run('examples/exp002')
