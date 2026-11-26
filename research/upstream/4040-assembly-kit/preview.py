import numpy as np
import trimesh as tm
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from pathlib import Path
R=Path(__file__).parent
# Read generated GLB, convert back to engineering mm for orthographic plotting.
s=tm.load(R/'frame-500/assembly.glb',force='scene')
fig,axs=plt.subplots(1,2,figsize=(12,6),gridspec_kw={'width_ratios':[1.35,1]});fig.patch.set_facecolor('#f4f6f8')
for ax,detail in zip(axs,[False,True]):
    faces=[];cols=[]
    for node in s.graph.nodes_geometry:
        if detail and not (node in ['left','bottom'] or node.startswith('left-bottom-')):continue
        T,name=s.graph[node];m=s.geometry[name].copy();m.apply_transform(T)
        v=m.vertices[:,[0,2,1]]*1000;v[:,1]*=-1
        tr=v[m.faces]
        if detail:
            # Crop by plot bounds, not geometry.
            pass
        c=np.array(m.visual.face_colors[:,:3],float)/255
        n=np.cross(tr[:,1]-tr[:,0],tr[:,2]-tr[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-12)
        light=np.array([-.35,-.6,.72]); shade=.48+.52*np.clip(n@light,0,1);c=c*shade[:,None]+.13*(1-shade[:,None]);faces.append(tr);cols.append(c)
    tr=np.concatenate(faces); c=np.concatenate(cols)
    eye=np.array([1.25,-2.1,1.45]);eye/=np.linalg.norm(eye);right=np.cross([0,0,1],eye);right/=np.linalg.norm(right);up=np.cross(eye,right)
    xy=np.stack([tr@right,tr@up],axis=-1);dep=(tr@eye).mean(axis=1);idx=np.argsort(dep)
    ax.add_collection(PolyCollection(xy[idx],facecolors=c[idx],edgecolors='none',antialiased=False));ax.set_aspect('equal');ax.set_facecolor('#f4f6f8');ax.axis('off')
    if detail:
        center=np.array([30,0,53]);x=center@right;y=center@up;ax.set_xlim(x-73,x+73);ax.set_ylim(y-70,y+70)
    else:
        ax.autoscale_view();ax.margins(.07)
    ax.set_title('ASSEMBLY / 28 INSTANCES' if not detail else 'CORNER / BRACKET + FASTENERS',fontsize=12,color='#25323e',pad=10)
fig.suptitle('LEAN-STUDIO  /  V0.2-C  /  E4040t PROBE',fontsize=17,color='#25323e',fontweight='bold');fig.text(.5,.025,'Actual generated mesh · engineering prototype, not supplier-certified',ha='center',color='#60717e',fontsize=10);fig.tight_layout(rect=(0,.05,1,.92));fig.savefig(R/'preview.png',dpi=150);plt.close(fig)
