# -*- coding: utf-8 -*-
"""GAME 3 — SENSOR HUNTER : ล่าเซนเซอร์ทั่วสนาม
อ้างอิงคลิปทบทวนที่ 3: 38 Arduino Sensors You Should Know — How They Work & Where to Use Them"""
from cpe_common import *

THEME = {
    "PRIMARY_RGB": "52,211,153",  "PRIMARY_HEX": "#34d399",
    "SECOND_RGB":  "244,114,182", "SECOND_HEX":  "#f472b6",
    "GOLD_RGB":    "250,204,21",  "GOLD_HEX":    "#facc15",
    "GOLD2_RGB":   "254,240,138", "GOLD2_HEX":   "#fef08b",
    "RED_RGB":     "248,113,113", "RED_HEX":     "#f87171",
    "BG_RGB":      "3,18,13",     "BG_HEX":      "#03120d",
    "PANEL_RGB":   "8,38,28",
    "PANEL2_RGB":  "12,50,37",
    "BG2_HEX":     "#061d15",
    "INK_HEX":     "#072519",
    "TEXT_HEX":    "#e5faf1",
    "MUTED_HEX":   "#94c2b0",
    "MUTED2_HEX":  "#5e8a79",
    "MUTED3_HEX":  "#4c7666",
    "SECOND2_HEX": "#f9a8d4",
    "PRIM2_HEX":   "#6ee7b7",
    "LIGHT_EMBER": "#047857", "LIGHT_CORNER": "#be185d", "LIGHT_GOLD": "#a16207",
    "LIGHT_GOLD2": "#854d0e", "LIGHT_RED": "#b91c1c",
}

EXTRA_CSS = LAB_CSS + """
.questrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px;margin:10px 0}
.optrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:10px 0;min-height:48px}
.optrow .pick{text-align:center;font-weight:600}
.dexgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:7px;margin:12px 0}
.dexgrid .pick{font-size:.8rem;padding:9px 9px 8px;min-height:64px}
.dexgrid .pick .no{display:block;font-family:var(--mono);font-size:.68rem;color:var(--muted);letter-spacing:1px}
.dexgrid .pick.g-a{border-left:3px solid var(--ember)} .dexgrid .pick.g-d{border-left:3px solid var(--corner)}
.dexgrid .pick.g-b{border-left:3px solid var(--gold)} .dexgrid .pick.g-o{border-left:3px solid var(--red)}
.sigtag{display:inline-block;font-family:var(--mono);font-size:.72rem;padding:1px 8px;border-radius:999px;background:var(--ember-dim);border:1px solid var(--line);margin-left:6px}
.divfig{font-family:var(--mono);font-size:.86rem;line-height:1.5;padding:12px 14px;border-radius:12px;border:1px solid var(--line);background:rgba(var(--ink-panel-rgb),.6);white-space:pre}
@media(max-width:560px){.dexgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:7px;margin:12px 0}
.dexgrid .pick{font-size:.8rem;padding:9px 9px 8px;min-height:64px}
.dexgrid .pick .no{display:block;font-family:var(--mono);font-size:.68rem;color:var(--muted);letter-spacing:1px}
.dexgrid .pick.g-a{border-left:3px solid var(--ember)} .dexgrid .pick.g-d{border-left:3px solid var(--corner)}
.dexgrid .pick.g-b{border-left:3px solid var(--gold)} .dexgrid .pick.g-o{border-left:3px solid var(--red)}
.sigtag{display:inline-block;font-family:var(--mono);font-size:.72rem;padding:1px 8px;border-radius:999px;background:var(--ember-dim);border:1px solid var(--line);margin-left:6px}
.divfig{font-size:.74rem}}
"""

HERO = """<svg class="cityart" viewBox="0 0 480 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ภาพจอเรดาร์ล่าเซนเซอร์">
  <defs>
    <radialGradient id="gRad" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(52,211,153,.30)"/><stop offset="100%" stop-color="rgba(52,211,153,0)"/></radialGradient>
    <filter id="fGlow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x="0" y="0" width="480" height="300" rx="18" fill="#03120d"/>
  <circle cx="240" cy="140" r="120" fill="url(#gRad)"/>
  <g fill="none" stroke="#34d399" stroke-width="1.5" opacity=".6">
    <circle cx="240" cy="140" r="40"/><circle cx="240" cy="140" r="80"/><circle cx="240" cy="140" r="120"/>
    <path d="M120 140 H360 M240 20 V260"/>
  </g>
  <path d="M240 140 L340 74 A120 120 0 0 1 360 140 Z" fill="rgba(52,211,153,.35)"/>
  <g filter="url(#fGlow)">
    <circle cx="312" cy="104" r="6" fill="#facc15"/><circle cx="178" cy="92" r="6" fill="#f472b6"/>
    <circle cx="200" cy="198" r="6" fill="#34d399"/><circle cx="300" cy="200" r="6" fill="#f472b6"/>
  </g>
  <g font-family="monospace" font-size="10" font-weight="700">
    <text x="322" y="100" fill="#facc15">MQ-3</text><text x="120" y="88" fill="#f472b6">HC-SR04</text>
    <text x="150" y="214" fill="#34d399">DS18B20</text><text x="310" y="216" fill="#f472b6">PMS5003</text>
  </g>
  <text x="240" y="288" text-anchor="middle" font-size="10" letter-spacing="3" fill="#94c2b0">SCAN · IDENTIFY · CONNECT · CALIBRATE</text>
</svg>"""


