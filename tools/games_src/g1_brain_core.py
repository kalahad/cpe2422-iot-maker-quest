# -*- coding: utf-8 -*-
"""GAME 1 — BRAIN CORE : ถอดรหัสสมองกลฝังตัว
อ้างอิงคลิปทบทวนที่ 1: The Brain Behind Everything — Why Microcontrollers Rule the Modern World"""
from cpe_common import *

THEME = {
    "PRIMARY_RGB": "34,211,238",  "PRIMARY_HEX": "#22d3ee",
    "SECOND_RGB":  "163,230,53",  "SECOND_HEX":  "#a3e635",
    "GOLD_RGB":    "250,204,21",  "GOLD_HEX":    "#facc15",
    "GOLD2_RGB":   "254,240,138", "GOLD2_HEX":   "#fef08a",
    "RED_RGB":     "244,63,94",   "RED_HEX":     "#f43f5e",
    "BG_RGB":      "3,14,22",     "BG_HEX":      "#030e16",
    "PANEL_RGB":   "10,34,48",
    "PANEL2_RGB":  "14,46,64",
    "BG2_HEX":     "#06202e",
    "INK_HEX":     "#082230",
    "TEXT_HEX":    "#e6f7fb",
    "MUTED_HEX":   "#93b8c4",
    "MUTED2_HEX":  "#5f8796",
    "MUTED3_HEX":  "#4d7380",
    "SECOND2_HEX": "#d9f99d",
    "PRIM2_HEX":   "#67e8f9",
    "LIGHT_EMBER": "#0e7490", "LIGHT_CORNER": "#4d7c0f", "LIGHT_GOLD": "#a16207",
    "LIGHT_GOLD2": "#854d0e", "LIGHT_RED": "#be123c",
}

EXTRA_CSS = LAB_CSS + """
.chipmap{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0;padding:14px;border-radius:16px;
  border:2px solid var(--ember);background:rgba(var(--ink-panel-rgb),.55);position:relative}
.chipmap .pick{text-align:center;font-family:var(--mono);font-size:.78rem;padding:12px 6px}
.chipmap .pick.core{grid-column:span 2;grid-row:span 2;display:flex;flex-direction:column;justify-content:center;font-size:.95rem}
@media(max-width:560px){.chipmap{grid-template-columns:repeat(2,1fr)}}
"""

HERO = """<svg class="cityart" viewBox="0 0 480 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ภาพชิปไมโครคอนโทรลเลอร์เรืองแสง">
  <defs>
    <radialGradient id="gCore" cx="50%" cy="48%" r="60%"><stop offset="0%" stop-color="rgba(34,211,238,.45)"/><stop offset="100%" stop-color="rgba(34,211,238,0)"/></radialGradient>
    <filter id="fGlow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x="0" y="0" width="480" height="300" rx="18" fill="#030e16"/>
  <circle cx="240" cy="140" r="150" fill="url(#gCore)"/>
  <g stroke="#22d3ee" stroke-width="2" fill="none" opacity=".55">
    <path d="M30 60 H150 L170 80 H180"/><path d="M30 120 H170"/><path d="M30 200 H150 L170 180 H180"/>
    <path d="M450 60 H330 L310 80 H300"/><path d="M450 120 H310"/><path d="M450 200 H330 L310 180 H300"/>
    <path d="M200 20 V70"/><path d="M240 20 V70"/><path d="M280 20 V70"/><path d="M200 210 V262"/><path d="M240 210 V262"/><path d="M280 210 V262"/>
  </g>
  <rect x="170" y="70" width="140" height="140" rx="14" fill="#082230" stroke="#22d3ee" stroke-width="3" filter="url(#fGlow)"/>
  <rect x="195" y="95" width="90" height="90" rx="8" fill="none" stroke="#a3e635" stroke-width="2"/>
  <text x="240" y="135" text-anchor="middle" font-size="20" font-weight="700" fill="#22d3ee" font-family="monospace">MCU</text>
  <text x="240" y="156" text-anchor="middle" font-size="8.5" fill="#a3e635" font-family="monospace">CPU·FLASH·SRAM</text><text x="240" y="170" text-anchor="middle" font-size="8.5" fill="#a3e635" font-family="monospace">GPIO·ADC·TIMER</text>
  <circle cx="150" cy="80" r="5" fill="#facc15" filter="url(#fGlow)"/><circle cx="330" cy="180" r="5" fill="#facc15" filter="url(#fGlow)"/>
  <circle cx="240" cy="262" r="5" fill="#a3e635" filter="url(#fGlow)"/>
  <text x="240" y="288" text-anchor="middle" font-size="10" letter-spacing="3" fill="#93b8c4">INPUT · PROCESS · OUTPUT · REAL-TIME · LOW POWER</text>
</svg>"""

