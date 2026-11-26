from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 p=b.new_page(viewport={'width':1440,'height':980},accept_downloads=True);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 # Actual page source with local assets inlined because navigation is blocked by policy.
 import base64
 html=(R/'index.html').read_text()
 for name in ('assets.js','graph.js','ui.js'):
  html=html.replace(f'<script src="{name}?v=021"></script>','<script>'+(R/name).read_text()+'</script>')
 html=html.replace('src="offline-reference.png"','src="data:image/png;base64,'+base64.b64encode((R/'offline-reference.png').read_bytes()).decode()+'"')
 p.set_content(html);p.wait_for_function('window.leanState && leanState().parts.length===28');p.wait_for_timeout(200)
 def state():return p.evaluate('leanState()')
 def click(id):p.locator('#'+id).click()
 def check(name,cond):assert cond,name;print('PASS',name)
 check('five catalog types and standard assembly',p.locator('#catalog .asset').count()==5 and state()['parts'].__len__()==28)
 p.locator('#beam').fill('800');click('resizeframe');check('template resize via UI',state()['template']['beam_mm']==800 and next(x for x in state()['parts'] if x['id']=='right')['position'][0]==840)
 p.screenshot(path=str(R/'preview-ui.png'))
 click('free');click('insert');p.locator('#orientation').select_option('X');p.locator('#x').fill('100');click('insert');check('free insert two profiles',len(state()['parts'])==2)
 click('attach');check('auto mate and hardware',len(state()['parts'])==7 and len(state()['joints'])==8 and state()['parts'][1]['position']==[20,0,20]);p.locator('#partlist').select_option('P2');click('capb');p.locator('#editlength').fill('800');click('resizepart');check('free resize cap follows',next(x for x in state()['parts'] if x['id']=='P2-cap-b')['position']==[820,0,20])
 p.locator('#partlist').select_option('C3-bracket');check('rigid edit disabled',p.locator('#editlength').is_disabled());p.locator('#partlist').select_option('P2');before=state()
 with p.expect_download() as d:click('save')
 d.value.save_as(R/'saved-example.json');click('remove');check('delete cascades',len(state()['parts'])==1);click('undo');check('undo restores graph',state()==before);click('free');p.locator('#importfile').set_input_files(R/'saved-example.json');p.wait_for_function('leanState().parts.length===8');check('JSON import restores design',state()==before)
 check('BOM reflects active graph',sum(int(x.inner_text()) for x in p.locator('#bom tr td:last-child').all())==8)
 click('free');click('insert');check('first inserted part auto selected',p.evaluate('leanSelection()')=='P1' and p.locator('#applypos').is_enabled());p.locator('#catalog button').click();check('catalog click inserts and offsets duplicate start',len(state()['parts'])==2 and state()['parts'][1]['position']==[100,80,0] and p.evaluate('leanSelection()')=='P2');p.locator('#posx').fill('240');p.locator('#posy').fill('160');p.locator('#posz').fill('50');click('applypos');check('coordinate edit updates graph',state()['parts'][1]['position']==[240,160,50]);click('undo');check('coordinate move undo',state()['parts'][1]['position']==[100,80,0]);check('no uncaught browser errors',not errors);print('RENDER STATUS:',p.locator('#renderstatus').inner_text());print('WebGL2:',p.evaluate("!!document.createElement('canvas').getContext('webgl2')"));b.close()
