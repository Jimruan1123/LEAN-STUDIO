from playwright.sync_api import sync_playwright
from pathlib import Path
p=Path(__file__).parent
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    page=b.new_page(viewport={'width':1440,'height':850},accept_downloads=True); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((p/'index.html').read_text());page.wait_for_timeout(300)
    def state():return page.evaluate('inspectLean()')
    assert len(state()['parts'])==9;print('PASS standard template')
    page.locator('#width').fill('1800');page.locator('#resize').click();assert state()['width']==1800 and any(x['l']==1720 for x in state()['parts']);print('PASS 1500→1800')
    page.locator('#module').click();assert any(x['role']=='shelf' for x in state()['parts']);print('PASS module')
    page.locator('#tube').click();page.locator('#edit_l').fill('800');page.locator('#apply').click();q=state()['parts'][-1];assert (q['l'],q['d'],q['h'])==(800,28,28);print('PASS tube length')
    page.locator('#plate').click();page.locator('#edit_h').fill('30');page.locator('#apply').click();assert state()['parts'][-1]['h']==30;print('PASS plate thickness')
    page.locator('#files').set_input_files([p/'part.glb',p/'part.json']);page.wait_for_function("inspectLean().parts.some(p=>p.kind==='rigid')");assert page.locator('#edit_l').is_disabled();print('PASS external GLB import & rigid lock')
    page.locator('#rotate').click();assert state()['parts'][-1]['rot']==90;print('PASS rotate')
    before=state()
    with page.expect_download() as d:page.locator('#save').click()
    d.value.save_as(p/'saved-example.json');page.locator('#free').click();assert len(state()['parts'])==0;page.locator('#profile').click();assert len(state()['parts'])==1;print('PASS free construction')
    page.locator('#project').set_input_files(p/'saved-example.json');page.wait_for_function('inspectLean().parts.length===13');assert state()==before;print('PASS JSON round trip')
    page.locator('#undo').click();assert len(state()['parts'])==1;print('PASS undo')
    page.locator('#standard').click();page.locator('#width').fill('1800');page.locator('#resize').click();page.locator('#module').click();page.screenshot(path=str(p/'preview.png'));assert not errors,errors;print('PASS browser no page errors; screenshot')
    b.close()