ZONES = """
<!-- ===== PREVIEW 1 ===== -->
<section id="scr-preview1" class="screen">
  <div class="panel">
    <span class="tag">Before Sector 01</span>
    <h2>กำลังจะเข้าสู่: ห้องสแกนสมอง (Brain Scan)</h2>
    <div class="dcard">
      <div class="ico"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="14" y="14" width="52" height="52" rx="8" fill="none" stroke="#22d3ee" stroke-width="3"/>
        <rect x="28" y="28" width="24" height="24" rx="4" fill="#a3e635"/></svg></div>
      <div><div class="skillcard" style="margin:0">
        <div class="sk-name">ทักษะที่จะได้: MCU ต่างจาก MPU อย่างไร</div>
        <p class="muted" style="margin:6px 0 0">แยกได้ว่าอุปกรณ์รอบตัวใช้ "สมองแบบไหน" และเหตุผลทางวิศวกรรมที่เลือก ทั้งต้นทุน พลังงาน และการตอบสนองแบบเวลาจริง</p>
      </div></div>
    </div>
    <div class="btn-row"><button class="btn primary" data-goto="scr-lesson1">เข้าห้องนี้</button></div>
  </div>
</section>

<!-- ===== SECTOR 1 ===== -->
<section id="scr-lesson1" class="screen">
  <div class="panel">
    <span class="tag">Sector 01 · Brain Scan</span>
    <h2>ห้องสแกนสมอง: ไมโครคอนโทรลเลอร์ (MCU) กับ ไมโครโพรเซสเซอร์ (MPU)</h2>
    <p>รอบตัวเรามีคอมพิวเตอร์ซ่อนอยู่มากกว่าที่เห็น เครื่องซักผ้า รีโมท ไมโครเวฟ จนถึงระบบเบรก ABS ในรถยนต์ ล้วนมี
      <b>ไมโครคอนโทรลเลอร์ (Microcontroller, MCU)</b> เป็นสมอง ความต่างสำคัญคือ MCU รวม <b>CPU + หน่วยความจำ + อุปกรณ์รอบข้าง (I/O)</b>
      ไว้ใน <b>ชิปตัวเดียว</b> ส่วน MPU มีเพียงหน่วยประมวลผลที่เร็วมาก แต่ต้องต่อ RAM ภายนอก และมักรันระบบปฏิบัติการเต็มรูปแบบ</p>
    <div class="tbl-wrap"><table>
      <tr><th>ประเด็น</th><th>MCU (เช่น ATmega328P, ESP32)</th><th>MPU (เช่น CPU โน้ตบุ๊ก, SoC ของ Raspberry Pi)</th></tr>
      <tr><td>โครงสร้าง</td><td>CPU, Flash, SRAM, GPIO, ADC, Timer อยู่ในชิปเดียว</td><td>เน้นแกนประมวลผล ต้องมี RAM และหน่วยเก็บข้อมูลภายนอก</td></tr>
      <tr><td>ซอฟต์แวร์</td><td>Bare-metal หรือ RTOS เปิดเครื่องแล้วทำงานทันที</td><td>รัน OS เช่น Linux/Windows บูตนานกว่า</td></tr>
      <tr><td>พลังงาน/ราคา</td><td>ต่ำมาก ใช้แบตเตอรี่ได้นาน ราคาหลักสิบถึงหลักร้อยบาท</td><td>สูงกว่า ต้องระบายความร้อน ราคาสูงกว่า</td></tr>
      <tr><td>จุดแข็ง</td><td>ควบคุมฮาร์ดแวร์ตรง ๆ ตอบสนองแบบเวลาจริง (Real-time)</td><td>งานคำนวณหนัก กราฟิก มัลติทาสก์ หลายแอป</td></tr>
    </table></div>
    <div class="tbl-wrap"><table>
      <tr><th colspan="2">5 เหตุผลที่ MCU ครองโลก (สรุปจากคลิป The Brain Behind Everything)</th></tr>
      <tr><td>1. ราคาถูก</td><td>รีโมททีวีราคาไม่กี่ร้อยบาทก็มี MCU อยู่ข้างใน</td></tr>
      <tr><td>2. ประหยัดพลังงาน</td><td>ใช้ถ่านหรือแบตเตอรี่ได้นานเป็นเดือนถึงเป็นปี</td></tr>
      <tr><td>3. เปิดแล้วทำงานทันที</td><td>ไม่ต้องรอบูตระบบปฏิบัติการแบบคอมพิวเตอร์</td></tr>
      <tr><td>4. ควบคุมฮาร์ดแวร์โดยตรง</td><td>อ่านเซนเซอร์และสั่งมอเตอร์ รีเลย์ ได้จากขาของชิปเอง</td></tr>
      <tr><td>5. เชื่อถือได้</td><td>ทำงานเดิมซ้ำได้แม่นยำต่อเนื่องหลายปีในเครื่องจักร</td></tr>
    </table></div>
    <div class="keyfact"><b>ระวังชื่อคล้าย:</b> <b>Raspberry Pi Pico</b> (ชิป RP2040) เป็นบอร์ด <b>MCU</b> แบบเดียวกับ Arduino Uno และ ESP32 แต่ <b>Raspberry Pi 4/5</b> เป็นคอมพิวเตอร์บอร์ดเดี่ยวที่ใช้ MPU และรัน Linux</div>
    <div class="keyfact"><b>จำง่าย:</b> ถ้างานคือ "อ่านเซนเซอร์ ตัดสินใจ สั่งอุปกรณ์" ซ้ำ ๆ ด้วยพลังงานต่ำ เลือก MCU · ถ้างานคือ "รันแอปหลายตัว ประมวลผลภาพ/วิดีโอ" เลือก MPU</div>

    <h3 style="margin-top:18px">ห้องทดลอง: คัดแยกสมองกล (Device Sorter)</h3>
    <p class="muted">แตะเลือกอุปกรณ์ 1 ชิ้น แล้วตัดสินว่าใช้ MCU หรือ MPU เป็นสมองหลัก — คัดแยกถูกครบ 6 ชิ้นขึ้นไปรับเหรียญตรา</p>
    <div class="pickgrid" id="devGrid">
      <button class="pick" data-dev="washer">เครื่องซักผ้าอัตโนมัติ<small>ควบคุมมอเตอร์ วาล์วน้ำ ตั้งเวลา</small></button>
      <button class="pick" data-dev="rpi">Raspberry Pi รัน Linux<small>เปิดเว็บเบราว์เซอร์ได้</small></button>
      <button class="pick" data-dev="remote">รีโมททีวี<small>ใช้ถ่าน AAA ได้เป็นปี</small></button>
      <button class="pick" data-dev="laptop">โน้ตบุ๊ก<small>CPU หลายคอร์ RAM 16 GB</small></button>
      <button class="pick" data-dev="thermo">เทอร์โมมิเตอร์วัดไข้ดิจิทัล<small>อ่านค่า แสดงผล แล้วดับ</small></button>
      <button class="pick" data-dev="phone">สมาร์ทโฟน<small>รันแอปหลายตัวพร้อมกัน</small></button>
      <button class="pick" data-dev="abs">ระบบเบรก ABS รถยนต์<small>ต้องตอบสนองระดับมิลลิวินาที</small></button>
      <button class="pick" data-dev="band">สายรัดข้อมือนับก้าว<small>ชาร์จสัปดาห์ละครั้ง</small></button>
    </div>
    <div class="labrow">
      <button class="btn sm" data-cls="mcu">สมองคือ MCU</button>
      <button class="btn sm" data-cls="mpu">สมองคือ MPU</button>
    </div>
    <div class="status-line" id="devStatus">เลือกอุปกรณ์ก่อน แล้วกดปุ่มตัดสิน</div>
    <div class="btn-row"><button class="btn primary" data-quiz="check1">ไปทำแบบฝึกหัดห้องนี้</button></div>
  </div>
</section>

<!-- ===== PREVIEW 2 ===== -->
<section id="scr-preview2" class="screen">
  <div class="panel">
    <span class="tag">Before Sector 02</span>
    <h2>กำลังจะเข้าสู่: ห้องเอกซเรย์ชิป (Chip X-Ray)</h2>
    <div class="dcard">
      <div class="ico"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="10" width="28" height="28" rx="4" fill="#22d3ee"/><rect x="42" y="10" width="28" height="12" rx="3" fill="#a3e635"/>
        <rect x="42" y="26" width="28" height="12" rx="3" fill="#facc15"/><rect x="10" y="42" width="60" height="28" rx="4" fill="none" stroke="#22d3ee" stroke-width="3"/></svg></div>
      <div><div class="skillcard" style="margin:0">
        <div class="sk-name">ทักษะที่จะได้: อวัยวะภายใน MCU และการแปลงสัญญาณ ADC</div>
        <p class="muted" style="margin:6px 0 0">รู้หน้าที่ของ Flash, SRAM, EEPROM, GPIO, ADC, Timer/PWM และบัสสื่อสาร พร้อมคำนวณค่า ADC ได้เอง</p>
      </div></div>
    </div>
    <div class="btn-row"><button class="btn primary" data-goto="scr-lesson2">เข้าห้องนี้</button></div>
  </div>
</section>

<!-- ===== SECTOR 2 ===== -->
<section id="scr-lesson2" class="screen">
  <div class="panel">
    <span class="tag">Sector 02 · Chip X-Ray</span>
    <h2>ห้องเอกซเรย์ชิป: ข้างในไมโครคอนโทรลเลอร์มีอะไร</h2>
    <p>MCU เปรียบเหมือน "โรงงานจิ๋ว" ในชิปเดียว มีผู้จัดการ (CPU) ตู้เก็บคู่มือถาวร (Flash) โต๊ะทำงานชั่วคราว (SRAM)
      สมุดบันทึกที่ไม่หายเมื่อปิดไฟ (EEPROM) และประตูเข้า-ออกสู่โลกภายนอก (Peripherals)</p>
    <div class="tbl-wrap"><table>
      <tr><th>ส่วนประกอบ</th><th>Arduino Uno (ATmega328P)</th><th>ESP32-WROOM-32</th></tr>
      <tr><td>CPU / ความถี่สัญญาณนาฬิกา</td><td>8-bit AVR · 16 MHz</td><td>32-bit Xtensa LX6 สองคอร์ · สูงสุด 240 MHz</td></tr>
      <tr><td>Flash (เก็บโปรแกรม)</td><td>32 KB</td><td>4 MB (ชิปภายนอกบนโมดูล)</td></tr>
      <tr><td>SRAM (ตัวแปรขณะทำงาน)</td><td>2 KB</td><td>520 KB</td></tr>
      <tr><td>ADC</td><td>10 บิต (0–1023) อ้างอิง 5 V</td><td>12 บิต (0–4095) ช่วงราว 0–3.3 V</td></tr>
      <tr><td>การสื่อสารไร้สาย</td><td>ไม่มี</td><td>Wi-Fi 2.4 GHz + Bluetooth/BLE</td></tr>
    </table></div>
    <div class="codebox">ค่าดิจิทัลจาก ADC  =  (แรงดันที่วัด / แรงดันอ้างอิง) × (2^n − 1)

Uno   : 2.5 V / 5.0 V × 1023  ≈ 512
ESP32 : 1.65 V / 3.3 V × 4095 ≈ 2048</div>

    <h3 style="margin-top:18px">ห้องทดลอง 1: เอกซเรย์ชิป (Chip X-Ray)</h3>
    <p class="muted">แตะแต่ละบล็อกในชิปเพื่อดูหน้าที่และตัวอย่างการใช้งานจริงในโปรเจกต์</p>
    <div class="chipmap">
      <button class="pick core" data-blk="core">CPU CORE<small>ผู้จัดการโรงงาน</small></button>
      <button class="pick" data-blk="flash">FLASH</button>
      <button class="pick" data-blk="sram">SRAM</button>
      <button class="pick" data-blk="eeprom">EEPROM / NVS</button>
      <button class="pick" data-blk="gpio">GPIO</button>
      <button class="pick" data-blk="adc">ADC</button>
      <button class="pick" data-blk="timer">TIMER / PWM</button>
      <button class="pick" data-blk="comm">UART · I2C · SPI</button>
      <button class="pick" data-blk="wdt">WATCHDOG</button>
    </div>
    <div class="status-line" id="blkStatus">ยังไม่ได้เลือกบล็อก</div>

    <h3 style="margin-top:18px">ห้องทดลอง 2: เครื่องแปลงสัญญาณ ADC</h3>
    <p class="muted">เลื่อนแรงดันอินพุต แล้วสลับบอร์ด เพื่อดูว่าค่าดิจิทัลที่ MCU "เห็น" เปลี่ยนไปอย่างไร</p>
    <div class="labrow">
      <button class="toggle on" id="adcBoard">บอร์ด: Arduino Uno · 10 บิต · 5.0 V</button>
    </div>
    <input type="range" class="rng" id="adcVin" min="0" max="500" value="250" aria-label="แรงดันอินพุต">
    <div class="labrow"><span class="readout" id="adcV">2.50<small>V</small></span><span class="readout" id="adcRaw">512<small>/ 1023</small></span></div>
    <div class="meter"><i id="adcBar"></i></div>
    <div class="status-line" id="adcStatus">เลื่อนแถบเพื่อเริ่มทดลอง</div>
    <div class="btn-row"><button class="btn primary" data-quiz="check2">ไปทำแบบฝึกหัดห้องนี้</button></div>
  </div>
</section>

<!-- ===== PREVIEW 3 ===== -->
<section id="scr-preview3" class="screen">
  <div class="panel">
    <span class="tag">Before Sector 03</span>
    <h2>กำลังจะเข้าสู่: ห้องลูปนิรันดร์ (The Super Loop)</h2>
    <div class="dcard">
      <div class="ico"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 40a20 20 0 1 1 6 14" fill="none" stroke="#22d3ee" stroke-width="5" stroke-linecap="round"/>
        <path d="M14 56l12-2-2-12" fill="none" stroke="#facc15" stroke-width="4" stroke-linecap="round"/></svg></div>
      <div><div class="skillcard" style="margin:0">
        <div class="sk-name">ทักษะที่จะได้: โครงสร้างโปรแกรมฝังตัว setup() / loop()</div>
        <p class="muted" style="margin:6px 0 0">Input → Process → Output, Polling กับ Interrupt, delay() ที่ทำให้ระบบ "หูหนวก", millis(), Watchdog และโหมดประหยัดพลังงาน</p>
      </div></div>
    </div>
    <div class="btn-row"><button class="btn primary" data-goto="scr-lesson3">เข้าห้องนี้</button></div>
  </div>
</section>

<!-- ===== SECTOR 3 ===== -->
<section id="scr-lesson3" class="screen">
  <div class="panel">
    <span class="tag">Sector 03 · The Super Loop</span>
    <h2>ห้องลูปนิรันดร์: ชีวิตของโปรแกรมบน MCU</h2>
    <p>โปรแกรมบน MCU ไม่มีวัน "จบ" เมื่อจ่ายไฟ <code>setup()</code> ทำงาน <b>ครั้งเดียว</b> เพื่อตั้งค่าขา เริ่มต้นเซนเซอร์ และเชื่อมต่อ Wi-Fi
      จากนั้น <code>loop()</code> วนซ้ำ <b>ตลอดไป</b> ตามจังหวะ อ่านค่า (Input) → ตัดสินใจ (Process) → สั่งงาน (Output)</p>
    <div class="flowrow">
      <div class="fbox in"><b>INPUT</b>อ่านเซนเซอร์ เช่น อุณหภูมิ ฝุ่น ปุ่มกด</div>
      <div class="fbox"><b>PROCESS</b>เทียบเกณฑ์ กรองสัญญาณ คำนวณ</div>
      <div class="fbox out"><b>OUTPUT</b>สั่งรีเลย์ บัซเซอร์ จอ หรือส่งแจ้งเตือน</div>
    </div>
    <div class="codebox">void setup() {            // ทำครั้งเดียวตอนเปิดเครื่อง
  pinMode(FAN, OUTPUT);
  Serial.begin(115200);
}

void loop() {             // วนซ้ำตลอดไป
  float t = readTemp();   // INPUT
  if (t &gt; 30.0) {         // PROCESS
    digitalWrite(FAN, HIGH); // OUTPUT
  } else {
    digitalWrite(FAN, LOW);
  }
}</div>
    <div class="tbl-wrap"><table>
      <tr><th>เทคนิค</th><th>ความหมาย</th><th>ใช้เมื่อ</th></tr>
      <tr><td>Polling</td><td>วนถามสถานะซ้ำ ๆ ใน loop()</td><td>เหตุการณ์ไม่เร่งด่วน เช่น อ่านอุณหภูมิทุก 2 วินาที</td></tr>
      <tr><td>Interrupt</td><td>ฮาร์ดแวร์ขัดจังหวะ CPU ทันทีเมื่อเกิดเหตุ</td><td>เหตุการณ์สั้นและห้ามพลาด เช่น นับพัลส์จากเซนเซอร์วัดการไหลของน้ำ</td></tr>
      <tr><td>delay(ms)</td><td>หยุดรอแบบ blocking ทำอย่างอื่นไม่ได้</td><td>เฉพาะงานทดลองสั้น ๆ</td></tr>
      <tr><td>millis()</td><td>อ่านเวลาที่ผ่านไปแล้วตัดสินใจ ไม่หยุดรอ</td><td>ระบบจริงที่ต้องตอบสนองหลายงานพร้อมกัน</td></tr>
      <tr><td>Watchdog</td><td>ตัวจับเวลาที่รีเซ็ตชิปเมื่อโปรแกรมค้าง</td><td>อุปกรณ์ที่ต้องทำงานเองตลอด 24 ชั่วโมง</td></tr>
    </table></div>

    <h3 style="margin-top:18px">ห้องทดลอง: เครื่องจำลองลูป (Loop Simulator)</h3>
    <p class="muted">ระบบพัดลมอัตโนมัติ: เกณฑ์เปิดพัดลมคือ T &gt; 30 °C และมีปุ่มฉุกเฉินที่ผู้ใช้กดระหว่างทาง
      เลือกอุณหภูมิ แล้วสลับวิธีหน่วงเวลา เพื่อดูว่าระบบตอบสนองปุ่มฉุกเฉินช้าแค่ไหน — ทดลองครบ 4 แบบขึ้นไปรับเหรียญตรา</p>
    <div class="labrow">
      <button class="btn sm" data-loop="26">T = 26 °C</button>
      <button class="btn sm" data-loop="31">T = 31 °C</button>
      <button class="btn sm" data-loop="35">T = 35 °C</button>
      <button class="toggle off" id="loopMode">delay(3000) แบบ blocking</button>
    </div>
    <div class="tape" id="loopTape">ผลการจำลองจะปรากฏที่นี่</div>
    <div class="status-line" id="loopStatus">ยังไม่ได้เริ่มจำลอง</div>
    <div class="btn-row"><button class="btn primary" data-quiz="check3">ไปทำแบบฝึกหัดห้องนี้</button></div>
  </div>
</section>
"""

