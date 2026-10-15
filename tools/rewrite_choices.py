# -*- coding: utf-8 -*-
"""แทนที่ชุดตัวเลือกในคลังข้อสอบ gN_*.py แบบปลอดภัย (ใช้ตำแหน่งจาก AST ไม่ใช้ค้นหาข้อความ)

usage: python3 tools/rewrite_choices.py <module> <rewrite_file.py>
  rewrite_file.py ต้องมี REW = {ลำดับข้อ: [ถูก, ผิด, ผิด, ผิด], ...}
  ลำดับข้อ = ลำดับตามบรรทัดในไฟล์ (ตรงกับ #n ที่ bank_lint --dump แสดง)
ข้อที่ไม่อยู่ใน REW คงเดิม · ตรวจว่าตัวเลือกไม่ซ้ำและมี 4 ตัวก่อนเขียนไฟล์"""
import ast, sys, os, runpy

def items(src):
    tree = ast.parse(src); out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Tuple) and len(n.elts) == 3 and isinstance(n.elts[1], ast.List) and len(n.elts[1].elts) == 4:
            out.append(n)
    out.sort(key=lambda n: (n.lineno, n.col_offset))
    return out

def apply(path, rew):
    src = open(path, encoding='utf-8').read()
    nodes = items(src)
    # ast ให้ col_offset เป็นไบต์ UTF-8 จึงแปลงเป็นตำแหน่งตัวอักษร
    b = src.encode('utf-8')
    def pos(line, col):
        lines = b.split(b'\n')
        return len(b'\n'.join(lines[:line - 1]).decode('utf-8')) + (1 if line > 1 else 0) + len(lines[line - 1][:col].decode('utf-8'))
    edits = []
    for i, c in rew.items():
        assert len(c) == 4 and len(set(c)) == 4, 'item %d needs 4 unique choices' % i
        lst = nodes[i].elts[1]
        s, e = pos(lst.lineno, lst.col_offset), pos(lst.end_lineno, lst.end_col_offset)
        ind = ' ' * (len(src[:s].rsplit('\n', 1)[-1]) + 1)   # ย่อหน้าให้ตรงกับวงเล็บเปิด
        edits.append((s, e, '[' + (',\n' + ind).join(repr(x) for x in c) + ']'))
    for s, e, t in sorted(edits, reverse=True):
        src = src[:s] + t + src[e:]
    ast.parse(src)
    open(path, 'w', encoding='utf-8').write(src)
    return len(edits)

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    mod, rf = sys.argv[1], sys.argv[2]
    rew = runpy.run_path(rf)['REW']
    n = apply(os.path.join(here, 'games_src', mod + '.py'), rew)
    print(mod, 'rewrote', n, 'items')
