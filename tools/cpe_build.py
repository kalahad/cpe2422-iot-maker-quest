# -*- coding: utf-8 -*-
"""
CPE2422/2428 Game Builder — สร้างเกมใหม่จากแม่แบบ GNR1007 UI v7.0 (game4_logic_labyrinth.html)
หลักการ: ใช้ไฟล์เกมฉบับสมบูรณ์ล่าสุดเป็นแม่แบบ แล้ว "ปลูกถ่าย" เนื้อหา ธีม ห้องทดลอง และคลังข้อสอบใหม่
ทุกจุดที่แทนที่ต้องเจอ anchor จริง (assert) ถ้าแม่แบบเปลี่ยน สคริปต์จะหยุดทันทีแทนการสร้างไฟล์เสีย

usage:  python3 tools/cpe_build.py            (สร้างทุกเกมลง ../ แล้วรัน apply_core ต่อ)
"""
import re, os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = open(os.path.join(HERE, 'template_game4.html'), encoding='utf-8').read()

# พาเลตต์ของแม่แบบ (game4) — จะถูกแทนด้วยพาเลตต์ของแต่ละเกม
G4 = {
    "PRIMARY_RGB": "192,132,252", "PRIMARY_HEX": "#c084fc",
    "SECOND_RGB":  "74,222,128",  "SECOND_HEX":  "#4ade80",
    "GOLD_RGB":    "251,191,36",  "GOLD_HEX":    "#fbbf24",
    "GOLD2_RGB":   "253,230,138", "GOLD2_HEX":   "#fde68a",
    "RED_RGB":     "251,113,133", "RED_HEX":     "#fb7185",
    "BG_RGB":      "13,7,24",     "BG_HEX":      "#0d0718",
    "PANEL_RGB":   "30,18,54",
    "PANEL2_RGB":  "42,25,74",
    "BG2_HEX":     "#120a20",
    "INK_HEX":     "#1a1030",
    "TEXT_HEX":    "#efe7fb",
    "MUTED_HEX":   "#a898c4",
    "MUTED2_HEX":  "#7b6a96",
    "MUTED3_HEX":  "#6a5a84",
    "SECOND2_HEX": "#86efac",
    "PRIM2_HEX":   "#d8b4fe",
}

def recolor(s, theme):
    keys = sorted(G4, key=lambda k: -len(G4[k]))
    # ใช้ placeholder สองขั้น ป้องกันสีใหม่ไปชนสีเก่าตัวอื่น
    for i, k in enumerate(keys):
        s = s.replace(G4[k], '@@C%02d@@' % i)
    for i, k in enumerate(keys):
        s = s.replace('@@C%02d@@' % i, theme[k])
    return s

def sub1(s, pattern, repl, flags=re.S, label=''):
    new, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
    assert n == 1, 'anchor not found: ' + (label or pattern[:60])
    return new

def between(s, start, end, repl, keep=True, label=''):
    i = s.find(start); assert i >= 0, 'start anchor missing: ' + (label or start[:50])
    j = s.find(end, i + len(start)); assert j >= 0, 'end anchor missing: ' + (label or end[:50])
    if keep:
        return s[:i + len(start)] + repl + s[j:]
    return s[:i] + repl + s[j:]

def rep(s, old, new, label='', count=1):
    assert old in s, 'text not found: ' + (label or old[:60])
    return s.replace(old, new) if count == 0 else s.replace(old, new, count)

CHECK_TPL = """<section id="scr-check{N}" class="screen">
  <div class="panel">
    <span class="tag">Checkpoint · {TAG}</span>
    <h2>ด่านฝึกหัด: {TITLE}</h2>
    <p class="muted">3 ข้อ เล่นในโหมดอาร์เคด ทำผิดได้ ไม่มีผลต่อคะแนนดาว — จุดประสงค์คือให้แน่ใจว่าเข้าใจก่อนไปด่านถัดไป</p>
    <div class="status-line" id="check{N}Result">ยังไม่ได้ลงด่านฝึกหัดนี้</div>
    <div class="btn-row"><button class="btn primary" data-requiz="check{N}" style="flex:1">เริ่มด่านฝึกหัด (สุ่มข้อใหม่ทุกครั้ง)</button></div>
    <div class="btn-row" id="check{N}Next" style="display:none">
      {NEXT}
    </div>
  </div>
</section>

"""
NEXTS = ['<button class="btn primary" data-goto="scr-preview2">ไปด่านถัดไป</button>',
         '<button class="btn primary" data-goto="scr-preview3">ไปด่านถัดไป</button>',
         '<button class="btn primary" id="goPost">ไปแบบทดสอบหลังเรียน</button>']