LAB_JS = r"""
/* ---- LAB 1: Device Sorter ---- */
const DEVICES={
  washer:{a:'mcu',why:'งานควบคุมเฉพาะทาง ลำดับขั้นตายตัว ต้องสั่งมอเตอร์และวาล์วตรง ๆ ราคาต้องต่ำ'},
  rpi:{a:'mpu',why:'Raspberry Pi ใช้ SoC ตระกูล ARM Cortex-A ต่อ RAM ภายนอก และรันระบบปฏิบัติการ Linux เต็มรูปแบบ'},
  remote:{a:'mcu',why:'ทำงานเฉพาะตอนกดปุ่มแล้วกลับไปหลับ กินไฟระดับไมโครแอมป์ ถ่านจึงอยู่ได้เป็นปี'},
  laptop:{a:'mpu',why:'CPU โน้ตบุ๊กเป็นหน่วยประมวลผลอเนกประสงค์ ต้องมี RAM และ SSD ภายนอก รัน OS และแอปจำนวนมาก'},
  thermo:{a:'mcu',why:'อ่านเซนเซอร์ แปลงค่าผ่าน ADC แสดงผล แล้วปิดตัว เป็นงาน Input-Process-Output แบบง่าย'},
  phone:{a:'mpu',why:'สมาร์ทโฟนใช้ Application Processor แบบ SoC รันระบบปฏิบัติการและแอปหลายตัวพร้อมกัน (ภายในยังมี MCU ย่อยช่วยงานเฉพาะด้วย)'},
  abs:{a:'mcu',why:'ระบบเบรกต้องตอบสนองแบบเวลาจริงที่คาดเดาได้ (deterministic) ระดับมิลลิวินาที จึงใช้ MCU เกรดยานยนต์'},
  band:{a:'mcu',why:'เน้นประหยัดพลังงานสูงสุด อ่านเซนเซอร์ความเร่งเป็นช่วง ๆ แล้วส่งข้อมูลผ่าน BLE'}
};
let devSel=null;
function pickDev(k){
  devSel=k; $$('#devGrid .pick').forEach(b=>b.classList.toggle('sel',b.dataset.dev===k));
  const st=$('#devStatus'); st.className='status-line'; st.textContent='เลือกแล้ว — อุปกรณ์นี้ใช้ MCU หรือ MPU เป็นสมองหลัก';
}
function judgeDev(cls){
  const st=$('#devStatus');
  if(!devSel){st.className='status-line';st.textContent='กรุณาแตะเลือกอุปกรณ์ก่อน';SFX.play('wrong');return;}
  const d=DEVICES[devSel], btn=$('#devGrid [data-dev="'+devSel+'"]');
  btn.classList.remove('sel','ok','bad');
  if(cls===d.a){
    btn.classList.add('ok'); st.className='status-line ok';
    st.innerHTML='ถูกต้อง — <b>'+d.a.toUpperCase()+'</b> · '+d.why; SFX.play('correct');
    markLab('lab1',devSel);
    if(labCount('lab1')===8) toast('คัดแยกครบทั้ง 8 อุปกรณ์แล้ว');
  } else {
    btn.classList.add('bad'); st.className='status-line';
    st.innerHTML='ยังไม่ใช่ — ลองคิดใหม่: ต้องรัน OS และแอปหลายตัว หรือเป็นงานควบคุมเฉพาะที่ประหยัดพลังงาน'; SFX.play('wrong');
  }
  devSel=null;
}

/* ---- LAB 2a: Chip X-Ray ---- */
const BLOCKS={
  core:'<b>CPU Core</b> ดึงคำสั่งจาก Flash มาถอดรหัสและประมวลผลทีละคำสั่งตามจังหวะสัญญาณนาฬิกา — Uno 16 MHz หนึ่งรอบสัญญาณนาฬิกายาว 62.5 ns',
  flash:'<b>Flash</b> หน่วยความจำไม่ลบเลือน (non-volatile) เก็บโปรแกรมที่อัปโหลด ปิดไฟแล้วโปรแกรมยังอยู่',
  sram:'<b>SRAM</b> หน่วยความจำลบเลือน (volatile) เก็บตัวแปรขณะโปรแกรมทำงาน ปิดไฟแล้วค่าหายหมด Uno มีเพียง 2 KB จึงต้องระวังอาร์เรย์และ String ขนาดใหญ่',
  eeprom:'<b>EEPROM / NVS</b> เก็บค่าตั้งค่าที่ต้องจำข้ามการปิดเครื่อง เช่น ค่าคาลิเบรตเซนเซอร์ หรือเกณฑ์แจ้งเตือน (ESP32 ใช้พื้นที่ใน Flash จำลองเป็น NVS)',
  gpio:'<b>GPIO</b> ขาอเนกประสงค์ ตั้งเป็นอินพุตอ่านปุ่ม/เซนเซอร์ดิจิทัล หรือเอาต์พุตสั่ง LED/รีเลย์ ระดับแรงดัน HIGH/LOW',
  adc:'<b>ADC</b> แปลงแรงดันแอนะล็อกเป็นตัวเลข ใช้กับเซนเซอร์ที่ให้แรงดันต่อเนื่อง เช่น LDR, MQ-3, pH, ความชื้นดิน',
  timer:'<b>Timer / PWM</b> นับเวลาด้วยฮาร์ดแวร์ และสร้างพัลส์ PWM ปรับความสว่าง LED ความเร็วพัดลม หรือสั่งเซอร์โว',
  comm:'<b>UART / I2C / SPI</b> ช่องสื่อสารกับโมดูลอื่น เช่น จอ OLED (I2C) เซนเซอร์ฝุ่น PMS5003 (UART) การ์ด SD (SPI)',
  wdt:'<b>Watchdog Timer</b> ต้องถูก "ป้อน" (reset) เป็นระยะ ถ้าโปรแกรมค้างจนไม่ได้ป้อน ชิปจะรีเซ็ตตัวเอง สำคัญมากกับระบบเฝ้าระวังที่ไม่มีคนดูแล'
};
function showBlk(k){
  $$('.chipmap .pick').forEach(b=>b.classList.toggle('sel',b.dataset.blk===k));
  const b=$('.chipmap [data-blk="'+k+'"]'); b.classList.add('ok');
  const st=$('#blkStatus'); st.className='status-line ok'; st.innerHTML=BLOCKS[k]; SFX.play('ping');
  markLab('lab2','blk_'+k,6);
}
/* ---- LAB 2b: ADC ---- */
let adcEsp=false;
function adcUpdate(user){
  const pos=+$('#adcVin').value/100;            /* 0.00 – 5.00 */
  const vref=adcEsp?3.3:5.0, max=adcEsp?4095:1023;
  const v=Math.min(pos,5);
  let raw=Math.round(Math.min(v,vref)/vref*max);
  $('#adcV').innerHTML=v.toFixed(2)+'<small>V</small>';
  $('#adcRaw').innerHTML=raw+'<small>/ '+max+'</small>';
  $('#adcBar').style.width=(raw/max*100)+'%';
  const st=$('#adcStatus');
  if(adcEsp&&v>3.3){st.className='status-line';st.innerHTML='<b>อันตราย</b> — ขา ESP32 รับแรงดันได้ไม่เกิน 3.3 V ค่าอ่านจะอิ่มตัวที่ '+max+' และชิปอาจเสียหาย ต้องใช้วงจรแบ่งแรงดันก่อนเข้าขา';}
  else {st.className='status-line ok';st.innerHTML='ค่าที่ได้ = '+v.toFixed(2)+' / '+vref.toFixed(1)+' × '+max+' ≈ <b>'+raw+'</b> · ความละเอียด 1 ขั้น ≈ '+(vref/max*1000).toFixed(2)+' mV';}
  if(user){ markLab('lab2',(adcEsp?'adc12_':'adc10_')+(v>3.3?'hi':'lo'),4); }
}

/* ---- LAB 3: Loop Simulator ---- */
let loopMillis=false, loopBusy=false;
function runLoop(t){
  if(loopBusy) return; loopBusy=true;
  const tape=$('#loopTape'), st=$('#loopStatus');
  tape.innerHTML=''; st.className='status-line'; st.textContent='เปิดเครื่อง...';
  const fan=t>30;
  const steps=[['setup()',''],['อ่าน T='+t,''],[t+(fan?' &gt; 30':' ≤ 30'),''],['FAN '+(fan?'ON':'OFF'),fan?'hi':'lo']];
  if(loopMillis){ steps.push(['กดปุ่มฉุกเฉิน','lo'],['ตอบสนองใน ~1 ms','hi'],['loop() รอบถัดไป','']); }
  else { steps.push(['delay(3000)...',''],['กดปุ่มฉุกเฉิน','lo'],['ยังรออยู่ใน delay','lo'],['ตอบสนองช้าสุด 3 s','lo']); }
  let i=0;
  const step=()=>{
    if(i<steps.length){const s=document.createElement('span');s.innerHTML=steps[i][0];if(steps[i][1])s.className=steps[i][1];tape.appendChild(s);
      SFX.play(i===0?'ping':'tick'); i++; setTimeout(step,REDUCED?40:380);}
    else{
      loopBusy=false; st.className='status-line ok';
      st.innerHTML=(fan?'T = '+t+' เกิน 30 °C จึงสั่ง <b>พัดลมเปิด</b>':'T = '+t+' ยังไม่เกินเกณฑ์ <b>พัดลมปิด</b>')+' · '+
        (loopMillis?'ใช้ <code>millis()</code> แบบไม่หยุดรอ loop() วนเร็วมาก ปุ่มฉุกเฉินจึงถูกตรวจแทบทันที':
          'ใช้ <code>delay(3000)</code> CPU หยุดรอทั้งหมด ปุ่มที่กดระหว่างนั้นอาจตอบสนองช้าถึง 3 วินาทีหรือพลาดไปเลย ถ้าเป็นปุ่มสั้น ๆ ควรใช้ millis() หรือ interrupt');
      SFX.play('correct'); markLab('lab3',t+'|'+(loopMillis?'ms':'dl'));
      if(labCount('lab3')>=6) toast('ทดลองครบทุกรูปแบบแล้ว');
    }
  };
  step();
}
"""

