# -*- coding: utf-8 -*-
"""QA ด่าน 5 BENCH READY: เล่นจนจบด้วยเบราว์เซอร์จริง ถ่ายภาพทุกชนิดโจทย์ บอส และหน้าผล
ตรวจ PAGE SCROLL (เอกสารเลื่อนได้) / H-SCROLL (ล้นแนวนอน) / ข้อผิดพลาด JavaScript
usage: python3 tools/g5_shots.py <w> <h> [dark|light] [group] [board]"""
import sys, os, asyncio, random
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

async def main(w, h, theme='dark', grp='S3', board='c38'):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': w, 'height': h})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and 'net::' not in m.text and errs.append(m.text))
        await pg.add_init_script("localStorage.setItem('cpe2422_theme','%s');localStorage.setItem('cpe2422_board','%s')" % (theme, board))
        await pg.goto('file://' + os.path.join(ROOT, 'game5_bench_ready.html')); await pg.wait_for_timeout(500)
        out = '/tmp/g5/%dx%d_%s_%s' % (w, h, theme, board); os.makedirs('/tmp/g5', exist_ok=True)
        bad = []
        async def snap(name):
            v = await pg.evaluate("""(()=>{const s=document.querySelector('.scr.on');return [document.documentElement.scrollHeight-innerHeight,
              document.documentElement.scrollWidth-innerWidth, s?s.scrollWidth-s.clientWidth:0, s?s.scrollHeight-s.clientHeight:0]})()""")
            await pg.screenshot(path='%s_%s.png' % (out, name))
            if v[0] > 1: bad.append(('PAGE SCROLL', name, v))
            if v[1] > 1 or v[2] > 1: bad.append(('H-SCROLL', name, v))
            return v
        await snap('intro')
        await pg.fill('#iSid', '6911111111'); await pg.fill('#iNick', 'ทดสอบ')
        await pg.click('#grpChips .chip[data-g="%s"]' % grp)
        await pg.click('button[type=submit]'); await pg.wait_for_timeout(400)
        seen = {}; inner = {}
        for k in range(30):
            if not await pg.is_visible('#sPlay'): break
            it = await pg.evaluate("(()=>{const c=BENCH.state().cur.it;return {t:c.t,id:c.id,ok:c.ok||null,n:(c.code||c.items||c.c||[]).length}})()")
            t = it['t']; first = t not in seen
            if first: v = await snap('q_%s' % t); inner[t] = v[3]
            right = random.random() < 0.6
            if t == 'mcq':
                idx = await pg.evaluate("BENCH.state().cur.choices.indexOf(%d)" % (0 if right else 1))
                await pg.click('#qBody .opt >> nth=%d' % idx)
            elif t == 'num':
                await pg.fill('#numIn', '1')
            elif t == 'pin':
                key = it['ok'][0] if right else '34'
                await pg.click('#bbox .np-pin[data-k="%s"] >> nth=0' % key)
            elif t == 'bug':
                await pg.click('#qBody .line >> nth=%d' % (0 if not right else await pg.evaluate("BENCH.state().cur.it.ok[0]")))
            elif t == 'order':
                for i in range(it['n']):
                    await pg.click('#qBody button[data-a="add"][data-i="%d"]' % i)
            if k == 0:
                await pg.click('#btnHint')
            await pg.click('#btnSure' if random.random() < .5 else '#btnUnsure'); await pg.wait_for_timeout(250)
            if first: await snap('a_%s' % t); seen[t] = 1
            await pg.click('#btnNext'); await pg.wait_for_timeout(200)
        await snap('boss')
        for i in range(6):
            await pg.click('.brow[data-i="%d"] .tg button >> nth=%d' % (i, random.randint(0, 1)))
        await pg.click('#btnBoss'); await pg.wait_for_timeout(300); await snap('boss_done')
        await pg.click('#btnBoss'); await pg.wait_for_timeout(900); await snap('result')
        code = await pg.text_content('#rCode')
        res = await pg.evaluate("JSON.parse(localStorage.getItem('cpe2422_results'))['6911111111'].game5")
        await pg.click('#btnVerify') if await pg.is_visible('#btnVerify') else None
        print('%dx%d %s %s grp=%s types=%s code=%s stars=%s verdict=%s' % (w, h, theme, board, grp, sorted(seen), code, res['post'], res['verdict']))
        print('  inner-scroll per type:', inner)
        print('  errors:', errs or 'none')
        for x in bad: print('  ', *x)
        await b.close()

a = sys.argv[1:]
asyncio.run(main(int(a[0]), int(a[1]), a[2] if len(a) > 2 else 'dark', a[3] if len(a) > 3 else 'S3', a[4] if len(a) > 4 else 'c38'))