# ---- คลังข้อมูล 38 เซนเซอร์ตามลำดับในคลิป (จากสรุปของผู้สอน) ----
SENSORS = [
 # (ลำดับ, ชื่อ, ชื่อไทย, ชนิดสัญญาณ, กลุ่มกรอง, หลักการ, การประยุกต์ Smart)
 (1,'Push Button','ปุ่มกด','Digital In','d','อินพุตดิจิทัล HIGH/LOW ต้องทำ Debounce ตัดการสั่นของหน้าสัมผัส','ปุ่มหยุดฉุกเฉิน, ปุ่มเลือกโหมดแมนนวล'),
 (2,'Joystick Module','คันโยกควบคุม','Analog ×2 + Digital','a','Potentiometer 2 ตัว (แกน X, Y เข้า ADC) และปุ่มกดอีก 1 ปุ่ม','ควบคุมหุ่นยนต์สำรวจ แท่นกล้อง Pan-Tilt ผ่าน Wi-Fi'),
 (3,'NTC Thermistor','เทอร์มิสเตอร์ NTC','Analog','a','ความต้านทานลดลงเมื่ออุณหภูมิสูงขึ้น อ่านผ่านวงจรแบ่งแรงดันเข้า ADC','เฝ้าอุณหภูมิเครื่องจักร ระบบจัดการพลังงาน'),
 (4,'LDR','ตัวต้านทานไวแสง','Analog','a','ความต้านทานลดลงเมื่อแสงมากขึ้น อ่านผ่านวงจรแบ่งแรงดัน','ไฟถนนอัตโนมัติ ส่งค่าความสว่างขึ้น Dashboard'),
 (5,'DS18B20','เซนเซอร์อุณหภูมิดิจิทัล','1-Wire','b','ประมวลผลในตัว สื่อสาร One-Wire ต้องมี pull-up มีแอดเดรสไม่ซ้ำกัน','วัดอุณหภูมิถังน้ำหลายใบบนสายเส้นเดียว'),
 (6,'DHT11','อุณหภูมิและความชื้น','Digital Single-Bus','b','วัดอุณหภูมิและความชื้นสัมพัทธ์ ส่งข้อมูลดิจิทัลสายเดียว','มอนิเตอร์ห้องแล็บ โรงเรือนอัจฉริยะ'),
 (7,'MQ-2','แก๊สและควัน','Analog + Digital','a','ความต้านทานเปลี่ยนเมื่อสัมผัสแก๊สติดไฟหรือควัน AO ดูแนวโน้ม DO เทียบเกณฑ์','เตือนแก๊สรั่วและควันไฟ (ต้องคาลิเบรต)'),
 (8,'HC-SR04','วัดระยะอัลตราโซนิก','Digital Timing','d','จับเวลาคลื่นสะท้อน Trig/Echo คำนวณระยะแบบไม่สัมผัส','ถังขยะอัจฉริยะ ระดับน้ำ หุ่นยนต์หลบหลีก'),
 (9,'Flame Sensor','ตรวจเปลวไฟ','Analog + Digital','a','ตรวจรังสีอินฟราเรดจากเปลวไฟ','เฝ้าระวังอัคคีภัยห้องเครื่องจักร หุ่นยนต์ดับเพลิง'),
 (10,'IR Receiver','รับสัญญาณอินฟราเรด','Digital Pulse','d','รับและถอดสัญญาณ IR ที่มอดูเลต (มักเป็น 38 kHz) จากรีโมท','สั่งงานอุปกรณ์ในอาคารด้วยรีโมท'),
 (11,'IR Transmitter','ส่งสัญญาณอินฟราเรด','Output (PWM)','o','LED อินฟราเรดส่งรหัสที่มอดูเลตตามโปรโตคอล','รีโมทครอบจักรวาล ESP32 สั่งแอร์'),
 (12,'Laser Transmitter','กำเนิดลำแสงเลเซอร์','Output (Digital)','o','สร้างลำแสงเลเซอร์ ควบคุมเปิด/ปิด ห้ามส่องเข้าตา','Laser Tripwire นับวัตถุที่ตัดลำแสง'),
 (13,'Optical Light Barrier','สวิตช์แสงกั้น','Digital In','d','ตัวส่งและตัวรับหันหน้าเข้าหากัน วัตถุตัดลำแสงแล้วสถานะเปลี่ยน','นับชิ้นงานบนสายพาน'),
 (14,'Obstacle Avoidance','ตรวจสิ่งกีดขวางระยะใกล้','Digital In','d','ปล่อย IR แล้ววัดแสงสะท้อนกลับจากวัตถุ','ป้องกันชนของหุ่นยนต์ส่งของ'),
 (15,'Line Tracking','ตรวจจับเส้นทาง','Digital/Analog','d','พื้นสว่างสะท้อน IR มากกว่าพื้นมืด','AGV เดินตามเส้นในโรงงาน'),
 (16,'Reed Switch','สวิตช์แม่เหล็กหลอดแก้ว','Digital In','d','หน้าสัมผัสต่อ/ตัดเมื่อแม่เหล็กเข้าใกล้','ตรวจประตูหน้าต่างเปิด-ปิด'),
 (17,'PIR Motion','ตรวจความเคลื่อนไหว PIR','Digital In','d','ตรวจการเปลี่ยนแปลงรังสี IR จากวัตถุร้อนที่เคลื่อนที่','เปิดไฟตามการใช้ห้อง ระบบกันขโมย'),
 (18,'Digital Hall','สนามแม่เหล็กดิจิทัล','Digital In','d','เปลี่ยนสถานะเมื่อมีสนามแม่เหล็ก','นับพัลส์วัดรอบมอเตอร์ (RPM)'),
 (19,'Linear Hall','สนามแม่เหล็กเชิงเส้น','Analog','a','แรงดันแปรตามความเข้มสนามแม่เหล็ก','วัดตำแหน่งเชิงเส้นละเอียด'),
 (20,'Vibration Sensor','ตรวจการสั่นสะเทือน','Digital In','d','สวิตช์กลไกเปลี่ยนสถานะเมื่อสั่นหรือกระแทก','กันขโมย ตรวจการงัดแงะ'),
 (21,'Tilt Switch','ตรวจการเอียง','Digital In','d','หน้าสัมผัสภายในเปลี่ยนเมื่อเอียงจากตำแหน่งปกติ','ตรวจเสาไฟหรือป้ายล้ม/เอียง'),
 (22,'Rotary Encoder','ตัวหมุนรหัสเชิงมุม','Digital ×3','d','พัลส์ 2 เฟสบอกระยะและทิศทาง พร้อมปุ่มกด','ปุ่มหมุนปรับเมนู HMI'),
 (23,'Touch Sensor','เซนเซอร์สัมผัส','Digital In','d','ตรวจการสัมผัสด้วยความจุไฟฟ้า (หรือ Touch Pin ของ ESP32)','สวิตช์สัมผัส แผงควบคุมกันน้ำ'),
 (24,'Knock Sensor','ตรวจการเคาะ','Digital/Analog','d','ตรวจแรงเคาะหรือการสั่นสั้น ๆ','ปลดล็อกประตูด้วยจังหวะเคาะ'),
 (25,'Sound Sensor','เซนเซอร์เสียงความไวสูง','Analog + Digital','a','ไมโครโฟนกับวงจรขยาย AO และ DO ตามเกณฑ์','ตบมือเปิดไฟ ตรวจเสียงดังผิดปกติ'),
 (26,'TCS3200','จำแนกสี','Frequency','b','ตัวรับแสงกับฟิลเตอร์ RGB ให้เอาต์พุตเป็นความถี่ตามความเข้มสี','คัดแยกสีชิ้นงานบนสายพาน'),
 (27,'Pulse Sensor','อัตราการเต้นหัวใจ','Analog','a','วัดปริมาตรเลือดใต้ผิวด้วยแสง (PPG)','มอนิเตอร์ความเหนื่อยล้าของคนงาน'),
 (28,'Active Buzzer','บัซเซอร์แบบแอคทีฟ','Output (Digital)','o','มีวงจรกำเนิดความถี่ในตัว จ่าย HIGH ก็ดัง','เสียงเตือนสถานะ'),
 (29,'Passive Buzzer','บัซเซอร์แบบพาสซีฟ','Output (PWM)','o','ต้องป้อนความถี่ด้วย PWM จึงเปลี่ยนโทนเสียงได้','เตือนไล่ระดับเสียงตามความรุนแรง'),
 (30,'RGB LED','LED สามสี','Output (PWM ×3)','o','ผสมแดง เขียว น้ำเงิน ด้วย PWM 3 ช่อง','ไฟสถานะ เขียว=ปกติ แดง=ผิดปกติ'),
 (31,'Soil Moisture','ความชื้นในดิน','Analog + Digital','a','วัดการนำไฟฟ้าของดินระหว่างอิเล็กโทรด','รดน้ำอัตโนมัติ ฟาร์มอัจฉริยะ'),
 (32,'Rain Sensor','ตรวจน้ำฝน','Analog + Digital','a','หยดน้ำบนลายทองแดงเปลี่ยนการนำไฟฟ้า','ปิดหน้าต่างเมื่อฝนตก'),
 (33,'Load Cell + HX711','วัดแรงและน้ำหนัก','HX711 (DT/SCK)','b','Strain gauge ใน Wheatstone bridge ให้สัญญาณเล็กมาก HX711 ขยายและแปลง 24 บิต','เครื่องชั่ง วัดแรงกดโครงสร้าง'),
 (34,'Flex Sensor','วัดการโค้งงอ','Analog','a','ความต้านทานเปลี่ยนตามองศาการงอ','ถุงมือสั่งงานแขนกล'),
 (35,'RFID RC522','เครื่องอ่าน RFID','SPI','b','อ่านรหัสแท็ก 13.56 MHz ไร้สาย สื่อสารกับ MCU ผ่าน SPI','ควบคุมการเข้าออก ลงเวลา'),
 (36,'Relay Module','โมดูลรีเลย์','Output (Digital)','o','สวิตช์ควบคุมด้วยไฟฟ้า แยกวงจรควบคุมแรงดันต่ำออกจากวงจรโหลดแรงดันสูง','สั่งปั๊มน้ำ พัดลม หลอดไฟ'),
 (37,'Fingerprint','สแกนลายนิ้วมือ','UART','b','ประมวลผลลายนิ้วมือในโมดูล เทียบ Template ส่งผลทาง UART','ประตูความปลอดภัยสูง ลงเวลา'),
 (38,'RCWL-0516','เรดาร์ไมโครเวฟ','Digital In','d','ส่งไมโครเวฟและจับคลื่นสะท้อนแบบ Doppler ตรวจผ่านวัสดุบางที่ไม่ใช่โลหะได้','ตรวจคนแบบซ่อนใต้ฝ้า'),
]
import json as _json
SENSORS_JS = _json.dumps([{'n':a,'name':b,'th':c,'sig':d,'g':e,'how':f,'app':g} for a,b,c,d,e,f,g in SENSORS], ensure_ascii=False)