LAB_WIRING = r"""
  const dv=e.target.closest('[data-dev]'); if(dv){SFX.play('select');pickDev(dv.dataset.dev);return;}
  const cl=e.target.closest('[data-cls]'); if(cl){judgeDev(cl.dataset.cls);return;}
  const bk=e.target.closest('[data-blk]'); if(bk){showBlk(bk.dataset.blk);return;}
  const lp=e.target.closest('[data-loop]'); if(lp){SFX.play('click');runLoop(+lp.dataset.loop);return;}
  if(e.target.closest('#adcBoard')){
    adcEsp=!adcEsp; const b=$('#adcBoard');
    b.textContent=adcEsp?'บอร์ด: ESP32 · 12 บิต · 3.3 V':'บอร์ด: Arduino Uno · 10 บิต · 5.0 V';
    SFX.play('select'); adcUpdate(true); return;
  }
  if(e.target.closest('#loopMode')){
    loopMillis=!loopMillis; const b=$('#loopMode');
    b.textContent=loopMillis?'millis() แบบไม่หยุดรอ':'delay(3000) แบบ blocking';
    b.className='toggle '+(loopMillis?'on':'off'); SFX.play('select'); return;
  }
"""
INIT_EXTRA = " $('#adcVin').addEventListener('input',()=>adcUpdate(true)); adcUpdate(false);"