DECOR = r"""if(ACT.theme==='circuit'){
    /* ลายวงจร PCB + พัลส์สัญญาณวิ่งตามลายทองแดง */
    ctx.globalAlpha=.16; ctx.strokeStyle=c.ember; ctx.lineWidth=2;
    for(let k=0;k<7;k++){const y=14+k*(H/7), x0=(k*53)%60;
      ctx.beginPath(); ctx.moveTo(x0,y); ctx.lineTo(W*0.35+x0,y); ctx.lineTo(W*0.42+x0,y+12); ctx.lineTo(W,y+12); ctx.stroke();
      ctx.beginPath(); ctx.arc(W*0.35+x0,y,3,0,Math.PI*2); ctx.stroke();}
    ctx.globalAlpha=.9;
    for(let k=0;k<7;k++){const y=14+k*(H/7)+((t/18+k*90)%W>W*0.4?12:0), px=(t/(5+k%3)+k*137)%W;
      ctx.fillStyle=k%2?c.corner:c.gold; ctx.fillRect(px,y-1.5,7,3);}
    ctx.globalAlpha=1;
  } else if(ACT.theme==='radar'){
    /* จอเรดาร์สแกนหาเซนเซอร์ */
    const cx=W*0.82, cy=H*0.42, R=Math.min(W*0.2,H*0.42);
    ctx.globalAlpha=.18; ctx.strokeStyle=c.corner; ctx.lineWidth=1;
    for(let r=1;r<=3;r++){ctx.beginPath();ctx.arc(cx,cy,R*r/3,0,Math.PI*2);ctx.stroke();}
    ctx.beginPath();ctx.moveTo(cx-R,cy);ctx.lineTo(cx+R,cy);ctx.moveTo(cx,cy-R);ctx.lineTo(cx,cy+R);ctx.stroke();
    const a=t/900; ctx.globalAlpha=.30; ctx.fillStyle=c.corner;
    ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,R,a,a+0.5);ctx.closePath();ctx.fill();
    ctx.globalAlpha=.75;
    for(let k=0;k<5;k++){const ba=k*1.3, br=R*(0.3+((k*0.17)%0.6));
      const vis=((a-ba)%(Math.PI*2)+Math.PI*2)%(Math.PI*2)<1.6;
      if(vis){ctx.fillStyle=k%2?c.gold:c.ember;ctx.beginPath();ctx.arc(cx+Math.cos(ba)*br,cy+Math.sin(ba)*br,3.2,0,Math.PI*2);ctx.fill();}}
    ctx.globalAlpha=1;
  } else if(ACT.theme==='launch'){
    /* ฐานปล่อยจรวด: ดาว + เส้นนับถอยหลัง */
    ctx.globalAlpha=.55; ctx.fillStyle=c.text;
    for(let k=0;k<40;k++){const sx=(k*97)%W, sy=(k*53+t*0.02*(1+k%3))%H; ctx.fillRect(sx,sy,1.6,1.6);}
    ctx.globalAlpha=.14; ctx.strokeStyle=c.gold; ctx.lineWidth=2;
    const gx=W*0.86; ctx.beginPath(); ctx.moveTo(gx,H); ctx.lineTo(gx,H*0.12); ctx.stroke();
    for(let k=0;k<8;k++){const y=H*0.16+k*H*0.1; ctx.beginPath(); ctx.moveTo(gx-10,y); ctx.lineTo(gx+10,y+8); ctx.stroke();}
    ctx.globalAlpha=1;
  } else if(ACT.theme==='dungeon'){"""

