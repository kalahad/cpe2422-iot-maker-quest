#!/usr/bin/env python3
"""ติดตั้งชั้นดีไซน์ NEO ARCADE ลงเกมทุกไฟล์ (รันหลัง cpe_core/apply_core.py · รันซ้ำได้)
usage: python3 tools/neo/apply_neo.py <games_dir>"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'games_src'))
from neo_cards import CARDS
CSS = open(os.path.join(HERE, 'neo.css'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'pinout.css'), encoding='utf-8').read()
JS = open(os.path.join(HERE, 'pinout.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'neo.js'), encoding='utf-8').read()
M1, M2 = '<!-- NEO:BEGIN -->', '<!-- NEO:END -->'

def process(path):
    s = open(path, encoding='utf-8').read()
    s = re.sub(re.escape(M1) + r'.*?' + re.escape(M2) + r'\n?', '', s, flags=re.S)
    name = os.path.basename(path); game = name.split('_')[0]
    s = re.sub(r'<html lang="th"[^>]*>', '<html lang="th" data-game="%s">' % game, s, count=1)
    cards = json.dumps(CARDS.get(name, {}), ensure_ascii=False)
    block = (M1 + '\n<style id="neo-css">\n' + CSS + '\n</style>\n<script>window.NEO_CARDS=' + cards + ';</script>\n'
             '<script id="neo-js">\n' + JS + '\n</script>\n' + M2 + '\n')
    i = s.rindex('</body>')
    s = s[:i] + block + s[i:]
    open(path, 'w', encoding='utf-8').write(s)
    print('neo ->', name)

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    for f in sorted(os.listdir(d)):
        if re.match(r'game\d+_.*\.html$', f): process(os.path.join(d, f))