B = {}
B['district1'] = [
 ('ข้อใดอธิบายไมโครคอนโทรลเลอร์ (MCU) ได้ถูกต้องที่สุด',
  ['ชิปที่รวม CPU หน่วยความจำ และอุปกรณ์รอบข้างอย่าง GPIO, ADC, Timer ไว้ในตัวเดียว เพื่องานควบคุมเฉพาะทาง',
   'หน่วยประมวลผลความเร็วสูงที่ต้องต่อ RAM ภายนอกและรันระบบปฏิบัติการเสมอ',
   'การ์ดจอสำหรับประมวลผลกราฟิก',
   'หน่วยความจำสำรองข้อมูลแบบถาวร'],
  'จุดเด่นของ MCU คือการรวมทุกอย่างที่จำเป็นต่อการควบคุมไว้ใน "ชิปเดียว" ทำให้เล็ก ราคาถูก และประหยัดพลังงาน'),
 ('ทีมต้องการทำเซนเซอร์วัดความชื้นดินในแปลงเกษตร ใช้แบตเตอรี่ได้นานหลายเดือน ส่งค่าทุก 15 นาที ควรเลือกสมองกลแบบใด',
  ['MCU ที่มีโหมด Deep Sleep เช่น ESP32 เพราะกินไฟต่ำมากระหว่างพัก',
   'คอมพิวเตอร์โน้ตบุ๊กเพราะประมวลผลเร็ว',
   'MPU ที่รัน Linux ตลอดเวลาเพราะเขียนโปรแกรมง่ายกว่า',
   'ไม่ต้องใช้สมองกล ต่อเซนเซอร์เข้า Wi-Fi โดยตรงได้เลย'],
  'งานอ่านค่าเป็นช่วง ๆ แล้วพัก เหมาะกับ MCU ที่ปลุกตื่นขึ้นมาทำงานสั้น ๆ แล้วกลับไป Deep Sleep ซึ่งกินไฟระดับไมโครแอมป์ (ตัวชิป)'),
 ('ข้อใดเป็นจุดเด่นของ MPU เมื่อเทียบกับ MCU',
  ['รองรับงานคำนวณหนักและระบบปฏิบัติการเต็มรูปแบบ เช่น ประมวลผลภาพ วิดีโอ และรันหลายแอปพร้อมกัน',
   'กินไฟน้อยกว่า MCU เสมอ',
   'รวม ADC และ GPIO ไว้ในชิปเดียวโดยไม่ต้องมีอุปกรณ์ภายนอก',
   'บูตเครื่องได้เร็วกว่าในระดับมิลลิวินาทีเสมอ'],
  'MPU ออกแบบเพื่อพลังประมวลผลสูง แลกกับการต้องใช้ RAM ภายนอก กินไฟมากกว่า และบูตนานกว่า'),
 ('ระบบเบรก ABS ในรถยนต์ใช้ MCU แทนคอมพิวเตอร์ทั่วไป เหตุผลทางวิศวกรรมที่สำคัญที่สุดคือข้อใด',
  ['ต้องตอบสนองแบบเวลาจริงที่คาดเดาได้ (deterministic real-time) และทำงานเชื่อถือได้ในสภาพแวดล้อมรุนแรง',
   'เพราะ MCU มีหน้าจอสัมผัสในตัว',
   'เพราะ MCU ประมวลผลกราฟิกได้ดีกว่า',
   'เพราะ MCU ต้องเชื่อมต่ออินเทอร์เน็ตตลอดเวลา'],
  'งานความปลอดภัยต้องรู้แน่ชัดว่าจะตอบสนองภายในกี่มิลลิวินาที MCU ที่รันโปรแกรมเฉพาะงานโดยไม่มี OS ขนาดใหญ่จึงเหมาะกว่า'),
 ('Raspberry Pi 4 ที่รัน Linux และเปิดเว็บเบราว์เซอร์ได้ จัดเป็นอุปกรณ์ประเภทใด',
  ['คอมพิวเตอร์บอร์ดเดี่ยว (SBC) ที่ใช้ MPU/SoC ตระกูล ARM Cortex-A',
   'ไมโครคอนโทรลเลอร์ 8 บิต แบบเดียวกับ Arduino Uno',
   'เซนเซอร์อุณหภูมิ',
   'โมดูลรีเลย์'],
  'Raspberry Pi เป็น Single Board Computer ใช้ SoC ที่มีแกน Cortex-A ต่อ RAM และรัน OS ต่างจาก Arduino ที่เป็นบอร์ด MCU'),
 ('ข้อใดคือตัวอย่างของ "ระบบฝังตัว (Embedded System)" ที่ชัดเจนที่สุด',
  ['เครื่องปรับอากาศที่มีวงจรควบคุมอุณหภูมิอัตโนมัติอยู่ภายใน',
   'โปรแกรมพิมพ์เอกสารบนโน้ตบุ๊ก',
   'เว็บไซต์ร้านค้าออนไลน์',
   'ไฟล์สเปรดชีตคำนวณงบประมาณ'],
  'ระบบฝังตัวคือคอมพิวเตอร์ขนาดเล็กที่ฝังอยู่ในอุปกรณ์เพื่อทำหน้าที่เฉพาะ ผู้ใช้มักไม่รู้ตัวว่ามีคอมพิวเตอร์อยู่ข้างใน'),
 ('เหตุใดอุปกรณ์อย่างรีโมททีวีจึงใช้ถ่านได้นานเป็นปี',
  ['MCU อยู่ในโหมดหลับ (sleep) เกือบตลอดเวลา และตื่นมาทำงานสั้น ๆ เฉพาะเมื่อกดปุ่ม',
   'เพราะรีโมทมีแผงโซลาร์เซลล์ในตัวทุกรุ่น',
   'เพราะรีโมทไม่ได้ใช้ไฟฟ้าในการส่งสัญญาณ',
   'เพราะ MCU ในรีโมทรันระบบปฏิบัติการ Linux ที่ประหยัดไฟ'],
  'กลยุทธ์ "หลับให้นาน ตื่นให้สั้น" คือหัวใจของการออกแบบอุปกรณ์ใช้แบตเตอรี่ ซึ่ง MCU ทำได้ดีมาก'),
 ('Arduino Uno กับ ESP32 ต่างกันในด้านใดที่ส่งผลโดยตรงต่อโปรเจกต์ IoT มากที่สุด',
  ['ESP32 มี Wi-Fi และ Bluetooth ในตัว ส่วน Uno ไม่มีการสื่อสารไร้สาย',
   'Uno มี Wi-Fi แต่ ESP32 ไม่มี',
   'ทั้งสองบอร์ดใช้ CPU ตัวเดียวกัน',
   'ESP32 ใช้ได้เฉพาะภาษา Python'],
  'ESP32 รวม Wi-Fi 2.4 GHz และ Bluetooth/BLE ไว้ในชิป จึงส่งข้อมูลขึ้นคลาวด์หรือแจ้งเตือนมือถือได้โดยไม่ต้องเพิ่มโมดูล'),
 ('การเขียนโปรแกรมแบบ "Bare-metal" บน MCU หมายถึงข้อใด',
  ['โปรแกรมทำงานบนฮาร์ดแวร์โดยตรง ไม่มีระบบปฏิบัติการคั่นกลาง',
   'โปรแกรมที่เขียนด้วยภาษา Python บนคลาวด์',
   'โปรแกรมที่ต้องรันบน Windows เท่านั้น',
   'การเขียนโปรแกรมบนแผ่นโลหะ'],
  'Bare-metal คือโปรแกรมควบคุมฮาร์ดแวร์โดยตรง ตัวอย่างคือ Arduino sketch ทั่วไป ส่วนงานซับซ้อนขึ้นอาจใช้ RTOS เช่น FreeRTOS บน ESP32'),
 ('ทีมต้องการระบบกล้องจดจำใบหน้าความละเอียดสูง เก็บวิดีโอ และแสดงผลบนหน้าเว็บพร้อมกัน ตัวเลือกที่เหมาะสมกว่าคือข้อใด',
  ['ใช้ MPU/SBC เช่น Raspberry Pi เพราะต้องประมวลผลภาพหนักและรันหลายบริการพร้อมกัน',
   'ใช้ Arduino Uno เพียงตัวเดียวเพราะราคาถูกที่สุด',
   'ใช้เซนเซอร์ LDR แทนกล้อง',
   'ใช้รีเลย์ควบคุมกล้อง'],
  'การเลือกฮาร์ดแวร์ต้องดูภาระงาน งานวิดีโอความละเอียดสูงและเว็บเซิร์ฟเวอร์เกินขีดความสามารถของ MCU 8 บิตอย่างมาก'),
 ('ข้อความใด "ไม่ถูกต้อง" เกี่ยวกับไมโครคอนโทรลเลอร์',
  ['MCU ทุกตัวต้องติดตั้งระบบปฏิบัติการ Windows ก่อนใช้งาน',
   'MCU เปิดเครื่องแล้วเริ่มรันโปรแกรมได้แทบทันที',
   'MCU ควบคุมขาอินพุต/เอาต์พุตได้โดยตรง',
   'MCU มีหน่วยความจำโปรแกรมอยู่ในตัว'],
  'MCU ส่วนใหญ่ไม่ใช้ OS ขนาดใหญ่ บางระบบใช้ RTOS ขนาดเล็ก แต่ไม่มีการติดตั้ง Windows'),
 ('ในรถยนต์สมัยใหม่หนึ่งคันมีหน่วยควบคุมอิเล็กทรอนิกส์ (ECU) หลายสิบตัว สาเหตุหลักที่ใช้ MCU กระจายหลายตัวแทนคอมพิวเตอร์ใหญ่ตัวเดียวคือข้อใด',
  ['แต่ละระบบ (เครื่องยนต์ เบรก ถุงลม กระจก) ต้องการการควบคุมเฉพาะทางที่ตอบสนองเร็วและแยกความเสี่ยงกันได้',
   'เพราะ MCU ตัวเดียวราคาแพงกว่าคอมพิวเตอร์ใหญ่',
   'เพราะกฎหมายห้ามใช้คอมพิวเตอร์ในรถยนต์',
   'เพราะ MCU ทุกตัวต้องทำงานเหมือนกัน'],
  'การกระจายงานให้ MCU เฉพาะทางทำให้ระบบตอบสนองแบบเวลาจริง และถ้าระบบหนึ่งขัดข้องจะไม่ลากระบบอื่นล่มตามไปด้วย'),
]
B['district2'] = [
 ('หน่วยความจำส่วนใดใน MCU ทำหน้าที่เก็บ "โปรแกรม" ที่อัปโหลดลงไป และไม่หายเมื่อปิดไฟ',
  ['Flash', 'SRAM', 'รีจิสเตอร์ชั่วคราวของ ADC', 'แคชของ Wi-Fi'],
  'Flash เป็นหน่วยความจำไม่ลบเลือน (non-volatile) ใช้เก็บโค้ดโปรแกรม ส่วน SRAM ใช้เก็บตัวแปรขณะทำงานและหายเมื่อปิดไฟ'),
 ('ตัวแปร int count ที่เพิ่มค่าขึ้นเรื่อย ๆ ใน loop() ถูกเก็บไว้ที่หน่วยความจำใด และจะเกิดอะไรขึ้นเมื่อถอดไฟ',
  ['เก็บใน SRAM และค่าจะหายเมื่อถอดไฟ เปิดใหม่จะเริ่มจากค่าตั้งต้น',
   'เก็บใน Flash และค่าจะคงอยู่ตลอดไป',
   'เก็บใน EEPROM อัตโนมัติทุกครั้ง',
   'เก็บในเซนเซอร์'],
  'ตัวแปรทั่วไปอยู่ใน SRAM ซึ่งลบเลือน หากต้องการจำค่าข้ามการปิดเครื่อง ต้องสั่งบันทึกลง EEPROM/NVS เอง'),
 ('ระบบ Smart AC ต้องจำอุณหภูมิที่ผู้ใช้ตั้งไว้ แม้ไฟดับแล้วไฟมาใหม่ ควรเก็บค่านี้ที่ใด',
  ['EEPROM หรือ NVS (Preferences) ซึ่งไม่ลบเลือน',
   'ตัวแปรธรรมดาใน SRAM',
   'รีจิสเตอร์ของ Timer',
   'บัฟเฟอร์ของ Serial Monitor'],
  'ค่าตั้งค่าที่ต้องอยู่รอดหลังไฟดับต้องเก็บในหน่วยความจำไม่ลบเลือน บน ESP32 นิยมใช้ไลบรารี Preferences ที่เก็บใน NVS'),
 ('Arduino Uno มี ADC ความละเอียด 10 บิต แรงดันอ้างอิง 5.0 V ถ้าขาอนาล็อกได้รับแรงดัน 2.5 V ค่า analogRead() จะประมาณเท่าใด',
  ['ประมาณ 512', 'ประมาณ 2500', 'ประมาณ 4095', 'ประมาณ 25'],
  '10 บิตมีค่า 0–1023 คำนวณ 2.5/5.0 × 1023 ≈ 511.5 จึงได้ประมาณ 511–512'),
 ('ESP32 มี ADC 12 บิต ช่วงค่าดิจิทัลที่อ่านได้คือข้อใด',
  ['0 ถึง 4095', '0 ถึง 1023', '0 ถึง 255', '0 ถึง 65535'],
  'ความละเอียด n บิตให้ค่า 0 ถึง 2^n − 1 ดังนั้น 12 บิตคือ 0–4095'),
 ('ESP32 (ADC 12 บิต ช่วงราว 0–3.3 V) อ่านค่าได้ 2048 แรงดันที่ขาอินพุตโดยประมาณคือเท่าใด',
  ['ประมาณ 1.65 V', 'ประมาณ 3.3 V', 'ประมาณ 2.5 V', 'ประมาณ 0.5 V'],
  '2048/4095 × 3.3 ≈ 1.65 V (ในทางปฏิบัติ ADC ของ ESP32 ไม่เป็นเชิงเส้นสมบูรณ์ ควรใช้ analogReadMilliVolts() ที่มีการชดเชยค่า)'),
 ('ส่วนประกอบใดใน MCU ใช้สร้างสัญญาณ PWM เพื่อหรี่ไฟ LED หรือปรับความเร็วพัดลม DC',
  ['Timer/PWM', 'ADC', 'EEPROM', 'Watchdog'],
  'PWM สร้างจาก Timer ฮาร์ดแวร์ที่สลับขา HIGH/LOW ด้วยสัดส่วนเวลา (duty cycle) ที่กำหนด ทำให้กำลังเฉลี่ยที่โหลดได้รับเปลี่ยนไป'),
 ('หน้าที่ของ Watchdog Timer คือข้อใด',
  ['รีเซ็ต MCU อัตโนมัติเมื่อโปรแกรมค้างจนไม่ได้รีเซ็ตตัวจับเวลาตามกำหนด',
   'แปลงแรงดันแอนะล็อกเป็นดิจิทัล',
   'เก็บโปรแกรมถาวร',
   'เพิ่มความเร็ว CPU'],
  'Watchdog ช่วยให้อุปกรณ์ที่ไม่มีคนเฝ้า เช่น ระบบเฝ้าห้อง Server ฟื้นตัวเองได้เมื่อซอฟต์แวร์ค้าง'),
 ('MCU ที่ทำงานด้วยสัญญาณนาฬิกา 16 MHz หนึ่งรอบสัญญาณนาฬิกามีคาบเวลาเท่าใด',
  ['62.5 ns', '16 µs', '1.6 ms', '0.16 s'],
  'คาบ T = 1/f = 1/16,000,000 วินาที = 62.5 นาโนวินาที'),
 ('Arduino Uno มี SRAM เพียง 2 KB การกระทำใดเสี่ยงทำให้หน่วยความจำไม่พอที่สุด',
  ['ประกาศอาร์เรย์ float ขนาด 1000 ช่องเพื่อเก็บข้อมูลย้อนหลัง',
   'ประกาศตัวแปร int หนึ่งตัว',
   'ใช้ digitalWrite() สั่ง LED',
   'อ่านค่า analogRead() หนึ่งครั้ง'],
  'float ใช้ 4 ไบต์ 1000 ช่องจึงใช้ราว 4000 ไบต์ เกิน 2 KB ทันที งานเก็บข้อมูลจำนวนมากควรใช้บอร์ดที่มี RAM มากกว่า หรือส่งข้อมูลขึ้นคลาวด์'),
 ('ถ้าเพิ่มความละเอียด ADC จาก 10 บิตเป็น 12 บิต ที่แรงดันอ้างอิงเท่าเดิม ผลที่ได้คือข้อใด',
  ['แบ่งช่วงแรงดันละเอียดขึ้น 4 เท่า ค่าต่อหนึ่งขั้นเล็กลง',
   'แรงดันที่วัดได้สูงสุดเพิ่มขึ้น 4 เท่า',
   'วัดค่าได้หยาบลง',
   'ไม่มีผลใด ๆ'],
  '10 บิตมี 1024 ระดับ 12 บิตมี 4096 ระดับ จึงแยกความต่างของแรงดันได้ละเอียดขึ้น 4 เท่า แต่ช่วงแรงดันสูงสุดยังเท่าเดิม'),
 ('อุปกรณ์รอบข้าง (peripheral) ใดของ MCU ใช้คุยกับจอ OLED หรือเซนเซอร์ BMP280 ด้วยสายสัญญาณเพียง 2 เส้น',
  ['I2C (SDA และ SCL)', 'UART (TX และ RX) แบบหนึ่งต่อหลาย', 'ADC', 'EEPROM'],
  'I2C ใช้สาย SDA (ข้อมูล) และ SCL (สัญญาณนาฬิกา) ต่ออุปกรณ์หลายตัวบนบัสเดียวกันได้โดยแยกด้วยแอดเดรส'),
]
B['district1'] += [
 ('คลิป "The Brain Behind Everything" สรุปเหตุผลที่ MCU ถูกใช้ในอุปกรณ์รอบตัว ข้อใดครบถ้วนที่สุด',
  ['ราคาถูก ประหยัดพลังงาน เปิดแล้วทำงานทันที ควบคุมฮาร์ดแวร์ได้โดยตรง และเชื่อถือได้ในระยะยาว',
   'แสดงกราฟิกสามมิติได้ดี รันเกมได้ลื่น และมีพัดลมระบายความร้อน',
   'มี RAM หลายกิกะไบต์และฮาร์ดดิสก์ในตัว',
   'ต้องเชื่อมต่ออินเทอร์เน็ตตลอดเวลาจึงจะทำงานได้'],
  'ห้าเหตุผลนี้อธิบายว่าทำไมเครื่องใช้ไฟฟ้า ของเล่น รถยนต์ และเครื่องจักรจำนวนมหาศาลจึงเลือก MCU แทนคอมพิวเตอร์ทั่วไป'),
 ('บอร์ดใดต่อไปนี้ "ไม่ใช่" บอร์ดไมโครคอนโทรลเลอร์',
  ['Raspberry Pi 4 ที่รันระบบปฏิบัติการ Linux', 'Arduino Uno', 'ESP32 DevKit', 'Raspberry Pi Pico (RP2040)'],
  'Raspberry Pi Pico ใช้ชิป RP2040 ซึ่งเป็น MCU แม้ชื่อจะคล้าย Raspberry Pi 4 ที่เป็นคอมพิวเตอร์บอร์ดเดี่ยวแบบ MPU'),
 ('ข้อใดเรียงลำดับ "Sensor → Decision → Action" ของถังขยะอัจฉริยะได้ถูกต้อง',
  ['อัลตราโซนิกวัดระดับขยะ → MCU ตัดสินว่าเกิน 80% หรือไม่ → ส่งแจ้งเตือนและเปิดไฟสถานะสีแดง',
   'ส่งแจ้งเตือน → วัดระดับขยะ → ตัดสินใจ',
   'MCU ตัดสินใจ → วัดระดับขยะ → ไม่ต้องสั่งงานใด',
   'เปิดไฟสถานะ → ปิดไฟสถานะ → วัดระดับขยะ'],
  'ทุกโปรเจกต์ในเทอมนี้เขียนได้ด้วยแบบแผนเดียวกัน: เซนเซอร์อ่านโลกจริง MCU ตัดสินใจ แล้ว Actuator ลงมือ'),
]