ZONES = """
<!-- ===== PREVIEW 1 ===== -->
<section id="scr-preview1" class="screen">
  <div class="panel">
    <span class="tag">Before Hunt 01</span>
    <h2>กำลังจะเข้าสู่: ล่าที่ 1 สมุดสะสมเซนเซอร์ (Sensor Dex)</h2>
    <div class="dcard">
      <div class="ico"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="12" y="12" width="24" height="24" rx="5" fill="#34d399"/><rect x="44" y="12" width="24" height="24" rx="5" fill="none" stroke="#f472b6" stroke-width="3"/>
        <rect x="12" y="44" width="24" height="24" rx="5" fill="none" stroke="#facc15" stroke-width="3"/><rect x="44" y="44" width="24" height="24" rx="5" fill="#f472b6"/></svg></div>
      <div><div class="skillcard" style="margin:0">
        <div class="sk-name">ทักษะที่จะได้: รู้จักเซนเซอร์ 38 ชนิดในคลิป แยกชนิดสัญญาณ และงานแอนะล็อกเชิงสิ่งแวดล้อม</div>
        <p class="muted" style="margin:6px 0 0">NTC, LDR, DS18B20, DHT11, MQ-2, Flame, Sound, Soil, Rain, Pulse, Flex, Joystick และ Linear Hall</p>
      </div></div>
    </div>
    <div class="btn-row"><button class="btn primary" data-goto="scr-lesson1">ออกล่า</button></div>
  </div>
</section>

<!-- ===== HUNT 1 ===== -->
<section id="scr-lesson1" class="screen">
  <div class="panel">
    <span class="tag">Hunt 01 · Sensor Dex</span>
    <h2>ล่าที่ 1: สมุดสะสมเซนเซอร์ 38 ชนิด</h2>
    <p>เซนเซอร์คือ "ประสาทสัมผัส" ของระบบ ก่อนเลือกตัวใดให้ตอบ 3 คำถามของ <b>System Design Framework</b> ให้ได้ก่อนเสมอ</p>
    <div class="flowrow">
      <div class="fbox in"><b>1 · REQUIREMENTS</b>ช่วงการวัด (Range) ความแม่นยำ (Accuracy) ความละเอียด (Resolution) และอินเทอร์เฟซ: Analog, Digital, 1-Wire, SPI, UART</div>
      <div class="fbox"><b>2 · EMBEDDED LOOP</b>Physical World → Sensor → Microcontroller (Logic) → Actuator (Output)</div>
      <div class="fbox out"><b>3 · PRACTICE</b>คาลิเบรต (MQ-2, HX711) · Debounce สวิตช์กลไก · ความปลอดภัยเมื่อใช้รีเลย์กับไฟแรงสูง</div>
    </div>
    <div class="tbl-wrap"><table>
      <tr><th>ชนิดสัญญาณ</th><th>อ่านด้วย</th><th>ตัวอย่างจากคลิป</th></tr>
      <tr><td>Analog</td><td>ADC (ESP32: ขา ADC1 GPIO32–39)</td><td>NTC, LDR, Flex, Pulse, Linear Hall, Joystick</td></tr>
      <tr><td>Analog + Digital (AO/DO)</td><td>ADC หรือ digitalRead ตามเกณฑ์ที่หมุนตั้ง</td><td>MQ-2, Flame, Sound, Soil, Rain</td></tr>
      <tr><td>Digital</td><td>digitalRead / interrupt</td><td>Button, PIR, Reed, Hall, Tilt, Vibration, RCWL-0516</td></tr>
      <tr><td>โปรโตคอลเฉพาะ</td><td>ไลบรารี</td><td>DS18B20 (1-Wire), DHT11 (Single-Bus), RC522 (SPI), Fingerprint (UART), HX711, TCS3200 (ความถี่)</td></tr>
      <tr><td>เอาต์พุต</td><td>digitalWrite / PWM</td><td>Buzzer, RGB LED, Relay, IR/Laser Transmitter</td></tr>
    </table></div>

    <h3 style="margin-top:18px">ห้องทดลอง: สมุดสะสมเซนเซอร์ (Sensor Dex)</h3>
    <p class="muted">แตะการ์ดเพื่อสแกนเซนเซอร์แต่ละตัว ใช้ปุ่มกรองตามชนิดสัญญาณ — สะสมครบ 30 ใบขึ้นไปรับเหรียญตรา</p>
    <div class="labrow">
      <button class="btn sm" data-dexf="all">ทั้งหมด</button><button class="btn sm" data-dexf="a">Analog</button>
      <button class="btn sm" data-dexf="d">Digital</button><button class="btn sm" data-dexf="b">โปรโตคอล</button>
      <button class="btn sm" data-dexf="o">เอาต์พุต</button>
      <span class="readout" id="dexCount">0<small>/ 38 ใบ</small></span>
    </div>
    <div class="dexgrid" id="dexGrid"></div>
    <div class="status-line" id="dexStatus">ยังไม่ได้สแกนการ์ดใด</div>
    <div class="btn-row"><button class="btn primary" data-quiz="check1">ไปทำแบบฝึกหัดด่านนี้</button></div>
  </div>
</section>

<!-- ===== PREVIEW 2 ===== -->
<section id="scr-preview2" class="screen">
  <div class="panel">
    <span class="tag">Before Hunt 02</span>
    <h2>กำลังจะเข้าสู่: ล่าที่ 2 ทุ่งเคลื่อนไหว (Motion Plains)</h2>
    <div class="dcard">
      <div class="ico"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <path d="M24 26a20 20 0 0 1 0 28M32 18a30 30 0 0 1 0 44" stroke="#34d399" stroke-width="3" fill="none"/>
        <rect x="52" y="28" width="16" height="24" rx="3" fill="#f472b6"/></svg></div>
      <div><div class="skillcard" style="margin:0">
        <div class="sk-name">ทักษะที่จะได้: ระยะทาง การมีคนอยู่ ตำแหน่ง และสวิตช์</div>
        <p class="muted" style="margin:6px 0 0">คำนวณระยะ HC-SR04 เทียบ PIR กับเรดาร์ไมโครเวฟ และใช้ Reed, Hall, Tilt, Encoder, Light barrier ให้ถูกงาน</p>
      </div></div>
    </div>
    <div class="btn-row"><button class="btn primary" data-goto="scr-lesson2">ออกล่า</button></div>
  </div>
</section>

<!-- ===== HUNT 2 ===== -->
<section id="scr-lesson2" class="screen">
  <div class="panel">
    <span class="tag">Hunt 02 · Motion Plains</span>
    <h2>ล่าที่ 2: ระยะทาง การเคลื่อนไหว และตำแหน่ง</h2>
    <p><b>HC-SR04</b> ปล่อยคลื่นอัลตราโซนิก 40 kHz แล้วจับเวลาเสียงสะท้อน ระยะทาง = เวลา × ความเร็วเสียง ÷ 2
      ส่วน <b>PIR</b> ตรวจ <b>การเปลี่ยนแปลง</b> ของรังสีอินฟราเรด จึงจับคนที่เคลื่อนที่ได้ดีแต่ <b>มองไม่เห็นคนนั่งหรือนอนนิ่ง</b>
      และ <b>RCWL-0516</b> ใช้คลื่นไมโครเวฟแบบ Doppler ตรวจผ่านวัสดุบางที่ไม่ใช่โลหะได้</p>
    <div class="codebox">ความเร็วเสียงในอากาศ  v ≈ 331.3 + 0.606 × T(°C)  m/s   (ที่ 20 °C ≈ 343 m/s)
ระยะ (cm) = t(µs) × 0.0343 / 2  ≈  t / 58
ตัวอย่าง: t = 580 µs  →  580 × 0.0343 / 2 ≈ 9.9 cm   · ช่วงวัดของ HC-SR04 ราว 2–400 cm</div>
    <div class="tbl-wrap"><table>
      <tr><th>เซนเซอร์</th><th>หลักการ</th><th>ใช้ในโปรเจกต์</th></tr>
      <tr><td>PIR</td><td>การเปลี่ยนแปลงรังสีอินฟราเรด</td><td>คนเดินผ่าน เปิดไฟ/เครื่องไล่แมลง</td></tr>
      <tr><td>RCWL-0516</td><td>ไมโครเวฟ Doppler จับวัตถุเคลื่อนที่ ซ่อนหลังฝ้าได้</td><td>ตรวจคนแบบซ่อนอุปกรณ์</td></tr>
      <tr><td>mmWave (เช่น LD2410)</td><td>เรดาร์ 24 GHz จับการขยับเล็กน้อยอย่างการหายใจ</td><td>รู้ว่ามีคนนอนอยู่ (Smart AC)</td></tr>
      <tr><td>Reed / Digital Hall</td><td>สนามแม่เหล็กเปลี่ยนสถานะ</td><td>ประตูเปิด-ปิด · นับรอบ RPM</td></tr>
      <tr><td>Tilt / Vibration / Knock</td><td>สวิตช์กลไกหรือเพียโซตอบสนองการเอียง สั่น เคาะ</td><td>เสาไฟล้ม งัดแงะ ตรวจแรงกระแทก</td></tr>
      <tr><td>Rotary Encoder</td><td>พัลส์ 2 เฟส (A/B) บอกระยะและทิศทาง</td><td>ปุ่มหมุนตั้งเกณฑ์บนจอ</td></tr>
      <tr><td>Light barrier / Laser + LDR</td><td>วัตถุตัดลำแสงแล้วสถานะเปลี่ยน</td><td>นับชิ้นงาน ระบบกันบุกรุก</td></tr>
    </table></div>

    <h3 style="margin-top:18px">ห้องทดลอง: เครื่องวัดระยะอัลตราโซนิก</h3>
    <p class="muted">เลื่อนเวลาเสียงสะท้อน (echo) และสลับอุณหภูมิอากาศ — ลองให้เจอทั้งระยะปกติ ใกล้เกิน และไกลเกิน</p>
    <div class="labrow"><button class="toggle on" id="usTemp">อากาศ 20 °C</button></div>
    <input type="range" class="rng" id="usT" min="50" max="26000" value="1160" aria-label="เวลาเสียงสะท้อน">
    <div class="labrow"><span class="readout" id="usTime">1160<small>µs</small></span><span class="readout" id="usDist">19.9<small>cm</small></span></div>
    <div class="meter"><i id="usBar"></i></div>
    <div class="status-line" id="usStatus">เลื่อนแถบเพื่อเริ่มวัด</div>
    <h3 style="margin-top:14px">PIR ปะทะ เรดาร์</h3>
    <div class="labrow">
      <button class="btn sm" data-pir="walk">คนเดินเข้าห้อง</button>
      <button class="btn sm" data-pir="still">คนนอนหลับนิ่ง</button>
      <button class="btn sm" data-pir="wall">คนเดินหลังฝ้ายิปซัม</button>
    </div>
    <div class="status-line" id="pirStatus">เลือกสถานการณ์เพื่อเทียบผลของเซนเซอร์</div>
    <div class="btn-row"><button class="btn primary" data-quiz="check2">ไปทำแบบฝึกหัดด่านนี้</button></div>
  </div>
</section>

<!-- ===== PREVIEW 3 ===== -->
<section id="scr-preview3" class="screen">
  <div class="panel">
    <span class="tag">Before Hunt 03</span>
    <h2>กำลังจะเข้าสู่: ล่าที่ 3 ถ้ำถอดรหัสสัญญาณ (Signal Cave)</h2>
    <div class="dcard">
      <div class="ico"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <path d="M40 8v16M40 56v16" stroke="#34d399" stroke-width="3"/><rect x="32" y="24" width="16" height="12" fill="#facc15"/>
        <rect x="32" y="44" width="16" height="12" fill="#f472b6"/><path d="M48 40h20" stroke="#34d399" stroke-width="3"/></svg></div>
      <div><div class="skillcard" style="margin:0">
        <div class="sk-name">ทักษะที่จะได้: AO/DO, วงจรแบ่งแรงดัน, โปรโตคอลของโมดูล และเอาต์พุต</div>
        <p class="muted" style="margin:6px 0 0">HX711, RC522, Fingerprint, TCS3200, IR, Buzzer, RGB LED, Relay พร้อมการคาลิเบรตและกรองสัญญาณ</p>
      </div></div>
    </div>
    <div class="btn-row"><button class="btn primary" data-goto="scr-lesson3">ออกล่า</button></div>
  </div>
</section>

<!-- ===== HUNT 3 ===== -->
<section id="scr-lesson3" class="screen">
  <div class="panel">
    <span class="tag">Hunt 03 · Signal Cave</span>
    <h2>ล่าที่ 3: ถอดรหัสสัญญาณและโมดูล</h2>
    <p>โมดูลราคาประหยัด (MQ-2, Flame, Sound, Soil, Rain) มีวงจรเปรียบเทียบ LM393 ให้ 2 ขา คือ <b>AO</b> (แรงดันต่อเนื่อง)
      และ <b>DO</b> (HIGH/LOW ตามเกณฑ์ที่หมุนตั้ง) ถ้าต้องการตัวเลขไปคำนวณหรือส่งขึ้นคลาวด์ ให้ใช้ <b>AO</b>
      ส่วนเซนเซอร์ 5 V ต้องลดแรงดันก่อนเข้า ESP32 ด้วยวงจรแบ่งแรงดัน</p>
    <div class="divfig">Vin (5 V) ──[ R1 ]──┬── Vout → ขา ESP32
                    │
                  [ R2 ]
                    │
                   GND        Vout = Vin × R2 / (R1 + R2)</div>
    <div class="tbl-wrap"><table>
      <tr><th>โมดูล</th><th>วิธีสื่อสาร / ขับ</th><th>จุดที่ต้องรู้</th></tr>
      <tr><td>Load Cell + HX711</td><td>DT และ SCK (โปรโตคอลเฉพาะ)</td><td>ADC 24 บิต ต้อง Tare และคาลิเบรตด้วยน้ำหนักที่รู้ค่า</td></tr>
      <tr><td>RFID RC522</td><td>SPI</td><td>ไฟเลี้ยง 3.3 V ต่อ ESP32 ได้ตรง แต่ละโมดูลต้องมีขา CS</td></tr>
      <tr><td>Fingerprint</td><td>UART</td><td>ประมวลผลลายนิ้วมือในโมดูลเอง ESP32 ได้รับเพียงผลเทียบ</td></tr>
      <tr><td>TCS3200</td><td>ความถี่ของคลื่นสี่เหลี่ยม</td><td>ความเข้มสีมากความถี่สูง อ่านด้วยการจับความกว้างพัลส์</td></tr>
      <tr><td>IR Receiver / Transmitter</td><td>พัลส์ดิจิทัล / PWM ความถี่พาห์</td><td>รีโมทส่วนใหญ่ใช้คลื่นพาห์ราว 38 kHz</td></tr>
      <tr><td>Active / Passive Buzzer</td><td>Digital / PWM</td><td>แอคทีฟดังทันทีเมื่อ HIGH พาสซีฟต้องป้อนความถี่</td></tr>
      <tr><td>RGB LED</td><td>PWM 3 ช่อง</td><td>ต้องมีตัวต้านทานทุกขาสี</td></tr>
      <tr><td>Relay Module</td><td>Digital</td><td>แยกวงจรควบคุมแรงดันต่ำจากโหลด 220 V งานไฟบ้านต้องปิดกล่องมิดชิดและมีผู้ควบคุม</td></tr>
    </table></div>

    <h3 style="margin-top:18px">ห้องทดลอง: สร้างวงจรแบ่งแรงดัน (Divider Builder)</h3>
    <p class="muted">สัญญาณ ECHO 5 V ต้องลดลงก่อนเข้า ESP32 เลือก R1 และ R2 ให้ Vout ไม่เกิน 3.3 V แต่ยังสูงกว่าเกณฑ์อ่าน HIGH (≈ 2.48 V) — ลอง 5 ชุดขึ้นไปรับเหรียญตรา</p>
    <div class="labrow"><b class="muted">R1:</b>
      <button class="btn sm" data-r1="1000">1 kΩ</button><button class="btn sm" data-r1="2000">2 kΩ</button>
      <button class="btn sm" data-r1="4700">4.7 kΩ</button><button class="btn sm" data-r1="10000">10 kΩ</button></div>
    <div class="labrow"><b class="muted">R2:</b>
      <button class="btn sm" data-r2="1000">1 kΩ</button><button class="btn sm" data-r2="2000">2 kΩ</button>
      <button class="btn sm" data-r2="3300">3.3 kΩ</button><button class="btn sm" data-r2="10000">10 kΩ</button></div>
    <div class="labrow"><span class="readout" id="dvR">R1 1 kΩ · R2 2 kΩ</span><span class="readout" id="dvV">3.33<small>V</small></span></div>
    <div class="meter"><i id="dvBar"></i></div>
    <div class="status-line" id="dvStatus">เลือกค่าตัวต้านทาน</div>
    <div class="btn-row"><button class="btn primary" data-quiz="check3">ไปทำแบบฝึกหัดด่านนี้</button></div>
  </div>
</section>
"""

