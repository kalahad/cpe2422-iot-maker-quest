# -*- coding: utf-8 -*-
"""ด่าน 5 BENCH READY — ด่านตรวจความพร้อมก่อนต่อวงจรจริง (หน้าเดี่ยว ไม่ผ่านแม่แบบ game4)

usage:  python3 tools/games_src/g5_bench_ready.py   -> เขียน game5_bench_ready.html ที่รากของ repo
- โจทย์อยู่ใน g5_items.py (ตรวจความยาวตัวเลือกด้วย bank_lint ก่อนสร้างทุกครั้ง)
- ผังบอร์ดใช้ tools/neo/pinout.js ในโหมด quiz (ไม่มีป้ายสีบอกใบ้)
- ผลบันทึกที่ localStorage['cpe2422_results'][รหัสนักศึกษา].game5 ให้หน้ารวมแสดงดาว
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, HERE); sys.path.insert(0, TOOLS)
import g5_items as G
import bank_lint

MCQ = G.mcq_bank()
CFG = {'title': 'BENCH READY', 'filename': 'game5_bench_ready.html'}

PAGE = r"""<!DOCTYPE html>
<html lang="th" data-game="game5" data-standalone="1">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>BENCH READY · ด่านตรวจก่อนต่อวงจรจริง | CPE2422/2428</title>
<meta name="description" content="ด่าน 5 BENCH READY: ตรวจความพร้อม 6 ทักษะก่อนประกอบวงจรจริง ขาและการต่อสาย ไฟเลี้ยง เซนเซอร์ โค้ด ความปลอดภัย และการไล่หาปัญหา — CPE2422/2428 ผศ.ดร.กุลวลัญช์ วรุณสิน มหาวิทยาลัยรามคำแหง">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Kanit:wght@300;400;500;600&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<script>try{var t=localStorage.getItem('cpe2422_theme');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}</script>
<style>
/* ================= BENCH READY · Neon Arcade (ด่าน 5) ================= */
:root{--disp:'Chakra Petch','Kanit',sans-serif;--font:'Kanit','Sarabun',sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace;
  --fs-h:clamp(24px,3vw,42px);--fs-b:clamp(15px,1.2vw,18px);--fs-s:clamp(12px,.95vw,14px);--r:18px}