B['district3'] = [
 ('ในโปรแกรม Arduino ฟังก์ชัน setup() และ loop() ทำงานอย่างไร',
  ['setup() ทำงานครั้งเดียวตอนเริ่ม จากนั้น loop() วนซ้ำไปเรื่อย ๆ ไม่สิ้นสุด',
   'loop() ทำงานครั้งเดียว แล้ว setup() วนซ้ำ',
   'ทั้งสองฟังก์ชันทำงานพร้อมกันตลอดเวลา',
   'loop() ทำงาน 10 รอบแล้วโปรแกรมจบ'],
  'นี่คือโครงสร้าง Super Loop พื้นฐานของระบบฝังตัว โปรแกรมไม่มีวันจบตราบใดที่ยังจ่ายไฟ'),
 ('พิจารณาโปรแกรมต่อไปนี้ ' + code('int n = 0;\n\nvoid setup() {\n  Serial.begin(115200);\n  n = 5;\n}\n\nvoid loop() {\n  n = n + 1;\n  Serial.println(n);\n  delay(1000);\n}') + 'ค่าแรกที่พิมพ์ออกทาง Serial Monitor คือเท่าใด',
  ['6', '5', '1', '0'],
  'setup() กำหนด n = 5 หนึ่งครั้ง จากนั้น loop() รอบแรกเพิ่มเป็น 6 แล้วพิมพ์ 6 รอบถัดไปพิมพ์ 7, 8, ... ทุก 1 วินาที'),
 ('ลำดับการทำงานของระบบควบคุมอัตโนมัติแบบพื้นฐานคือข้อใด',
  ['Input → Process → Output', 'Output → Input → Process', 'Process → Output → Input', 'Input → Output โดยไม่ต้องประมวลผล'],
  'อ่านค่าจากเซนเซอร์ (Input) ตัดสินใจหรือคำนวณ (Process) แล้วสั่งอุปกรณ์หรือแจ้งเตือน (Output) วนซ้ำต่อเนื่อง'),
 ('ระบบตรวจควันไฟใช้ delay(10000) ใน loop() เพื่อ "ประหยัดการอ่านค่า" ผลเสียที่สำคัญที่สุดคือข้อใด',
  ['ระหว่างหน่วงเวลา MCU ไม่ทำอะไรเลย หากเกิดควันหรือมีคนกดปุ่มปิดเสียงเตือน ระบบอาจตอบสนองช้าถึง 10 วินาที',
   'เซนเซอร์ควันจะเสียทันที',
   'MCU จะประหยัดไฟลงจนเหลือศูนย์',
   'ไม่มีผลเสีย เป็นวิธีที่ดีที่สุด'],
  'delay() เป็นการหยุดรอแบบ blocking สำหรับระบบความปลอดภัยควรใช้ millis() ตรวจเวลาแบบไม่หยุดรอ หรือใช้ interrupt กับเหตุการณ์เร่งด่วน'),
 ('เซนเซอร์วัดการไหลของน้ำส่งพัลส์สั้น ๆ หลายร้อยครั้งต่อวินาที วิธีนับพัลส์ที่เหมาะสมที่สุดคือข้อใด',
  ['ใช้ Interrupt (attachInterrupt) ให้ฮาร์ดแวร์เรียกฟังก์ชันนับทุกครั้งที่มีขอบสัญญาณ',
   'ใช้ delay(1000) แล้วอ่าน digitalRead() หนึ่งครั้ง',
   'ใช้ analogRead() ทุก 5 วินาที',
   'ไม่ต้องนับ ให้เดาจากเวลา'],
  'เหตุการณ์ที่เกิดเร็วและสั้นมากเสี่ยงหลุดหากใช้ polling ช้า ๆ Interrupt ทำให้ MCU ตอบสนองทันทีที่เกิดขอบสัญญาณ'),
 ('ข้อใดคือความแตกต่างระหว่าง Polling และ Interrupt',
  ['Polling คือโปรแกรมวนถามสถานะเอง ส่วน Interrupt คือฮาร์ดแวร์ขัดจังหวะ CPU ทันทีเมื่อเกิดเหตุการณ์',
   'Polling ใช้ได้เฉพาะ ESP32 ส่วน Interrupt ใช้ได้เฉพาะ Uno',
   'ทั้งสองคำมีความหมายเหมือนกัน',
   'Interrupt คือการหน่วงเวลาด้วย delay()'],
  'Polling เข้าใจง่ายแต่เปลือง CPU และอาจพลาดเหตุการณ์สั้น ๆ ส่วน Interrupt ตอบสนองเร็วแต่ต้องเขียนฟังก์ชันให้สั้นและปลอดภัย'),
 ('พิจารณาโปรแกรมต่อไปนี้ ' + code('unsigned long last = 0;\n\nvoid loop() {\n  if (millis() - last >= 2000) {\n    last = millis();\n    readSensor();\n  }\n  checkButton();\n}') + 'ข้อใดอธิบายพฤติกรรมของโปรแกรมได้ถูกต้อง',
  ['อ่านเซนเซอร์ทุก ๆ ราว 2 วินาที และตรวจปุ่มทุกรอบของ loop() โดยไม่ต้องหยุดรอ',
   'อ่านเซนเซอร์เพียงครั้งเดียวแล้วหยุด',
   'หยุดรอ 2 วินาทีทุกรอบแบบเดียวกับ delay(2000)',
   'ตรวจปุ่มได้เพียงทุก 2 วินาที'],
  'รูปแบบ millis() - last >= interval คือการตั้งเวลาแบบไม่หยุดรอ (non-blocking) ทำให้งานอื่นเช่นตรวจปุ่มยังทำงานได้ตลอด'),
 ('อุปกรณ์เฝ้าระวังห้อง Server ต้องทำงานเอง 24 ชั่วโมงโดยไม่มีคนกดรีเซ็ต วิธีใดช่วยให้ระบบฟื้นตัวเองเมื่อโปรแกรมค้าง',
  ['เปิดใช้ Watchdog Timer และป้อน (reset) ตัวจับเวลาในลูปหลักอย่างสม่ำเสมอ',
   'ใส่ delay() ยาว ๆ เพื่อให้ CPU พัก',
   'ถอดสาย USB ออก',
   'ลดความละเอียด ADC'],
  'เมื่อโปรแกรมค้างจนไม่ได้ป้อน Watchdog ชิปจะรีเซ็ตตัวเองและเริ่มทำงานใหม่ เป็นแนวปฏิบัติมาตรฐานของระบบที่ไม่มีคนดูแล'),
 ('สถานีวัดฝุ่นใช้แบตเตอรี่ ต้องการส่งค่าทุก 10 นาที แนวทางใดยืดอายุแบตเตอรี่ได้มากที่สุด',
  ['ตื่นขึ้นมาอ่านค่าและส่งข้อมูล แล้วเข้า Deep Sleep จนถึงรอบถัดไป',
   'เปิด Wi-Fi ค้างไว้และวน loop() ตลอดเวลา',
   'เพิ่ม delay(600000) ใน loop() โดยไม่ปิด Wi-Fi',
   'เพิ่มความถี่สัญญาณนาฬิกาให้สูงสุด'],
  'delay() ไม่ได้ทำให้ชิปประหยัดไฟมากนักเพราะ CPU และ Wi-Fi ยังทำงาน Deep Sleep ปิดเกือบทุกส่วนทำให้กินไฟลดลงหลายเท่าตัว'),
 ('พิจารณาโปรแกรมต่อไปนี้ ' + code('void loop() {\n  float t = readTemp();\n  if (t > 30.0) {\n    digitalWrite(FAN, HIGH);\n  } else {\n    digitalWrite(FAN, LOW);\n  }\n}') + 'ถ้าอุณหภูมิอยู่ที่ 30.0 °C พอดี พัดลมจะเป็นอย่างไร',
  ['ปิด เพราะ 30.0 > 30.0 เป็นเท็จ จึงเข้า else',
   'เปิด เพราะถึงเกณฑ์แล้ว',
   'เปิดสลับปิดทุกรอบ',
   'โปรแกรมหยุดทำงาน'],
  'เครื่องหมาย > ไม่รวมค่าที่เท่ากัน ค่าขอบเป็นจุดที่ต้องระบุให้ชัดในข้อกำหนดของระบบเสมอ'),
 ('ปุ่มกดเชิงกลมักเกิดสัญญาณกระเด้ง (bounce) หลายครั้งในเสี้ยววินาที ผลที่อาจเกิดกับโปรแกรมนับจำนวนครั้งที่กดคือข้อใด',
  ['นับเกินจริง เพราะการกดหนึ่งครั้งถูกอ่านเป็นหลายครั้ง จึงต้องทำ debounce',
   'นับขาดเสมอ',
   'ทำให้ ADC เสีย',
   'ไม่มีผล เพราะปุ่มเป็นดิจิทัล'],
  'หน้าสัมผัสโลหะสั่นช่วงสั้น ๆ ก่อนนิ่ง วิธีแก้คือ debounce ด้วยซอฟต์แวร์ (รอให้สถานะนิ่งราว 20–50 ms) หรือใช้วงจร RC'),
 ('เหตุใดฟังก์ชันที่ถูกเรียกจาก Interrupt (ISR) ควรเขียนให้สั้นที่สุด',
  ['เพราะระหว่างทำ ISR งานหลักและ interrupt อื่นอาจถูกพักไว้ ถ้ายาวเกินไปจะทำให้ระบบหน่วงหรือพลาดเหตุการณ์',
   'เพราะ ISR ใช้ได้เพียง 1 บรรทัดตามกฎภาษา C',
   'เพราะ ISR ทำงานบน Flash เท่านั้น',
   'เพราะ ISR จะลบตัวแปรทั้งหมด'],
  'แนวปฏิบัติคือใน ISR ให้แค่ตั้งธงหรือเพิ่มตัวนับ (ตัวแปรแบบ volatile) แล้วไปประมวลผลต่อใน loop() ห้ามใช้ delay() หรือ Serial.print() ยาว ๆ ใน ISR'),
]

