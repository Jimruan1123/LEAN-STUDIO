import json, struct, pathlib
p=pathlib.Path(__file__).parent
v=[]; idx=[]
for x,y,z,w,d,h in [(0,0,0,40,40,5),(0,0,5,5,40,35)]:
    off=len(v)
    for a,b,c in [(0,0,0),(w,0,0),(w,d,0),(0,d,0),(0,0,h),(w,0,h),(w,d,h),(0,d,h)]:
        v.append(((x+a)/1000,(z+c)/1000,-(y+b)/1000))
    idx += [off+i for i in [0,2,1,0,3,2,4,5,6,4,6,7,0,1,5,0,5,4,1,2,6,1,6,5,2,3,7,2,7,6,3,0,4,3,4,7]]
b=struct.pack('<'+'f'*len(v)*3,*[a for row in v for a in row])+struct.pack('<'+'H'*len(idx),*idx)
g={'asset':{'version':'2.0','generator':'LEAN-STUDIO independent demo'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}],'meshes':[{'primitives':[{'attributes':{'POSITION':0},'indices':1}]}],'buffers':[{'byteLength':len(b)}],'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':len(v)*12,'target':34962},{'buffer':0,'byteOffset':len(v)*12,'byteLength':len(idx)*2,'target':34963}],'accessors':[{'bufferView':0,'componentType':5126,'count':len(v),'type':'VEC3','min':[min(r[i] for r in v) for i in range(3)],'max':[max(r[i] for r in v) for i in range(3)]},{'bufferView':1,'componentType':5123,'count':len(idx),'type':'SCALAR'}]}
j=json.dumps(g,separators=(',',':')).encode();j+=b' '*(-len(j)%4);b+=b'\0'*(-len(b)%4)
(p/'part.glb').write_bytes(struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(b))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(b),b'BIN\0')+b)
(p/'part.json').write_text(json.dumps({'schema_version':'0.2-preview','part_id':'DEMO-BRACKET-40','revision':'1','name':'示例角码','edit_mode':'rigid','units':'mm','coordinate_system':'RH_Z_UP','dimensions':[40,40,40],'interfaces':[{'id':'base','position':[0,0,0],'direction':[0,0,-1]}],'source':'self_authored','engineering_status':'NEEDS_REVIEW'},ensure_ascii=False,indent=2))