LAB_JS = r"""
/* ---- LAB 1: Sensor Dex (38 การ์ดตามลำดับในคลิป) ---- */
const DEX=""" + SENSORS_JS + r""";
const DEXG={a:'Analog',d:'Digital',b:'โปรโตคอล',o:'เอาต์พุต'};
let dexF='all';
function renderDex(){
  const h=$('#dexGrid'); if(!h) return;
  h.innerHTML=DEX.map((s,i)=>{
    const got=state.labs.lab1.indexOf('s'+s.n)>=0;
    const hide=(dexF!=='all'&&s.g!==dexF);
    return '<button class="pick dex g-'+s.g+(got?' ok':'')+'" data-dex="'+i+'"'+(hide?' style="display:none"':'')+'><span class="no">#'+String(s.n).padStart(2,'0')+'</span>'+s.name+'<small>'+(got?s.th:'แตะเพื่อสแกน')+'</small></button>';
  }).join('');
  $('#dexCount').innerHTML=labCount('lab1')+'<small>/ 38 ใบ</small>';
}
function scanDex(i){
  const s=DEX[i];
  const isNew=markLab('lab1','s'+s.n,3);
  const st=$('#dexStatus'); st.className='status-line ok';
  st.innerHTML='<b>#'+s.n+' '+s.name+' · '+s.th+'</b> <span class="sigtag">'+s.sig+'</span><br>หลักการ: '+s.how+'<br>ประยุกต์ Smart: '+s.app;
  SFX.play(isNew?'ping':'select'); renderDex();
  const b=$('#dexGrid [data-dex="'+i+'"]'); if(b) b.classList.add('sel');
  if(isNew&&labCount('lab1')===38){toast('สะสมครบทั้ง 38 ใบแล้ว');SFX.play('fanfare');}
}

/* ---- LAB 2: Ultrasonic + PIR vs Radar ---- */
let usHot=false;
function usUpdate(user){
  const t=+$('#usT').value, T=usHot?35:20, v=331.3+0.606*T, d=t*1e-6*v/2*100;
  $('#usTime').innerHTML=t+'<small>µs</small>'; $('#usDist').innerHTML=d.toFixed(1)+'<small>cm</small>';
  $('#usBar').style.width=Math.min(100,d/400*100)+'%';
  const st=$('#usStatus'); let k;
  if(d<2){k='near';st.className='status-line';st.innerHTML='ใกล้เกินไป — HC-SR04 วัดได้ตั้งแต่ราว 2 cm คลื่นที่ส่งกับที่สะท้อนกลับซ้อนกันจนแยกไม่ออก';}
  else if(d>400){k='far';st.className='status-line';st.innerHTML='ไกลเกินช่วง — เกินราว 400 cm สัญญาณสะท้อนอ่อนเกินกว่าจะเชื่อถือได้ โปรแกรมควรกำหนด timeout ใน pulseIn()';}
  else {k='ok';st.className='status-line ok';st.innerHTML='ระยะ = '+t+' µs × '+v.toFixed(1)+' m/s ÷ 2 ≈ <b>'+d.toFixed(1)+' cm</b> (ที่ '+T+' °C) · อุณหภูมิสูงขึ้น เสียงเร็วขึ้น ระยะที่คำนวณได้จึงเปลี่ยนเล็กน้อย';}
  if(user) markLab('lab2','us_'+k+'_'+T,3);
}
const PIRCASE={
  walk:'<b>PIR: พบ</b> · <b>RCWL-0516: พบ</b> · <b>mmWave: พบ</b> — การเดินทำให้รังสีอินฟราเรดเปลี่ยนและเกิด Doppler ทุกเซนเซอร์จึงจับได้',
  still:'<b>PIR: ไม่พบ</b> · <b>RCWL-0516: มักไม่พบ</b> · <b>mmWave: ยังพบ</b> — คนนอนนิ่งแทบไม่ทำให้สัญญาณเปลี่ยน ระบบ Smart AC ที่ใช้ PIR อย่างเดียวจึงอาจปิดแอร์ใส่คนที่กำลังหลับ',
  wall:'<b>PIR: ไม่พบ</b> · <b>RCWL-0516: พบ</b> — PIR มองผ่านฝ้าหรือกระจกไม่ได้ แต่คลื่นไมโครเวฟทะลุวัสดุบางที่ไม่ใช่โลหะได้ จึงซ่อนอุปกรณ์ใต้ฝ้าได้ (และอาจจับคนห้องข้าง ๆ ได้ด้วย ต้องปรับตำแหน่ง)'
};
function runPir(k){ const st=$('#pirStatus'); st.className='status-line'+(k==='walk'?' ok':''); st.innerHTML=PIRCASE[k]; SFX.play(k==='walk'?'ping':'alarm'); markLab('lab2','pir_'+k,3); }

/* ---- LAB 3: Divider Builder ---- */
let r1=1000, r2=2000;
function fmtR(r){ return r>=1000?(r/1000)+' kΩ':r+' Ω'; }
function dvUpdate(user){
  const v=5*r2/(r1+r2);
  $('#dvR').textContent='R1 '+fmtR(r1)+' · R2 '+fmtR(r2); $('#dvV').innerHTML=v.toFixed(2)+'<small>V</small>';
  $('#dvBar').style.width=(v/5*100)+'%';
  const st=$('#dvStatus');
  if(v>3.3){st.className='status-line';st.innerHTML='<b>เกิน 3.3 V</b> — เสี่ยงทำให้ขา ESP32 เสียหาย เพิ่ม R1 หรือลด R2';if(user)SFX.play('alarm');}
  else if(v<2.48){st.className='status-line';st.innerHTML='<b>ต่ำเกินไป</b> — ปลอดภัยแต่ ESP32 อาจอ่านเป็น LOW หรือก้ำกึ่ง (เกณฑ์ HIGH ≈ 0.75 × 3.3 V = 2.48 V) ลด R1 หรือเพิ่ม R2';if(user)SFX.play('wrong');}
  else {st.className='status-line ok';st.innerHTML='<b>ผ่าน</b> — Vout = 5 × '+fmtR(r2)+' / ('+fmtR(r1)+' + '+fmtR(r2)+') ≈ '+v.toFixed(2)+' V ปลอดภัยและอ่านเป็น HIGH ได้แน่นอน';if(user)SFX.play('correct');}
  if(user) markLab('lab3',r1+'|'+r2,3);
}
"""