STAR = star_table([
 ('CORE ARCHITECT', 'เข้าใจสมองกลฝังตัวครบทุกมิติ พร้อมไปด่าน PIN WARS เพื่อลงลึกขา ESP32'),
 ('CHIP WHISPERER', 'แม่นยำสูง เหลืออีกจุดเดียวก็เต็ม ย้อนอ่านคำอธิบายข้อที่พลาด'),
 ('SIGNAL TRACER', 'ผ่านเกณฑ์ความเข้าใจพื้นฐาน ลองเล่นห้องทดลอง ADC และ Loop อีกรอบ'),
 ('CIRCUIT CADET', 'เริ่มจับหลักได้ ควรทบทวนตาราง MCU กับ MPU และหน้าที่ของหน่วยความจำ'),
 ('BOOTLOADER', 'พอมีพื้นฐาน แนะนำให้เล่นห้องทดลองให้ครบทั้ง 3 ห้องก่อนสอบใหม่'),
 ('POWER-ON RESET', 'ยังไม่คุ้นเนื้อหา ไม่เป็นไร เริ่มจากห้องสแกนสมองแล้วค่อย ๆ ไล่ไปทีละห้อง'),
])

BADGES = r"""[
  {id:'perfect',  name:'NEURAL MASTER',   desc:'Posttest ถูกครบ 6 ข้อ',                  test:s => s.post === 6},
  {id:'zero2hero',name:'BRAIN UPGRADE',   desc:'คะแนนเพิ่มขึ้น 3 ข้อขึ้นไปจาก Pretest',     test:s => (s.post - s.pre) >= 3},
  {id:'fast',     name:'LOW LATENCY',     desc:'ตอบถูกภายใน 8 วินาที',                   test:s => s.fastCorrect},
  {id:'labrat',   name:'LAB ENGINEER',    desc:'เล่นห้องทดลองครบทั้งสามห้อง',             test:s => s.labs.lab1.length >= 6 && s.labs.lab2.length >= 8 && s.labs.lab3.length >= 4},
  {id:'combo',    name:'ZERO JITTER',     desc:'ตอบถูกติดกัน 5 ข้อขึ้นไป',               test:s => s.maxCombo >= 5},
  {id:'sweep',    name:'TRIPLE SECTOR',   desc:'ได้ 2/2 ครบทั้งสามห้อง',                 test:s => s.postByD.district1 === 2 && s.postByD.district2 === 2 && s.postByD.district3 === 2}
]"""

