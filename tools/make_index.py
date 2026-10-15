# -*- coding: utf-8 -*-
"""สร้างหน้า index.html (แผนที่ภารกิจ 4 ด่าน) ของ CPE2422/2428 จากหน้า index ของ GNR1007 UI v7.0"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
s = open(os.path.join(HERE, 'template_index.html'), encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert old in s, 'missing: ' + old[:70]
    s = s.replace(old, new) if count == 0 else s.replace(old, new, count)

def resub(pat, new):
    global s
    s2, n = re.subn(pat, lambda m: new, s, count=1, flags=re.S)
    assert n == 1, 'missing re: ' + pat[:60]
    s = s2

rep("gnr1007_theme", "cpe2422_theme", 0)
resub(r'<title>.*?</title>', '<title>CPE2422/2428 · ภารกิจ IoT Maker Quest | มหาวิทยาลัยรามคำแหง</title>')
resub(r'<meta name="description" content=".*?">', '<meta name="description" content="ชุดเกมบทเรียน 5 ด่าน วิชา CPE2422 อิเล็กทรอนิกส์วิศวกรรม และ CPE2428 ปฏิบัติการ: ไมโครคอนโทรลเลอร์ ESP32 เซนเซอร์ 38 ชนิด และโปรเจกต์ IoT S1–S7 และด่านตรวจความพร้อมก่อนต่อวงจรจริง คณะวิศวกรรมศาสตร์ มหาวิทยาลัยรามคำแหง">')
resub(r'/\* =+\n   GNR1007 Learning Game Series.*?=+ \*/', "/* =================================================================\n   CPE2422/2428 IoT Maker Quest — หน้าแผนที่ภารกิจ 5 ด่าน (ต่อยอดจาก GNR1007 index v4.1 · UI v7.0)\n   - ลงทะเบียนด้วยรหัสนักศึกษา 10 หลัก หรือรหัสลับจากผู้สอน + ชื่อเล่น\n   - โหมดมืด/สว่าง ความต่างสีข้อความ >= 4.5:1\n   ================================================================= */")
rep('<p class="sub">GNR1007 · เตรียมสอบ กว ด้านการเขียนโปรแกรม</p>', '<p class="sub">CPE2422 / CPE2428 · ภาคเรียนที่ 1/2569</p>')
rep('<h1>ผจญภัยโลกภาษา C <span>GNR1007</span></h1>', '<h1>IoT Maker Quest <span>CPE2422/2428</span></h1>')
resub(r'<p>เคลียร์ให้ครบ 11 ด่าน.*?</p>', '<p>เคลียร์ให้ครบ 5 ด่าน สะสมดาว จากสมองกล สู่ขา ESP32 เซนเซอร์ 38 ชนิด ปล่อยโปรเจกต์ IoT ของกลุ่ม และผ่านด่านตรวจ BENCH READY ก่อนต่อวงจรจริง</p>')
rep('เคลียร์แล้ว <b>0 / 11</b> ด่าน', 'เคลียร์แล้ว <b>0 / 5</b> ด่าน')
rep('aria-label="แผนที่ด่าน 11 ด่าน"', 'aria-label="แผนที่ภารกิจ 5 ด่าน"')
rep('<b id="uStars">0 / 76</b>', '<b id="uStars">0 / 30</b>')
rep('ผศ.ดร.กุลวลัญช์ วรุณสิน · index v4.1 · UI v7.0', 'ผศ.ดร.กุลวลัญช์ วรุณสิน · CPE2422/2428 index v1.0 · UI v7.0')

GAMES = """var GAMES=[
    {k:'game1', f:'game1_brain_core.html',   n:'BRAIN CORE',       th:'ถอดรหัสสมองกลฝังตัว',     tp:'MCU · MEMORY · ADC · LOOP',        d:1, ch:'คลิปที่ 1',   acc:'#22d3ee', accl:'#0e7490', max:6},
    {k:'game2', f:'game2_pin_wars.html',     n:'PIN WARS',         th:'สังเวียนขา ESP32',         tp:'GPIO · ADC1/ADC2 · PWM · BUS',     d:1, ch:'คลิปที่ 2',   acc:'#ff7a30', accl:'#c2410c', max:6},
    {k:'game3', f:'game3_sensor_hunter.html',n:'SENSOR HUNTER',    th:'ล่าเซนเซอร์ 38 ชนิด',      tp:'SENSOR DEX · AO/DO · DIVIDER',     d:2, ch:'คลิปที่ 3',   acc:'#34d399', accl:'#047857', max:6},
    {k:'game4', f:'game4_launchpad.html',    n:'PROJECT LAUNCHPAD',th:'ฐานปล่อยโปรเจกต์ S1–S7',   tp:'IPO · DRIVER · HYSTERESIS · IoT',  d:3, ch:'โปรเจกต์กลุ่ม',acc:'#818cf8', accl:'#4338ca', max:6},
    {k:'game5', f:'game5_bench_ready.html',  n:'BENCH READY',      th:'ด่านตรวจก่อนต่อวงจรจริง',  tp:'6 ทักษะ · SMOKE TEST · เรดาร์',    d:3, ch:'ก่อนประกอบจริง',acc:'#ffc21a', accl:'#9a5b00', max:6}
  ];"""
resub(r'var GAMES=\[.*?\];', GAMES)
resub(r"var DAYS=\{.*?\};", "var DAYS={1:'3 ต.ค.',2:'3 ต.ค.',3:'17–31 ต.ค.'};")
rep("var ID_KEY='gnr1007_student', RES_KEY='gnr1007_results'", "var ID_KEY='cpe2422_student', RES_KEY='cpe2422_results'")
ZONES = """var ZONES={1:{n:'ฐานสมองกล',s:'คลิปที่ 1–2 · MCU และขา ESP32',c:'#22d3ee',cl:'#0e7490'},
             2:{n:'สนามล่าเซนเซอร์',s:'คลิปที่ 3 · เซนเซอร์ 38 ชนิด',c:'#34d399',cl:'#047857'},
             3:{n:'ฐานปล่อยโปรเจกต์',s:'Lab 17–31 ต.ค. · โปรเจกต์ S1–S7 · ตรวจก่อนต่อวงจร',c:'#818cf8',cl:'#4338ca'}};"""
resub(r"var ZONES=\{1:.*?\}\};", ZONES)
ICON = """var ICON={
   game1:'<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M9.5 3v4M14.5 3v4M9.5 17v4M14.5 17v4M3 9.5h4M3 14.5h4M17 9.5h4M17 14.5h4"/>',
   game2:'<rect x="6" y="3" width="12" height="18" rx="2"/><circle cx="9.5" cy="8" r="1.2"/><circle cx="9.5" cy="12" r="1.2"/><circle cx="9.5" cy="16" r="1.2"/><circle cx="14.5" cy="8" r="1.2"/><circle cx="14.5" cy="12" r="1.2"/><circle cx="14.5" cy="16" r="1.2"/>',
   game3:'<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12l6-5"/><circle cx="16" cy="9" r="1"/>',
   game4:'<path d="M12 2.5c3 3 4 7 3.4 11H8.6C8 9.5 9 5.5 12 2.5z"/><circle cx="12" cy="9" r="1.6"/><path d="M8.6 13.5L6 17l3-1M15.4 13.5L18 17l-3-1M10 17l2 4 2-4"/>',
   game5:'<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'};"""
resub(r"var ICON=\{.*?\};", ICON)
resub(r"function rankOf\(st\)\{var R=\[.*?\];", "function rankOf(st){var R=[[0,'ผู้เริ่มต้นภารกิจ'],[7,'นักประดิษฐ์ฝึกหัด'],[14,'วิศวกร IoT'],[21,'นักสร้างระบบตัวจริง'],[27,'ปรมาจารย์ Maker']],r=R[0];")
rep("[1,2,3,4,5].map(function(z){", "[1,2,3].map(function(z){")
resub(r"var P=port\?\[\[85,\.885\].*?\]\]\n\s*:\[\[80,\.84\].*?\]\];",
      "var P=port?[[110,.86],[290,.7],[110,.53],[290,.36],[150,.17]]\n              :[[120,.72],[320,.36],[520,.68],[720,.36],[900,.68]];")
resub(r"var ZL=\{1:\[250,\.93\].*?\};", "var ZL={1:[220,.93],2:[520,.93],3:[810,.1]};")
rep("[1,2,3,4,5].forEach(function(z){var x=ZL[z][0]", "[1,2,3].forEach(function(z){var x=ZL[z][0]")
rep("var an=(z===5?' text-anchor=\"end\"':'');", "var an=(z===3?' text-anchor=\"middle\"':(z===2?' text-anchor=\"middle\"':''));")
rep("(g.k==='game10'||g.k==='game11'?38:31)", "(g.k==='game5'?38:33)")
s = s.replace('/* 5 โซน (เพิ่มด่าน 11) ยังอยู่ในจอเดียวบนจอเตี้ย */', '')
s = s.replace("แต่ละด่านใช้เวลาราว 15 นาที", "แต่ละด่านใช้เวลาราว 15–20 นาที")
s = s.replace("'ครบทั้ง '+GAMES.length+' ด่านแล้ว พร้อมสำหรับการสอบ'", "'ครบทั้ง '+GAMES.length+' ด่านแล้ว พร้อมลุยโปรเจกต์และสอบปลายภาค'")

# ---- NEO ARCADE restyle ----
NEO = open(os.path.join(HERE, 'neo', 'index_neo.css'), encoding='utf-8').read()
CHIP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="7" y="7" width="10" height="10" rx="2"/><path d="M9.5 3v4M14.5 3v4M9.5 17v4M14.5 17v4M3 9.5h4M3 14.5h4M17 9.5h4M17 14.5h4"/></svg>'
s = s.replace('<div class="logo" aria-hidden="true">{}</div>', '<div class="logo" aria-hidden="true">' + CHIP + '</div>')
s = s.replace('family=Bai+Jamjuree:wght@500;600;700&', 'family=Chakra+Petch:wght@600;700&family=Kanit:wght@400;500;600;700&family=Bai+Jamjuree:wght@500;600;700&')
s = s.replace('</head>', '<style id="neo-index">\n' + NEO + '</style>\n</head>', 1)
left = [w for w in ('GNR1007', 'gnr1007', 'game11', 'ภาษา C') if w in s]
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(s)
print('index.html written; leftovers:', left)
