# -*- coding: utf-8 -*-
"""ตัวช่วยร่วมสำหรับคอนฟิกเกม CPE2422/2428"""
import json, html

def code(s):
    """บล็อกโค้ด/ข้อมูลประกอบที่ฝังในตัวข้อ (escape < > & ให้อัตโนมัติ)"""
    return '<div class="qcode codebox">' + html.escape(s, quote=False) + '</div>'

def bank_js(bank):
    """bank = {'district1':[(q, [ถูก, ผิด, ผิด, ผิด], อธิบาย), ...], ...} -> JS object literal
    ตัวเลือกแรกคือคำตอบที่ถูกเสมอ (เอนจินสลับตัวเลือกให้ทุกครั้งที่สุ่ม)"""
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    import bank_lint
    bank_lint.check_bank(bank)   # กันคำตอบยาวเดาได้ — ผิดกฎแล้วหยุด build
    out = {}
    for d, items in bank.items():
        arr = []
        for q, c, e in items:
            assert len(c) == 4 and len(set(c)) == 4, 'choices must be 4 unique: ' + q[:40]
            arr.append({'q': q, 'c': c, 'a': 0, 'e': e})
        out[d] = arr
    return json.dumps(out, ensure_ascii=False, indent=1)

def star_table(rows):
    """rows = [(rank, msg) x6] สำหรับคะแนน 6,5,4,3,2,0"""
    mins = [6, 5, 4, 3, 2, 0]
    return '[\n' + ',\n'.join('  {min:%d, stars:%d, rank:%s, msg:%s}' % (m, m, json.dumps(r, ensure_ascii=False), json.dumps(g, ensure_ascii=False))
                             for m, (r, g) in zip(mins, rows)) + '\n]'

def navstops(l1, l2, l3):
    return """[
  {key:'pretest',  label:'PRETEST',  screens:['scr-pretest'], icon:'p'},
  {key:'d1',       label:'%s', screens:['scr-preview1','scr-lesson1','scr-check1'], icon:'m', district:'district1'},
  {key:'d2',       label:'%s', screens:['scr-preview2','scr-lesson2','scr-check2'], icon:'c', district:'district2'},
  {key:'d3',       label:'%s', screens:['scr-preview3','scr-lesson3','scr-check3'], icon:'n', district:'district3'},
  {key:'posttest', label:'POSTTEST', screens:['scr-posttest'], icon:'t'},
  {key:'summary',  label:'REPORT',   screens:['scr-summary'], icon:'s'}
]""" % (l1, l2, l3)

def avatars(bg, cols):
    """อวตาร 6 แบบ ธีมอิเล็กทรอนิกส์: ชิป, หุ่นยนต์, สายฟ้า, คลื่นสัญญาณ, เสาอากาศ, หลอด LED"""
    c = cols
    shapes = [
        '<rect x="15" y="15" width="22" height="22" rx="3" fill="%s"/><path d="M19 11v4M26 11v4M33 11v4M19 37v4M26 37v4M33 37v4M11 19h4M11 26h4M11 33h4M37 19h4M37 26h4M37 33h4" stroke="%s" stroke-width="2"/>' % (c[0], c[0]),
        '<rect x="14" y="17" width="24" height="18" rx="5" fill="%s"/><circle cx="21" cy="26" r="3" fill="%s"/><circle cx="31" cy="26" r="3" fill="%s"/><path d="M26 17v-6" stroke="%s" stroke-width="2.5"/><circle cx="26" cy="10" r="2.5" fill="%s"/>' % (c[1], bg, bg, c[1], c[1]),
        '<path d="M20 12h12l-3 12h6l-11 16 3-12h-6z" fill="%s"/>' % c[2],
        '<path d="M10 26c4-10 8-10 12 0s8 10 12 0 6-8 8-4" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % c[3],
        '<path d="M26 40V22" stroke="%s" stroke-width="3"/><path d="M17 17a13 13 0 0 1 18 0M13 12a19 19 0 0 1 26 0" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round"/><circle cx="26" cy="22" r="3.5" fill="%s"/>' % (c[4], c[4], c[4]),
        '<path d="M18 30a8 8 0 1 1 16 0v4H18z" fill="%s"/><path d="M21 34v8M31 34v8" stroke="%s" stroke-width="2.5"/>' % (c[5], c[5]),
    ]
    items = []
    for i, sh in enumerate(shapes):
        items.append("'" + ('<circle cx="26" cy="26" r="24" fill="%s" stroke="%s" stroke-width="2"/>' % (bg, c[i])) + sh + "'")
    return '[\n  ' + ',\n  '.join(items) + '\n]'