LAB_WIRING = r"""
  const dx=e.target.closest('[data-dex]'); if(dx){scanDex(+dx.dataset.dex);return;}
  const df=e.target.closest('[data-dexf]'); if(df){dexF=df.dataset.dexf;SFX.play('select');renderDex();return;}
  const pr=e.target.closest('[data-pir]'); if(pr){runPir(pr.dataset.pir);return;}
  const a1=e.target.closest('[data-r1]'); if(a1){r1=+a1.dataset.r1;dvUpdate(true);return;}
  const a2=e.target.closest('[data-r2]'); if(a2){r2=+a2.dataset.r2;dvUpdate(true);return;}
  if(e.target.closest('#usTemp')){usHot=!usHot;const b=$('#usTemp');b.textContent='อากาศ '+(usHot?35:20)+' °C';b.className='toggle '+(usHot?'off':'on');SFX.play('select');usUpdate(true);return;}
"""
INIT_EXTRA = " renderDex(); $('#usT').addEventListener('input',()=>usUpdate(true)); usUpdate(false); dvUpdate(false); const _g=goto_; goto_=function(id){_g(id); if(id==='scr-lesson1') renderDex();};"

B = {}
B['district1'] = [
 ('NTC Thermistor มีพฤติกรรมอย่างไรเมื่ออุณหภูมิสูงขึ้น และอ่านค่าอย่างไร',
  ['ความต้านทานลดลง จึงต่อเป็นวงจรแบ่งแรงดันแล้วอ่านแรงดันด้วย ADC', 'ความต้านทานเพิ่มขึ้นและส่งค่าผ่าน I2C', 'ส่งพัลส์ความถี่ตามอุณหภูมิ', 'ให้เอาต์พุตดิจิทัล HIGH เมื่อเกิน 30 °C เสมอ'],
  'NTC ย่อจาก Negative Temperature Coefficient ความต้านทานแปรผกผันกับอุณหภูมิ ต้องแปลงค่าด้วยสมการ (เช่น Beta equation) จึงได้องศาเซลเซียส'),
 ('LDR ต่อเป็นวงจรแบ่งแรงดันกับตัวต้านทานคงที่ เมื่อแสงมากขึ้น ความต้านทานของ LDR จะเป็นอย่างไร',
  ['ลดลง', 'เพิ่มขึ้น', 'คงที่', 'กลายเป็นอนันต์'],
  'LDR มีความต้านทานสูงในที่มืดและลดลงเมื่อสว่าง แรงดันที่จุดกึ่งกลางจึงเปลี่ยนตามแสง ใช้ทำไฟถนนอัตโนมัติ'),
 ('ระบบตู้เลี้ยงกุ้งต้องวัดอุณหภูมิน้ำ 3 จุดด้วยสายสัญญาณเส้นเดียว เซนเซอร์ใดเหมาะสมที่สุด',
  ['DS18B20 รุ่นกันน้ำ ต่อหลายตัวบน 1-Wire โดยแต่ละตัวมีแอดเดรสไม่ซ้ำกัน', 'DHT11 สามตัวต่อขาเดียวกัน', 'LDR สามตัว', 'NTC สามตัวต่อขนานเข้า ADC ขาเดียว'],
  'DS18B20 มีรหัส 64 บิตจากโรงงาน จึงแยกอ่านทีละตัวได้บนสายเส้นเดียว ต้องมีตัวต้านทาน pull-up (นิยม 4.7 kΩ)'),
 ('DHT11 ส่งข้อมูลอะไรออกมา และใช้สัญญาณแบบใด',
  ['อุณหภูมิและความชื้นสัมพัทธ์ ส่งเป็นข้อมูลดิจิทัลสายเดียว (Single-Bus)', 'เฉพาะความดันอากาศผ่าน SPI', 'ระดับแก๊สเป็นแรงดันแอนะล็อก', 'ระยะทางด้วยพัลส์ Echo'],
  'DHT11 ราคาถูก ความแม่นยำปานกลาง (ราว ±2 °C) ถ้าต้องการแม่นกว่าใช้ DHT22 หรือ SHT31'),
 ('โมดูล MQ-2 มีทั้งขา AO และ DO ถ้าต้องการ "ดูแนวโน้มความเข้มข้นของควัน" เพื่อส่งขึ้นกราฟบน Dashboard ควรใช้ขาใด',
  ['AO ผ่าน ADC เพราะให้ค่าต่อเนื่อง', 'DO เพราะให้ค่าละเอียดกว่า', 'ขา VCC', 'ไม่ต้องต่อขาสัญญาณ'],
  'DO ให้เพียงเกิน/ไม่เกินเกณฑ์จากวงจรเปรียบเทียบ ส่วน AO ให้ค่าต่อเนื่องที่นำไปพล็อตและคำนวณได้ และ MQ-2 ต้องคาลิเบรตก่อนใช้งานจริง'),
 ('Flame Sensor ตรวจจับเปลวไฟด้วยหลักการใด และมีข้อควรระวังอะไร',
  ['ตรวจรังสีอินฟราเรดจากเปลวไฟ แสงแดดหรือหลอดไส้ที่มีอินฟราเรดสูงอาจทำให้แจ้งเตือนผิด', 'วัดอุณหภูมิอากาศรอบตัว', 'วัดควันด้วยฟิล์มสารกึ่งตัวนำ', 'ใช้คลื่นอัลตราโซนิก'],
  'ระบบเฝ้าระวังอัคคีภัยจึงควรใช้หลายเซนเซอร์ร่วมกัน เช่น Flame + MQ-2 + อุณหภูมิ เพื่อลดการแจ้งเตือนเท็จ'),
 ('Sound Sensor ความไวสูงแบบโมดูลเหมาะกับงานใดมากที่สุด',
  ['ตรวจเสียงดังเกินเกณฑ์หรือเสียงตบมือเพื่อสั่งงาน (ค่าที่ได้เป็นระดับสัมพัทธ์ ไม่ใช่ dB ที่สอบเทียบแล้ว)', 'วัดระดับเสียงเป็น dB(A) ตามมาตรฐานกฎหมายได้ทันที', 'บันทึกเสียงพูดคุณภาพสูง', 'วัดความถี่ของคลื่นวิทยุ'],
  'การวัดเสียงดังในงานอาชีวอนามัยตามกฎหมายต้องใช้เครื่องวัดที่สอบเทียบ โมดูลนี้ใช้เป็นระบบเฝ้าระวังเบื้องต้นได้'),
 ('Soil Moisture Sensor แบบสองขาอิเล็กโทรดวัดความชื้นในดินด้วยหลักการใด',
  ['วัดการนำไฟฟ้าของดินระหว่างอิเล็กโทรด ดินชื้นนำไฟฟ้าได้ดีกว่า', 'วัดน้ำหนักของดิน', 'ส่งคลื่นอัลตราโซนิกลงดิน', 'วัดสีของดินด้วยแสง'],
  'หัววัดแบบนี้ผุกร่อนเร็วเมื่อจ่ายไฟค้างไว้ วิธีลดคือจ่ายไฟเฉพาะตอนอ่าน หรือเลือกรุ่น capacitive'),
 ('Rain Sensor ให้เอาต์พุตแบบใด และนำไปใช้อย่างไรในอาคารอัจฉริยะ',
  ['AO และ DO จากการนำไฟฟ้าของหยดน้ำบนลายทองแดง ใช้สั่งปิดหน้าต่างเมื่อฝนตก', 'ส่งข้อมูลปริมาณน้ำฝนเป็นมิลลิเมตรผ่าน UART', 'ให้ค่าอุณหภูมิของน้ำฝน', 'ตรวจความเร็วลม'],
  'แผ่นตรวจฝนบอกได้ว่ามีน้ำหรือไม่และมากน้อยเชิงสัมพัทธ์ ถ้าต้องการปริมาณฝนเป็นมิลลิเมตรต้องใช้เครื่องวัดฝนแบบกระเปาะกระดก (tipping bucket)'),
 ('Pulse Sensor วัดอัตราการเต้นของหัวใจด้วยหลักการใด',
  ['Photoplethysmography (PPG) วัดการเปลี่ยนปริมาตรเลือดใต้ผิวด้วยแสง ให้เอาต์พุตแอนะล็อก', 'วัดสัญญาณไฟฟ้าหัวใจด้วยอิเล็กโทรด 12 ลีด', 'วัดแรงกดของนิ้ว', 'วัดอุณหภูมิผิว'],
  'นำมาประยุกต์มอนิเตอร์ความเหนื่อยล้าของคนงานได้ แต่ไม่ใช่เครื่องมือแพทย์ ต้องสื่อสารข้อจำกัดให้ผู้ใช้ทราบ'),
 ('Joystick Module หนึ่งตัวต้องใช้ขาของ ESP32 อย่างไร',
  ['ขาแอนะล็อก 2 ขา (แกน X และ Y) และขาดิจิทัล 1 ขา (ปุ่มกด)', 'ขาดิจิทัลเพียงขาเดียว', 'บัส I2C เท่านั้น', 'ขา UART TX และ RX'],
  'แกนทั้งสองเป็น Potentiometer ตำแหน่งกลางจะอ่านได้ราวครึ่งสเกล (ประมาณ 2048 บน ESP32) ควรจ่ายไฟ 3.3 V ให้โมดูลเพื่อไม่ให้แรงดันเกินขา ADC'),
 ('Flex Sensor เปลี่ยนแปลงอย่างไรเมื่อถูกงอ',
  ['ความต้านทานเปลี่ยนตามองศาการงอ อ่านผ่านวงจรแบ่งแรงดันเข้า ADC', 'ส่งข้อมูลมุมเป็นองศาผ่าน SPI', 'ให้พัลส์ทุกครั้งที่งอครบ 10 องศา', 'ไม่เปลี่ยนแปลง ใช้วัดน้ำหนัก'],
  'ใช้ทำถุงมืออัจฉริยะสั่งงานแขนกล หรือตรวจการงอข้อต่อในงานกายภาพ'),
 ('Linear Hall Sensor ต่างจาก Digital Hall Sensor อย่างไร',
  ['Linear ให้แรงดันแอนะล็อกแปรตามความเข้มสนามแม่เหล็ก ส่วน Digital ให้เพียงมี/ไม่มีสนามแม่เหล็ก', 'Linear ใช้วัดอุณหภูมิ', 'Digital ให้ค่าละเอียดกว่าเสมอ', 'ทั้งสองแบบเหมือนกันทุกประการ'],
  'Linear Hall เหมาะวัดตำแหน่งละเอียด ส่วน Digital Hall เหมาะนับรอบหรือตรวจตำแหน่งเปิด/ปิด'),
 ('ตามกรอบ System Design Framework ในคลิป ขั้นแรกของการเลือกเซนเซอร์คืออะไร',
  ['วิเคราะห์ข้อกำหนด: ช่วงการวัด ความแม่นยำ ความละเอียด และอินเทอร์เฟซสัญญาณ', 'ซื้อเซนเซอร์ที่ถูกที่สุดก่อน', 'เขียนโค้ดแจ้งเตือนผ่านมือถือก่อน', 'ออกแบบกล่องใส่วงจรก่อน'],
  'ถ้าข้อกำหนดไม่ชัด เช่น ต้องวัดถึงกี่องศา แม่นแค่ไหน จะเลือกเซนเซอร์ผิดและต้องรื้อระบบภายหลัง'),
]
B['district2'] = [
 ('ปุ่มกดเชิงกลมักให้สัญญาณกระเด้งหลายครั้งในเสี้ยววินาที วิธีแก้ที่ถูกต้องคือข้อใด',
  ['ทำ Debounce ด้วยซอฟต์แวร์ (รอให้สถานะนิ่งราว 20–50 ms) หรือวงจร RC', 'เพิ่มแรงดันเป็น 5 V', 'ใช้ analogRead() แทน', 'กดปุ่มให้แรงขึ้น'],
  'ถ้าไม่ทำ Debounce ปุ่มหยุดฉุกเฉินหรือปุ่มเลือกโหมดอาจถูกนับหลายครั้งต่อการกดหนึ่งครั้ง'),
 ('HC-SR04 วัดเวลาเสียงสะท้อนได้ 1160 µs ที่ 20 °C ระยะถึงวัตถุประมาณเท่าใด',
  ['ประมาณ 20 cm', 'ประมาณ 40 cm', 'ประมาณ 10 cm', 'ประมาณ 2 m'],
  'ระยะ = 1160 × 0.0343 / 2 ≈ 19.9 cm ต้องหารสองเพราะเสียงเดินทางไปและกลับ'),
 ('ถังขยะอัจฉริยะติด HC-SR04 ไว้ที่ฝาด้านบน ความลึกถัง 60 cm วัดระยะถึงผิวขยะได้ 12 cm ขยะเต็มประมาณกี่เปอร์เซ็นต์',
  ['80%', '20%', '12%', '72%'],
  'ความสูงขยะ = 60 − 12 = 48 cm คิดเป็น 48/60 = 80% ใช้เป็นเกณฑ์แจ้งให้เก็บขยะได้'),
 ('PIR Motion Sensor ตรวจจับสิ่งใด',
  ['การเปลี่ยนแปลงของรังสีอินฟราเรดจากวัตถุที่มีความร้อนซึ่งเคลื่อนที่', 'ระยะทางด้วยคลื่นเสียง', 'สนามแม่เหล็ก', 'ความเข้มข้นของแก๊ส'],
  'PIR เป็นเซนเซอร์แบบ Passive ไม่ได้ปล่อยคลื่นเอง เมื่อคนนั่งหรือนอนนิ่ง รูปแบบรังสีไม่เปลี่ยน PIR จึงอาจรายงานว่าไม่มีคน'),
 ('RCWL-0516 ต่างจาก PIR อย่างไร',
  ['ใช้คลื่นไมโครเวฟแบบ Doppler ตรวจการเคลื่อนไหวผ่านวัสดุบางที่ไม่ใช่โลหะได้ จึงซ่อนใต้ฝ้าได้', 'ใช้แสงเลเซอร์วัดระยะ', 'ตรวจได้เฉพาะวัตถุที่เป็นโลหะ', 'ต้องสัมผัสผู้ใช้โดยตรง'],
  'ข้อดีคือซ่อนอุปกรณ์ได้ ข้อควรระวังคืออาจตรวจเจอการเคลื่อนไหวหลังผนังหรือห้องข้างเคียง'),
 ('ระบบ Smart AC ใช้ PIR ตัดสินว่า "ไม่มีคน" แล้วปิดแอร์ ปัญหาใดน่าจะเกิดตอนกลางดึก',
  ['ผู้ใช้นอนหลับนิ่ง PIR ไม่เห็นการเคลื่อนไหว แอร์จึงถูกปิดทั้งที่มีคนนอนอยู่', 'PIR จะเปิดแอร์ค้างไว้ตลอดคืน', 'PIR วัดอุณหภูมิผิด', 'ไม่มีปัญหาใด ๆ'],
  'ทางแก้คือใช้เรดาร์ mmWave ที่จับการหายใจได้ หรือใช้ตรรกะเวลาร่วม เช่น ไม่ปิดแอร์ในช่วงเวลานอน'),
 ('Line Tracking Sensor แยกพื้นสีขาวกับเส้นสีดำได้เพราะเหตุใด',
  ['พื้นสว่างสะท้อนแสงอินฟราเรดกลับมามากกว่าพื้นสีเข้มที่ดูดกลืนแสง', 'พื้นสีดำมีอุณหภูมิสูงกว่า', 'เส้นสีดำมีสนามแม่เหล็ก', 'เซนเซอร์อ่านสีจากกล้อง'],
  'หลักการเดียวกันใช้กับ AGV ในโรงงาน ระยะติดตั้งจากพื้นต้องคงที่ ไม่อย่างนั้นค่าสะท้อนจะเปลี่ยน'),
 ('ระบบนับชิ้นงานบนสายพานใช้ Optical Light Barrier สถานะสัญญาณเปลี่ยนเมื่อใด',
  ['เมื่อชิ้นงานผ่านตัดลำแสงระหว่างตัวส่งกับตัวรับ', 'เมื่ออุณหภูมิเพิ่มขึ้น', 'เมื่อสายพานหยุด', 'เมื่อมีเสียงดัง'],
  'นับครั้งละขอบสัญญาณ (edge) ด้วย interrupt จะแม่นกว่าการวนอ่านช้า ๆ โดยเฉพาะสายพานความเร็วสูง'),
 ('Reed Switch นิยมใช้ในบ้านและอาคารอัจฉริยะเพื่อทำอะไร',
  ['ตรวจจับประตูหรือหน้าต่างเปิด-ปิดเมื่อแม่เหล็กเข้าใกล้หรือออกห่าง', 'วัดความชื้นในอากาศ', 'วัดอัตราการเต้นหัวใจ', 'วัดค่า pH'],
  'Reed switch เป็นหน้าสัมผัสในหลอดแก้ว ราคาถูก ใช้งานง่าย ใช้ร่วมกับ INPUT_PULLUP ได้โดยตรง'),
 ('Digital Hall Sensor ติดคู่กับแม่เหล็กบนแกนหมุน 1 ลูก นับพัลส์ได้ 50 ครั้งใน 1 วินาที ความเร็วรอบคือเท่าใด',
  ['3000 RPM', '50 RPM', '500 RPM', '300 RPM'],
  'แม่เหล็ก 1 ลูกให้ 1 พัลส์ต่อรอบ 50 รอบ/วินาที × 60 = 3000 รอบต่อนาที'),
 ('Rotary Encoder บอก "ทิศทางการหมุน" ได้อย่างไร',
  ['ดูว่าสัญญาณเฟส A หรือเฟส B เปลี่ยนก่อน เพราะพัลส์ 2 เฟสเหลื่อมกัน', 'ดูจากความยาวของสายไฟ', 'อ่านจากแรงดันแอนะล็อก', 'Encoder บอกทิศทางไม่ได้'],
  'Encoder แบบ Quadrature ให้พัลส์ 2 เฟสที่เหลื่อมกันราวหนึ่งในสี่คาบ ลำดับการเปลี่ยนบอกทิศ จำนวนพัลส์บอกระยะ'),
 ('Tilt Switch เหมาะกับงานใดในงานวิศวกรรมโยธาและความปลอดภัย',
  ['แจ้งเตือนเมื่อเสาไฟ ป้าย หรือโครงสร้างชั่วคราวเอียงหรือล้มเกินตำแหน่งปกติ', 'วัดมุมเอียงละเอียดระดับ 0.01 องศา', 'วัดน้ำหนักบรรทุกของสะพาน', 'วัดระดับน้ำในเขื่อน'],
  'Tilt switch ให้เพียงเอียง/ไม่เอียง ถ้าต้องการวัดมุมละเอียดควรใช้ IMU อย่าง MPU6050'),
 ('Touch Sensor แบบ capacitive มีข้อดีอย่างไรเมื่อเทียบกับปุ่มกดเชิงกล',
  ['ไม่มีหน้าสัมผัสเชิงกลที่สึกหรอ ทำแผงควบคุมกันน้ำได้ และ ESP32 มี Touch Pin ในตัว', 'ราคาแพงกว่าและใช้ไฟ 12 V', 'ต้องกดแรงกว่าปุ่มทั่วไป', 'ทำงานได้เฉพาะในที่มืด'],
  'เหมาะกับแผงควบคุมที่ต้องทำความสะอาดบ่อยหรือโดนน้ำ'),
 ('Vibration Sensor, Tilt Switch และ Knock Sensor มีลักษณะร่วมกันอย่างไร',
  ['ตอบสนองต่อเหตุการณ์ทางกลอย่างการสั่น การเอียง หรือการเคาะ และส่วนใหญ่ให้เอาต์พุตดิจิทัล', 'ทั้งหมดใช้วัดอุณหภูมิ', 'ทั้งหมดสื่อสารผ่าน SPI', 'ทั้งหมดต้องใช้ไฟ 220 V'],
  'เหตุการณ์เหล่านี้สั้นมาก ควรอ่านด้วย interrupt หรือวนอ่านถี่ และอาจต้องกรองไม่ให้แจ้งเตือนซ้ำ'),
]
B['district3'] = [
 ('โมดูลที่มีทั้ง AO และ DO (เช่น MQ-2, Rain, Sound) ขา DO ทำงานอย่างไร',
  ['ให้ HIGH/LOW เมื่อค่าข้ามเกณฑ์ที่ตั้งด้วยโพเทนชิโอมิเตอร์บนโมดูล ผ่านวงจรเปรียบเทียบ', 'ให้ค่าความเข้มข้นเป็น ppm โดยตรง', 'เป็นขาจ่ายไฟ', 'ใช้สื่อสาร I2C'],
  'DO เหมาะกับการเตือนแบบเปิด/ปิด ส่วน AO เหมาะกับการแสดงผลและส่งข้อมูลขึ้นคลาวด์'),
 ('วงจรแบ่งแรงดัน Vin = 5 V, R1 = 1 kΩ (ด้านบน), R2 = 2 kΩ (ต่อลง GND) แรงดัน Vout คือเท่าใด',
  ['ประมาณ 3.33 V', '1.67 V', '2.5 V', '5 V'],
  'Vout = 5 × 2/(1+2) ≈ 3.33 V ปลอดภัยต่อขา ESP32 และยังสูงพอให้อ่านเป็น HIGH'),
 ('ถ้าใช้ R1 = 10 kΩ และ R2 = 3.3 kΩ ลดสัญญาณดิจิทัล 5 V เข้า ESP32 จะเกิดปัญหาใด',
  ['Vout ≈ 1.24 V ต่ำกว่าเกณฑ์ HIGH (ราว 2.48 V) จึงอาจอ่านเป็น LOW', 'Vout สูงเกิน 3.3 V จนขาเสีย', 'ไม่มีปัญหา', 'ESP32 รีเซ็ตทันที'],
  'การลดแรงดันต้องทั้งปลอดภัยและยังตีความเป็น HIGH ได้แน่นอน (ESP32: VIH ≈ 0.75 × VDD)'),
 ('Load Cell ต้องใช้ร่วมกับ HX711 เพราะเหตุใด',
  ['Strain gauge ใน Wheatstone bridge ให้สัญญาณระดับมิลลิโวลต์ HX711 ขยายและแปลงเป็นดิจิทัล 24 บิต ส่งผ่านขา DT และ SCK', 'HX711 เป็นแหล่งจ่ายไฟ 220 V', 'HX711 แปลงน้ำหนักเป็นแสง', 'Load Cell ส่งค่าเป็นกิโลกรัมผ่าน Wi-Fi อยู่แล้ว'],
  'ก่อนใช้งานต้อง Tare (ตั้งศูนย์) และคาลิเบรตด้วยน้ำหนักที่รู้ค่าเพื่อหาค่า calibration factor'),
 ('RFID Reader RC522 สื่อสารกับ ESP32 ผ่านบัสใด',
  ['SPI', 'Analog', '1-Wire', 'ADC2'],
  'RC522 ใช้ SPI และใช้ไฟเลี้ยง 3.3 V จึงต่อ ESP32 ได้โดยตรง ใช้ทำระบบควบคุมการเข้าออกหรือลงเวลา'),
 ('Fingerprint Sensor ในคลิปสื่อสารด้วยโปรโตคอลใด และงานหนักทำที่ใด',
  ['UART (TX/RX) โดยโมดูลประมวลผลและเทียบลายนิ้วมือกับ Template ภายในตัวเอง', 'I2C โดย ESP32 ประมวลผลภาพลายนิ้วมือเอง', 'แอนะล็อกเข้า ADC', 'PWM'],
  'การที่โมดูลประมวลผลเองทำให้ MCU ขนาดเล็กใช้งานได้ ESP32 รับเพียงผลว่าตรงกับ ID ใด'),
 ('TCS3200 Color Sensor ให้เอาต์พุตแบบใด',
  ['คลื่นสี่เหลี่ยมที่ความถี่แปรตามความเข้มของสีที่เลือกด้วยฟิลเตอร์ RGB', 'แรงดันแอนะล็อก 0–3.3 V ตามสี', 'ข้อความชื่อสีผ่าน UART', 'ค่า HIGH/LOW เท่านั้น'],
  'อ่านด้วยการวัดความกว้างพัลส์หรือความถี่ (เช่น pulseIn) แล้วเทียบสัดส่วน R:G:B เพื่อคัดแยกสีชิ้นงาน'),
 ('IR Receiver ทั่วไป (เช่น VS1838B) ออกแบบให้รับสัญญาณรีโมทที่มีคลื่นพาห์ความถี่เท่าใด',
  ['ราว 38 kHz', 'ราว 50 Hz', 'ราว 2.4 GHz', 'ราว 13.56 MHz'],
  'รีโมทส่งแสงอินฟราเรดที่มอดูเลตด้วยคลื่นพาห์ 38 kHz ตัวรับถอดคลื่นพาห์ออกแล้วให้พัลส์ดิจิทัลแก่ MCU'),
 ('ระบบ ESP32 Universal Remote สั่งแอร์ ต้องใช้อุปกรณ์ใดในการส่งคำสั่ง',
  ['IR Transmitter (LED อินฟราเรด) ส่งรหัสที่มอดูเลตตามโปรโตคอลของแอร์', 'IR Receiver เพียงอย่างเดียว', 'Flame Sensor', 'Reed Switch'],
  'ขั้นตอนจริงคือใช้ IR Receiver อ่านรหัสจากรีโมทเดิมก่อน แล้วใช้ IR Transmitter ส่งรหัสนั้นซ้ำ แนะนำขับ LED ผ่านทรานซิสเตอร์เพื่อเพิ่มระยะ'),
 ('Active Buzzer กับ Passive Buzzer ต่างกันอย่างไร',
  ['Active มีวงจรกำเนิดความถี่ในตัว จ่าย HIGH ก็ดัง ส่วน Passive ต้องป้อนความถี่ด้วย PWM จึงเปลี่ยนโทนเสียงได้', 'Passive ดังกว่าเสมอ', 'Active ต้องใช้ไฟ 220 V', 'ทั้งสองแบบใช้งานเหมือนกันทุกประการ'],
  'ถ้าต้องการเสียงเตือนไล่ระดับตามความรุนแรง ให้ใช้ Passive Buzzer กับฟังก์ชัน tone() หรือ LEDC'),
 ('RGB LED แสดงสีเหลืองได้อย่างไร',
  ['ผสมแสงแดงกับเขียวด้วย PWM ส่วนน้ำเงินปิด', 'จ่ายไฟเฉพาะขาน้ำเงิน', 'ใช้ analogRead()', 'RGB LED แสดงสีเหลืองไม่ได้'],
  'ใช้ PWM 3 ช่องปรับสัดส่วนสีได้ เหมาะทำไฟสถานะ เช่น เขียว=ปกติ เหลือง=เฝ้าระวัง แดง=ผิดปกติ น้ำเงิน=เชื่อมต่อ Wi-Fi'),
 ('Relay Module มีบทบาทสำคัญที่สุดในเชิงความปลอดภัยอย่างไร',
  ['แยกวงจรควบคุมแรงดันต่ำของ MCU ออกจากวงจรโหลดแรงดันสูง เช่น ไฟบ้าน 220 V', 'เพิ่มความละเอียด ADC', 'ลดแรงดันจาก 5 V เป็น 3.3 V สำหรับสัญญาณข้อมูล', 'ใช้วัดกระแสไฟฟ้า'],
  'งานที่แตะไฟ 220 V ต้องอยู่ในกล่องปิดมิดชิด มีฟิวส์ และอยู่ภายใต้การควบคุมของผู้มีความรู้ ในห้องเรียนควรทดลองกับโหลดแรงดันต่ำก่อน'),
 ('ข้อใดอธิบายความต่างระหว่าง "ความละเอียด (resolution)" และ "ความแม่นยำ (accuracy)" ได้ถูกต้อง',
  ['ความละเอียดคือค่าที่เปลี่ยนได้เล็กที่สุดที่อ่านได้ ส่วนความแม่นยำคือค่าที่อ่านใกล้ค่าจริงแค่ไหน', 'ทั้งสองคำมีความหมายเหมือนกัน', 'ความละเอียดสูงหมายถึงแม่นยำเสมอ', 'ความแม่นยำคือจำนวนบิตของ ADC'],
  'เซนเซอร์อาจแสดงทศนิยมสองตำแหน่ง (ละเอียด) แต่คลาดจากค่าจริง ±2 °C (ไม่แม่น) รายงานโปรเจกต์ควรระบุทั้งสองค่า'),
 ('ค่าจาก MQ-2 ที่อ่านทุก 1 วินาทีกระตุกขึ้นลงมาก ทำให้แจ้งเตือนผิดพลาด วิธีปรับปรุงที่เหมาะสมที่สุดคือข้อใด',
  ['ใช้ค่าเฉลี่ยเคลื่อนที่หลายค่า และกำหนดว่าต้องเกินเกณฑ์ต่อเนื่องระยะหนึ่งก่อนแจ้งเตือน', 'ลดเกณฑ์แจ้งเตือนให้ต่ำลงมาก', 'ถอดฮีตเตอร์ออก', 'อ่านค่าครั้งเดียวตอนเปิดเครื่อง'],
  'การกรองสัญญาณและเงื่อนไขเวลาลดการแจ้งเตือนเท็จ ซึ่งทำให้ผู้ใช้เลิกเชื่อถือระบบ'),
]
STAR = star_table([
 ('APEX HUNTER', 'อ่านเซนเซอร์ได้ครบทุกมิติ พร้อมออกแบบระบบตรวจวัดของโปรเจกต์ได้ทันที'),
 ('SIGNAL TRACKER', 'แม่นยำสูง เหลืออีกจุดเดียว ทบทวนข้อที่พลาดแล้วล่าใหม่'),
 ('FIELD SCOUT', 'ผ่านเกณฑ์พื้นฐาน ลองเล่นห้องทดลองวงจรแบ่งแรงดันอีกรอบ'),
 ('TRAIL FINDER', 'เริ่มจับหลักได้ ทบทวนตารางเซนเซอร์และหลักการ PIR กับ mmWave'),
 ('BASE CAMP', 'พอมีพื้นฐาน แนะนำให้ทำภารกิจล่าเซนเซอร์ให้ครบก่อนสอบใหม่'),
 ('NEW RECRUIT', 'ยังไม่คุ้นเนื้อหา ไม่เป็นไร เริ่มจากภารกิจล่าเซนเซอร์ทีละข้อ'),
])

