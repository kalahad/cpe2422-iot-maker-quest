# -*- coding: utf-8 -*-
"""สร้างไฟล์ "คลังข้อสอบและเฉลยผู้สอน" (HTML พิมพ์ได้) จากคอนฟิกเกมทั้ง 4 ด่าน
ห้ามเผยแพร่ไฟล์นี้บน GitHub Pages ของนักศึกษา"""
import os, sys, html, re, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, 'games_src'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(HERE)), 'CPE2422_คลังข้อสอบและเฉลยผู้สอน_v1.1.html')  # เก็บนอก repo เสมอ
MODS = ['g1_brain_core', 'g2_pin_wars', 'g3_sensor_hunter', 'g4_launchpad']

def labels(js):
    return dict(re.findall(r"(district\d):'([^']*)'", js))

parts = []; total = 0
for m in MODS:
    g = importlib.import_module(m); cfg = g.CFG; lb = labels(cfg['skill_labels'])
    parts.append('<h2>%s</h2><p class="meta">ไฟล์ %s</p>' % (html.escape(cfg['title']), cfg['filename']))
    for d, items in g.B.items():
        parts.append('<h3>%s · %s (%d ข้อ)</h3><ol>' % (d.replace('district', 'ด่านย่อย '), html.escape(lb.get(d, d)), len(items)))
        for q, c, e in items:
            total += 1
            opts = ''.join('<li%s>%s</li>' % (' class="ans"' if i == 0 else '', c[i]) for i in range(4))
            parts.append('<li class="q"><div>%s</div><ol type="A" class="opts">%s</ol><div class="ex"><b>เฉลย:</b> %s · %s</div></li>' % (q, opts, c[0], e))
        parts.append('</ol>')

# ---------- ด่าน 5 BENCH READY (หลายชนิดโจทย์ + บอส Smoke Test) ----------
import g5_items as G5
parts.append('<h2>BENCH READY · ด่านตรวจก่อนต่อวงจรจริง</h2><p class="meta">ไฟล์ game5_bench_ready.html · สุ่ม 18 ข้อจากคลัง %d ข้อ ปรับระดับตามทักษะ + บอส 1 ชุด</p>' % len(G5.ITEMS))
TN = {'mcq': 'ปรนัย', 'num': 'กรอกตัวเลข', 'pin': 'คลิกขาบนบอร์ด', 'bug': 'คลิกบรรทัดที่ผิด', 'order': 'เรียงลำดับ'}
for sk, meta in G5.SKILLS.items():
    its = [x for x in G5.ITEMS if x['s'] == sk]
    parts.append('<h3>ทักษะ %s · %s (%d ข้อ)</h3><ol>' % (sk, html.escape(meta['n']), len(its)))
    for it in sorted(its, key=lambda x: (x.get('g', ''), x['l'])):
        total += 1
        tag = 'ระดับ %d · %s%s%s' % (it['l'], TN[it['t']], ' · กลุ่ม ' + it['g'] if it.get('g') else '', ' · ความปลอดภัย' if it.get('safe') else '')
        if it['t'] == 'mcq':
            body = '<ol type="A" class="opts">%s</ol>' % ''.join('<li%s>%s</li>' % (' class="ans"' if i == 0 else '', c) for i, c in enumerate(it['c']))
            ans = it['c'][0]
        elif it['t'] == 'num':
            body = ''; ans = '%s %s (ยอมรับ %s–%s)' % (it['ans'], it.get('unit', ''), it['lo'], it['hi'])
        elif it['t'] == 'pin':
            body = ''; ans = ', '.join(('GPIO' + k) if k.isdigit() else k for k in it['ok'])
        elif it['t'] == 'bug':
            body = '<div class="codebox">%s</div>' % '\n'.join('%2d  %s' % (i + 1, html.escape(l)) for i, l in enumerate(it['code']))
            ans = 'บรรทัดที่ ' + ', '.join(str(i + 1) for i in it['ok'])
        else:
            body = ''; ans = ' → '.join(it['items'])
        parts.append('<li class="q"><div class="meta">%s · %s</div><div>%s</div>%s<div class="ex"><b>เฉลย:</b> %s · %s</div></li>' % (it['id'], tag, it['q'], body, ans, it['e']))
    parts.append('</ol>')
parts.append('<h3>บอส Smoke Test (%d ชุด ชุดละ 6 แถว เวลา %d วินาที)</h3>' % (len(G5.BOSS), G5.BOSS_SECONDS))
for b in G5.BOSS:
    parts.append('<p><b>%s</b></p><ol>' % html.escape(b['t']))
    for r in b['rows']:
        total += 1
        parts.append('<li class="q"><div>%s</div><div class="ex"><b>เฉลย: %s</b>%s · %s</div></li>' % (html.escape(r[0]), 'ผ่าน' if r[1] else 'ต้องแก้', ' (จุดอันตราย)' if r[3] else '', html.escape(r[4])))
    parts.append('</ol>')

doc = """<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>คลังข้อสอบและเฉลยผู้สอน CPE2422/2428</title>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#fff;--ink:#14181f;--muted:#5b6475;--ok:#0f7a3d;--line:#d9dee7;--code:#f3f5f9}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11151b;--ink:#e8ecf2;--muted:#9aa5b5;--ok:#4ade80;--line:#2a313c;--code:#1a2029}}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Sarabun',sans-serif;line-height:1.6}
main{max-width:920px;margin:0 auto;padding:24px 16px 60px}
h1{font-size:1.5rem;margin:0 0 4px} h2{margin-top:36px;border-bottom:2px solid var(--line);padding-bottom:6px} h3{color:var(--muted);font-size:1.05rem}
.meta{color:var(--muted);font-size:.9rem;margin:0}
li.q{margin:14px 0;padding:10px 12px;border:1px solid var(--line);border-radius:10px;break-inside:avoid}
.opts li{margin:2px 0}.opts li.ans{color:var(--ok);font-weight:600}
.ex{margin-top:6px;font-size:.92rem;color:var(--muted)}
.codebox{white-space:pre-wrap;font-family:Consolas,monospace;font-size:.85rem;background:var(--code);border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin:6px 0}
.warn{border-left:4px solid #d97706;padding:8px 12px;background:var(--code);border-radius:0 8px 8px 0}
@media print{li.q{border-color:#ccc} body{background:#fff;color:#000}}
</style></head><body><main>
<h1>คลังข้อสอบและเฉลยผู้สอน · IoT Maker Quest</h1>
<p class="meta">CPE2422 อิเล็กทรอนิกส์วิศวกรรม / CPE2428 ปฏิบัติการ · ภาคเรียนที่ 1/2569 · ผศ.ดร.กุลวลัญช์ วรุณสิน · รวม %d ข้อ</p>
<p class="warn">เอกสารสำหรับผู้สอนเท่านั้น ห้ามอัปโหลดขึ้น GitHub Pages ที่เปิดให้นักศึกษา · ในเกมจริงตัวเลือกจะถูกสลับลำดับทุกครั้ง (ในเอกสารนี้ตัวเลือก A คือคำตอบที่ถูกเสมอ)</p>
%s
</main></body></html>""" % (total, '\n'.join(parts))
open(OUT, 'w', encoding='utf-8').write(doc)
print('answer key:', OUT, 'questions:', total)