HOWTO_CLIMB = 'ตัวละครไต่ขึ้น 1 ชั้น ทันที · ต่อเนื่องหลายข้อได้โบนัส Combo'
COURSE = 'CPE2422 อิเล็กทรอนิกส์วิศวกรรม · CPE2428 ปฏิบัติการอิเล็กทรอนิกส์วิศวกรรม'

LAB_CSS = """
.pickgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:12px 0}
.pick{padding:11px 12px;border-radius:12px;border:1px solid var(--line);background:rgba(var(--panel-rgb),.6);color:var(--text);
  cursor:pointer;text-align:left;font-family:var(--font);font-size:.88rem;line-height:1.4;transition:.2s;position:relative}
.pick small{display:block;color:var(--muted);font-size:.74rem;margin-top:3px}
.pick:hover{border-color:var(--ember);transform:translateY(-1px)}
.pick.sel{border-color:var(--gold);box-shadow:0 0 0 2px var(--ember-dim)}
.pick.ok{border-color:var(--corner)}
.pick.ok::after{content:'\\2713';position:absolute;top:6px;right:9px;color:var(--corner);font-weight:700}
.pick.bad{border-color:var(--red)}
.pick.bad::after{content:'\\2715';position:absolute;top:6px;right:9px;color:var(--red);font-weight:700}
.labrow{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:10px 0}
.readout{font-family:var(--mono);font-size:1.5rem;font-weight:600;color:var(--gold);letter-spacing:1px}
.readout small{font-size:.8rem;color:var(--muted);margin-left:6px;letter-spacing:0}
.meter{height:14px;border-radius:8px;background:rgba(var(--ink-panel-rgb),.7);border:1px solid var(--line);overflow:hidden;margin:8px 0}
.meter i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--corner),var(--gold),var(--red));transition:width .25s}
input[type=range].rng{width:100%;accent-color:var(--ember);margin:8px 0}
.toggle{padding:9px 14px;border-radius:11px;cursor:pointer;font-family:var(--mono);font-size:.8rem;font-weight:700;
  border:1px solid var(--line);background:var(--ember-dim);color:var(--muted);transition:.2s}
.toggle.on{color:var(--bg);background:var(--corner);border-color:var(--corner)}
.toggle.off{color:var(--bg);background:var(--red);border-color:var(--red)}
.tape{font-family:var(--mono);font-size:.92rem;min-height:46px;display:flex;align-items:center;gap:6px;flex-wrap:wrap;
  padding:12px 14px;border-radius:12px;background:rgba(var(--ink-panel-rgb),.7);border:1px solid var(--line)}
.tape span{padding:3px 9px;border-radius:8px;background:var(--ember-dim);animation:tapein .3s ease}
.tape span.hi{background:var(--corner);color:var(--bg)}
.tape span.lo{background:var(--red);color:var(--bg)}
@keyframes tapein{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.flowrow{display:flex;flex-wrap:wrap;gap:8px;align-items:stretch;margin:10px 0}
.fbox{flex:1 1 150px;padding:10px 12px;border-radius:12px;border:1px dashed var(--line);background:rgba(var(--panel-rgb),.5);font-size:.86rem}
.fbox b{display:block;font-family:var(--mono);font-size:.72rem;color:var(--ember);letter-spacing:1px;margin-bottom:4px}
.fbox.in b{color:var(--corner)} .fbox.out b{color:var(--gold)}
.keyfact{border-left:3px solid var(--gold);padding:8px 12px;margin:12px 0;background:var(--ember-dim);border-radius:0 10px 10px 0;font-size:.9rem}
"""