BADGES = r"""[
  {id:'perfect',  name:'APEX PREDATOR',   desc:'Posttest ถูกครบ 6 ข้อ',                  test:s => s.post === 6},
  {id:'zero2hero',name:'SHARP EYES',      desc:'คะแนนเพิ่มขึ้น 3 ข้อขึ้นไปจาก Pretest',     test:s => (s.post - s.pre) >= 3},
  {id:'fast',     name:'QUICK SCAN',      desc:'ตอบถูกภายใน 8 วินาที',                   test:s => s.fastCorrect},
  {id:'labrat',   name:'FIELD RESEARCHER',desc:'เล่นห้องทดลองครบทั้งสามด่าน',             test:s => s.labs.lab1.length >= 30 && s.labs.lab2.length >= 4 && s.labs.lab3.length >= 5},
  {id:'combo',    name:'LOCKED ON',       desc:'ตอบถูกติดกัน 5 ข้อขึ้นไป',               test:s => s.maxCombo >= 5},
  {id:'sweep',    name:'TRIPLE TROPHY',   desc:'ได้ 2/2 ครบทั้งสามด่าน',                 test:s => s.postByD.district1 === 2 && s.postByD.district2 === 2 && s.postByD.district3 === 2}
]"""

ADVICE = r"""
  const tips=[];
  if(labCount('lab1')<30) tips.push('สะสมการ์ดใน Sensor Dex ให้ได้อย่างน้อย 30 ใบ แล้วเลือกเซนเซอร์ที่ตรงกับโปรเจกต์กลุ่มลงในรายการวัสดุ (BOM)');
  if(labCount('lab2')<4) tips.push('ลองให้เครื่องวัดอัลตราโซนิกแสดงทั้งระยะใกล้เกินและไกลเกิน และเทียบ PIR กับ mmWave ในสถานการณ์คนนอนนิ่ง');
  if(labCount('lab3')<5) tips.push('ลองหลายชุดค่าตัวต้านทานในวงจรแบ่งแรงดัน จนหาชุดที่ทั้งปลอดภัยและยังอ่านเป็น HIGH ได้');
  if(postInfo.stars===6) tips.push('ได้ครบ 6 ดาวแล้ว ขั้นต่อไปคือเขียนแผนคาลิเบรตเซนเซอร์หลักของโปรเจกต์กลุ่ม พร้อมวิธีพิสูจน์ความแม่นยำ');
  return tips;
"""

