import sys, os, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
async def main(f, w, h, theme='dark', tag=''):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':h})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script("localStorage.setItem('cpe2422_theme','%s');sessionStorage.setItem('cpe2422_student',JSON.stringify({sid:'6911111111',via:'id',raw:'6911111111',nick:'k'}))"%theme)
        await pg.goto('file://'+os.path.join(ROOT,f)); await pg.wait_for_timeout(700)
        g=f.split('_')[0]; out=f'/tmp/ns/{g}_{tag}{w}x{h}_{theme}'
        os.makedirs('/tmp/ns',exist_ok=True)
        async def snap(name):
            sh=await pg.evaluate("(()=>{const p=document.querySelector('.screen.active .panel');return [document.documentElement.scrollHeight,innerHeight,(document.querySelector('.screen.active')||{}).scrollHeight, p?p.scrollWidth-p.clientWidth:0, document.documentElement.scrollWidth-innerWidth]})()")
            await pg.screenshot(path=f'{out}_{name}.png'); return sh
        r={}
        r['wel']=await snap('wel')
        await pg.fill('#playerName','k'); await pg.click('#btnStart'); await pg.wait_for_timeout(600)
        r['pre']=await snap('pre')
        await pg.evaluate("state.unlocked=['pretest','d1','d2','d3','posttest','summary'];goto_('scr-preview1')"); await pg.wait_for_timeout(500); r['prev']=await snap('prev')
        await pg.evaluate("goto_('scr-lesson1')"); await pg.wait_for_timeout(500); r['l1s0']=await snap('l1s0')
        for k in range(1,20):
            n=await pg.query_selector('#scr-lesson1 .neo-next')
            if not n or not await n.is_visible(): break
            await n.click(); await pg.wait_for_timeout(700); r['l1s%d'%k]=await snap('l1s%d'%k)
        ov=await pg.evaluate("Array.from(document.querySelectorAll('#scr-lesson1 .neo-slide')).map((s,i)=>[i,s.scrollHeight-s.clientHeight,(s._in||{}).style?s._in.style.zoom:''])")
        print('  slides(i,overflow,zoom):', ov)
        await pg.evaluate("state.pre=1;state.post=4;state.preByD={district1:1,district2:0,district3:0};state.postByD={district1:2,district2:1,district3:1};state.maxCombo=3;showSummary()")
        await pg.wait_for_timeout(1800); r['sum']=await snap('sum')
        print(f, w, h, theme, 'errors:', errs)
        for k,v in r.items():
            if v[0]>v[1]+2: print('  PAGE SCROLL', k, v)
            if v[3]>1 or v[4]>1: print('  H-SCROLL', k, v)
        await b.close()
args=sys.argv[1:]
asyncio.run(main(args[0], int(args[1]), int(args[2]), args[3] if len(args)>3 else 'dark'))