def build(cfg, outdir):
    s = TPL
    s = re.sub(r'<!-- GNR-CORE:BEGIN -->.*?<!-- GNR-CORE:END -->\n?', '', s, flags=re.S)
    s = s.replace("'gnr1007_theme'", "'cpe2422_theme'")
    s = s.replace('gnr1007_theme', 'cpe2422_theme')

    # ---------- HEAD ----------
    s = sub1(s, r'<title>.*?</title>', '<title>%s | CPE2422/2428</title>' % cfg['title'])
    s = sub1(s, r'<meta name="description" content=".*?">', '<meta name="description" content="%s">' % cfg['desc'])
    s = sub1(s, r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="%s">' % cfg['title'])
    s = sub1(s, r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="%s">' % cfg['ogdesc'])
    s = sub1(s, r'<link rel="icon" href=".*?">', '<link rel="icon" href="%s">' % cfg['favicon'])
    s = sub1(s, r'/\* =+\n   LOGIC LABYRINTH.*?=+ \*/',
             "/* ================================================================\n   %s  v1.0 \"%s · CLIMB MODE\"\n"
             "   Single-file Web App — HTML + CSS + JavaScript (no backend)\n"
             "   วิชา CPE2422 อิเล็กทรอนิกส์วิศวกรรม / CPE2428 ปฏิบัติการอิเล็กทรอนิกส์วิศวกรรม — ภาคเรียนที่ 1/2569\n"
             "   ผู้พัฒนา: ผศ.ดร.กุลวลัญช์ วรุณสิน\n"
             "   สาขาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยรามคำแหง\n"
             "   Engine: GNR1007 Learning Game Series UI v7.0 (CLIMB MODE)\n"
             "   ================================================================ */" % (cfg['title'], cfg['edition']), label='header comment')

    # ---------- THEME ----------
    th = cfg['theme']
    s = recolor(s, th)
    # light block: ใช้สีหลักของธีม แล้วให้ apply_core คำนวณความต่างสีให้อ่านได้
    m = re.search(r':root\[data-theme="light"\]\{(.*?)\n  color-scheme:light;', s, re.S)
    assert m, 'light block'
    light = m.group(1)
    for tok, val in (('ember', th['LIGHT_EMBER']), ('corner', th['LIGHT_CORNER']), ('gold', th['LIGHT_GOLD']),
                     ('gold2', th['LIGHT_GOLD2']), ('red', th['LIGHT_RED'])):
        light = re.sub(r'--%s:#[0-9a-fA-F]{6}' % tok, '--%s:%s' % (tok, val), light, count=1)
    er = th['LIGHT_EMBER'].lstrip('#'); er = '%d,%d,%d' % tuple(int(er[i:i+2], 16) for i in (0, 2, 4))
    light = re.sub(r'--ember-dim:rgba\([\d,]+,', '--ember-dim:rgba(%s,' % er, light, count=1)
    light = re.sub(r'--line:rgba\([\d,]+,', '--line:rgba(%s,' % er, light, count=1)
    s = s[:m.start(1)] + light + s[m.end(1):]

    s = between(s, '/* ---------- theme extras ---------- */\n', '\n/* v6.01', cfg['extra_css'], label='extra css')

    # ---------- BODY ----------
    s = rep(s, 'aria-label="ด่านไต่หอเขาวงกต"', 'aria-label="%s"' % cfg['arcade_label'])
    s = rep(s, '<div class="brand"><i class="dot"></i><span>LOGIC LABYRINTH</span></div>',
            '<div class="brand"><i class="dot"></i><span>%s</span></div>' % cfg['brand'])
    s = sub1(s, r'<svg class="cityart".*?</svg>\n    <h1 class="title">.*?</h1>\n    <p class="subtitle">.*?</p>',
             cfg['hero_svg'] + '\n    <h1 class="title">%s</h1>\n    <p class="subtitle">%s</p>' % (cfg['title'], cfg['subtitle']), label='hero')
    s = rep(s, '<span class="tag">Adventurer Registration</span>', '<span class="tag">%s</span>' % cfg['login_tag'])
    s = sub1(s, r'<div class="feature-row">.*?</div>',
             '<div class="feature-row"><span>โหมดไต่หอ · เล่นด้วยการตอบอย่างเดียว</span>%s</div>' % cfg['features'], label='features')
    s = rep(s, 'ตัวละครไต่หอเขาวงกตขึ้น 1 ชั้น ทันที', cfg['climb_text'], count=0)

    zones = cfg['zones_html'].strip('\n') + '\n\n'
    for n, ((tag, title), nxt) in enumerate(zip(cfg['checks'], NEXTS), start=1):
        zones += CHECK_TPL.replace('{N}', str(n)).replace('{TAG}', tag).replace('{TITLE}', title).replace('{NEXT}', nxt)
    s = between(s, '<!-- ===== PREVIEW 1 ===== -->', '\n<!-- ===== POSTTEST ===== -->', zones, keep=False, label='zones')
    s = rep(s, '6 ข้อใหม่ (ห้องละ 2 ข้อ) เพื่อวัดความเข้าใจหลังผ่านครบทั้ง 3 ห้องของเขาวงกต', cfg['post_desc'])
    s = rep(s, '<span class="tag">Expedition Report</span>', '<span class="tag">%s</span>' % cfg['report_tag'])
    s = rep(s, '<h2>สรุปผลภารกิจ LOGIC LABYRINTH</h2>', '<h2>สรุปผลภารกิจ %s</h2>' % cfg['brand'])
    s = sub1(s, r'<footer>.*?</footer>',
             '<footer>\n  <p><b>%s</b> · %s</p>\n'
             '  <p>ผศ.ดร.กุลวลัญช์ วรุณสิน · สาขาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยรามคำแหง</p>\n'
             '  <p class="fmono">%s v1.0 — CLIMB MODE (TAP-ONLY) · MOBILE FIRST · SINGLE-FILE BUILD</p>\n</footer>'
             % (cfg['course'], cfg['footer_line'], cfg['brand']), label='footer')

    # ---------- JS ----------
    s = between(s, 'const BANK = ', '\nconst SKILL_LABELS', cfg['bank'].strip() + ';', label='bank')
    s = sub1(s, r"const SKILL_LABELS = \{.*?\};", 'const SKILL_LABELS = %s;' % cfg['skill_labels'], label='skill labels')
    s = sub1(s, r"const SKEY = '.*?';", "const SKEY = '%s';" % cfg['skey'])
    s = between(s, 'const STAR_TABLE = ', '\nconst MAX_STARS', cfg['star_table'].strip() + ';', label='star table')
    s = between(s, 'const NAVSTOPS = ', '\nconst ICONS', cfg['navstops'].strip() + ';', label='navstops')
    s = rep(s, "toast('ห้องนี้ยังไม่ปลดล็อก เดินตามลำดับก่อนนะครับ')", "toast('%s')" % cfg['lock_msg'])
    a = cfg['act']
    s = sub1(s, r"const ACT=\{.*?\};", "const ACT={floorWord:'%s',topWord:'%s',groundWord:'%s',theme:'%s'};" % (a['floor'], a['top'], a['ground'], a['theme']))
    s = rep(s, "if(ACT.theme==='dungeon'){", DECOR)
    s = sub1(s, r"\$\('#rvSub'\)\.textContent=kind==='pre'\?'.*?':info\.msg;", "$('#rvSub').textContent=kind==='pre'?'%s':info.msg;" % cfg['pre_sub'], label='pre sub')
    s = rep(s, "go.textContent=kind==='pre'?'เข้าห้องแรก':", "go.textContent=kind==='pre'?'%s':" % cfg['go_first'])
    s = between(s, '/* ============ 11) GAME-SPECIFIC LABS ============ */\n', '\n/* ============ 12) SUMMARY + RADAR ============ */', cfg['lab_js'].strip('\n') + '\n', label='labs')
    s = between(s, 'const BADGE_DEFS = ', '\nfunction weakestDistrict', cfg['badges'].strip() + ';', label='badges')
    s = sub1(s, r"function extraTips\(postInfo\)\{.*?\n \}\nfunction showSummary", 'function extraTips(postInfo){\n' + cfg['advice_js'].strip('\n') + '\n}\nfunction showSummary', label='advice')
    s = rep(s, "$('#sumWho').textContent='ผู้ผจญภัย: '", "$('#sumWho').textContent='%s: '" % cfg['role'])
    s = rep(s, "a.download='GNR1007_D2_labyrinth_'", "a.download='%s_'" % cfg['filekey'])
    s = between(s, 'const AVATARS = ', '\nfunction renderAvatars', cfg['avatars'].strip() + ';', label='avatars')
    s = between(s, "startQuiz(rq.dataset.requiz);return;}\n", "\n});\n$('#preLaunch')", cfg['lab_wiring'].strip('\n') + '\n', label='wiring')
    s = rep(s, "renderNav('scr-welcome'); renderSwCode();", "renderNav('scr-welcome');" + cfg.get('init_extra', ''))
    s = s.replace('ด่านทดสอบก่อนเรียน</h2>', 'ด่านทดสอบก่อนเรียน</h2>')

    # ตรวจว่าไม่มีร่องรอยเนื้อหาเดิมหลงเหลือ
    leftovers = [w for w in ('เขาวงกต', 'LABYRINTH', 'runGate', 'brkToggle', 'switch (day)', 'ผู้ผจญภัย') if w in s]
    assert not leftovers, 'leftover template content: %s' % leftovers
    path = os.path.join(outdir, cfg['filename'])
    open(path, 'w', encoding='utf-8').write(s)
    return path

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(HERE, 'games_src'))
    names = sys.argv[1:] or ['g1_brain_core', 'g2_pin_wars', 'g3_sensor_hunter', 'g4_launchpad']
    for nm in names:
        mod = importlib.import_module(nm)
        p = build(mod.CFG, ROOT)
        print('built', p)
