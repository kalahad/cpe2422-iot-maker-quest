# -*- coding: utf-8 -*-
"""ตรวจคุณภาพเกมแบบ headless: เล่นครบทั้งเกม + กดห้องทดลองทุกปุ่ม + ทดสอบสุ่ม Pre/Post 400 รอบ
usage: python3 tools/qa_headless.py game1_brain_core.html [...]"""
import sys, os, json, asyncio
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

async def answer_round(page, n_expected=None, pick_correct=True):
    cnt = 0
    while True:
        await page.wait_for_timeout(60)
        if await page.is_visible('#acEnd.show'):
            break
        ready = await page.evaluate("typeof AC!=='undefined'&&AC.on&&!!AC.qs[AC.idx]")
        btns = await page.query_selector_all('#acQCard .choice') if ready else []
        if not btns:
            await page.wait_for_timeout(100); continue
        idx = 0
        if pick_correct:
            idx = await page.evaluate("AC.qs[AC.idx].a")
        await btns[idx].click()
        await page.click('#acNextQ')
        cnt += 1
        assert cnt < 50
    await page.click('#acEndGo')
    return cnt

async def run(path):
    errs = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 390, 'height': 844})
        page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        page.on('console', lambda m: errs.append('console: ' + m.text) if m.type == 'error' and 'net::' not in m.text and 'Failed to load resource' not in m.text else None)
        page.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
        await page.goto('file://' + os.path.join(ROOT, path))
        await page.wait_for_timeout(400)
        # 1) สุ่ม Pre/Post 400 รอบ ไม่ซ้ำ + คลังข้อสอบ
        rep = await page.evaluate("""() => {
          let dup=0; for(let k=0;k<400;k++){const pre=stratifiedSix([]).map(q=>q.qid);const post=stratifiedSix(pre).map(q=>q.qid);
            if(post.some(x=>pre.includes(x))) dup++; }
          const sizes=Object.fromEntries(Object.entries(BANK).map(([k,v])=>[k,v.length]));
          let bad=[]; Object.values(BANK).flat().forEach((q,i)=>{ if(q.c.length!==4||new Set(q.c).size!==4||q.a!==0||!q.e) bad.push(i); });
          return {dup,sizes,bad};
        }""")
        # 2) ลงทะเบียน
        await page.fill('#gnrSid', '6912345678')
        await page.fill('#playerName', 'QA')
        await page.click('#btnStart')
        await page.wait_for_timeout(300)
        assert await page.is_visible('.neo-brief'), 'briefing missing'
        await page.click('#preLaunch')
        n_pre = await answer_round(page, pick_correct=False)
        await page.wait_for_selector('#rvGo', state='visible', timeout=6000)
        await page.click('#rvGo')
        for z in (1, 2, 3):
            await page.wait_for_selector('#scr-preview%d.active' % z, timeout=4000)
            await page.click('#scr-preview%d [data-goto]' % z)
            await page.wait_for_timeout(200)
            # เดินสไลด์ทีละใบ (NEO deck) และกดทุกปุ่มในสไลด์นั้น (ห้องทดลอง/การ์ดพลิก/Boss)
            nsl = await page.evaluate("document.querySelectorAll('#scr-lesson%d .neo-slide').length" % z)
            assert nsl >= 4, 'deck missing z%d' % z
            for si in range(nsl):
                sel = '#scr-lesson%d .neo-slide.on button' % z
                for rnd in range(2):
                    n = len(await page.query_selector_all(sel))
                    for k in range(n):
                        els = await page.query_selector_all(sel)
                        if k >= len(els): break
                        try:
                            if await els[k].is_visible():
                                await els[k].click(timeout=1000)
                        except Exception as ex:
                            errs.append('click fail z%d s%d: %s' % (z, si, str(ex)[:80]))
                        await page.wait_for_timeout(300 if rnd == 0 else 120)
                        if await page.is_visible('#npModal.show'):
                            if not await page.query_selector('#npModal .np-board svg .np-pin'): errs.append('pin modal empty z%d s%d' % (z, si))
                            await page.keyboard.press('Escape'); await page.wait_for_timeout(120)
                rng = await page.query_selector('#scr-lesson%d .neo-slide.on input[type=range]' % z)
                if rng:
                    for v in ('0', '9999', '1'):
                        await page.evaluate("([sel,v])=>{const r=document.querySelector(sel);r.value=v;r.dispatchEvent(new Event('input',{bubbles:true}));}", ['#scr-lesson%d .neo-slide.on input[type=range]' % z, v])
                        await page.wait_for_timeout(120)
                if si < nsl - 1:
                    await page.click('#scr-lesson%d .neo-next' % z); await page.wait_for_timeout(420)
            ov = await page.evaluate("document.documentElement.scrollHeight>innerHeight+2")
            if ov: errs.append('page scroll on lesson %d' % z)
            await page.click('#scr-lesson%d [data-quiz]' % z)
            await page.click('[data-requiz="check%d"]' % z)
            await answer_round(page)
            await page.wait_for_timeout(200)
            await page.click('#check%dNext button' % z)
        await page.wait_for_selector('#scr-posttest.active', timeout=4000)
        await page.click('#postLaunch')
        await answer_round(page, pick_correct=True)
        await page.wait_for_selector('#rvGo', state='visible', timeout=6000)
        await page.click('#rvGo')
        await page.wait_for_timeout(1500)
        summ = await page.evaluate("({post:state.post, pre:state.pre, labs:[state.labs.lab1.length,state.labs.lab2.length,state.labs.lab3.length], badges:document.querySelectorAll('#neoSum .bd.on').length, neoSum:!!document.querySelector('#neoSum .ring'), scroll:document.documentElement.scrollHeight>innerHeight+2, res:localStorage.getItem('cpe2422_results')})")
        await page.screenshot(path=os.path.join(ROOT, 'tools', 'qa_' + path.replace('.html', '.png')), full_page=False)
        await b.close()
    return rep, n_pre, summ, errs

if __name__ == '__main__':
    files = sys.argv[1:]
    ok = True
    for f in files:
        rep, n_pre, summ, errs = asyncio.run(run(f))
        print('==', f)
        print('  bank sizes', rep['sizes'], ' bad', rep['bad'], ' pre/post dup in 400 runs:', rep['dup'])
        print('  pretest q:', n_pre, ' summary:', {k: v for k, v in summ.items() if k != 'res'})
        print('  results stored:', (summ['res'] or '')[:160])
        print('  errors:', errs if errs else 'none')
        ok = ok and not errs and rep['dup'] == 0 and not rep['bad'] and summ['post'] == 6 and summ['neoSum'] and not summ['scroll']
    print('ALL OK' if ok else 'ISSUES FOUND')