CFG = {
    'filename': 'game3_sensor_hunter.html',
    'title': 'SENSOR HUNTER : ล่าเซนเซอร์ทั่วสนาม',
    'brand': 'SENSOR HUNTER',
    'edition': 'RADAR EDITION',
    'desc': 'เกมทบทวนเซนเซอร์ 38 ชนิดจากคลิป: NTC, LDR, DS18B20, DHT11, MQ-2, HC-SR04, PIR, RCWL-0516, HX711, RC522, Relay, AO/DO และวงจรแบ่งแรงดัน — CPE2422/2428 · ผศ.ดร.กุลวลัญช์ วรุณสิน มหาวิทยาลัยรามคำแหง',
    'ogdesc': 'ล่าเซนเซอร์ 3 ด่าน เลือก ต่อ และคาลิเบรตให้ถูก วัดผลก่อน-หลังเรียนด้วยระบบดาว 6 ดวง',
    'favicon': "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%2303120d'/><circle cx='50' cy='50' r='32' fill='none' stroke='%2334d399' stroke-width='6'/><path d='M50 50 L76 32 A32 32 0 0 1 82 50 Z' fill='%2334d399'/><circle cx='64' cy='40' r='5' fill='%23facc15'/></svg>",
    'theme': THEME,
    'extra_css': EXTRA_CSS,
    'arcade_label': 'ด่านไต่หอเรดาร์',
    'hero_svg': HERO,
    'subtitle': 'สวมบทบาท <b>นักล่าเซนเซอร์</b> ออกสำรวจ 3 ดินแดน สมุดสะสมเซนเซอร์ 38 ใบตามคลิป ทุ่งเคลื่อนไหวของ HC-SR04, PIR และเรดาร์ไมโครเวฟ ไปจนถึงถ้ำถอดรหัสสัญญาณ AO/DO วงจรแบ่งแรงดัน และโมดูล HX711, RC522, Relay สะสม XP และดาว วัดพัฒนาการก่อน–หลังเรียน',
    'login_tag': 'Hunter Registration',
    'features': '<span>CPE2422 · คลิปทบทวนที่ 3</span><span>38 SENSORS · AO/DO · DIVIDER</span><span>PRETEST / POSTTEST</span><span>ระบบดาว 6 ดวง</span><span>XP &amp; COMBO</span><span>ส่งออกคะแนน CSV</span>',
    'climb_text': 'ตัวละครไต่หอเรดาร์ขึ้น 1 ชั้น ทันที',
    'zones_html': ZONES,
    'checks': [('Hunt 01', 'สมุดสะสมเซนเซอร์'), ('Hunt 02', 'ทุ่งเคลื่อนไหว'), ('Hunt 03', 'ถ้ำถอดรหัสสัญญาณ')],
    'post_desc': '6 ข้อใหม่ (ด่านละ 2 ข้อ) เพื่อวัดความเข้าใจหลังล่าครบทั้ง 3 ดินแดน',
    'report_tag': 'Hunting Report',
    'course': COURSE.split(' · ')[0],
    'footer_line': 'เกมทบทวนคลิปที่ 3: 38 Arduino Sensors You Should Know — ภาคเรียนที่ 1/2569',
    'bank': bank_js(B),
    'skill_labels': "{district1:'Sensor Dex & แอนะล็อก', district2:'การเคลื่อนไหว & ตำแหน่ง', district3:'ถอดรหัสสัญญาณ & โมดูล'}",
    'skey': 'cpe_sensorhunter_v1_state',
    'star_table': STAR,
    'navstops': navstops('H1 DEX', 'H2 MOTION', 'H3 SIGNAL'),
    'lock_msg': 'ดินแดนนี้ยังไม่ปลดล็อก ล่าตามลำดับก่อนนะครับ',
    'act': {'floor': 'ชั้น', 'top': 'ยอดหอเรดาร์', 'ground': 'ฐานค่าย', 'theme': 'radar'},
    'pre_sub': 'นี่คือเส้นฐานของคุณ — เดี๋ยวเรามาวัดกันใหม่หลังล่าครบทั้ง 3 ดินแดน',
    'go_first': 'ออกล่าด่านแรก',
    'lab_js': LAB_JS,
    'lab_wiring': LAB_WIRING,
    'init_extra': INIT_EXTRA,
    'badges': BADGES,
    'advice_js': ADVICE,
    'role': 'นักล่าเซนเซอร์',
    'filekey': 'CPE2422_G3_sensorhunter',
    'avatars': avatars('#072519', ['#34d399', '#f472b6', '#facc15', '#f87171', '#6ee7b7', '#f9a8d4']),
}
