import sys, os, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
async def main(f,w,h,theme='dark'):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':h})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script("localStorage.setItem('cpe2422_theme','%s');sessionStorage.setItem('cpe2422_student',JSON.stringify({sid:'6911111111',via:'id',raw:'6911111111',nick:'k'}))"%theme)
        await pg.goto('file://'+os.path.join(ROOT,f)); await pg.wait_for_timeout(600)
        g=f.split('_')[0]; out=f'/tmp/ns/pin_{g}_{w}x{h}_{theme}'; os.makedirs('/tmp/ns',exist_ok=True)
        await pg.fill('#playerName','k'); await pg.click('#btnStart'); await pg.wait_for_timeout(400)
        await pg.evaluate("state.unlocked=['pretest','d1','d2','d3','posttest','summary'];goto_('scr-lesson1')"); await pg.wait_for_timeout(400)
        await pg.click('#scr-lesson1 .neo-next'); await pg.wait_for_timeout(500)
        sel='#scr-lesson1 .neo-slide.on .np-zoom' if w>900 else '#scr-lesson1 .neo-slide.on .np-chip'
        if await pg.is_visible(sel): await pg.click(sel)
        else: await pg.click('#btnPin')
        await pg.wait_for_timeout(400); await pg.screenshot(path=out+'_modal.png')
        k=await pg.query_selector('#npModal .np-pin[data-k="34"]')
        if k: await k.click(); await pg.wait_for_timeout(200); await pg.screenshot(path=out+'_modal34.png')
        await pg.click('#npModal [data-b="v30"]'); await pg.wait_for_timeout(300); await pg.screenshot(path=out+'_modal30.png')
        await pg.click('#npModal [data-b="c38"]'); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
        # arcade
        await pg.evaluate("goto_('scr-pretest')"); await pg.wait_for_timeout(300)
        await pg.click('#preLaunch'); await pg.wait_for_timeout(3600)
        await pg.screenshot(path=out+'_arcade.png')
        await pg.click('#acPin'); await pg.wait_for_timeout(400); await pg.screenshot(path=out+'_arcmodal.png')
        print(f,w,h,theme,'errors',errs, 'modal open', await pg.is_visible('#npModal.show'))
        await b.close()
a=sys.argv[1:]; asyncio.run(main(a[0],int(a[1]),int(a[2]),a[3] if len(a)>3 else 'dark'))
