# -*- coding: utf-8 -*-
"""ตัวตรวจ "คำตอบยาวเดาได้" ของคลังข้อสอบ CPE2422/2428

ปัญหาที่แก้: ถ้าตัวเลือกที่ถูกยาวหรือละเอียดกว่าตัวลวงเสมอ ผู้เรียนเลือกข้อยาวที่สุดก็ได้คะแนนโดยไม่ต้องรู้เนื้อหา
กฎ (ใช้ทั้งตอน build และเรียกตรวจเอง):
  1. รายข้อ  ความยาวคำตอบถูกต้องอยู่ในช่วง  median(ตัวลวง) x [0.70, 1.25]  (+-6 ตัวอักษรสำหรับตัวเลือกสั้น)
  2. รายด่าน คำตอบถูกเป็นข้อที่ยาวที่สุดเดี่ยว ๆ ไม่เกิน 30% และสั้นที่สุดเดี่ยว ๆ ไม่เกิน 35%
  3. บอตเดามั่ว (เลือกข้อยาวสุด / สั้นสุด / ยาวรองลงมา) ต้องได้คะแนนคาดหมายไม่เกิน 35%
ความยาวนับเฉพาะตัวอักษรที่มองเห็น (ตัด HTML tag และสระ/วรรณยุกต์ไทยที่ไม่กินที่)

usage:  python3 tools/bank_lint.py            รายงานทุกด่าน + บอตเดามั่ว
        python3 tools/bank_lint.py --items    แสดงรายข้อที่ผิดกฎ
"""
import re, html, unicodedata, statistics, sys, os, importlib

ITEM_HI, ITEM_LO, SLACK = 1.25, 0.70, 6
MAX_LONGEST, MAX_SHORTEST, MAX_BOT = 0.30, 0.35, 0.35


def vlen(s):
    t = html.unescape(re.sub(r'<[^>]+>', '', s))
    return sum(1 for ch in t if unicodedata.category(ch) != 'Mn')


def item_issue(c):
    L = [vlen(x) for x in c]
    med = statistics.median(L[1:])
    if L[0] > med * ITEM_HI + SLACK:
        return 'ยาวเกิน (%d เทียบตัวลวง %d)' % (L[0], med)
    if L[0] < med * ITEM_LO - SLACK:
        return 'สั้นเกิน (%d เทียบตัวลวง %d)' % (L[0], med)
    return ''


def bot_scores(items):
    """คะแนนคาดหมายของบอต 3 แบบ (กรณีเท่ากันหลายข้อ หารโอกาส)"""
    out = {'longest': 0.0, 'shortest': 0.0, 'second': 0.0}
    for c in items:
        L = [vlen(x) for x in c]
        for key, target in (('longest', max(L)), ('shortest', min(L)), ('second', sorted(L)[-2])):
            ties = [i for i, v in enumerate(L) if v == target]
            if 0 in ties:
                out[key] += 1 / len(ties)
    n = max(1, len(items))
    return {k: v / n for k, v in out.items()}


def bank_report(choices):
    """choices = list ของ [ถูก, ผิด, ผิด, ผิด]"""
    n = len(choices)
    longest = sum(1 for c in choices if vlen(c[0]) > max(vlen(x) for x in c[1:]))
    shortest = sum(1 for c in choices if vlen(c[0]) < min(vlen(x) for x in c[1:]))
    bad = [(i, item_issue(c)) for i, c in enumerate(choices) if item_issue(c)]
    bots = bot_scores(choices)
    errs = []
    if bad:
        errs.append('%d ข้อผิดกฎความยาวรายข้อ' % len(bad))
    if longest / n > MAX_LONGEST:
        errs.append('คำตอบถูกยาวสุด %.0f%% (เกิน %.0f%%)' % (100 * longest / n, 100 * MAX_LONGEST))
    if shortest / n > MAX_SHORTEST:
        errs.append('คำตอบถูกสั้นสุด %.0f%% (เกิน %.0f%%)' % (100 * shortest / n, 100 * MAX_SHORTEST))
    for k, v in bots.items():
        if v > MAX_BOT:
            errs.append('บอต %s ได้ %.0f%%' % (k, 100 * v))
    return {'n': n, 'longest': longest / n, 'shortest': shortest / n, 'bots': bots, 'bad': bad, 'errors': errs}


def check_bank(bank, name=''):
    """เรียกจาก cpe_common.bank_js — ผิดกฎแล้วหยุด build (ตั้ง CPE_LINT=off เพื่อข้ามชั่วคราว)"""
    allc = [c for items in bank.values() for (_q, c, _e) in items]
    r = bank_report(allc)
    if r['errors'] and os.environ.get('CPE_LINT', 'on') != 'off':
        lines = ['คลังข้อสอบ %s ไม่ผ่านกฎความยาว: %s' % (name, '; '.join(r['errors']))]
        flat = [(d, q, c) for d, items in bank.items() for (q, c, _e) in items]
        for i, why in r['bad'][:40]:
            d, q, c = flat[i]
            lines.append('  [%s] %s -> %s' % (d, re.sub(r'<[^>]+>', '', q)[:70], why))
        raise SystemExit('\n'.join(lines))
    return r


if __name__ == '__main__':
    HERE = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(HERE, 'games_src'))
    os.environ['CPE_LINT'] = 'off'
    show = '--items' in sys.argv
    mods = ['g1_brain_core', 'g2_pin_wars', 'g3_sensor_hunter', 'g4_launchpad', 'g5_bench_ready']
    ok = True
    print('%-18s %4s %8s %8s %8s %8s %8s  %s' % ('ด่าน', 'ข้อ', 'ยาวสุด', 'สั้นสุด', 'บอตยาว', 'บอตสั้น', 'บอตรอง', 'ผล'))
    for m in mods:
        try:
            g = importlib.import_module(m)
        except ModuleNotFoundError:
            continue
        bank = getattr(g, 'B', None) or getattr(g, 'MCQ', None)
        if not bank:
            continue
        allc = [c for items in bank.values() for (_q, c, _e) in items]
        r = bank_report(allc)
        ok &= not r['errors']
        print('%-18s %4d %7.0f%% %7.0f%% %7.0f%% %7.0f%% %7.0f%%  %s' % (
            m, r['n'], 100 * r['longest'], 100 * r['shortest'], 100 * r['bots']['longest'],
            100 * r['bots']['shortest'], 100 * r['bots']['second'], 'ผ่าน' if not r['errors'] else 'ไม่ผ่าน'))
        if show:
            flat = [(d, q, c) for d, items in bank.items() for (q, c, _e) in items]
            for i, why in r['bad']:
                d, q, c = flat[i]
                print('    [%s] %s -> %s' % (d, re.sub(r'<[^>]+>', '', q)[:60], why))
    print('สรุป:', 'ผ่านทุกด่าน' if ok else 'ยังมีด่านไม่ผ่าน')
    sys.exit(0 if ok else 1)
