"""Abstract graph experiment; NOT a geometric or engineering design engine."""
from dataclasses import dataclass, field
from collections import Counter
import json

@dataclass
class Graph:
    parts: dict = field(default_factory=dict)
    joints: list = field(default_factory=list)

    def add(self, id, family, length=None, module='base'):
        if id in self.parts or family not in {'alu40','pipe28','panel'}:
            raise ValueError('duplicate or unknown family')
        if family != 'panel' and (not isinstance(length, int) or length <= 0):
            raise ValueError('positive integer example length required')
        self.parts[id] = dict(family=family, length_mm=length, module=module)

    def connect(self, a, b):
        if a == b or a not in self.parts or b not in self.parts:
            raise ValueError('invalid nodes')
        if self.parts[a]['family'] != self.parts[b]['family']:
            raise ValueError('abstract family mismatch; adapter undefined')
        edge = tuple(sorted((a,b)))
        if edge in self.joints:
            raise ValueError('duplicate edge')
        self.joints.append(edge)

    def remove_module(self, module):
        removed={k for k,v in self.parts.items() if v['module']==module}
        self.parts={k:v for k,v in self.parts.items() if k not in removed}
        self.joints=[e for e in self.joints if not removed.intersection(e)]

    def bom(self):
        counts=Counter((p['family'], p['length_mm']) for p in self.parts.values())
        return [dict(family=f,length_mm=l,qty=q) for (f,l),q in sorted(counts.items())]

    def snapshot(self):
        return dict(parts=self.parts, joints=sorted(self.joints), bom=self.bom(), engineering_status='NEEDS_REVIEW')


def workbench(width=1500, depth=750, height=850, tool_panel=False):
    if not all(type(v) is int and v>80 for v in (width,depth,height)):
        raise ValueError('invalid example dimensions')
    g=Graph()
    for i in range(4): g.add(f'leg{i}', 'alu40', height-25)
    for i,length in enumerate((width-80,depth-80,width-80,depth-80)):
        g.add(f'rail{i}','alu40',length)
        g.connect(f'rail{i}',f'leg{i}')
        g.connect(f'rail{i}',f'leg{(i+1)%4}')
    g.add('desktop','panel')  # no interface model yet
    if tool_panel:
        for i in (2,3):
            g.add(f'post{i}','alu40',400,'tool_panel')
            g.connect(f'post{i}',f'leg{i}')
        g.add('toolpanel','panel',module='tool_panel')
    return g

if __name__=='__main__':
    print(json.dumps({'before':workbench().snapshot(),'after':workbench(1800,tool_panel=True).snapshot()},indent=2))