ADVICE = r"""
  const tips=[];
  if(labCount('lab1')<6) tips.push('ยังคัดแยกอุปกรณ์ไม่ครบในห้องสแกนสมอง ลองตั้งคำถามกับตัวเองว่า "ต้องรัน OS หรือไม่" และ "ต้องประหยัดไฟแค่ไหน"');
  if(labCount('lab2')<8) tips.push('เปิดบล็อกในชิปให้ครบ และลองสลับบอร์ด Uno กับ ESP32 ในเครื่องแปลง ADC สังเกตว่าเกิน 3.3 V กับ ESP32 แล้วเกิดอะไรขึ้น');
  if(labCount('lab3')<4) tips.push('ลองจำลองลูปทั้งแบบ delay() และ millis() เพื่อเห็นด้วยตาว่าทำไมระบบจริงไม่ควรใช้ delay() ยาว ๆ');
  if(postInfo.stars===6) tips.push('ได้ครบ 6 ดาวแล้ว ขั้นต่อไปคือเขียนโค้ดโปรเจกต์กลุ่มให้ใช้ millis() แทน delay() ทั้งหมด');
  return tips;
"""

CFG = {
    'filename': 'game1_brain_core.html',
    'title': 'BRAIN CORE : ถอดรหัสสมองกลฝังตัว',
    'brand': 'BRAIN CORE',
    'edition': 'NEURAL LAB EDITION',
    'desc': 'เกมทบทวนไมโครคอนโทรลเลอร์ MCU กับ MPU หน่วยความจำ ADC และโครงสร้าง setup/loop — CPE2422/2428 · ผศ.ดร.กุลวลัญช์ วรุณสิน มหาวิทยาลัยรามคำแหง',
    'ogdesc': 'สแกน เอกซเรย์ และจำลองสมองกลใน 3 ห้องทดลอง วัดผลก่อน-หลังเรียนด้วยระบบดาว 6 ดวง',
    'favicon': "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%23030e16'/><rect x='26' y='26' width='48' height='48' rx='8' fill='none' stroke='%2322d3ee' stroke-width='8'/><rect x='40' y='40' width='20' height='20' fill='%23a3e635'/></svg>",
    'theme': THEME,
    'extra_css': EXTRA_CSS,
    'arcade_label': 'ด่านไต่แกนสมองกล',
    'hero_svg': HERO,
    'subtitle': 'สวมบทบาท <b>วิศวกรสมองกล</b> เจาะเข้า 3 ห้องทดลองของชิป ตั้งแต่สแกนว่าอุปกรณ์ใดใช้ MCU หรือ MPU เอกซเรย์อวัยวะในชิปพร้อมคำนวณ ADC จนถึงจำลองลูปนิรันดร์ของโปรแกรมฝังตัว สะสม XP และดาว วัดพัฒนาการก่อน–หลังเรียน',
    'login_tag': 'Engineer Registration',
    'features': '<span>CPE2422 · คลิปทบทวนที่ 1</span><span>MCU · MEMORY · ADC · LOOP</span><span>PRETEST / POSTTEST</span><span>ระบบดาว 6 ดวง</span><span>XP &amp; COMBO</span><span>ส่งออกคะแนน CSV</span>',
    'climb_text': 'ตัวละครไต่แกนสมองกลขึ้น 1 ชั้น ทันที',
    'zones_html': ZONES,
    'checks': [('Sector 01', 'ห้องสแกนสมอง'), ('Sector 02', 'ห้องเอกซเรย์ชิป'), ('Sector 03', 'ห้องลูปนิรันดร์')],
    'post_desc': '6 ข้อใหม่ (ห้องละ 2 ข้อ) เพื่อวัดความเข้าใจหลังผ่านครบทั้ง 3 ห้องของแกนสมองกล',
    'report_tag': 'Neural Lab Report',
    'course': COURSE.split(' · ')[0],
    'footer_line': 'เกมทบทวนคลิปที่ 1: The Brain Behind Everything — ภาคเรียนที่ 1/2569',
    'bank': bank_js(B),
    'skill_labels': "{district1:'MCU กับ MPU', district2:'อวัยวะในชิป & ADC', district3:'setup/loop & การจับเวลา'}",
    'skey': 'cpe_braincore_v1_state',
    'star_table': STAR,
    'navstops': navstops('S1 SCAN', 'S2 X-RAY', 'S3 LOOP'),
    'lock_msg': 'ห้องนี้ยังไม่ปลดล็อก ทำตามลำดับก่อนนะครับ',
    'act': {'floor': 'ชั้น', 'top': 'แกนสมองกลสูงสุด', 'ground': 'ฐานชิป', 'theme': 'circuit'},
    'pre_sub': 'นี่คือเส้นฐานของคุณ — เดี๋ยวเรามาวัดกันใหม่หลังผ่านครบทั้ง 3 ห้อง',
    'go_first': 'เข้าห้องแรก',
    'lab_js': LAB_JS,
    'lab_wiring': LAB_WIRING,
    'init_extra': INIT_EXTRA,
    'badges': BADGES,
    'advice_js': ADVICE,
    'role': 'วิศวกรสมองกล',
    'filekey': 'CPE2422_G1_braincore',
    'avatars': avatars('#082230', ['#22d3ee', '#a3e635', '#facc15', '#f43f5e', '#67e8f9', '#fef08a']),
}
