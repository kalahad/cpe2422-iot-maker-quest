#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้าง QR code สำหรับเกมบทเรียน CPE2422/2428 ทั้ง 4 เกม + หน้ารวม index.html
ใช้เมื่อเปิด GitHub Pages แล้วและทราบ URL จริง

วิธีใช้:
    pip install qrcode[pil] --break-system-packages
    python3 generate_qr.py https://<username>.github.io/<repo>/

ผลลัพธ์:
    qr_output/<ชื่อไฟล์>.png      -- QR แยกทีละเกม (สำหรับพิมพ์ติดบอร์ด/สไลด์)
    qr_output/qr_sheet.html      -- ชีตรวม QR ทั้งหมดพร้อมชื่อเกม ไว้พิมพ์แจกครั้งเดียว
"""
import sys, os, html

GAMES = [
    ("index.html",               "CPE2422/2428 · หน้าแผนที่ภารกิจ IoT Maker Quest"),
    ("game1_brain_core.html",    "Game 01 · BRAIN CORE"),
    ("game2_pin_wars.html",      "Game 02 · PIN WARS"),
    ("game3_sensor_hunter.html", "Game 03 · SENSOR HUNTER"),
    ("game4_launchpad.html",     "Game 04 · PROJECT LAUNCHPAD"),
]

def main():
    if len(sys.argv) < 2:
        print("ใช้งาน: python3 generate_qr.py https://<username>.github.io/<repo>/")
        sys.exit(1)
    base = sys.argv[1].rstrip("/") + "/"

    import qrcode
    outdir = "qr_output"
    os.makedirs(outdir, exist_ok=True)

    cards = []
    for fname, label in GAMES:
        url = base + fname
        img = qrcode.make(url, box_size=10, border=2)
        png_name = os.path.splitext(fname)[0] + ".png"
        img.save(os.path.join(outdir, png_name))
        cards.append((png_name, label, url))
        print(f"สร้างแล้ว: {png_name}  ->  {url}")

    sheet_cards = "\n".join(
        f"""<div class="card">
  <img src="{html.escape(png)}" alt="QR {html.escape(label)}">
  <div class="label">{html.escape(label)}</div>
  <div class="url">{html.escape(url)}</div>
</div>""" for png, label, url in cards
    )

    sheet = f"""<!DOCTYPE html>
<html lang="th"><head><meta charset="UTF-8">
<title>CPE2422/2428 · ชีต QR รวมเกมทั้งหมด</title>
<style>
  body{{font-family:'Sarabun',system-ui,sans-serif;background:#fff;color:#111;margin:0;padding:24px}}
  h1{{font-size:1.2rem;margin:0 0 4px}}
  p{{color:#555;margin:0 0 20px;font-size:.85rem}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:18px}}
  .card{{border:1px solid #ddd;border-radius:10px;padding:14px;text-align:center;break-inside:avoid}}
  .card img{{width:100%;max-width:180px;height:auto}}
  .label{{font-weight:600;margin-top:8px;font-size:.9rem}}
  .url{{font-family:monospace;font-size:.68rem;color:#777;word-break:break-all;margin-top:4px}}
  @media print{{ body{{padding:0}} }}
</style></head>
<body>
<h1>CPE2422/2428 · QR เกมบทเรียนทั้งหมด</h1>
<p>สแกนเพื่อเข้าเล่นแต่ละเกมโดยตรง (ฐาน URL: {html.escape(base)})</p>
<div class="grid">
{sheet_cards}
</div>
</body></html>
"""
    with open(os.path.join(outdir, "qr_sheet.html"), "w", encoding="utf-8") as f:
        f.write(sheet)
    print(f"\nสร้างชีตรวมแล้ว: {outdir}/qr_sheet.html (เปิดในเบราว์เซอร์แล้วสั่งพิมพ์ได้เลย)")

if __name__ == "__main__":
    main()