:root:not([data-theme="light"]){--bg:#08080f;--bg2:#11111e;--glass:rgba(255,255,255,.045);--glass2:rgba(255,255,255,.085);--edge:rgba(255,255,255,.11);
  --text:#f4f4ff;--mute:#a9aac8;--a:#ffc21a;--b:#2ee6ff;--ok:#3dff8b;--bad:#ff4d6d;--ink:#08080f;color-scheme:dark}
:root[data-theme="light"]{--bg:#f4f4f9;--bg2:#e8e9f3;--glass:rgba(255,255,255,.82);--glass2:#fff;--edge:rgba(20,22,60,.14);
  --text:#13142a;--mute:#4b4e72;--a:#9a5b00;--b:#00788f;--ok:#0f7a3d;--bad:#be123c;--ink:#fff;color-scheme:light}
:root{--n-a:var(--a);--n-b:var(--b);--n-r:var(--bad);--n-edge:var(--edge);--n-glass:var(--glass);--n-text:var(--text);--n-mute:var(--mute);--n-bg:var(--bg)}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{height:100dvh;overflow:hidden;background:var(--bg);color:var(--text);font-family:var(--font);font-size:var(--fs-b);line-height:1.55}
body::before{content:'';position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:radial-gradient(70% 55% at 85% -10%,color-mix(in srgb,var(--a) 16%,transparent),transparent 60%),
             radial-gradient(60% 50% at -10% 110%,color-mix(in srgb,var(--b) 14%,transparent),transparent 60%),
             linear-gradient(color-mix(in srgb,var(--text) 4%,transparent) 1px,transparent 1px) 0 0/28px 28px,
             linear-gradient(90deg,color-mix(in srgb,var(--text) 4%,transparent) 1px,transparent 1px) 0 0/28px 28px}
button{font:inherit;color:inherit}
code{font-family:var(--mono);font-size:.9em;padding:1px 6px;border-radius:6px;background:var(--glass2);border:1px solid var(--edge)}
#app{height:100dvh;display:flex;flex-direction:column}
.hz{height:6px;flex:none;background:repeating-linear-gradient(135deg,var(--a) 0 14px,var(--ink) 14px 28px);opacity:.9}
/* ---------- แถบบน ---------- */
.tb{flex:none;display:flex;align-items:center;gap:12px;padding:8px clamp(10px,2vw,22px);border-bottom:1px solid var(--edge);background:color-mix(in srgb,var(--bg) 80%,transparent);backdrop-filter:blur(8px)}
.ib{width:40px;height:40px;flex:none;display:grid;place-items:center;border-radius:12px;border:1px solid var(--edge);background:var(--glass);cursor:pointer;text-decoration:none;color:var(--text)}
.ib:hover{border-color:var(--a)}
.brand{display:flex;flex-direction:column;line-height:1.1;min-width:0}
.brand b{font-family:var(--disp);font-size:clamp(17px,1.6vw,22px);letter-spacing:.5px;color:var(--a)}
.brand small{color:var(--mute);font-size:var(--fs-s);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hud{margin-left:auto;display:flex;align-items:center;gap:clamp(8px,1.4vw,18px)}
.hud[hidden]{display:none}
.trace{display:flex;align-items:center;gap:4px}
.trace i{width:9px;height:9px;border-radius:50%;background:var(--glass2);border:1px solid var(--edge)}
.trace i.ok{background:var(--ok);border-color:var(--ok);box-shadow:0 0 8px var(--ok)}
.trace i.no{background:var(--bad);border-color:var(--bad)}
.trace i.now{background:var(--a);border-color:var(--a);box-shadow:0 0 10px var(--a)}
.trace i.bs{width:16px;border-radius:5px}
.fuses{display:flex;gap:5px}
.fuse{width:26px;height:14px;border-radius:4px;border:2px solid var(--a);position:relative;background:color-mix(in srgb,var(--a) 22%,transparent)}
.fuse::after{content:'';position:absolute;left:3px;right:3px;top:50%;height:2px;margin-top:-1px;background:var(--a)}
.fuse.out{border-color:var(--mute);background:none;opacity:.45}
.fuse.out::after{background:linear-gradient(90deg,var(--mute) 40%,transparent 40% 60%,var(--mute) 60%)}
.fuse.blow{animation:blow .7s}
@keyframes blow{0%,100%{transform:none}20%{transform:scale(1.5);background:var(--bad);box-shadow:0 0 18px var(--bad)}50%{transform:scale(.9)}}
.combo{white-space:nowrap;font-family:var(--disp);font-weight:700;font-size:var(--fs-s);padding:4px 10px;border-radius:99px;border:1px solid var(--edge);color:var(--mute);min-width:84px;text-align:center}
.combo.hot{color:var(--ink);background:var(--a);border-color:var(--a);box-shadow:0 0 16px color-mix(in srgb,var(--a) 60%,transparent)}
main{flex:1;min-height:0;position:relative}
.scr{position:absolute;inset:0;display:none;padding:clamp(10px,1.8vw,22px);overflow:auto}
.scr.on{display:flex;flex-direction:column}
.card{background:var(--glass);border:1px solid var(--edge);border-radius:var(--r);backdrop-filter:blur(6px)}
.btn{border:1px solid var(--edge);background:var(--glass2);border-radius:14px;padding:11px 18px;cursor:pointer;font-weight:600;font-size:var(--fs-b);display:inline-flex;align-items:center;justify-content:center;gap:8px;text-decoration:none;color:var(--text)}
.btn:hover{border-color:var(--a)}
.btn.pri{background:var(--a);color:var(--ink);border-color:var(--a);font-family:var(--disp);font-weight:700}
.btn.pri:hover{filter:brightness(1.08)}
.btn.alt{border-color:var(--b);color:var(--b)}
.btn:disabled{opacity:.45;cursor:not-allowed}
.kick{font-family:var(--disp);font-weight:600;color:var(--b);font-size:var(--fs-s);letter-spacing:.5px}
/* ---------- หน้าแรก ---------- */
.intro{flex:1;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(300px,.85fr);gap:clamp(14px,2.4vw,34px);align-items:center;max-width:1280px;width:100%;margin:0 auto}
.hero h1{font-family:var(--disp);font-size:clamp(40px,6.6vw,92px);line-height:.95;margin:6px 0 10px;letter-spacing:1px}
.hero h1 span{color:var(--a);text-shadow:0 0 28px color-mix(in srgb,var(--a) 45%,transparent)}
.hero .lead{font-size:clamp(16px,1.4vw,21px);margin:0 0 16px;max-width:36em}
.rules{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.rule{padding:12px 14px;display:flex;gap:12px;align-items:flex-start}
.rule svg{flex:none;color:var(--a)}
.rule b{display:block;font-family:var(--disp);font-size:clamp(14px,1.1vw,16px)}
.rule span{color:var(--mute);font-size:var(--fs-s);line-height:1.45;display:block}
.form{padding:clamp(14px,1.8vw,24px);display:flex;flex-direction:column;gap:12px}
.form h2{margin:0;font-family:var(--disp);font-size:clamp(18px,1.6vw,24px)}
.fld label{display:flex;justify-content:space-between;font-size:var(--fs-s);color:var(--mute);margin-bottom:4px}
.fld input{width:100%;padding:11px 14px;border-radius:12px;border:1px solid var(--edge);background:var(--glass2);color:var(--text);font:inherit;font-size:var(--fs-b)}
.fld input:focus{outline:2px solid var(--b);outline-offset:1px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{border:1px solid var(--edge);background:var(--glass2);border-radius:99px;padding:6px 12px;cursor:pointer;font-size:var(--fs-s);font-weight:600}
.chip.on{border-color:var(--a);background:color-mix(in srgb,var(--a) 22%,transparent)}
.err{color:var(--bad);font-size:var(--fs-s);min-height:1.2em}
.gname{font-size:var(--fs-s);color:var(--mute);min-height:1.3em}
.foot{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:var(--fs-s);color:var(--mute)}
.foot a,.foot button{color:var(--mute);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline;font-size:var(--fs-s)}
/* ---------- โจทย์ ---------- */
.qcard{flex:1;min-height:0;display:flex;flex-direction:column;max-width:1280px;width:100%;margin:0 auto;padding:clamp(12px,1.8vw,24px);gap:12px;position:relative;overflow:hidden}
.qhead{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.sk{font-family:var(--disp);font-weight:700;padding:4px 12px;border-radius:99px;background:color-mix(in srgb,var(--b) 18%,transparent);border:1px solid var(--b);font-size:var(--fs-s)}
.lv{display:inline-flex;gap:3px;align-items:center;font-size:var(--fs-s);color:var(--mute);font-family:var(--disp)}
.lv i{width:16px;height:6px;border-radius:3px;background:var(--glass2);border:1px solid var(--edge)}
.lv i.on{background:var(--a);border-color:var(--a)}
.gtag{font-size:var(--fs-s);padding:3px 10px;border-radius:99px;border:1px dashed var(--a);color:var(--a);font-weight:600}
.qno{margin-left:auto;font-family:var(--mono);color:var(--mute);font-size:var(--fs-s)}
.qtext{font-size:clamp(18px,1.75vw,26px);font-weight:500;line-height:1.5;margin:0}
.qbody{flex:1;min-height:0;display:flex;flex-direction:column;gap:10px;overflow:auto;padding:2px}
.qbody.pin{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,auto);gap:16px;overflow:hidden}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.opt{display:flex;gap:12px;align-items:flex-start;text-align:left;padding:13px 15px;border-radius:14px;border:1px solid var(--edge);background:var(--glass2);cursor:pointer;font-size:clamp(15px,1.25vw,18px);line-height:1.45}
.opt b{flex:none;width:28px;height:28px;border-radius:8px;display:grid;place-items:center;font-family:var(--disp);background:var(--glass);border:1px solid var(--edge)}
.opt:hover{border-color:var(--b)}
.opt.sel{border-color:var(--a);background:color-mix(in srgb,var(--a) 16%,transparent)}
.opt.sel b{background:var(--a);color:var(--ink);border-color:var(--a)}
.opt.ok{border-color:var(--ok);background:color-mix(in srgb,var(--ok) 15%,transparent)}
.opt.bad{border-color:var(--bad);background:color-mix(in srgb,var(--bad) 14%,transparent)}
.lock .opt,.lock .line,.lock .ord button,.lock .np-pin{pointer-events:none}
.numrow{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.numrow input{width:min(260px,60vw);font-family:var(--mono);font-size:clamp(22px,2.2vw,30px);padding:10px 14px;border-radius:14px;border:2px solid var(--edge);background:var(--glass2);color:var(--text)}
.numrow input:focus{outline:none;border-color:var(--a)}
.numrow .u{font-family:var(--disp);font-size:clamp(18px,1.6vw,24px);color:var(--mute)}
.numrow.ok input{border-color:var(--ok)} .numrow.bad input{border-color:var(--bad)}
.code{font-family:var(--mono);font-size:clamp(13px,1.05vw,16px);border-radius:14px;border:1px solid var(--edge);background:color-mix(in srgb,#05060c 80%,var(--bg));overflow:auto;padding:8px 0}
:root[data-theme="light"] .code{background:#f7f7fb}
.line{display:flex;width:100%;text-align:left;border:0;background:none;padding:3px 14px;cursor:pointer;white-space:pre;font-family:inherit;font-size:inherit;border-left:3px solid transparent}
.line i{font-style:normal;color:var(--mute);width:2.2em;flex:none;user-select:none}
.line:hover{background:var(--glass2)}
.line.sel{background:color-mix(in srgb,var(--a) 18%,transparent);border-left-color:var(--a)}
.line.ok{background:color-mix(in srgb,var(--ok) 16%,transparent);border-left-color:var(--ok)}
.line.bad{background:color-mix(in srgb,var(--bad) 16%,transparent);border-left-color:var(--bad)}
.ord{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.ord h4{margin:0 0 6px;font-size:var(--fs-s);color:var(--mute);font-weight:500}
.ord .col{display:flex;flex-direction:column;gap:8px}
.ord button{text-align:left;padding:11px 13px;border-radius:12px;border:1px solid var(--edge);background:var(--glass2);cursor:pointer;display:flex;gap:10px;align-items:center;font-size:clamp(14px,1.15vw,17px)}
.ord button b{flex:none;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:var(--a);color:var(--ink);font-family:var(--disp)}
.ord .slot{border-style:dashed;color:var(--mute);min-height:46px;pointer-events:none}
.ord button.ok{border-color:var(--ok)} .ord button.bad{border-color:var(--bad)}
.pinside{display:flex;flex-direction:column;gap:10px;min-height:0;overflow:auto}
.picked{font-family:var(--disp);font-size:clamp(18px,1.6vw,24px);padding:10px 14px;border-radius:14px;border:1px dashed var(--edge);color:var(--mute)}
.picked.has{border-style:solid;border-color:var(--a);color:var(--text)}
.boardbox{min-height:0;height:100%;display:flex;justify-content:center;border-radius:16px;background:radial-gradient(120% 80% at 50% 0%,color-mix(in srgb,var(--a) 10%,transparent),transparent 60%),color-mix(in srgb,#05070d 70%,var(--bg));border:1px solid var(--edge);padding:6px}
.boardbox svg{height:100%;width:auto;max-width:100%}
.np-pin .np-qring{stroke:transparent}
.np-pin{cursor:pointer}
.np-pin:hover .np-qring{stroke:var(--b)}
.np-pin.q-sel .np-qring{stroke:#ffc21a}
.np-pin.q-ok .np-qring{stroke:#3dff8b}
.np-pin.q-bad .np-qring{stroke:#ff4d6d}
.hint{font-size:var(--fs-s);padding:10px 14px;border-radius:12px;border:1px dashed var(--b);color:var(--text);background:color-mix(in srgb,var(--b) 8%,transparent)}
.acts{flex:none;display:flex;align-items:center;gap:10px;flex-wrap:wrap;border-top:1px solid var(--edge);padding-top:12px}
.acts .sp{flex:1}
.acts .note{font-size:var(--fs-s);color:var(--mute)}
.fb{flex:none;border-top:1px solid var(--edge);padding-top:12px;display:none;gap:14px;align-items:flex-start}
.fb.on{display:flex}
.fb .vd{font-family:var(--disp);font-weight:700;font-size:clamp(22px,2.4vw,34px);line-height:1;flex:none;padding:10px 14px;border-radius:14px}
.fb .vd.ok{color:var(--ink);background:var(--ok)} .fb .vd.no{color:#fff;background:var(--bad)}
.fb .tx{flex:1;min-width:0;font-size:clamp(14px,1.15vw,17px);max-height:24vh;overflow:auto}
.fb .tx p{margin:0 0 4px} .fb .tx .ans{font-weight:600}
.flash-ok{animation:fok .6s} .flash-no{animation:fno .5s}
@keyframes fok{30%{box-shadow:0 0 0 3px var(--ok),0 0 40px color-mix(in srgb,var(--ok) 50%,transparent)}}
@keyframes fno{20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-3px)}80%{box-shadow:0 0 0 3px var(--bad)}}
.shake{animation:fno .4s}
/* ---------- บอส ---------- */
.boss{flex:1;min-height:0;display:flex;flex-direction:column;max-width:1180px;width:100%;margin:0 auto;padding:clamp(12px,1.8vw,24px);gap:10px}
.boss h2{margin:0;font-family:var(--disp);font-size:clamp(20px,2.3vw,32px);line-height:1.15}
.boss h2 span{color:var(--bad)}
.tbar{height:10px;border-radius:6px;background:var(--glass2);overflow:hidden;border:1px solid var(--edge)}
.tbar i{display:block;height:100%;width:100%;background:linear-gradient(90deg,var(--bad),var(--a),var(--ok));transform-origin:left;transition:transform .25s linear}
.brow{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 10px;align-items:center;padding:8px 12px;border-radius:14px;border:1px solid var(--edge);background:var(--glass2)}
.brow p{margin:0;font-size:clamp(14px,1.15vw,17px)}
.brow .why{grid-column:1/-1;font-size:var(--fs-s);color:var(--mute);display:none}
.brow.done .why{display:block}
.brow.ok{border-color:var(--ok)} .brow.bad{border-color:var(--bad)}
.tg{display:flex;gap:6px}
.tg button{border:1px solid var(--edge);background:var(--glass);border-radius:10px;padding:7px 12px;cursor:pointer;font-weight:600;font-size:var(--fs-s);white-space:nowrap}
.tg button.on[data-v="1"]{background:var(--ok);color:var(--ink);border-color:var(--ok)}
.tg button.on[data-v="0"]{background:var(--bad);color:#fff;border-color:var(--bad)}
.blist{flex:1;min-height:0;overflow:auto;display:flex;flex-direction:column;gap:8px}
@media (min-width:1100px){.blist{display:grid;grid-template-columns:1fr 1fr;align-content:start}.brow p{font-size:15px}}
/* ---------- ผลลัพธ์ ---------- */
.res{flex:1;min-height:0;display:grid;grid-template-columns:minmax(300px,.9fr) minmax(0,1.1fr);gap:clamp(12px,1.8vw,22px);max-width:1320px;width:100%;margin:0 auto}
.rl{display:flex;flex-direction:column;gap:10px;min-height:0;padding:clamp(12px,1.6vw,20px)}
.stamp{display:flex;align-items:center;gap:14px}
.stamp .badge{font-family:var(--disp);font-weight:700;font-size:clamp(18px,1.8vw,26px);padding:8px 14px;border-radius:12px;border:3px solid currentColor;transform:rotate(-3deg);animation:stamp .5s cubic-bezier(.2,1.6,.4,1) both;white-space:nowrap}
@keyframes stamp{from{transform:scale(2.2) rotate(-12deg);opacity:0}}
.stamp .badge.R{color:var(--ok)} .stamp .badge.C{color:var(--a)} .stamp .badge.N{color:var(--bad)}
.stamp .pct{font-family:var(--disp);font-size:clamp(34px,4vw,56px);font-weight:700;line-height:1}
.stamp .pct small{display:block;font-size:var(--fs-s);color:var(--mute);font-weight:500}
.stars{display:flex;gap:4px}
.stars svg{width:22px;height:22px}
.radar{flex:1;min-height:0;display:flex;justify-content:center}
.radar svg{height:100%;width:100%;max-height:420px}
.rr{display:flex;flex-direction:column;gap:12px;min-height:0;overflow:auto;padding:clamp(12px,1.6vw,20px)}
.rr h3{margin:0 0 6px;font-family:var(--disp);font-size:clamp(15px,1.2vw,18px)}
.skr{display:grid;grid-template-columns:14px minmax(120px,1fr) minmax(80px,1.4fr) 44px;gap:8px;align-items:center;font-size:var(--fs-s);padding:3px 0}
.dot{width:12px;height:12px;border-radius:50%}
.dot.g{background:var(--ok)} .dot.y{background:var(--a)} .dot.r{background:var(--bad)}
.bar{height:10px;border-radius:6px;background:var(--glass2);overflow:hidden}
.bar i{display:block;height:100%;border-radius:6px}
.skr b{font-family:var(--mono);text-align:right}
.conf{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.conf div{padding:9px 11px;border-radius:12px;border:1px solid var(--edge);font-size:var(--fs-s)}
.conf div b{display:block;font-family:var(--disp);font-size:clamp(20px,1.8vw,26px)}
.conf .c1{border-color:var(--ok)} .conf .c3{border-color:var(--bad);background:color-mix(in srgb,var(--bad) 8%,transparent)}
.rx{display:flex;flex-direction:column;gap:8px}
.rx .it{padding:10px 12px;border-radius:12px;border:1px solid var(--edge);background:var(--glass2);font-size:var(--fs-s)}
.rx .it h4{margin:0 0 4px;font-size:clamp(14px,1.1vw,16px);display:flex;gap:8px;align-items:center}
.rx .it ul{margin:4px 0 0;padding-left:18px}
.rx .it a{color:var(--b)}
.rx .it .warn{color:var(--bad);font-weight:600}
.codebox{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.codebox output{font-family:var(--mono);font-size:clamp(13px,1.05vw,16px);padding:9px 12px;border-radius:12px;border:1px dashed var(--a);word-break:break-all;flex:1;min-width:220px}
.rbtn{display:flex;gap:8px;flex-wrap:wrap}
/* ---------- กล่องตรวจรหัส ---------- */
.dlg{position:fixed;inset:0;z-index:50;display:none;place-items:center;padding:16px;background:color-mix(in srgb,#02030a 70%,transparent);backdrop-filter:blur(6px)}
.dlg.on{display:grid}
.dlg .card{width:min(860px,100%);max-height:90dvh;overflow:auto;padding:18px;background:var(--bg2)}
.dlg textarea{width:100%;min-height:110px;font-family:var(--mono);font-size:14px;padding:10px;border-radius:12px;border:1px solid var(--edge);background:var(--glass2);color:var(--text)}
.dlg table{width:100%;border-collapse:collapse;font-size:13px;margin-top:10px}
.dlg th,.dlg td{border-bottom:1px solid var(--edge);padding:6px;text-align:left}
.dlg .v1{color:var(--ok);font-weight:700} .dlg .v0{color:var(--bad);font-weight:700}
.toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);padding:10px 16px;border-radius:12px;background:var(--text);color:var(--bg);font-size:var(--fs-s);opacity:0;transition:.25s;pointer-events:none;z-index:60}
.toast.on{opacity:1}
/* ---------- จอเล็ก ---------- */
@media (max-width:900px){
  .intro{grid-template-columns:1fr;align-items:start}
  .rules{grid-template-columns:1fr 1fr}
  .opts{grid-template-columns:1fr}
  .qbody.pin{display:flex;flex-direction:column;overflow:auto}
  .qbody.pin .boardbox{height:auto;flex:none}
  .qbody.pin .boardbox svg{width:100%;height:auto;max-width:440px}
  .pinside p{display:none}
  .pinside{flex:none;overflow:visible}
  .radar{flex:none;height:min(320px,80vw)}
  .res{grid-template-columns:1fr;flex:none}
  .rr{overflow:visible}
  .radar svg{max-height:300px}
  .ord{grid-template-columns:1fr}
  .trace{display:none}
}
@media (max-width:560px){
  .rules{grid-template-columns:1fr}
  .rules{display:none}
  .hero h1{margin:4px 0 6px}
  .brand small{display:none}
  .combo{min-width:0;padding:4px 8px;font-size:11px}
  .brand b{font-size:16px}
  .hero h1{font-size:44px}
  .qtext{font-size:18px}
  .brow{grid-template-columns:1fr}
  .fb .tx{max-height:30vh}
  .fb{flex-direction:column}
}
@media (max-height:760px) and (min-width:901px){ .rule span{display:none} .hero .lead{margin-bottom:10px} }
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
__PINCSS__
</style>
</head>
<body>
<div id="app">
<div class="hz" aria-hidden="true"></div>
<header class="tb">
  <a class="ib" href="index.html" aria-label="กลับหน้ารวมภารกิจ"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 11 12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/></svg></a>
  <div class="brand"><b>BENCH READY</b><small>ด่าน 5 · ตรวจความพร้อมก่อนต่อวงจรจริง</small></div>
  <div class="hud" id="hud" hidden>
    <div class="trace" id="trace" aria-label="ความคืบหน้า"></div>
    <div class="fuses" id="fuses" aria-label="ฟิวส์ที่เหลือ"></div>
    <div class="combo" id="combo">COMBO 0</div>
  </div>
  <button class="ib" id="btnTheme" aria-label="สลับโหมดสว่าง/มืด" style="margin-left:auto"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.9"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5a8.5 8.5 0 0 1 0 17z" fill="currentColor"/></svg></button>
</header>
<main>
<!-- ================= หน้าแรก ================= -->
<section class="scr on" id="sIntro">
  <div class="intro">
    <div class="hero">
      <div class="kick">ด่าน 5 · CPE2422/2428 · ก่อนวันประกอบวงจรจริง</div>
      <h1>BENCH <span>READY</span></h1>
      <p class="lead">สอบใบอนุญาตเข้าโต๊ะแล็บ: <b>18 โจทย์ 6 ทักษะ</b> แล้วปิดท้ายด้วยบอส <b>Smoke Test</b> ตรวจสายก่อนจ่ายไฟ ผลออกมาเป็นเรดาร์ 6 ด้าน บอกชัดว่าเรื่องไหนพร้อม เรื่องไหนต้องทวน</p>
      <div class="rules">
        <div class="card rule"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="8" width="18" height="8" rx="2"/><path d="M6 12h12"/></svg><div><b>ฟิวส์ 3 ดวง</b><span>ตอบผิดในข้อความปลอดภัย ฟิวส์ขาด 1 ดวง ฟิวส์หมดจะไม่ได้ใบอนุญาต</span></div></div>
        <div class="card rule"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/></svg><div><b>ส่งแบบมั่นใจ หรือไม่แน่ใจ</b><span>ระบบแยก "รู้จริง" ออกจาก "เดาถูก" และจับ "เข้าใจผิดแบบมั่นใจ" ที่อันตรายที่สุด</span></div></div>
        <div class="card rule"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 18h4v-5H4zM10 18h4V9h-4zM16 18h4V5h-4z"/></svg><div><b>ระดับปรับตามฝีมือ</b><span>ตอบถูกโจทย์จะยากขึ้น ตอบผิดจะง่ายลง แยกตามทักษะ ไม่มีโจทย์นอกเนื้อหาแล็บ</span></div></div>
        <div class="card rule"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l8 5v8l-8 5-8-5V8z"/><path d="M12 3v18M4 8l16 8M20 8L4 16"/></svg><div><b>เรดาร์ 6 ทักษะ + รหัสผล</b><span>ได้ใบสั่งทบทวนรายเรื่อง และรหัสผลไปวางในไฟล์ห้องควบคุมของกลุ่ม</span></div></div>
      </div>
    </div>
    <form class="card form" id="fStart" autocomplete="off" novalidate>
      <h2>ลงทะเบียนเข้าโต๊ะแล็บ</h2>
      <div class="fld"><label for="iSid"><span>รหัสนักศึกษา 10 หลัก หรือรหัสลับจากผู้สอน</span><span id="sidCnt">0/10</span></label><input id="iSid" inputmode="text" maxlength="12" placeholder="เช่น 69xxxxxxxx" spellcheck="false"></div>
      <div class="fld"><label for="iNick"><span>ชื่อเล่น</span></label><input id="iNick" maxlength="20" placeholder="เช่น ต้นกล้า"></div>
      <div class="fld"><label><span>กลุ่มโปรเจกต์ (โจทย์บางข้อจะอิงงานของกลุ่ม)</span></label><div class="chips" id="grpChips"></div><div class="gname" id="gName"></div></div>
      <div class="fld"><label><span>บอร์ดที่ใช้ประกอบจริง</span></label><div class="chips" id="brdChips"><button type="button" class="chip" data-b="c38">38 ขา · DevKitC</button><button type="button" class="chip" data-b="v30">30 ขา · DevKit V1</button></div></div>
      <div class="err" id="err" role="alert"></div>
      <button class="btn pri" type="submit">เริ่มตรวจความพร้อม</button>
      <div class="foot"><span>ใช้เวลาราว 15 นาที · เล่นซ้ำได้ โจทย์สุ่มใหม่ทุกครั้ง</span><button type="button" id="btnVerify">ตรวจรหัสผล (ผู้สอน)</button></div>
    </form>
  </div>
</section>
<!-- ================= โจทย์ ================= -->
<section class="scr" id="sPlay">
  <div class="card qcard" id="qcard">
    <div class="qhead"><span class="sk" id="qSk"></span><span class="lv" id="qLv"></span><span class="gtag" id="qG" hidden></span><span class="qno" id="qNo"></span></div>
    <p class="qtext" id="qText"></p>
    <div class="qbody" id="qBody"></div>
    <div class="acts" id="acts">
      <button class="btn" id="btnHint" type="button">คำใบ้ (ได้คะแนนครึ่งเดียว)</button>
      <span class="sp"></span>
      <span class="note" id="actNote"></span>
      <button class="btn alt" id="btnUnsure" type="button">ส่ง · ไม่แน่ใจ</button>
      <button class="btn pri" id="btnSure" type="button">ส่ง · มั่นใจ</button>
    </div>
    <div class="fb" id="fb"><div class="vd" id="fbVd"></div><div class="tx" id="fbTx"></div><button class="btn pri" id="btnNext" type="button">ข้อถัดไป</button></div>
  </div>
</section>
<!-- ================= บอส ================= -->
<section class="scr" id="sBoss">
  <div class="card boss">
        <h2 id="bTitle"></h2>
    <p style="margin:0" id="bLead">ตรวจรายการต่อสายก่อนเสียบ USB ภายใน <b id="bSec"></b> วินาที แต่ละแถวเลือก <b>ผ่าน</b> หรือ <b>ต้องแก้</b> ถ้าปล่อยจุดอันตรายผ่านไป ฟิวส์จะขาด</p>
    <div class="tbar"><i id="bBar"></i></div>
    <div class="blist" id="bList"></div>
    <div class="acts"><span class="note" id="bNote"></span><span class="sp"></span><button class="btn pri" id="btnBoss" type="button">ยืนยันผลการตรวจ</button></div>
  </div>
</section>
<!-- ================= ผล ================= -->
<section class="scr" id="sResult">
  <div class="res">
    <div class="card rl">
      <div class="kick" id="rWho"></div>
      <div class="stamp"><div class="pct" id="rPct"></div><div class="badge" id="rBadge"></div></div>
      <div class="stars" id="rStars"></div>
      <div class="radar" id="rRadar"></div>
      <div class="rbtn"><button class="btn pri" id="btnAgain" type="button">ตรวจอีกครั้ง (สุ่มโจทย์ใหม่)</button><a class="btn" href="index.html">กลับหน้ารวม</a></div>
    </div>
    <div class="card rr">
      <section><h3>คะแนนรายทักษะ</h3><div id="rSkills"></div></section>
      <section><h3>ความมั่นใจกับความถูกต้อง</h3><div class="conf" id="rConf"></div></section>
      <section><h3>ใบสั่งทบทวน</h3><div class="rx" id="rRx"></div></section>
      <section><h3>รหัสผล (วางในช่องหมายเหตุของไฟล์ห้องควบคุม)</h3><div class="codebox"><output id="rCode"></output><button class="btn" id="btnCopy" type="button">คัดลอก</button></div></section>
    </div>
  </div>
</section>
</main>
</div>
<div class="dlg" id="dlg" role="dialog" aria-modal="true" aria-labelledby="dlgH">
  <div class="card">
    <h3 id="dlgH" style="margin:0 0 6px;font-family:var(--disp)">ตรวจรหัสผล BENCH READY</h3>
    <p style="margin:0 0 8px;font-size:14px;color:var(--mute)">วางรหัสผลได้หลายบรรทัด ระบบตรวจเลขตรวจสอบ (K) เพื่อจับรหัสที่ถูกแก้ด้วยมือ และแปลงเป็นตาราง</p>
    <textarea id="dlgIn" placeholder="BR5-S3-4567-A80B67C90D58E75F70-T73-R-F2-K41"></textarea>
    <div style="display:flex;gap:8px;margin-top:8px"><button class="btn pri" id="dlgGo" type="button">ตรวจ</button><button class="btn" id="dlgX" type="button">ปิด</button></div>
    <div id="dlgOut"></div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
__PINJS__
</script>
<script>
/* ================= BENCH READY ENGINE ================= */
(function(){
'use strict';
var DATA=__DATA__;
var D=document, $=function(s){return D.querySelector(s);};
var ID_KEY='cpe2422_student', RES_KEY='cpe2422_results', SECRET='ru2569', MASK='xxxxxxxxxx';
var SK=Object.keys(DATA.skills), W={1:.7,2:.85,3:1}, ROUNDS=3;
var S=null;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}
function toast(m){var t=$('#toast');t.textContent=m;t.classList.add('on');clearTimeout(toast._t);toast._t=setTimeout(function(){t.classList.remove('on');},1800);}
function show(id){Array.prototype.forEach.call(D.querySelectorAll('.scr'),function(s){s.classList.toggle('on',s.id===id);});$('#hud').hidden=(id==='sIntro'||id==='sResult');}
function pinName(k){return /^\d+$/.test(k)?'GPIO'+k:k;}
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}

/* ---------- ธีม ---------- */
$('#btnTheme').addEventListener('click',function(){var t=D.documentElement.getAttribute('data-theme')==='light'?'dark':'light';D.documentElement.setAttribute('data-theme',t);ls('cpe2422_theme',t);});

/* ---------- ลงทะเบียน ---------- */
function checkId(raw){
  var v=(raw||'').trim(); if(v.toLowerCase()===SECRET) return {ok:true,sid:MASK,via:'code'};
  var d=v.replace(/[\s-]/g,''); if(!d) return {ok:false,msg:'กรุณากรอกรหัสนักศึกษา 10 หลัก'};
  if(/^\d+$/.test(d)){ if(d.length!==10) return {ok:false,msg:'รหัสนักศึกษาต้องมี 10 หลัก (ตอนนี้ '+d.length+' หลัก)'};
    if(!/^[5-7]\d{9}$/.test(d)) return {ok:false,msg:'รหัสนักศึกษาต้องขึ้นต้นด้วยปีที่เข้าศึกษา เช่น 69xxxxxxxx'}; return {ok:true,sid:d,via:'id'}; }
  return {ok:false,msg:'กรอกได้เฉพาะตัวเลข 10 หลัก หรือรหัสลับที่ได้รับจากผู้สอน'};
}
var grp=ls('cpe2422_group')||'', board=ls('cpe2422_board')||'c38'; if(board!=='v30') board='c38';
(function(){
  var h='<button type="button" class="chip" data-g="">ไม่ระบุ</button>';
  Object.keys(DATA.groups).forEach(function(g){h+='<button type="button" class="chip" data-g="'+g+'">'+g+'</button>';});
  $('#grpChips').innerHTML=h;
  function paint(){
    Array.prototype.forEach.call(D.querySelectorAll('#grpChips .chip'),function(b){b.classList.toggle('on',b.getAttribute('data-g')===grp);});
    Array.prototype.forEach.call(D.querySelectorAll('#brdChips .chip'),function(b){b.classList.toggle('on',b.getAttribute('data-b')===board);});
    $('#gName').textContent=grp?(grp+' · '+DATA.groups[grp]):'โจทย์ทั่วไปทั้งหมด';
  }
  $('#grpChips').addEventListener('click',function(e){var b=e.target.closest('.chip');if(!b)return;grp=b.getAttribute('data-g');paint();});
  $('#brdChips').addEventListener('click',function(e){var b=e.target.closest('.chip');if(!b)return;board=b.getAttribute('data-b');paint();});
  var cur=null; try{cur=JSON.parse(sessionStorage.getItem(ID_KEY)||'null');}catch(e){}
  if(cur&&cur.sid){$('#iSid').value=cur.raw||(cur.via==='id'?cur.sid:'');$('#iNick').value=cur.nick||'';}
  function live(){var v=$('#iSid').value.trim(),d=v.replace(/[\s-]/g,'');$('#sidCnt').textContent=v.toLowerCase()===SECRET?'รหัสลับ':((/^\d*$/.test(d)?d.length:'-')+'/10');}
  $('#iSid').addEventListener('input',live); live(); paint();
})();
$('#fStart').addEventListener('submit',function(e){
  e.preventDefault(); var r=checkId($('#iSid').value), err=$('#err');
  if(!r.ok){err.textContent=r.msg;$('#iSid').focus();return;}
  var nk=$('#iNick').value.trim(); if(!nk){err.textContent='กรุณากรอกชื่อเล่น เพื่อแสดงบนใบผล';$('#iNick').focus();return;}
  err.textContent='';
  try{sessionStorage.setItem(ID_KEY,JSON.stringify({sid:r.sid,via:r.via,raw:$('#iSid').value.trim(),nick:nk}));}catch(x){}
  ls('cpe2422_group',grp); ls('cpe2422_board',board);
  start({sid:r.sid,nick:nk});
});

/* ---------- เริ่มเกม ---------- */
function start(who){
  var seq=[], prev=null;
  for(var r=0;r<ROUNDS;r++){ var o=shuffle(SK); if(o[0]===prev){o.push(o.shift());} o.forEach(function(s){seq.push({s:s,r:r});}); prev=o[o.length-1]; }
  S={who:who,grp:grp,board:board,lvl:{},used:{},seq:seq,i:0,log:[],fuses:3,combo:0,bestCombo:0,cur:null,t0:Date.now()};
  SK.forEach(function(s){S.lvl[s]=2;});
  drawTrace(); drawFuses(false); drawCombo(); show('sPlay'); next(true);
}
function eligible(it){ return !S.used[it.id] && (!it.board||it.board===S.board); }
function pick(s,r){
  if(S.grp&&r>=1){ var gi=DATA.items.filter(function(it){return it.g===S.grp&&it.s===s&&eligible(it);}); if(gi.length) return gi[0]; }
  var L=S.lvl[s], tries=[L,L-1,L+1,L-2,L+2];
  for(var k=0;k<tries.length;k++){ var lv=tries[k]; if(lv<1||lv>3) continue;
    var pool=DATA.items.filter(function(it){return !it.g&&it.s===s&&it.l===lv&&eligible(it);}); if(pool.length) return shuffle(pool)[0]; }
  return null;
}
function drawTrace(){
  var h=''; S.seq.forEach(function(x,i){ var lg=S.log.filter(function(l){return l.k===i;})[0]; h+='<i class="'+(lg?(lg.ok?'ok':'no'):(i===S.i?'now':''))+'"></i>'; });
  h+='<i class="bs'+(S.i>=S.seq.length?' now':'')+'" title="บอส Smoke Test"></i>'; $('#trace').innerHTML=h;
}
function drawFuses(blowIdx){ var h=''; for(var i=0;i<3;i++) h+='<span class="fuse'+(i>=S.fuses?' out':'')+(blowIdx===i?' blow':'')+'"></span>'; $('#fuses').innerHTML=h; }
function drawCombo(){ var c=$('#combo'); c.textContent=S.combo>=2?('COMBO x'+S.combo):('COMBO '+S.combo); c.classList.toggle('hot',S.combo>=3); }

/* ---------- แสดงโจทย์ ---------- */
function next(first){
  if(!first) S.i++;
  if(S.i>=S.seq.length){ drawTrace(); return bossStart(); }
  var q=S.seq[S.i], it=pick(q.s,q.r); if(!it){ S.i++; return next(true); }
  S.used[it.id]=1; S.cur={it:it,sel:null,ord:[],hint:false,done:false,choices:null};
  drawTrace();
  var sk=DATA.skills[it.s];
  $('#qSk').textContent=sk.n;
  var lvl=it.l, lh='Lv '; for(var i=1;i<=3;i++) lh+='<i class="'+(i<=lvl?'on':'')+'"></i>'; $('#qLv').innerHTML=lh;
  var g=$('#qG'); g.hidden=!it.g; if(it.g) g.textContent='ภารกิจกลุ่ม '+it.g;
  $('#qNo').textContent='ข้อ '+(S.i+1)+' / '+S.seq.length;
  $('#qText').innerHTML=it.q;
  var b=$('#qBody'); b.className='qbody'; b.innerHTML='';
  $('#qcard').classList.remove('lock','flash-ok','flash-no');
  ({mcq:rMcq,num:rNum,pin:rPin,bug:rBug,order:rOrd})[it.t](b,it);
  $('#acts').style.display=''; $('#fb').classList.remove('on'); $('#btnHint').disabled=false; $('#actNote').textContent='';
  b.scrollTop=0;
}
function rMcq(b,it){
  var order=shuffle([0,1,2,3]); S.cur.choices=order;
  var h='<div class="opts">'; order.forEach(function(ci,k){ h+='<button type="button" class="opt" data-c="'+ci+'"><b>'+'ABCD'[k]+'</b><span>'+it.c[ci]+'</span></button>'; }); h+='</div>';
  b.innerHTML=h;
  b.querySelector('.opts').addEventListener('click',function(e){ var o=e.target.closest('.opt'); if(!o) return; S.cur.sel=+o.getAttribute('data-c');
    Array.prototype.forEach.call(b.querySelectorAll('.opt'),function(x){x.classList.toggle('sel',x===o);}); });
}
function rNum(b,it){
  b.innerHTML='<div class="numrow"><input id="numIn" inputmode="decimal" autocomplete="off" placeholder="กรอกตัวเลข" aria-label="คำตอบตัวเลข"><span class="u">'+esc(it.unit||'')+'</span></div><p class="note" style="margin:0;color:var(--mute);font-size:var(--fs-s)">ใช้จุดทศนิยมได้ ระบบยอมรับคำตอบที่ใกล้เคียงในช่วงคลาดเคลื่อนที่สมเหตุสมผล</p>';
  var inp=b.querySelector('input'); inp.addEventListener('input',function(){ S.cur.sel=inp.value.trim()===''?null:inp.value; });
  setTimeout(function(){try{inp.focus({preventScroll:true});}catch(e){}},60);
}
function rPin(b,it){
  b.classList.add('pin');
  b.innerHTML='<div class="pinside"><div class="picked" id="picked">แตะขาบนภาพบอร์ดเพื่อเลือก</div><p style="margin:0;color:var(--mute);font-size:var(--fs-s)">ภาพนี้คือบอร์ด '+(S.board==='v30'?'ESP32 DevKit V1 30 ขา':'ESP32-DevKitC V4 38 ขา')+' มองจากด้านบน เสาอากาศอยู่ด้านบน อ่านชื่อขาจากตัวอักษรที่พิมพ์บนบอร์ดเหมือนของจริง</p></div><div class="boardbox" id="bbox"></div>';
  $('#bbox').innerHTML=NeoPin.svg(S.board,{quiz:true});
  $('#bbox').addEventListener('click',function(e){ var p=e.target.closest('.np-pin'); if(!p||S.cur.done) return; var k=p.getAttribute('data-k'); S.cur.sel=k;
    Array.prototype.forEach.call(D.querySelectorAll('#bbox .np-pin'),function(x){x.classList.toggle('q-sel',x===p);});
    var pk=$('#picked'); pk.textContent='เลือก: '+pinName(k); pk.classList.add('has'); });
}
function rBug(b,it){
  var h='<div class="code" role="listbox" aria-label="โค้ด คลิกบรรทัดที่ผิด">'; it.code.forEach(function(ln,i){ h+='<button type="button" class="line" data-i="'+i+'"><i>'+(i+1)+'</i>'+esc(ln)+'</button>'; }); h+='</div>';
  b.innerHTML=h;
  b.querySelector('.code').addEventListener('click',function(e){ var l=e.target.closest('.line'); if(!l) return; S.cur.sel=+l.getAttribute('data-i');
    Array.prototype.forEach.call(b.querySelectorAll('.line'),function(x){x.classList.toggle('sel',x===l);}); });
}
function rOrd(b,it){
  var mix=shuffle(it.items.map(function(x,i){return i;})); if(mix.join()===it.items.map(function(x,i){return i;}).join()) mix.reverse(); S.cur.mix=mix;
  function paint(){
    var h='<div class="ord"><div class="col"><h4>ขั้นตอนทั้งหมด (แตะเพื่อเพิ่มเข้าลำดับ)</h4>';
    mix.forEach(function(i){ if(S.cur.ord.indexOf(i)<0) h+='<button type="button" data-i="'+i+'" data-a="add">'+esc(it.items[i])+'</button>'; });
    h+='</div><div class="col"><h4>ลำดับของคุณ (แตะเพื่อนำออก)</h4>';
    for(var k=0;k<it.items.length;k++){ var v=S.cur.ord[k]; h+= v==null?'<button type="button" class="slot"><b>'+(k+1)+'</b></button>':'<button type="button" data-i="'+v+'" data-a="rm" data-k="'+k+'"><b>'+(k+1)+'</b>'+esc(it.items[v])+'</button>'; }
    h+='</div></div>'; b.innerHTML=h;
    S.cur.sel=S.cur.ord.length===it.items.length?S.cur.ord.slice():null;
  }
  b.onclick=function(e){ var t=e.target.closest('button[data-a]'); if(!t||S.cur.done) return; var i=+t.getAttribute('data-i');
    if(t.getAttribute('data-a')==='add') S.cur.ord.push(i); else S.cur.ord.splice(S.cur.ord.indexOf(i),1); paint(); };
  paint();
}

/* ---------- คำใบ้และส่งคำตอบ ---------- */
$('#btnHint').addEventListener('click',function(){
  if(!S.cur||S.cur.hint) return; S.cur.hint=true; this.disabled=true;
  var d=D.createElement('div'); d.className='hint'; d.innerHTML='<b>คำใบ้:</b> '+S.cur.it.h; $('#qBody').insertBefore(d,$('#qBody').firstChild);
});
$('#btnSure').addEventListener('click',function(){submit('sure');});
$('#btnUnsure').addEventListener('click',function(){submit('unsure');});
function judge(it,sel){
  if(it.t==='mcq') return sel===0;
  if(it.t==='num'){ var v=parseFloat(String(sel).replace(',','.').replace(/[^\d.\-]/g,'')); return !isNaN(v)&&v>=it.lo&&v<=it.hi; }
  if(it.t==='pin') return it.ok.indexOf(String(sel))>=0;
  if(it.t==='bug') return it.ok.indexOf(sel)>=0;
  if(it.t==='order') return sel.join()===it.items.map(function(x,i){return i;}).join();
  return false;
}
function submit(conf){
  var c=S.cur; if(!c||c.done) return;
  if(c.sel==null||c.sel===''){ $('#actNote').textContent=c.it.t==='order'?'เรียงให้ครบทุกขั้นตอนก่อนส่ง':'เลือกหรือกรอกคำตอบก่อนส่ง'; var a=$('#acts'); a.classList.remove('shake'); void a.offsetWidth; a.classList.add('shake'); return; }
  c.done=true; var it=c.it, ok=judge(it,c.sel), pts=ok?W[it.l]*(c.hint?.5:1):0;
  S.log.push({k:S.i,id:it.id,s:it.s,l:it.l,t:it.t,ok:ok,conf:conf,hint:c.hint,tp:it.tp,safe:!!it.safe,g:it.g||'',pts:pts,e:it.e});
  S.lvl[it.s]=ok?Math.min(3,it.l+1):Math.max(1,it.l-1);
  var blown=false; if(ok){S.combo++;S.bestCombo=Math.max(S.bestCombo,S.combo);} else {S.combo=0; if(it.safe&&S.fuses>0){S.fuses--;blown=S.fuses;}}
  drawCombo(); drawFuses(blown===false?false:blown); drawTrace();
  $('#qcard').classList.add('lock',ok?'flash-ok':'flash-no');
  mark(it,c,ok);
  var vd=$('#fbVd'); vd.className='vd '+(ok?'ok':'no'); vd.textContent=ok?'PASS':'SPARK!';
  var tx='';
  if(!ok) tx+='<p class="ans">คำตอบที่ถูก: '+answerText(it)+'</p>';
  if(!ok&&it.safe) tx+='<p style="color:var(--bad);font-weight:600">ข้อความปลอดภัย: ฟิวส์ขาด 1 ดวง'+(S.fuses===0?' · ฟิวส์หมดแล้ว ผลรอบนี้จะยังไม่ได้ใบอนุญาต แต่ทำต่อเพื่อดูโปรไฟล์ทักษะให้ครบ':'')+'</p>';
  if(ok&&conf==='unsure') tx+='<p style="color:var(--a)">ถูกต้อง แต่คุณยังไม่มั่นใจ เรื่องนี้ควรทวนให้แน่นก่อนวันประกอบจริง</p>';
  if(!ok&&conf==='sure') tx+='<p style="color:var(--bad)">ตอบผิดแบบมั่นใจ เรื่องนี้จะถูกจัดเป็นลำดับแรกในใบสั่งทบทวน</p>';
  tx+='<p>'+it.e+'</p>';
  $('#fbTx').innerHTML=tx; $('#acts').style.display='none'; $('#fb').classList.add('on');
  $('#btnNext').textContent=S.i+1>=S.seq.length?'ไปด่านบอส Smoke Test':'ข้อถัดไป';
  setTimeout(function(){try{$('#btnNext').focus({preventScroll:true});}catch(e){}},50);
}
function answerText(it){
  if(it.t==='mcq') return it.c[0];
  if(it.t==='num') return it.ans+' '+(it.unit||'');
  if(it.t==='pin') return it.ok.length>6?('ขาใดก็ได้ในกลุ่มที่ไฮไลต์สีเขียว เช่น '+it.ok.slice(0,6).map(pinName).join(', ')):it.ok.map(pinName).join(' หรือ ');
  if(it.t==='bug') return 'บรรทัดที่ '+it.ok.map(function(i){return i+1;}).join(', ');
  if(it.t==='order') return it.items.map(function(x,i){return (i+1)+') '+x;}).join(' · ');
  return '';
}
function mark(it,c,ok){
  var b=$('#qBody');
  if(it.t==='mcq') Array.prototype.forEach.call(b.querySelectorAll('.opt'),function(o){ var ci=+o.getAttribute('data-c'); if(ci===0) o.classList.add('ok'); else if(ci===c.sel) o.classList.add('bad'); });
  if(it.t==='num') b.querySelector('.numrow').classList.add(ok?'ok':'bad');
  if(it.t==='bug') Array.prototype.forEach.call(b.querySelectorAll('.line'),function(l){ var i=+l.getAttribute('data-i'); if(it.ok.indexOf(i)>=0) l.classList.add('ok'); else if(i===c.sel) l.classList.add('bad'); });
  if(it.t==='pin') Array.prototype.forEach.call(D.querySelectorAll('#bbox .np-pin'),function(p){ var k=p.getAttribute('data-k'); p.classList.remove('q-sel'); if(it.ok.indexOf(k)>=0) p.classList.add('q-ok'); else if(k===String(c.sel)) p.classList.add('q-bad'); });
  if(it.t==='order') Array.prototype.forEach.call(b.querySelectorAll('button[data-a="rm"]'),function(x){ var k=+x.getAttribute('data-k'); x.classList.add(+x.getAttribute('data-i')===k?'ok':'bad'); });
}
$('#btnNext').addEventListener('click',function(){ next(false); });
D.addEventListener('keydown',function(e){
  if(!$('#sPlay').classList.contains('on')||!S||!S.cur) return;
  if(S.cur.done&&e.key==='Enter'){ e.preventDefault(); next(false); return; }
  if(!S.cur.done&&S.cur.it.t==='mcq'&&/^[1-4]$/.test(e.key)){ var o=D.querySelectorAll('#qBody .opt')[+e.key-1]; if(o) o.click(); }
});

/* ---------- บอส Smoke Test ---------- */
var B=null;
function bossStart(){
  var set=DATA.boss[Math.floor(Math.random()*DATA.boss.length)];
  B={set:set,ans:{},left:DATA.bossSec,done:false,t:null};
  $('#bTitle').innerHTML='<span>SMOKE TEST</span> · '+esc(set.t); $('#bSec').textContent=DATA.bossSec; $('#bNote').textContent='';
  var h=''; set.rows.forEach(function(r,i){ h+='<div class="brow" data-i="'+i+'"><p>'+(i+1)+'. '+esc(r[0])+'</p><div class="tg"><button type="button" data-v="1">ผ่าน</button><button type="button" data-v="0">ต้องแก้</button></div><div class="why"></div></div>'; });
  $('#bList').innerHTML=h; $('#btnBoss').textContent='ยืนยันผลการตรวจ'; $('#btnBoss').disabled=false;
  show('sBoss'); tick();
  B.t=setInterval(tick,1000);
}
function tick(){ if(!B||B.done) return; $('#bBar').style.transform='scaleX('+Math.max(0,B.left/DATA.bossSec)+')'; $('#bNote').textContent='เหลือ '+B.left+' วินาที'; if(B.left<=0){ bossEnd(true); return; } B.left--; }
$('#bList').addEventListener('click',function(e){ var t=e.target.closest('.tg button'); if(!t||B.done) return; var row=t.closest('.brow'), i=+row.getAttribute('data-i');
  B.ans[i]=t.getAttribute('data-v')==='1'; Array.prototype.forEach.call(row.querySelectorAll('.tg button'),function(x){x.classList.toggle('on',x===t);}); });
$('#btnBoss').addEventListener('click',function(){ if(B.done){ finish(); return; } bossEnd(false); });
function bossEnd(timeout){
  B.done=true; clearInterval(B.t); var miss=0, okc=0, firstBlow=false;
  B.set.rows.forEach(function(r,i){ var a=B.ans[i], ok=(a===r[1]); if(ok) okc++;
    var hazard=r[3]&&!r[1]&&a!==false; if(hazard&&S.fuses>0){ S.fuses--; firstBlow=S.fuses; miss++; }
    S.log.push({k:-1,id:'BOSS'+i,s:r[2],l:2,t:'boss',ok:ok,conf:null,hint:false,tp:'Smoke Test: '+(r[0].length>46?r[0].slice(0,44)+'…':r[0]),safe:!!r[3],g:'',pts:ok?W[2]:0,e:r[4]});
    var row=D.querySelector('.brow[data-i="'+i+'"]'); row.classList.add('done',ok?'ok':'bad');
    row.querySelector('.why').innerHTML='<b>'+(r[1]?'ผ่าน':'ต้องแก้')+'</b> · '+esc(r[4]); });
  drawFuses(firstBlow===false?false:firstBlow); $('#bList').scrollTop=0;
  $('#bNote').textContent=(timeout?'หมดเวลา · ':'')+'ตรวจถูก '+okc+' จาก '+B.set.rows.length+' แถว'+(miss?' · ปล่อยจุดอันตรายผ่าน '+miss+' จุด ฟิวส์ขาด':'');
  $('#btnBoss').textContent='ดูผลการตรวจความพร้อม';
}

/* ---------- ผลลัพธ์ ---------- */
function scores(){
  var o={}; SK.forEach(function(s){ var L=S.log.filter(function(l){return l.s===s;}); var e=L.reduce(function(a,l){return a+l.pts;},0); o[s]=L.length?Math.round(100*e/L.length):0; });
  return o;
}
function ck(str){ var h=7; for(var i=0;i<str.length;i++) h=(h*31+str.charCodeAt(i))%9973; return ('0'+(h%97)).slice(-2); }
function makeCode(sc,tot,vd){
  var sid=S.who.sid===MASK?'XXXX':S.who.sid.slice(-4), p=function(n){return ('0'+Math.min(99,n)).slice(-2);};
  var body='BR5-'+(S.grp||'S0')+'-'+sid+'-'+SK.map(function(s){return s+p(sc[s]);}).join('')+'-T'+p(tot)+'-'+vd+'-F'+S.fuses;
  return body+'-K'+ck(body+SECRET);
}
function radar(sc){
  var n=SK.length, cx=200, cy=190, R=135, pt=function(i,v){ var a=-Math.PI/2+i*2*Math.PI/n; return [cx+Math.cos(a)*R*v, cy+Math.sin(a)*R*v]; };
  var s='<svg viewBox="-46 0 492 380" role="img" aria-label="กราฟเรดาร์ทักษะ 6 ด้าน">';
  [.25,.5,.75,1].forEach(function(f){ s+='<polygon points="'+SK.map(function(k,i){return pt(i,f).join(',');}).join(' ')+'" fill="none" stroke="var(--edge)" stroke-width="'+(f===1?1.5:1)+'"'+(f===.75?' stroke-dasharray="5 4" style="stroke:var(--a);opacity:.7"':'')+'/>'; });
  SK.forEach(function(k,i){ var p=pt(i,1); s+='<line x1="'+cx+'" y1="'+cy+'" x2="'+p[0]+'" y2="'+p[1]+'" stroke="var(--edge)"/>'; });
  s+='<polygon points="'+SK.map(function(k,i){return pt(i,Math.max(.04,sc[k]/100)).join(',');}).join(' ')+'" fill="color-mix(in srgb,var(--b) 28%,transparent)" stroke="var(--b)" stroke-width="2.5"/>';
  SK.forEach(function(k,i){ var p=pt(i,Math.max(.04,sc[k]/100)), c=sc[k]>=75?'var(--ok)':sc[k]>=50?'var(--a)':'var(--bad)'; s+='<circle cx="'+p[0]+'" cy="'+p[1]+'" r="5.5" fill="'+c+'" stroke="var(--bg)" stroke-width="2"/>';
    var q=pt(i,1.2), an=Math.abs(q[0]-cx)<10?'middle':(q[0]>cx?'start':'end');
    s+='<text x="'+q[0]+'" y="'+(q[1]+4)+'" text-anchor="'+an+'" font-size="14" font-weight="600" fill="var(--text)" font-family="Kanit,sans-serif">'+esc(DATA.skills[k].short)+' <tspan fill="'+c+'" font-family="JetBrains Mono,monospace">'+sc[k]+'</tspan></text>'; });
  s+='<text x="'+(cx+4)+'" y="'+(cy-R*.75-4)+'" font-size="10" fill="var(--a)" font-family="Kanit,sans-serif">เกณฑ์ 75</text>';
  return s+'</svg>';
}
function finish(){
  var sc=scores(), vals=SK.map(function(s){return sc[s];}), tot=Math.round(vals.reduce(function(a,b){return a+b;},0)/vals.length), mn=Math.min.apply(null,vals);
  var vd=S.fuses>0&&tot>=70&&mn>=50?'R':(S.fuses>0&&tot>=55?'C':'N');
  var stars=Math.round(tot/100*6); if(vd!=='R') stars=Math.min(stars,4); if(vd==='N') stars=Math.min(stars,3);
  show('sResult');
  $('#rWho').textContent=S.who.nick+' · '+(S.who.sid===MASK?MASK:S.who.sid)+(S.grp?' · กลุ่ม '+S.grp:'')+' · บอร์ด '+(S.board==='v30'?'30 ขา':'38 ขา');
  $('#rPct').innerHTML=tot+'%<small>คะแนนความพร้อมรวม</small>';
  var bd=$('#rBadge'); bd.className='badge '+vd; bd.textContent={R:'BENCH READY',C:'พร้อมแบบมีเงื่อนไข',N:'ต้องเตรียมเพิ่ม'}[vd];
  var st=''; for(var i=0;i<6;i++) st+='<svg viewBox="0 0 20 20"><path d="M10 1.5l2.6 5.6 6 .7-4.5 4.1 1.2 6L10 15l-5.3 2.9 1.2-6L1.4 7.8l6-.7z" fill="'+(i<stars?'#f5b301':'var(--glass2)')+'" stroke="'+(i<stars?'#b45309':'var(--edge)')+'"/></svg>'; $('#rStars').innerHTML=st;
  $('#rRadar').innerHTML=radar(sc);
  var h=''; SK.slice().sort(function(a,b){return sc[a]-sc[b];}).forEach(function(s){ var v=sc[s], c=v>=75?'g':v>=50?'y':'r', col=v>=75?'var(--ok)':v>=50?'var(--a)':'var(--bad)';
    h+='<div class="skr"><span class="dot '+c+'"></span><span>'+esc(DATA.skills[s].n)+'</span><span class="bar"><i style="width:'+v+'%;background:'+col+'"></i></span><b>'+v+'</b></div>'; });
  $('#rSkills').innerHTML=h;
  var Q=S.log.filter(function(l){return l.conf;}), n=function(f){return Q.filter(f).length;};
  var c1=n(function(l){return l.ok&&l.conf==='sure';}), c2=n(function(l){return l.ok&&l.conf==='unsure';}), c3=n(function(l){return !l.ok&&l.conf==='sure';}), c4=n(function(l){return !l.ok&&l.conf==='unsure';});
  $('#rConf').innerHTML='<div class="c1"><b>'+c1+'</b>รู้จริง (ถูกและมั่นใจ)</div><div class="c2"><b>'+c2+'</b>ถูกแต่ไม่มั่นใจ · ทวนให้แน่น</div><div class="c3"><b>'+c3+'</b>เข้าใจผิดแบบมั่นใจ · แก้ก่อนต่อวงจร</div><div class="c4"><b>'+c4+'</b>ยังไม่รู้ · เรียนเพิ่ม</div>';
  var rx='', bad=S.log.filter(function(l){return !l.ok;});
  var conf=bad.filter(function(l){return l.conf==='sure'||(l.safe&&l.t==='boss');});
  if(conf.length){ rx+='<div class="it"><h4><span class="dot r"></span>แก้ก่อนวันประกอบจริง</h4><ul>'+conf.map(function(l){return '<li><b>'+esc(l.tp)+'</b> · '+l.e+'</li>';}).join('')+'</ul></div>'; }
  SK.slice().sort(function(a,b){return sc[a]-sc[b];}).forEach(function(s){
    if(sc[s]>=75) return; var miss=bad.filter(function(l){return l.s===s;}), sk=DATA.skills[s];
    var tps=[]; miss.forEach(function(l){ if(tps.indexOf(l.tp)<0) tps.push(l.tp); });
    rx+='<div class="it"><h4><span class="dot '+(sc[s]>=50?'y':'r')+'"></span>'+esc(sk.n)+' · '+sc[s]+'%</h4>'+
      (tps.length?'<div>เรื่องที่พลาด: '+tps.map(esc).join(' · ')+'</div>':'<div>ตอบถูกแต่ใช้คำใบ้หรือได้โจทย์ระดับพื้นฐาน ลองเล่นซ้ำเพื่อเก็บระดับที่สูงขึ้น</div>')+
      '<div>ทวนที่: '+sk.review.map(function(r){return '<a href="'+r[0]+'">'+esc(r[1])+'</a>';}).join(' · ')+'</div></div>';
  });
  if(!rx) rx='<div class="it"><h4><span class="dot g"></span>พร้อมลงมือ</h4>ทุกทักษะผ่านเกณฑ์ 75% ในวันประกอบจริง ให้ทำ Smoke Test ตรวจสายก่อนจ่ายไฟทุกครั้ง และช่วยตรวจงานของเพื่อนในกลุ่ม</div>';
  if(S.fuses===0) rx='<div class="it"><h4><span class="dot r"></span>ฟิวส์หมด</h4><span class="warn">พลาดเรื่องความปลอดภัยครบ 3 ครั้ง</span> ทวนหัวข้อความปลอดภัยด้านล่าง แล้วตรวจความพร้อมใหม่ก่อนจ่ายไฟวงจรจริง</div>'+rx;
  $('#rRx').innerHTML=rx;
  var code=makeCode(sc,tot,vd); $('#rCode').textContent=code; S.code=code;
  save(sc,tot,stars,vd,code);
}
function save(sc,tot,stars,vd,code){
  try{ var all=JSON.parse(localStorage.getItem(RES_KEY)||'{}'), k=S.who.sid||MASK; all[k]=all[k]||{}; var old=all[k].game5||{};
    all[k].game5={pre:old.pre!=null?old.pre:stars,post:stars,max:6,best:Math.max(stars,old.best||0),nick:S.who.nick,at:new Date().toISOString(),plays:(old.plays||0)+1,skills:sc,total:tot,verdict:vd,code:code,group:S.grp};
    localStorage.setItem(RES_KEY,JSON.stringify(all)); }catch(e){}
}
$('#btnCopy').addEventListener('click',function(){ var c=S&&S.code; if(!c) return;
  (navigator.clipboard?navigator.clipboard.writeText(c):Promise.reject()).then(function(){toast('คัดลอกรหัสผลแล้ว');},function(){ var r=D.createRange(); r.selectNodeContents($('#rCode')); var s=getSelection(); s.removeAllRanges(); s.addRange(r); toast('เลือกข้อความไว้แล้ว กด Ctrl+C'); }); });
$('#btnAgain').addEventListener('click',function(){ start(S.who); });

/* ---------- ตรวจรหัสผล (ผู้สอน) ---------- */
$('#btnVerify').addEventListener('click',function(){ $('#dlg').classList.add('on'); $('#dlgIn').focus(); });
$('#dlgX').addEventListener('click',function(){ $('#dlg').classList.remove('on'); });
$('#dlg').addEventListener('click',function(e){ if(e.target.id==='dlg') $('#dlg').classList.remove('on'); });
D.addEventListener('keydown',function(e){ if(e.key==='Escape') $('#dlg').classList.remove('on'); });
$('#dlgGo').addEventListener('click',function(){
  var rows=$('#dlgIn').value.split(/\s+/).filter(Boolean), re=/^(BR5-(S[0-7])-(\w{4})-A(\d\d)B(\d\d)C(\d\d)D(\d\d)E(\d\d)F(\d\d)-T(\d\d)-([RCN])-F(\d))-K(\d\d)$/;
  var h='<table><tr><th>กลุ่ม</th><th>รหัสท้าย</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th><th>รวม</th><th>ผล</th><th>ฟิวส์</th><th>ตรวจ</th></tr>';
  rows.forEach(function(r){ var m=re.exec(r.trim()); if(!m){ h+='<tr><td colspan="11">'+esc(r)+'</td><td class="v0">รูปแบบผิด</td></tr>'; return; }
    var ok=ck(m[1]+SECRET)===m[13];
    h+='<tr><td>'+m[2]+'</td><td>'+m[3]+'</td><td>'+m[4]+'</td><td>'+m[5]+'</td><td>'+m[6]+'</td><td>'+m[7]+'</td><td>'+m[8]+'</td><td>'+m[9]+'</td><td>'+m[10]+'</td><td>'+{R:'READY',C:'มีเงื่อนไข',N:'เตรียมเพิ่ม'}[m[11]]+'</td><td>'+m[12]+'</td><td class="'+(ok?'v1':'v0')+'">'+(ok?'ถูกต้อง':'ถูกแก้ไข')+'</td></tr>'; });
  $('#dlgOut').innerHTML=h+'</table>';
});
window.BENCH={state:function(){return S;}};
})();
</script>
</body>
</html>
"""


def build():
    G.validate()
    bank_lint.check_bank(MCQ, 'game5')
    neo = os.path.join(TOOLS, 'neo')
    pin_css = open(os.path.join(neo, 'pinout.css'), encoding='utf-8').read()
    pin_js = open(os.path.join(neo, 'pinout.js'), encoding='utf-8').read()
    data = {'items': G.ITEMS, 'skills': G.SKILLS, 'groups': G.GROUPS,
            'boss': [{'t': b['t'], 'rows': [list(r) for r in b['rows']]} for b in G.BOSS], 'bossSec': G.BOSS_SECONDS}
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    html = PAGE.replace('__PINCSS__', pin_css).replace('__PINJS__', pin_js).replace('__DATA__', js)
    out = os.path.join(ROOT, CFG['filename'])
    open(out, 'w', encoding='utf-8').write(html)
    print('%s written · %d items (%d mcq) · %d boss sets' % (CFG['filename'], len(G.ITEMS), sum(len(v) for v in MCQ.values()), len(G.BOSS)))


if __name__ == '__main__':
    build()
