"""Build browser asset registry from the isolated V0.2-C part packages."""
import json, pathlib, base64, sys, hashlib, shutil
r=pathlib.Path(__file__).parent
src=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else r
assets={}
for p in sorted((src/'parts').iterdir()):
 m=json.loads((p/'part.json').read_text());b=(p/'part.glb').read_bytes()
 assert hashlib.sha256(b).hexdigest()==m['geometry_sha256'],p
 m['glb']='data:model/gltf-binary;base64,'+base64.b64encode(b).decode();assets[m['category']]=m
assert set(assets)=={'profile','bracket','nut','screw','cap'}
(r/'assets.js').write_text('window.KIT='+json.dumps(assets,separators=(',',':'))+';\n')
if (src/'preview.png').exists():shutil.copyfile(src/'preview.png',r/'offline-reference.png')
print('Five verified GLB asset hashes; browser registry generated.')
