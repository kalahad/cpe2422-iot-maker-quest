import sys, os, asyncio
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from playwright.async_api import async_playwright
async def m(w,h,theme,reg):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':h})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        init="localStorage.setItem('cpe2422_theme','%s');"%theme
        if reg: init+="localStorage.setItem('cpe2422_student',JSON.stringify({sid:'6911111111',via:'id',raw:'6911111111',nick:'k'}));sessionStorage.setItem('cpe2422_student',JSON.stringify({sid:'6911111111',via:'id',raw:'6911111111',nick:'k'}))"
        await pg.add_init_script(init)
        os.makedirs('/tmp/ns',exist_ok=True)
        await pg.goto('file://'+os.path.join(ROOT,'index.html')); await pg.wait_for_timeout(1200)
        sh=await pg.evaluate("[document.documentElement.scrollHeight,innerHeight]")
        await pg.screenshot(path=f'/tmp/ns/index_{w}x{h}_{theme}_{reg}.png'); print(w,h,theme,reg,sh,errs)
        await b.close()
a=sys.argv; asyncio.run(m(int(a[1]),int(a[2]),a[3],int(a[4])))
