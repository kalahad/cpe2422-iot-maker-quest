import sys, os, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
async def main(f, theme='dark', w=1280, h=900):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':h})
        await pg.add_init_script("localStorage.setItem('cpe2422_theme','%s')"%theme)
        await pg.goto('file://'+os.path.join(ROOT,f)); await pg.wait_for_timeout(500)
        tag=f.split('_')[0]
        await pg.screenshot(path=f'/tmp/shot_{tag}_welcome_{theme}.png')
        for z in (1,2,3):
            await pg.evaluate(f"state.name='QA';state.unlocked=['pretest','d1','d2','d3'];goto_('scr-lesson{z}')")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'/tmp/shot_{tag}_lesson{z}_{theme}.png', full_page=True)
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else 'dark'))
