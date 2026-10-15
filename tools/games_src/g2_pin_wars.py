# -*- coding: utf-8 -*-
"""GAME 2 — PIN WARS : สังเวียนขา ESP32
อ้างอิงคลิปทบทวนที่ 2: ESP32 Explained — The Complete Beginner's Guide to GPIO, Pins & More
ข้อเท็จจริงอ้างอิง ESP32-WROOM-32 / DevKit V1 (ESP32 รุ่นดั้งเดิม)"""
from cpe_common import *

THEME = {
    "PRIMARY_RGB": "255,122,48",  "PRIMARY_HEX": "#ff7a30",
    "SECOND_RGB":  "56,189,248",  "SECOND_HEX":  "#38bdf8",
    "GOLD_RGB":    "251,191,36",  "GOLD_HEX":    "#fbbf24",
    "GOLD2_RGB":   "253,224,71",  "GOLD2_HEX":   "#fde047",
    "RED_RGB":     "239,68,68",   "RED_HEX":     "#ef4444",
    "BG_RGB":      "17,9,6",      "BG_HEX":      "#110906",
    "PANEL_RGB":   "40,22,14",
    "PANEL2_RGB":  "54,30,18",
    "BG2_HEX":     "#1a0e08",
    "INK_HEX":     "#24130b",
    "TEXT_HEX":    "#fbefe7",
    "MUTED_HEX":   "#c9a593",
    "MUTED2_HEX":  "#8f6b59",
    "MUTED3_HEX":  "#7a5a4a",
    "SECOND2_HEX": "#7dd3fc",
    "PRIM2_HEX":   "#ffa26b",
    "LIGHT_EMBER": "#c2410c", "LIGHT_CORNER": "#0369a1", "LIGHT_GOLD": "#a16207",
    "LIGHT_GOLD2": "#854d0e", "LIGHT_RED": "#b91c1c",
}

EXTRA_CSS = LAB_CSS + """
.pinboard{display:grid;grid-template-columns:repeat(auto-fill,minmax(74px,1fr));gap:6px;margin:12px 0}
.pinboard .pick{text-align:center;font-family:var(--mono);font-size:.78rem;padding:9px 4px}
.pinboard .pick small{font-size:.62rem}
.pinboard .pick.v-safe{border-bottom:3px solid var(--corner)}
.pinboard .pick.v-warn{border-bottom:3px solid var(--gold)}
.pinboard .pick.v-no{border-bottom:3px solid var(--red)}
.pinboard .pick.v-in{border-bottom:3px solid var(--ember)}
.legend{display:flex;gap:12px;flex-wrap:wrap;font-size:.76rem;color:var(--muted)}
.legend i{display:inline-block;width:12px;height:4px;border-radius:2px;margin-right:5px;vertical-align:middle}
"""

HERO = """<svg class="cityart" viewBox="0 0 480 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ภาพบอร์ด ESP32 กลางสังเวียน">
  <defs>
    <radialGradient id="gSpot" cx="50%" cy="45%" r="60%"><stop offset="0%" stop-color="rgba(255,122,48,.40)"/><stop offset="100%" stop-color="rgba(255,122,48,0)"/></radialGradient>
    <filter id="fGlow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x="0" y="0" width="480" height="300" rx="18" fill="#110906"/>
  <circle cx="240" cy="135" r="150" fill="url(#gSpot)"/>
  <path d="M60 40 L200 120 M420 40 L280 120" stroke="#fbbf24" stroke-width="2" opacity=".35"/>
  <rect x="150" y="70" width="180" height="140" rx="10" fill="#24130b" stroke="#ff7a30" stroke-width="3" filter="url(#fGlow)"/>
  <rect x="200" y="84" width="80" height="60" rx="4" fill="#3a2418" stroke="#c9a593" stroke-width="1.5"/>
  <text x="240" y="112" text-anchor="middle" font-size="13" font-weight="700" fill="#fbefe7" font-family="monospace">ESP32</text>
  <text x="240" y="128" text-anchor="middle" font-size="8" fill="#c9a593" font-family="monospace">WROOM-32</text>
  <path d="M212 84 v-10 h12 v10 M232 84 v-10 h12 v10 M252 84 v-10 h12 v10" fill="none" stroke="#38bdf8" stroke-width="2"/>
  <g fill="#fbbf24">
    <circle cx="164" cy="90" r="4"/><circle cx="164" cy="108" r="4"/><circle cx="164" cy="126" r="4"/><circle cx="164" cy="144" r="4"/><circle cx="164" cy="162" r="4"/><circle cx="164" cy="180" r="4"/><circle cx="164" cy="198" r="4"/>
    <circle cx="316" cy="90" r="4"/><circle cx="316" cy="108" r="4"/><circle cx="316" cy="126" r="4"/><circle cx="316" cy="144" r="4"/><circle cx="316" cy="162" r="4"/><circle cx="316" cy="180" r="4"/><circle cx="316" cy="198" r="4"/>
  </g>
  <circle cx="316" cy="126" r="7" fill="none" stroke="#ef4444" stroke-width="2"/><circle cx="164" cy="162" r="7" fill="none" stroke="#38bdf8" stroke-width="2"/>
  <text x="96" y="130" text-anchor="middle" font-size="11" font-weight="700" fill="#38bdf8" font-family="monospace">3.3V</text>
  <text x="384" y="130" text-anchor="middle" font-size="11" font-weight="700" fill="#ef4444" font-family="monospace">NO 5V!</text>
  <text x="240" y="192" text-anchor="middle" font-size="10" fill="#ff7a30" font-family="monospace">GPIO · ADC · PWM · I2C · SPI · UART</text>
  <text x="240" y="284" text-anchor="middle" font-size="10" letter-spacing="3" fill="#c9a593">PICK THE RIGHT PIN · OR LOSE THE ROUND</text>
</svg>"""

ZONES = """
<!-- ===== PREVIEW 1 ===== -->
<section id="scr-preview1" class="screen">
  <div class="panel">
    <span class="tag">Before Round 01</span>
    <h2>กำลังจะเข้าสู่: ยกที่ 1 ขาไหนปลอดภัย (Safe Pin Round)</h2>
    <div class="dcard">
      <div class="ico"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <rect x="18" y="12" width="44" height="56" rx="6" fill="none" stroke="#ff7a30" stroke-width="3"/>
        <circle cx="30" cy="28" r="5" fill="#38bdf8"/><circle cx="30" cy="44" r="5" fill="#fbbf24"/><circle cx="50" cy="36" r="5" fill="#ef4444"/></svg></div>
      <div><div class="skillcard" style="margin:0">
        <div class="sk-name">ทักษะที่จะได้: กฎความปลอดภัยของขา ESP32</div>
        <p class="muted" style="margin:6px 0 0">ลอจิก 3.3 V, กระแสต่อขา, ขาที่ห้ามใช้ (Flash), ขาอินพุตอย่างเดียว และขา Strapping ที่ทำให้บอร์ดบูตไม่ขึ้น</p>
      </div></div>
    </div>
    <div class="btn-row"><button class="btn primary" data-goto="scr-lesson1">ขึ้นสังเวียน</button></div>
  </div>
</section>

<!-- ===== ROUND 1 ===== -->
<section id="scr-lesson1" class="screen">
  <div class="panel">
    <span class="tag">Round 01 · Safe Pin Round</span>
    <h2>ยกที่ 1: ขาไหนปลอดภัย ขาไหนห้ามแตะ</h2>
    <p>ESP32 ทำงานที่ <b>ลอจิก 3.3 V</b> และ <b>ไม่ทนแรงดัน 5 V</b> ที่ขา GPIO ขาแต่ละขาจ่ายกระแสได้จำกัด ควรออกแบบไม่เกินราว
      <b>20 mA ต่อขา</b> (ค่าสูงสุดสัมบูรณ์ราว 40 mA) และไม่ใช่ทุกขาที่ใช้ได้อิสระ เพราะบางขาถูกจองไว้กับหน่วยความจำ Flash หรือมีบทบาทตอนบูต</p>
    <div class="tbl-wrap"><table>
      <tr><th colspan="2">กายวิภาคบอร์ด ESP32 DevKit (สรุปจากคลิป ESP32 Explained)</th></tr>
      <tr><td>ชิป → โมดูล → บอร์ดพัฒนา</td><td>ชิป ESP32 + Flash + เสาอากาศ PCB อยู่ในโมดูล (เช่น ESP32-WROOM-32) แล้ววางบนบอร์ดที่มีพอร์ต USB ปุ่ม และเรกูเลเตอร์</td></tr>
      <tr><td>ชิป USB-to-UART</td><td>CP2102, CH340, CH9102 ทำหน้าที่เดียวกัน คือแปลง USB เป็น UART เพื่ออัปโหลดโค้ด ถ้าคอมพิวเตอร์มองไม่เห็นพอร์ต มักต้องติดตั้งไดรเวอร์ให้ตรงชิป</td></tr>
      <tr><td>Flash / SRAM / PSRAM</td><td>Flash เก็บโปรแกรม ปิดไฟไม่หาย · SRAM ข้อมูลหายเมื่อปิดไฟ · บางบอร์ดมี PSRAM เพิ่มหน่วยความจำทำงานสำหรับกล้องหรือ AI</td></tr>
      <tr><td>ไฟเลี้ยง 3 ราง</td><td><b>5V</b> (จาก USB/VIN) · <b>3V3</b> (จากเรกูเลเตอร์) · <b>GND</b> (กราวด์ร่วมของทุกอุปกรณ์)</td></tr>
      <tr><td>Brownout Detector</td><td>เมื่อแรงดันตกต่ำกว่าเกณฑ์ ชิปจะรีเซ็ตตัวเองเพื่อป้องกันการทำงานผิดเพี้ยน สาเหตุรีเซ็ตที่พบบ่อยคือไฟไม่พอ Watchdog หมดเวลา หรือบั๊กซอฟต์แวร์</td></tr>
      <tr><td>GPIO Matrix</td><td>วงจรสลับสัญญาณภายในชิป ทำให้ย้าย UART, I2C, SPI และ PWM ไปใช้กับ GPIO <b>เกือบทุกขา</b>ได้ด้วยซอฟต์แวร์ เช่น <code>Wire.begin(25, 26)</code> ขา I2C/SPI ในผังจึงเป็นเพียง<b>ค่าเริ่มต้น</b> ยกเว้น GPIO34–39 ที่รับได้เฉพาะสัญญาณขาเข้า และ ADC, DAC, Touch ที่ผูกกับขาเฉพาะ</td></tr>
      <tr><td>LED บนบอร์ด</td><td>หลายบอร์ดต่อ LED ไว้ที่ GPIO2 แต่บางบอร์ดไม่มี LED ผู้ใช้ หรืออยู่ขาอื่น ต้องดูผังของบอร์ดตัวเอง</td></tr>
    </table></div>
    <div class="keyfact"><b>ขาแนะนำสำหรับมือใหม่ (จากคลิป):</b> GPIO4, 18, 19, 21, 22, 23, 25, 26, 33 · ต่อ LED ผ่านตัวต้านทานเสมอ: LED แดง (V<sub>f</sub> ≈ 2.0 V) ใช้ <b>220 Ω</b> ได้กระแสราว 6 mA หรือ <b>150 Ω</b> ได้ราว 8.7 mA · LED ฟ้า/ขาว (V<sub>f</sub> ≈ 3.0 V) ใช้ราว <b>47–68 Ω</b> คำนวณจาก R = (3.3 − V<sub>f</sub>) / I</div>
    <div class="tbl-wrap"><table>
      <tr><th>กลุ่มขา</th><th>ข้อควรระวัง</th></tr>
      <tr><td>GPIO6–11</td><td><b>ห้ามใช้</b> ต่อกับชิป SPI Flash ภายในโมดูล ใช้แล้วบอร์ดค้างหรือรีเซ็ต</td></tr>
      <tr><td>GPIO34, 35, 36 (VP), 39 (VN)</td><td><b>อินพุตอย่างเดียว</b> และไม่มีตัวต้านทาน pull-up/pull-down ภายใน เหมาะกับสัญญาณแอนะล็อก</td></tr>
      <tr><td>GPIO0, 2, 5, 12, 15</td><td>ขา <b>Strapping</b> สถานะตอนบูตกำหนดโหมดของชิป เช่น GPIO0 = LOW เข้าโหมดอัปโหลด, GPIO12 = HIGH ทำให้บูตไม่ขึ้น</td></tr>
      <tr><td>GPIO1 (TX0), GPIO3 (RX0)</td><td>ใช้กับการอัปโหลดโค้ดและ Serial Monitor ผ่าน USB</td></tr>
      <tr><td>GPIO4, 13, 16–19, 21–23, 25–27, 32, 33</td><td>ใช้งานทั่วไปได้สะดวกที่สุด (บนโมดูล WROVER ขา 16–17 ถูกใช้กับ PSRAM)</td></tr>
    </table></div>
    <div class="codebox">ตัวต้านทานจำกัดกระแส LED (LED แดง Vf ≈ 2.0 V, ต้องการ 10 mA)
R = (Vgpio − Vf) / I = (3.3 − 2.0) / 0.010 = 130 Ω  → เลือกค่ามาตรฐานที่สูงกว่า เช่น 150 Ω หรือ 220 Ω</div>

    <h3 style="margin-top:18px">ห้องทดลอง: ตรวจขาก่อนขึ้นสังเวียน (Pin Inspector)</h3>
    <p class="muted">แตะขาบนบอร์ดเพื่อตรวจสถานะ — ตรวจครบ 10 ขาขึ้นไปรับเหรียญตรา</p>
    <div class="legend"><span><i style="background:var(--corner)"></i>ใช้ได้สบาย</span><span><i style="background:var(--gold)"></i>ระวังตอนบูต/มีเงื่อนไข</span><span><i style="background:var(--ember)"></i>อินพุตอย่างเดียว</span><span><i style="background:var(--red)"></i>ห้ามใช้</span></div>
    <div class="pinboard" id="pinBoard"></div>
    <div class="status-line" id="pinStatus">ยังไม่ได้ตรวจขาใด</div>
    <div class="btn-row"><button class="btn primary" data-quiz="check1">ไปทำแบบฝึกหัดยกนี้</button></div>
  </div>
</section>

<!-- ===== PREVIEW 2 ===== -->
<section id="scr-preview2" class="screen">
  <div class="panel">
    <span class="tag">Before Round 02</span>
    <h2>กำลังจะเข้าสู่: ยกที่ 2 ดิจิทัลปะทะแอนะล็อก (Signal Clash)</h2>
    <div class="dcard">
      <div class="ico"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 56h14V24h14v32h14V24h14v32h8" fill="none" stroke="#ff7a30" stroke-width="3"/>
        <path d="M8 40c10-24 20 24 32 0s22 24 32 0" fill="none" stroke="#38bdf8" stroke-width="3"/></svg></div>
      <div><div class="skillcard" style="margin:0">
        <div class="sk-name">ทักษะที่จะได้: digitalRead/Write, INPUT_PULLUP, ADC 12 บิต, PWM</div>
        <p class="muted" style="margin:6px 0 0">อ่านปุ่มแบบลอจิกกลับด้าน เลือกขา ADC ให้ใช้ได้พร้อม Wi-Fi และคุมความสว่าง/ความเร็วด้วย PWM</p>
      </div></div>
    </div>
    <div class="btn-row"><button class="btn primary" data-goto="scr-lesson2">ขึ้นสังเวียน</button></div>
  </div>
</section>

<!-- ===== ROUND 2 ===== -->
<section id="scr-lesson2" class="screen">
  <div class="panel">
    <span class="tag">Round 02 · Signal Clash</span>
    <h2>ยกที่ 2: ดิจิทัลปะทะแอนะล็อก</h2>
    <p><b>ดิจิทัล</b> มีสองสถานะ HIGH/LOW ใช้กับปุ่ม สวิตช์ รีเลย์ ส่วน <b>แอนะล็อก</b> เป็นแรงดันต่อเนื่องที่ต้องผ่าน ADC 12 บิต (0–4095)
      กับดักที่เจอบ่อยที่สุดของ ESP32 คือ <b>ADC2 ใช้ไม่ได้ขณะ Wi-Fi ทำงาน</b> โปรเจกต์ IoT จึงควรต่อเซนเซอร์แอนะล็อกที่ขา <b>ADC1 (GPIO32–39)</b></p>
    <div class="codebox">pinMode(BTN, INPUT_PULLUP);        // ปุ่มต่อลง GND ไม่ต้องใส่ R ภายนอก
if (digitalRead(BTN) == LOW) {    // กด = LOW (ลอจิกกลับด้าน)
  digitalWrite(LED, HIGH);
}

int raw = analogRead(34);                 // ADC1 · 0–4095
int mv  = analogReadMilliVolts(34);       // ค่ามิลลิโวลต์ที่ชดเชยแล้ว

// PWM ความละเอียด 8 บิต: duty 0–255  → 64 ≈ 25%, 128 ≈ 50%, 255 = 100%</div>
    <div class="tbl-wrap"><table>
      <tr><th>ฟังก์ชันพิเศษ</th><th>ขา</th><th>หมายเหตุ</th></tr>
      <tr><td>ADC1</td><td>GPIO32–39</td><td>ใช้ได้เสมอ แม้เปิด Wi-Fi</td></tr>
      <tr><td>ADC2</td><td>GPIO0, 2, 4, 12–15, 25–27</td><td>ใช้ไม่ได้ขณะ Wi-Fi ทำงาน</td></tr>
      <tr><td>DAC 8 บิต</td><td>GPIO25, 26</td><td>ให้แรงดันแอนะล็อกจริง 0–255 ระดับ</td></tr>
      <tr><td>PWM (LEDC)</td><td>ขาเอาต์พุตเกือบทุกขา</td><td>16 ช่อง ตั้งความถี่และความละเอียดได้</td></tr>
      <tr><td>Touch</td><td>GPIO4, 0, 2, 15, 13, 12, 14, 27, 33, 32</td><td>สัมผัสแบบ capacitive ไม่ต้องมีปุ่มจริง</td></tr>
    </table></div>

    <h3 style="margin-top:18px">ห้องทดลอง: เครื่องวัดแอนะล็อกกับกับดัก Wi-Fi</h3>
    <p class="muted">เลือกขา เปิด/ปิด Wi-Fi แล้วเลื่อนแรงดัน — ทดลองครบ 5 แบบขึ้นไปรับเหรียญตรา</p>
    <div class="labrow">
      <button class="btn sm" data-apin="34">GPIO34 · ADC1</button>
      <button class="btn sm" data-apin="32">GPIO32 · ADC1</button>
      <button class="btn sm" data-apin="4">GPIO4 · ADC2</button>
      <button class="btn sm" data-apin="27">GPIO27 · ADC2</button>
      <button class="toggle off" id="wifiTgl">Wi-Fi: OFF</button>
    </div>
    <input type="range" class="rng" id="aVin" min="0" max="330" value="120" aria-label="แรงดันอินพุต">
    <div class="labrow"><span class="readout" id="aPinTxt">GPIO34</span><span class="readout" id="aV">1.20<small>V</small></span><span class="readout" id="aRaw">1489<small>/ 4095</small></span></div>
    <div class="meter"><i id="aBar"></i></div>
    <div class="status-line" id="aStatus">เลือกขาแล้วเลื่อนแรงดัน</div>
    <h3 style="margin-top:14px">ปุ่มแบบ INPUT_PULLUP</h3>
    <div class="labrow"><button class="btn sm" id="pullBtn">กดปุ่มค้างไว้ (แตะเพื่อสลับ)</button><span class="readout" id="pullRead">HIGH<small>ปล่อยปุ่ม</small></span></div>
    <div class="btn-row"><button class="btn primary" data-quiz="check2">ไปทำแบบฝึกหัดยกนี้</button></div>
  </div>
</section>

<!-- ===== PREVIEW 3 ===== -->
<section id="scr-preview3" class="screen">
  <div class="panel">
    <span class="tag">Before Round 03</span>
    <h2>กำลังจะเข้าสู่: ยกที่ 3 ศึกสายสื่อสาร (Bus Battle)</h2>
    <div class="dcard">
      <div class="ico"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 24h64M8 40h64M8 56h64" stroke="#38bdf8" stroke-width="3"/>
        <rect x="16" y="18" width="12" height="12" fill="#ff7a30"/><rect x="40" y="34" width="12" height="12" fill="#fbbf24"/><rect x="56" y="50" width="12" height="12" fill="#ff7a30"/></svg></div>
      <div><div class="skillcard" style="margin:0">
        <div class="sk-name">ทักษะที่จะได้: I2C, SPI, UART, 1-Wire และ Wi-Fi/BLE</div>
        <p class="muted" style="margin:6px 0 0">เลือกบัสให้ตรงกับโมดูล ต่อสายให้ถูก (TX ไขว้ RX, แอดเดรส I2C, ขา CS ของ SPI) และรู้ข้อจำกัดคลื่น 2.4 GHz</p>
      </div></div>
    </div>
    <div class="btn-row"><button class="btn primary" data-goto="scr-lesson3">ขึ้นสังเวียน</button></div>
  </div>
</section>

<!-- ===== ROUND 3 ===== -->
<section id="scr-lesson3" class="screen">
  <div class="panel">
    <span class="tag">Round 03 · Bus Battle</span>
    <h2>ยกที่ 3: ศึกสายสื่อสาร</h2>
    <p>เซนเซอร์และจอส่วนใหญ่ไม่ได้ส่งค่าเป็นแรงดันธรรมดา แต่คุยกับ ESP32 ผ่าน <b>โปรโตคอลอนุกรม</b> การเลือกบัสถูกตั้งแต่แรกช่วยให้เดินสายง่ายและไม่ชนขากัน</p>
    <div class="tbl-wrap"><table>
      <tr><th>บัส</th><th>สาย</th><th>จุดเด่น / กับดัก</th><th>ตัวอย่างโมดูล</th></tr>
      <tr><td>I2C</td><td>SDA (GPIO21), SCL (GPIO22)</td><td>หลายอุปกรณ์บน 2 เส้น แยกด้วย <b>แอดเดรส</b> ห้ามซ้ำกัน ต้องมี pull-up</td><td>OLED 0x3C, BMP280 0x76/0x77, MPU6050 0x68</td></tr>
      <tr><td>SPI</td><td>MOSI 23, MISO 19, SCK 18, CS 5</td><td>เร็วมาก แต่ทุกอุปกรณ์ต้องมีขา <b>CS</b> ของตัวเอง</td><td>การ์ด MicroSD, จอ TFT</td></tr>
      <tr><td>UART</td><td>TX, RX (ไขว้กัน)</td><td>ต่อแบบจุดต่อจุด <b>TX → RX</b> และ baud rate ต้องตรงกัน ควรใช้ UART2 (GPIO16/17) แทน UART0</td><td>PMS5003, GPS NEO-6M, เรดาร์ LD2410</td></tr>
      <tr><td>1-Wire</td><td>DATA เส้นเดียว + pull-up 4.7 kΩ</td><td>ต่อหลายตัวบนขาเดียว แต่ละตัวมีรหัส 64 บิตไม่ซ้ำกัน</td><td>DS18B20 วัดอุณหภูมิน้ำ</td></tr>
    </table></div>
    <div class="keyfact">Wi-Fi ของ ESP32 ใช้ได้เฉพาะคลื่น <b>2.4 GHz</b> ถ้าเราเตอร์หรือฮอตสปอตตั้งเป็น 5 GHz อย่างเดียว บอร์ดจะมองไม่เห็นเครือข่าย</div>

    <h3 style="margin-top:18px">ห้องทดลอง: จับคู่บัส (Bus Matchmaker)</h3>
    <p class="muted">แตะเลือกโมดูล แล้วเลือกบัสที่ถูกต้อง — จับคู่ถูก 6 โมดูลขึ้นไปรับเหรียญตรา</p>
    <div class="pickgrid" id="busGrid">
      <button class="pick" data-mod="oled">จอ OLED SSD1306<small>ขนาด 0.96 นิ้ว 4 ขา</small></button>
      <button class="pick" data-mod="bmp">BMP280<small>ความดันและอุณหภูมิ</small></button>
      <button class="pick" data-mod="pms">PMS5003<small>เซนเซอร์ฝุ่น PM2.5/PM10</small></button>
      <button class="pick" data-mod="sd">โมดูล MicroSD<small>บันทึกข้อมูลลงการ์ด</small></button>
      <button class="pick" data-mod="ds">DS18B20<small>หัววัดอุณหภูมิกันน้ำ</small></button>
      <button class="pick" data-mod="radar">LD2410<small>เรดาร์ตรวจจับคนนิ่ง</small></button>
      <button class="pick" data-mod="mpu">MPU6050<small>ความเร่งและไจโร</small></button>
      <button class="pick" data-mod="gps">GPS NEO-6M<small>พิกัดและเวลา</small></button>
    </div>
    <div class="labrow">
      <button class="btn sm" data-bus="i2c">I2C</button><button class="btn sm" data-bus="spi">SPI</button>
      <button class="btn sm" data-bus="uart">UART</button><button class="btn sm" data-bus="ow">1-Wire</button>
    </div>
    <div class="status-line" id="busStatus">เลือกโมดูลก่อน แล้วกดเลือกบัส</div>
    <div class="btn-row"><button class="btn primary" data-quiz="check3">ไปทำแบบฝึกหัดยกนี้</button></div>
  </div>
</section>
"""

LAB_JS = r"""
/* ---- LAB 1: Pin Inspector ---- */
const PINS=[
  ['0','warn','Strapping: ถ้าเป็น LOW ตอนบูตจะเข้าโหมดอัปโหลด (ปุ่ม BOOT) ใช้ได้แต่ห้ามต่ออุปกรณ์ที่ดึงลง LOW ตอนเปิดเครื่อง'],
  ['1','warn','TX0 ของ Serial/USB ใช้ส่งข้อความไป Serial Monitor และอัปโหลดโค้ด ต่ออุปกรณ์อื่นจะรบกวนการอัปโหลด'],
  ['2','warn','Strapping: ต้องเป็น LOW หรือปล่อยลอยตอนเข้าโหมดอัปโหลด บนบอร์ด DevKit หลายรุ่นต่อ LED บนบอร์ดไว้ ใช้เป็นเอาต์พุตได้'],
  ['3','warn','RX0 ของ Serial/USB รับข้อมูลจากคอมพิวเตอร์ ไม่ควรต่อเซนเซอร์'],
  ['4','safe','ใช้งานทั่วไปได้ดี รองรับ PWM, Touch (T0) แต่ ADC ของขานี้เป็น ADC2 ใช้ไม่ได้ขณะเปิด Wi-Fi'],
  ['5','warn','Strapping และส่งสัญญาณ PWM สั้น ๆ ตอนบูต ถ้าต่อรีเลย์อาจกระตุกตอนเปิดเครื่อง เป็นขา CS ของ VSPI ค่าเริ่มต้น'],
  ['6–11','no','ต่อกับชิป SPI Flash ภายในโมดูล ห้ามใช้เด็ดขาด บอร์ดจะค้างหรือรีเซ็ตวนซ้ำ'],
  ['12','warn','Strapping (MTDI): ถ้าถูกดึง HIGH ตอนบูต ชิปจะตั้งแรงดัน Flash เป็น 1.8 V ทำให้บูตไม่ขึ้น หลีกเลี่ยงต่อ pull-up'],
  ['13','safe','ใช้งานทั่วไปได้ รองรับ PWM และ Touch (ADC2)'],
  ['14','warn','ใช้ได้ แต่ส่งสัญญาณ PWM ช่วงบูต ควรหลีกเลี่ยงกับรีเลย์หรือมอเตอร์'],
  ['15','warn','Strapping (MTDO): ถ้าเป็น LOW ตอนบูตจะปิดข้อความบูตทาง Serial และส่ง PWM ตอนบูต'],
  ['16','safe','ใช้งานทั่วไปบน WROOM เป็น RX2 ของ UART2 ค่าเริ่มต้น (บน WROVER ถูกใช้กับ PSRAM)'],
  ['17','safe','ใช้งานทั่วไปบน WROOM เป็น TX2 ของ UART2 ค่าเริ่มต้น (บน WROVER ถูกใช้กับ PSRAM)'],
  ['18','safe','ใช้งานทั่วไป เป็น SCK ของ VSPI'],
  ['19','safe','ใช้งานทั่วไป เป็น MISO ของ VSPI'],
  ['21','safe','SDA ของ I2C ค่าเริ่มต้นใน Arduino'],
  ['22','safe','SCL ของ I2C ค่าเริ่มต้นใน Arduino'],
  ['23','safe','ใช้งานทั่วไป เป็น MOSI ของ VSPI'],
  ['25','safe','ใช้ได้ทั่วไป มี DAC1 8 บิต (ADC2)'],
  ['26','safe','ใช้ได้ทั่วไป มี DAC2 8 บิต (ADC2)'],
  ['27','safe','ใช้งานทั่วไป รองรับ PWM, Touch (ADC2)'],
  ['32','safe','ใช้งานทั่วไป เป็น ADC1 ใช้อ่านแอนะล็อกพร้อม Wi-Fi ได้'],
  ['33','safe','ใช้งานทั่วไป เป็น ADC1 ใช้อ่านแอนะล็อกพร้อม Wi-Fi ได้'],
  ['34','in','อินพุตอย่างเดียว ADC1 ไม่มี pull-up/pull-down ภายใน เหมาะกับเซนเซอร์แอนะล็อกอย่าง MQ-3, pH, LDR'],
  ['35','in','อินพุตอย่างเดียว ADC1 ไม่มี pull-up/pull-down ภายใน'],
  ['36','in','VP (SENSOR_VP) อินพุตอย่างเดียว ADC1'],
  ['39','in','VN (SENSOR_VN) อินพุตอย่างเดียว ADC1']
];
const VWORD={safe:'ใช้ได้สบาย',warn:'ระวัง',no:'ห้ามใช้',in:'อินพุตอย่างเดียว'};
function renderPins(){
  const h=$('#pinBoard'); if(!h) return;
  h.innerHTML=PINS.map((p,i)=>'<button class="pick" data-pin="'+i+'">GPIO'+p[0]+'<small>แตะเพื่อตรวจ</small></button>').join('');
}
function inspectPin(i){
  const p=PINS[i], b=$('#pinBoard [data-pin="'+i+'"]');
  b.className='pick v-'+p[1]+' sel'; b.innerHTML='GPIO'+p[0]+'<small>'+VWORD[p[1]]+'</small>';
  $$('#pinBoard .pick').forEach(x=>{ if(x!==b) x.classList.remove('sel'); });
  const st=$('#pinStatus'); st.className='status-line'+(p[1]==='safe'?' ok':'');
  st.innerHTML='<b>GPIO'+p[0]+' · '+VWORD[p[1]]+'</b> — '+p[2];
  SFX.play(p[1]==='no'?'alarm':(p[1]==='safe'?'correct':'ping'));
  markLab('lab1','p'+p[0],4);
  if(labCount('lab1')===PINS.length) toast('ตรวจครบทุกขาบนบอร์ดแล้ว');
}

/* ---- LAB 2: ADC + Wi-Fi trap + INPUT_PULLUP ---- */
let aPin=34, wifiOn=false, pressed=false;
function adc2(p){ return [0,2,4,12,13,14,15,25,26,27].indexOf(p)>=0; }
function aUpdate(user){
  const v=+$('#aVin').value/100, raw=Math.round(v/3.3*4095), st=$('#aStatus');
  $('#aPinTxt').textContent='GPIO'+aPin; $('#aV').innerHTML=v.toFixed(2)+'<small>V</small>';
  if(adc2(aPin)&&wifiOn){
    $('#aRaw').innerHTML='ERR<small>ADC2 ถูก Wi-Fi ใช้งาน</small>'; $('#aBar').style.width='0%';
    st.className='status-line'; st.innerHTML='<b>กับดัก!</b> GPIO'+aPin+' เป็น ADC2 ซึ่งใช้ไม่ได้ขณะ Wi-Fi ทำงาน โปรเจกต์ IoT ต้องย้ายเซนเซอร์แอนะล็อกไปที่ ADC1 (GPIO32–39)';
    if(user) SFX.play('alarm');
  } else {
    $('#aRaw').innerHTML=raw+'<small>/ 4095</small>'; $('#aBar').style.width=(raw/4095*100)+'%';
    st.className='status-line ok'; st.innerHTML='GPIO'+aPin+' ('+(adc2(aPin)?'ADC2':'ADC1')+') อ่านได้ ≈ '+raw+' จาก '+v.toFixed(2)+' V'+(wifiOn?' · ขณะเปิด Wi-Fi':'')+' · ค่าจริงของ ESP32 จะเพี้ยนบ้างช่วงปลายสเกล จึงควรใช้ analogReadMilliVolts()';
  }
  if(user) markLab('lab2',aPin+'|'+(wifiOn?'w':'n'),5);
}
function pullToggle(){
  pressed=!pressed;
  $('#pullRead').innerHTML=pressed?'LOW<small>กำลังกดปุ่ม</small>':'HIGH<small>ปล่อยปุ่ม</small>';
  $('#pullBtn').textContent=pressed?'ปล่อยปุ่ม':'กดปุ่มค้างไว้ (แตะเพื่อสลับ)';
  SFX.play(pressed?'tick':'select');
  toast(pressed?'กดแล้ว digitalRead() ได้ LOW เพราะปุ่มต่อลง GND':'ปล่อยปุ่ม pull-up ภายในดึงขาขึ้นเป็น HIGH');
  markLab('lab2','pull'+(pressed?1:0),3);
}

/* ---- LAB 3: Bus Matchmaker ---- */
const MODS={
  oled:{a:'i2c',why:'SSD1306 รุ่น 4 ขา (VCC, GND, SCL, SDA) ใช้ I2C แอดเดรส 0x3C เป็นส่วนใหญ่'},
  bmp:{a:'i2c',why:'BMP280 ใช้ I2C แอดเดรส 0x76 หรือ 0x77 เลือกได้จากขา SDO (รองรับ SPI ด้วย แต่โมดูลทั่วไปนิยม I2C)'},
  pms:{a:'uart',why:'PMS5003 ส่งเฟรมข้อมูลทาง UART 9600 baud ใช้ไฟเลี้ยง 5 V แต่ระดับสัญญาณ TX เป็น 3.3 V ต่อเข้า RX2 (GPIO16) ได้'},
  sd:{a:'spi',why:'การ์ด SD ต้องการความเร็วสูง ใช้ SPI (MOSI 23, MISO 19, SCK 18, CS 5)'},
  ds:{a:'ow',why:'DS18B20 ใช้ 1-Wire สายข้อมูลเส้นเดียว ต้องมี pull-up 4.7 kΩ ต่อหลายหัววัดบนขาเดียวได้'},
  radar:{a:'uart',why:'LD2410 ส่งข้อมูลสถานะการมีคนอยู่ทาง UART (ค่าเริ่มต้น 256000 baud) และมีขา OUT ดิจิทัลแจ้งว่ามีคน'},
  mpu:{a:'i2c',why:'MPU6050 ใช้ I2C แอดเดรส 0x68 (หรือ 0x69 เมื่อดึงขา AD0 ขึ้น)'},
  gps:{a:'uart',why:'GPS NEO-6M ส่งประโยค NMEA ทาง UART ค่าเริ่มต้น 9600 baud ต้องต่อ TX ของ GPS เข้า RX ของ ESP32'}
};
let modSel=null;
function pickMod(k){ modSel=k; $$('#busGrid .pick').forEach(b=>b.classList.toggle('sel',b.dataset.mod===k));
  const st=$('#busStatus'); st.className='status-line'; st.textContent='เลือกแล้ว — โมดูลนี้สื่อสารด้วยบัสใด'; }
function judgeBus(bus){
  const st=$('#busStatus');
  if(!modSel){st.className='status-line';st.textContent='กรุณาแตะเลือกโมดูลก่อน';SFX.play('wrong');return;}
  const m=MODS[modSel], b=$('#busGrid [data-mod="'+modSel+'"]'); b.classList.remove('sel','ok','bad');
  if(bus===m.a){ b.classList.add('ok'); st.className='status-line ok'; st.innerHTML='ถูกต้อง — '+m.why; SFX.play('correct'); markLab('lab3',modSel);
    if(labCount('lab3')===8) toast('จับคู่บัสครบทั้ง 8 โมดูลแล้ว'); }
  else { b.classList.add('bad'); st.className='status-line'; st.innerHTML='ยังไม่ใช่ — ลองดูจำนวนขาสัญญาณบนโมดูล: 2 เส้น SDA/SCL, 4 เส้นมี CS, TX/RX หรือสายข้อมูลเส้นเดียว'; SFX.play('wrong'); }
  modSel=null;
}
"""

LAB_WIRING = r"""
  const pn=e.target.closest('[data-pin]'); if(pn){inspectPin(+pn.dataset.pin);return;}
  const ap=e.target.closest('[data-apin]'); if(ap){SFX.play('select');aPin=+ap.dataset.apin;aUpdate(true);return;}
  const md=e.target.closest('[data-mod]'); if(md){SFX.play('select');pickMod(md.dataset.mod);return;}
  const bs=e.target.closest('[data-bus]'); if(bs){judgeBus(bs.dataset.bus);return;}
  if(e.target.closest('#pullBtn')){pullToggle();return;}
  if(e.target.closest('#wifiTgl')){
    wifiOn=!wifiOn; const b=$('#wifiTgl'); b.textContent='Wi-Fi: '+(wifiOn?'ON':'OFF'); b.className='toggle '+(wifiOn?'on':'off');
    SFX.play('select'); aUpdate(true); return;
  }
"""
INIT_EXTRA = " renderPins(); $('#aVin').addEventListener('input',()=>aUpdate(true)); aUpdate(false);"

B = {}
B['district1'] = [
 ('ระดับแรงดันลอจิกของขา GPIO บน ESP32 คือข้อใด',
  ['3.3 V และไม่ควรป้อน 5 V เข้าขาโดยตรง',
   '5 V เหมือน Arduino Uno และทนแรงดันได้ถึง 6 V',
   '1.8 V เหมือนหน่วยความจำ Flash ในโมดูล',
   '12 V เพื่อขับรีเลย์และมอเตอร์ได้โดยตรง'],
  'ESP32 เป็นชิปลอจิก 3.3 V ขา GPIO ไม่ได้ออกแบบให้ทนแรงดัน 5 V การป้อน 5 V เสี่ยงทำให้ขาหรือชิปเสียหาย'),
 ('เซนเซอร์อัลตราโซนิก HC-SR04 ใช้ไฟ 5 V และขา ECHO ส่งสัญญาณ HIGH ที่ 5 V ควรต่อเข้ากับ ESP32 อย่างไร',
  ['ผ่านตัวแบ่งแรงดัน 1 kΩ/2 kΩ ให้เหลือราว 3.3 V หรือใช้ตัวแปลงระดับลอจิก',
   'ต่อเข้าขา GPIO ตรง ๆ ได้เลย เพราะขาของ ESP32 ทนแรงดัน 5 V ได้ทุกขา',
   'ต่อเข้าขา 3V3 ของบอร์ด เพื่อให้แรงดันสองฝั่งเท่ากันพอดี',
   'ต่อผ่านตัวต้านทาน 10 kΩ เพียงตัวเดียว เพื่อลดแรงดันให้เหลือราว 3.3 V'],
  'Vout = 5 × 2k/(1k+2k) ≈ 3.33 V ปลอดภัยต่อขา ESP32 และยังสูงพอให้อ่านเป็น HIGH'),
 ('ขาใดของ ESP32-WROOM-32 ที่ "ห้ามใช้" เป็น GPIO เพราะต่ออยู่กับชิป Flash ภายในโมดูล',
  ['GPIO6 ถึง GPIO11', 'GPIO21 และ GPIO22', 'GPIO32 และ GPIO33', 'GPIO25 และ GPIO26'],
  'GPIO6–11 ถูกใช้สื่อสารกับ SPI Flash ที่เก็บโปรแกรม หากนำไปใช้จะทำให้บอร์ดค้างหรือรีเซ็ต'),
 ('GPIO34, 35, 36 และ 39 มีข้อจำกัดใด',
  ['อินพุตอย่างเดียว ไม่มี pull-up ภายใน',
   'เอาต์พุตอย่างเดียว และไม่มีวงจร ADC อยู่ภายใน',
   'ใช้ได้เฉพาะตอนปิด Wi-Fi เพราะเป็นขา ADC2 ทั้งหมด',
   'เป็นขาจ่ายไฟ 5 V สำหรับเลี้ยงเซนเซอร์ภายนอก'],
  'จึงเหมาะกับการอ่านเซนเซอร์แอนะล็อกผ่าน ADC1 แต่ถ้าต่อปุ่มต้องใส่ตัวต้านทาน pull-up/pull-down ภายนอกเอง'),
 ('นักศึกษาต่อตัวต้านทาน pull-up ไว้ที่ GPIO12 แล้วพบว่าบอร์ดบูตไม่ขึ้น สาเหตุที่เป็นไปได้มากที่สุดคือข้อใด',
  ['GPIO12 เป็นขา Strapping ที่กำหนดแรงดัน Flash ตอนบูต',
   'GPIO12 เป็นขาจ่ายไฟ 3.3 V การต่อ pull-up จึงลัดวงจรกับไฟเลี้ยง',
   'ตัวต้านทาน pull-up ดึงกระแสมากจน Wi-Fi และชิปทำงานไม่ได้',
   'GPIO12 เป็นขาอินพุตอย่างเดียว ต่อ pull-up แล้วชิปจึงค้างตอนบูต'],
  'ขา Strapping (0, 2, 5, 12, 15) ถูกอ่านสถานะตอนเปิดเครื่องเพื่อเลือกโหมด จึงต้องระวังสิ่งที่ต่อไว้ที่ขาเหล่านี้'),
 ('ต้องการขับ LED แดง (Vf ≈ 2.0 V) ด้วยกระแส 10 mA จากขา GPIO 3.3 V ตัวต้านทานจำกัดกระแสขั้นต่ำควรมีค่าประมาณเท่าใด',
  ['130 Ω (ใช้ค่ามาตรฐานที่สูงกว่า เช่น 150 Ω)',
   '13 Ω (ใช้ค่ามาตรฐานที่ต่ำกว่า เช่น 10 Ω)',
   '1.3 kΩ (ใช้ค่ามาตรฐานที่สูงกว่า เช่น 1.5 kΩ)',
   '330 kΩ (ใช้ค่ามาตรฐานที่ต่ำกว่า เช่น 220 kΩ)'],
  'R = (3.3 − 2.0)/0.010 = 130 Ω เลือกค่าที่สูงกว่าเล็กน้อยเพื่อลดกระแสและเผื่อความคลาดเคลื่อน'),
 ('ข้อใดคือแนวปฏิบัติที่ถูกต้องเรื่องกระแสของขา GPIO บน ESP32',
  ['ใช้ไม่เกินราว 20 mA ต่อขา โหลดกระแสสูงต้องผ่านทรานซิสเตอร์หรือ MOSFET',
   'ต่อมอเตอร์ DC เข้าขา GPIO ได้โดยตรง ถ้าเป็นมอเตอร์ขนาดเล็กกว่า 1 A',
   'ขา GPIO จ่ายกระแสได้ไม่จำกัด ขึ้นอยู่กับขนาดแหล่งจ่ายที่ต่อเข้ากับบอร์ด',
   'ต่อปั๊มน้ำ 12 V เข้าขา GPIO ได้โดยตรง ถ้าใช้สายไฟเส้นใหญ่และสั้นที่สุด'],
  'ขา GPIO มีไว้ส่ง "สัญญาณสั่งงาน" ไม่ใช่จ่ายกำลังให้โหลด โหลดอย่างมอเตอร์ ปั๊ม หรือรีเลย์ต้องผ่านวงจรขับเสมอ'),
 ('เซนเซอร์ PMS5003 ต้องการไฟเลี้ยง 5 V ส่วนแอปฯ ใช้ ESP32 รับข้อมูล การต่อกราวด์ (GND) ควรทำอย่างไร',
  ['ต่อ GND ของทุกอุปกรณ์และแหล่งจ่ายเข้าด้วยกัน',
   'แยก GND ของแต่ละอุปกรณ์ออกจากกัน เพื่อป้องกันกระแสไหลย้อน',
   'ไม่ต้องต่อ GND เพราะสาย TX/RX ส่งสัญญาณอ้างอิงมาให้แล้ว',
   'ต่อ GND ของเซนเซอร์เข้าขา 5V ของบอร์ดเพื่อให้ไฟครบวงจร'],
  'สัญญาณดิจิทัลคือแรงดันเทียบกับกราวด์ ถ้ากราวด์ไม่ร่วมกัน ระดับ HIGH/LOW จะไม่มีความหมายและการสื่อสารจะผิดพลาด'),
 ('การต่อเซนเซอร์เข้ากับ GPIO1 และ GPIO3 ของ ESP32 DevKit ทำให้เกิดปัญหาใดบ่อยที่สุด',
  ['อัปโหลดไม่ได้หรือ Serial เพี้ยน เพราะเป็นขา TX0/RX0 ของ USB',
   'Wi-Fi ช้าลง เพราะสองขานี้ใช้ร่วมกับวงจรเสาอากาศและวิทยุของโมดูล',
   'ADC อ่านค่าได้ละเอียดขึ้น เพราะเป็นขาที่มีตัวกรองสัญญาณ',
   'บอร์ดชาร์จแบตเตอรี่ไม่ได้ เพราะสองขานี้เป็นของวงจรจัดการพลังงาน'],
  'UART0 ถูกใช้อัปโหลดและดีบัก จึงควรย้ายอุปกรณ์ UART ไปที่ UART2 (GPIO16 RX2, GPIO17 TX2)'),
 ('ทีมต่อโมดูลรีเลย์ไว้ที่ GPIO5 แล้วพบว่ารีเลย์ "กระตุก" ทุกครั้งที่เปิดเครื่อง คำอธิบายที่เหมาะสมคือข้อใด',
  ['GPIO5 เป็นขา Strapping มีสัญญาณช่วงบูต ควรย้ายขา',
   'รีเลย์เสียจากการใช้งานนาน ต้องเปลี่ยนโมดูลรีเลย์ใหม่ทั้งชุดทันที',
   'โค้ดใน loop() ทำงานก่อน setup() จึงสั่งรีเลย์ก่อนที่จะตั้งค่าขาเสร็จ',
   'GPIO5 เป็นขาอินพุตอย่างเดียว จึงขับรีเลย์ได้ไม่เสถียร'],
  'อุปกรณ์ที่ห้ามทำงานเองโดยไม่ตั้งใจ เช่น รีเลย์ปั๊มน้ำหรือแอร์ ควรอยู่บนขาที่ไม่มีสัญญาณระหว่างบูต'),
 ('ขาใดบนบอร์ด ESP32 DevKit ที่ "ไม่ควร" ใช้จ่ายไฟให้เซอร์โวหรือปั๊มน้ำ',
  ['ขา 3V3 เพราะเรกูเลเตอร์เล็ก กระแสกระชากทำให้บอร์ดรีเซ็ต',
   'แหล่งจ่ายภายนอกขนาดพอเหมาะ ที่ต่อกราวด์ร่วมกับบอร์ด ESP32 อย่างถูกต้อง',
   'อะแดปเตอร์แยกที่จ่ายกระแสได้เพียงพอสำหรับมอเตอร์และปั๊มน้ำ',
   'โมดูล Buck converter ที่ลดแรงดันจากแบตและต่อกราวด์ร่วม'],
  'โหลดเชิงกลกินกระแสกระชากสูง ควรใช้แหล่งจ่ายแยกและต่อกราวด์ร่วมกับ ESP32 เพื่อไม่ให้แรงดันตกจนชิป brownout'),
 ('ข้อใดสรุปกลุ่มขาที่ "ใช้งานทั่วไปได้สะดวกที่สุด" บน ESP32-WROOM-32 ได้ถูกต้อง',
  ['GPIO4, 13, 16–19, 21–23, 25–27, 32, 33',
   'GPIO6–11 ที่อยู่ใกล้โมดูลและเดินสายได้สะดวกที่สุด',
   'GPIO0, 2, 12, 15 เท่านั้น เพราะเป็นขา Strapping',
   'GPIO34–39 สำหรับเอาต์พุตทุกชนิดรวมถึง PWM'],
  'กลุ่มนี้ไม่ติด Flash ไม่เป็นอินพุตอย่างเดียว และส่วนใหญ่ไม่มีบทบาทตอนบูต จึงเป็นตัวเลือกแรกของการออกแบบวงจร'),
]
B['district2'] = [
 ('พิจารณาโปรแกรมต่อไปนี้ ' + code('pinMode(BTN, INPUT_PULLUP);\n\nvoid loop() {\n  if (digitalRead(BTN) == LOW) {\n    digitalWrite(LED, HIGH);\n  } else {\n    digitalWrite(LED, LOW);\n  }\n}') + 'ปุ่มต่อระหว่างขา BTN กับ GND เมื่อ "กดปุ่ม" ค่า digitalRead(BTN) และ LED เป็นอย่างไร',
  ['อ่านได้ LOW และ LED ติด', 'อ่านได้ HIGH และ LED ติด', 'อ่านได้ LOW และ LED ดับ', 'อ่านได้ HIGH และ LED ดับ'],
  'INPUT_PULLUP ดึงขาขึ้นเป็น HIGH ตอนปล่อยปุ่ม เมื่อกดปุ่ม ขาถูกต่อลง GND จึงอ่านได้ LOW (ลอจิกกลับด้าน)'),
 ('ถ้าใช้ pinMode(BTN, INPUT) กับปุ่มที่ต่อลง GND โดยไม่มีตัวต้านทาน pull-up ภายนอก ผลที่เกิดขึ้นคือข้อใด',
  ['ขาลอย (floating) ค่าที่อ่านได้แกว่งไปมาแบบสุ่มตอนไม่ได้กดปุ่ม',
   'อ่านได้ HIGH อย่างมั่นคงเสมอ เพราะ GPIO มี pull-up ทุกขา',
   'คอมไพเลอร์แจ้งข้อผิดพลาดและไม่ยอมอัปโหลดโค้ดลงบอร์ด',
   'ปุ่มจะทำงานกลับด้านอัตโนมัติ กดแล้วอ่านได้ HIGH เสมอ'],
  'ขาอินพุตที่ไม่ถูกดึงไปทางใดทางหนึ่งจะรับสัญญาณรบกวนรอบข้าง จึงต้องใช้ pull-up/pull-down ภายในหรือภายนอกเสมอ'),
 ('โปรเจกต์ IoT ส่งข้อมูลผ่าน Wi-Fi และต้องอ่านเซนเซอร์แอนะล็อก MQ-3 ควรต่อเข้าขาใด',
  ['GPIO34 เพราะเป็น ADC1 ที่ใช้ได้แม้ Wi-Fi ทำงาน',
   'GPIO4 เพราะเป็น ADC2 ที่ใช้งานได้ดีเมื่อเปิด Wi-Fi',
   'GPIO25 เพราะเป็นขา DAC ที่อ่านแรงดันได้แม่นยำกว่า',
   'GPIO6 เพราะเป็นขาว่างที่ไม่มีอุปกรณ์อื่นใช้งานอยู่'],
  'ADC2 ถูกใช้ร่วมกับไดรเวอร์ Wi-Fi จึงอ่านค่าไม่ได้ขณะเชื่อมต่อ งาน IoT จึงต้องใช้ขา ADC1 (GPIO32–39)'),
 ('ESP32 อ่านค่า analogRead() ได้ 3071 จากช่วง 0–4095 (ช่วงแรงดันราว 0–3.3 V) แรงดันโดยประมาณคือเท่าใด',
  ['ประมาณ 2.5 V', 'ประมาณ 3.07 V', 'ประมาณ 1.0 V', 'ประมาณ 0.3 V'],
  '3071/4095 × 3.3 ≈ 2.47 V ในงานจริงควรใช้ analogReadMilliVolts() ที่ชดเชยความไม่เป็นเชิงเส้นของ ADC'),
 ('PWM ความละเอียด 8 บิต ตั้งค่า duty = 64 สัดส่วนเวลาที่ขาเป็น HIGH (duty cycle) ประมาณเท่าใด',
  ['25%', '64%', '50%', '6.4%'],
  '8 บิตมีระดับ 0–255 duty 64/255 ≈ 25% ถ้าตั้ง 128 จะได้ราว 50% และ 255 คือ 100%'),
 ('ข้อใดอธิบายหลักการของ PWM ได้ถูกต้อง',
  ['สลับ HIGH/LOW เร็ว ๆ แล้วปรับสัดส่วนเวลา HIGH',
   'สร้างแรงดันแอนะล็อกต่อเนื่องที่แท้จริงด้วยวงจร DAC ภายในชิป',
   'เพิ่มแรงดันที่ขาให้สูงเกิน 3.3 V เพื่อขับโหลดได้แรงขึ้น',
   'อ่านค่าจากเซนเซอร์อุณหภูมิด้วยการนับความกว้างของพัลส์'],
  'PWM ไม่ใช่แรงดันแอนะล็อกจริง แต่ LED หรือมอเตอร์ตอบสนองต่อค่าเฉลี่ย จึงดูเหมือนหรี่หรือช้าลงได้'),
 ('ต้องการแรงดันแอนะล็อกจริงจาก ESP32 (ไม่ใช่ PWM) เพื่อป้อนเข้าวงจรเสียง ควรใช้ขาใด',
  ['GPIO25 หรือ 26 ซึ่งมี DAC 8 บิต',
   'GPIO34 ซึ่งเป็นขาอินพุตอย่างเดียว',
   'GPIO6 ซึ่งต่อกับ Flash ภายในโมดูล',
   'GPIO1 ซึ่งเป็นขา TX0 ของ UART0'],
  'ESP32 รุ่นดั้งเดิมมี DAC 2 ช่องที่ GPIO25 (DAC1) และ GPIO26 (DAC2) ความละเอียด 8 บิต'),
 ('ค่า analogRead() ของ ESP32 ที่ความละเอียด 12 บิต ให้ช่วงค่าดิจิทัลเท่าใด',
  ['0–4095', '0–1023', '0–255', '0–3300'],
  'ค่าเริ่มต้นของ ESP32 ใน Arduino คือ 12 บิต ต่างจาก Arduino Uno ที่เป็น 10 บิต (0–1023) ต้องระวังเมื่อนำโค้ดของ Uno มาใช้'),
 ('นักศึกษาย้ายโค้ดจาก Arduino Uno มาใช้กับ ESP32 โดยไม่แก้สูตร voltage = raw × 5.0 / 1023 จะเกิดปัญหาใด',
  ['ค่าแรงดันผิด เพราะ ESP32 ใช้ช่วง 0–4095 และอ้างอิงราว 3.3 V',
   'คอมไพล์ไม่ผ่าน เพราะ ESP32 ไม่รองรับการคำนวณเลขทศนิยมแบบ float',
   'บอร์ดเปลี่ยนแรงดันอ้างอิงเป็น 5 V ให้อัตโนมัติ ค่าจึงถูก',
   'ไม่มีปัญหาใด ๆ เพราะ analogRead() ให้ค่าเหมือนกันทุกบอร์ดทุกรุ่น'],
  'ต้องปรับเป็น raw × 3.3/4095 หรือใช้ analogReadMilliVolts() ความผิดพลาดแบบนี้ทำให้ค่าเซนเซอร์ทั้งระบบเพี้ยน'),
 ('ESP32 รุ่นดั้งเดิมมีขา Touch แบบ capacitive เมื่อนิ้วแตะขา Touch ค่า touchRead() โดยทั่วไปจะเป็นอย่างไร',
  ['ค่าลดลงชัดเจน จึงตั้งเกณฑ์ต่ำกว่าค่าปกติเพื่อตรวจการแตะ',
   'ค่าเพิ่มขึ้นชัดเจน จึงตั้งเกณฑ์สูงกว่าค่าปกติเพื่อตรวจการแตะ',
   'ค่ากลายเป็น 4095 ทุกครั้ง เพราะนิ้วต่อขาเข้ากับไฟ 3.3 V',
   'ขาเปลี่ยนเป็นเอาต์พุตชั่วคราว และส่งสัญญาณกลับไปที่นิ้ว'],
  'บน ESP32 รุ่นดั้งเดิม ค่า touchRead() ลดลงเมื่อสัมผัส (รุ่น S2/S3 กลับด้าน) ใช้ทำปุ่มสัมผัสโดยไม่ต้องมีสวิตช์จริง'),
 ('เซนเซอร์ให้แรงดันสูงสุด 5 V ต้องการอ่านด้วย ADC ของ ESP32 วิธีที่ถูกต้องคือข้อใด',
  ['ลดด้วยตัวแบ่งแรงดันให้ไม่เกินราว 3.3 V แล้วคูณกลับในโปรแกรม',
   'ต่อเข้าขา ADC โดยตรง เพราะ ADC ของ ESP32 รับได้ถึง 5 V',
   'ต่อเข้าขา 3V3 แทน แล้วอ่านค่าจากขานั้นด้วย analogRead()',
   'ใช้ digitalRead() แทน analogRead() เพราะทนแรงดันได้สูงกว่า'],
  'วงจรแบ่งแรงดันป้องกันขาเสียหาย และโปรแกรมต้องคูณกลับตามอัตราส่วน เช่น ถ้าแบ่ง 2:3 ให้คูณผลด้วย 1.5'),
 ('ข้อใดคือการใช้ PWM ที่เหมาะสมในโปรเจกต์ชุดปลูกผักไฮโดรโปนิกส์บนโต๊ะ',
  ['หรี่ไฟ LED ปลูกพืชผ่าน MOSFET ตามเวลา',
   'อ่านค่า pH ของน้ำโดยวัดความกว้างพัลส์จากหัววัด',
   'อ่านอุณหภูมิน้ำจาก DS18B20 ผ่านขา PWM ของบอร์ด',
   'ตรวจว่าน้ำในถังหมดหรือไม่ด้วยการสั่ง PWM ไปที่ลูกลอย'],
  'PWM เป็นเอาต์พุต ใช้ปรับกำลังเฉลี่ยของโหลด ส่วนการวัด pH อุณหภูมิ และระดับน้ำเป็นงานฝั่งอินพุต'),
]
B['district3'] = [
 ('บัส I2C บน ESP32 (ค่าเริ่มต้นใน Arduino) ใช้ขาใด',
  ['SDA = GPIO21, SCL = GPIO22', 'SDA = GPIO1, SCL = GPIO3', 'SDA = GPIO6, SCL = GPIO7', 'SDA = GPIO34, SCL = GPIO35'],
  'I2C ใช้สาย 2 เส้น คือ SDA (ข้อมูล) และ SCL (สัญญาณนาฬิกา) และสามารถย้ายขาได้ด้วย Wire.begin(sda, scl)'),
 ('ทีมต่อ BMP280 สองตัวบนบัส I2C เดียวกัน แล้วอ่านค่าได้เพียงตัวเดียว สาเหตุที่น่าจะเป็นที่สุดคือข้อใด',
  ['แอดเดรสซ้ำกัน (0x76) ต้องตั้งตัวหนึ่งเป็น 0x77',
   'บัส I2C ต่ออุปกรณ์ได้เพียงตัวเดียวเสมอ ต้องใช้บัสละตัว',
   'BMP280 ต้องสื่อสารผ่าน UART เท่านั้น จึงอ่านผ่าน I2C ได้ตัวเดียว',
   'สาย I2C ยาวเกิน 10 เซนติเมตร ทำให้ตัวที่อยู่ไกลอ่านไม่ได้'],
  'อุปกรณ์บนบัส I2C แยกกันด้วยแอดเดรส ถ้าซ้ำกันจะชนกัน ใช้โปรแกรม I2C Scanner ตรวจแอดเดรสก่อนเขียนโค้ดเสมอ'),
 ('การต่อสาย UART ระหว่าง ESP32 กับ GPS NEO-6M ที่ถูกต้องคือข้อใด',
  ['TX ของ GPS ต่อ RX ของ ESP32 และ RX ต่อ TX (ไขว้กัน) พร้อม GND ร่วม',
   'TX ต่อ TX และ RX ต่อ RX เพื่อให้ชื่อขาตรงกันทั้งสองฝั่ง',
   'ต่อ TX ของ GPS เข้า TX ของ ESP32 พร้อม GND เพราะ GPS ส่งข้อมูลทางเดียว',
   'ต่อ TX ทั้งสองฝั่งเข้า 3V3 เพื่อดึงสายให้เป็น HIGH ตลอดเวลา'],
  'ขาส่ง (TX) ของฝั่งหนึ่งต้องเข้าขารับ (RX) ของอีกฝั่ง ความผิดพลาด "TX ต่อ TX" เป็นสาเหตุอันดับต้นของการอ่านข้อมูลไม่ได้'),
 ('Serial Monitor แสดงตัวอักษรขยะอ่านไม่ออก ขณะที่โค้ดเรียก Serial.begin(115200) สาเหตุที่พบบ่อยที่สุดคือข้อใด',
  ['baud rate ของ Serial Monitor ไม่ตรงกับในโค้ด',
   'ESP32 เสียหายจากไฟฟ้าสถิต ต้องเปลี่ยนบอร์ดใหม่',
   'สาย USB ยาวเกินไปทำให้สัญญาณอ่อนลงจนอ่านไม่ออก',
   'Wi-Fi รบกวนสัญญาณ Serial ต้องปิด Wi-Fi ระหว่างพิมพ์'],
  'ทั้งสองฝั่งของ UART ต้องใช้ความเร็วเดียวกัน หากไม่ตรงกันข้อมูลจะถูกถอดรหัสผิดเป็นอักขระแปลก ๆ'),
 ('อุปกรณ์ SPI สามตัว (การ์ด SD, จอ TFT, โมดูลวิทยุ) ใช้บัสเดียวกัน ข้อใดถูกต้อง',
  ['ใช้ MOSI, MISO, SCK ร่วมกัน แต่ละตัวมีขา CS แยกของตัวเอง',
   'ต้องมีสาย MOSI แยกทุกตัว แต่ใช้ขา CS ร่วมกันได้ทั้งบัสเพื่อประหยัดขา',
   'SPI ต่ออุปกรณ์ได้เพียงตัวเดียว ต้องใช้บัสละหนึ่งอุปกรณ์',
   'SPI ใช้สายเส้นเดียวเหมือน 1-Wire และแยกอุปกรณ์ด้วยรหัสประจำตัว'],
  'ESP32 เลือกคุยกับอุปกรณ์ตัวใดด้วยการดึงขา CS ของตัวนั้นลง LOW อุปกรณ์อื่นที่ CS เป็น HIGH จะไม่ตอบสนอง'),
 ('ระบบตู้เลี้ยงกุ้งต้องการวัดอุณหภูมิน้ำ 3 จุดด้วย DS18B20 สามหัว วิธีต่อที่ประหยัดขาที่สุดคือข้อใด',
  ['ขาเดียวแบบ 1-Wire และ pull-up 4.7 kΩ',
   'ใช้ 3 ขา ADC แยกกัน เพราะ DS18B20 ให้แรงดันแอนะล็อก',
   'ต่อผ่านบัส I2C ที่แอดเดรส 0x3C, 0x3D และ 0x3E',
   'ต่อเข้าขา TX0 และ RX0 แล้วอ่านด้วย Serial.read()'],
  'DS18B20 ทุกตัวมีรหัสประจำตัวไม่ซ้ำกันจากโรงงาน จึงต่อขนานบนสายเดียวกันได้หลายตัว'),
 ('ESP32 ค้นหาเครือข่าย Wi-Fi ของหอพักไม่เจอ ทั้งที่มือถือเห็น สาเหตุที่ควรตรวจสอบก่อนคือข้อใด',
  ['เราเตอร์อาจปล่อยเฉพาะ 5 GHz แต่ ESP32 รองรับเฉพาะ 2.4 GHz',
   'ESP32 ใช้ได้เฉพาะสัญญาณ 5G ของมือถือ จึงไม่รองรับเราเตอร์ในบ้านทั่วไป',
   'ต้องปิด Bluetooth ของมือถือทุกเครื่องก่อน ESP32 จึงจะมองเห็นเครือข่าย',
   'ESP32 ต้องเชื่อมต่อผ่านสาย LAN ก่อนจึงจะค้นหา Wi-Fi ได้'],
  'ESP32 รุ่นดั้งเดิมรองรับ Wi-Fi 802.11 b/g/n ย่าน 2.4 GHz เท่านั้น เมื่อใช้ฮอตสปอตจากมือถือให้ตั้งเป็น 2.4 GHz'),
 ('เซนเซอร์ฝุ่น PMS5003 ส่งข้อมูลทาง UART ควรต่อเข้าพอร์ตใดของ ESP32 เพื่อไม่รบกวนการอัปโหลดโค้ด',
  ['UART2 คือ RX2 = GPIO16, TX2 = GPIO17',
   'UART0 คือ GPIO1 และ GPIO3 ที่ต่อกับ USB',
   'ขา GPIO6–11 ที่ต่อกับ Flash ภายในโมดูล',
   'ขา I2C GPIO21–22 โดยใช้คำสั่ง Wire.read()'],
  'UART0 ใช้กับ USB สำหรับอัปโหลดและดีบัก ESP32 มี UART ฮาร์ดแวร์อีก 2 ชุด จึงควรใช้ HardwareSerial(2) กับเซนเซอร์'),
 ('ข้อใดเปรียบเทียบ I2C กับ SPI ได้ถูกต้อง',
  ['I2C ใช้ 2 เส้นแยกอุปกรณ์ด้วยแอดเดรส ส่วน SPI เร็วกว่าแต่ต้องมี CS ต่อตัว',
   'I2C เร็วกว่า SPI เสมอ และต้องใช้สาย CS แยกสำหรับอุปกรณ์ทุกตัวบนบัส',
   'SPI ใช้สายเส้นเดียว ส่วน I2C ต้องใช้สายอย่างน้อย 4 เส้น',
   'ทั้งสองบัสต้องต่อสาย TX และ RX ไขว้กันเหมือน UART'],
  'เลือก I2C เมื่อต้องการต่ออุปกรณ์หลายตัวด้วยสายน้อย เลือก SPI เมื่อต้องการความเร็ว เช่น การ์ด SD หรือจอสี'),
 ('บัส I2C ต้องมีตัวต้านทาน pull-up ที่สาย SDA และ SCL เพราะเหตุใด',
  ['ขา I2C เป็น open-drain จึงต้องมี pull-up ดึงสายกลับเป็น HIGH',
   'เพื่อเพิ่มแรงดันบนสายให้เป็น 5 V และส่งสัญญาณได้ไกลขึ้นกว่าเดิม',
   'เพื่อจำกัดกระแสไม่ให้สัญญาณ I2C ไปรบกวนการทำงานของวงจร Wi-Fi',
   'I2C ไม่จำเป็นต้องมี pull-up ถ้าสายสั้นกว่า 1 เมตร'],
  'โมดูลสำเร็จรูปหลายรุ่นใส่ pull-up (มักเป็น 4.7 kΩ หรือ 10 kΩ) มาให้แล้ว แต่ถ้าต่อหลายโมดูลค่า pull-up ขนานกันจะลดลง ต้องตรวจสอบ'),
 ('Bluetooth Low Energy (BLE) ของ ESP32 เหมาะกับงานใดมากที่สุด',
  ['ส่งข้อมูลน้อยระยะใกล้ไปยังมือถือแบบประหยัดไฟ',
   'สตรีมวิดีโอความละเอียดสูงไปยังคลาวด์อย่างต่อเนื่อง',
   'ส่งข้อมูลข้ามจังหวัดโดยไม่ต้องใช้อินเทอร์เน็ตเลย',
   'แทนสาย USB ในการอัปโหลดโค้ดและดีบักทุกครั้ง'],
  'BLE ออกแบบมาเพื่อข้อมูลน้อยและพลังงานต่ำ ส่วนการส่งขึ้นคลาวด์ระยะไกลใช้ Wi-Fi'),
 ('ทีมต้องการต่อจอ OLED, BMP280 และ MPU6050 พร้อมกันโดยใช้ขาน้อยที่สุด ควรเลือกวิธีใด',
  ['ต่อขนานบนบัส I2C เดียวกัน เพราะแอดเดรส 0x3C, 0x76, 0x68 ไม่ซ้ำกัน',
   'ใช้ UART คนละชุดทั้งสามตัว เพราะ ESP32 มี UART ฮาร์ดแวร์ถึงสามชุด',
   'ใช้ขา ADC สามขาแยกกัน แล้วอ่านค่าด้วย analogRead()',
   'ใช้บัส SPI ร่วมกันโดยไม่ต้องมีขา CS แยกให้แต่ละตัว'],
  'นี่คือจุดแข็งของ I2C อุปกรณ์หลายตัวใช้สายเพียง 2 เส้นตราบใดที่แอดเดรสไม่ชนกัน'),
]

B['district1'] += [
 ('เสียบสาย USB แล้ว Arduino IDE มองไม่เห็นพอร์ตของบอร์ด ESP32 (ไฟ Power LED ติดปกติ) สาเหตุที่ควรตรวจก่อนคือข้อใด',
  ['ไม่มีไดรเวอร์ CP2102/CH340 หรือสาย USB ชาร์จได้อย่างเดียว',
   'ESP32 ต้องเชื่อมต่อ Wi-Fi ให้สำเร็จก่อน คอมพิวเตอร์จึงจะเห็นพอร์ต COM',
   'ต้องถอดโมดูล ESP32 ออกจากบอร์ดพัฒนาก่อนเสียบสาย USB ทุกครั้ง',
   'ต้องจ่ายไฟ 12 V เข้าขา 3V3 เพิ่มเพื่อให้วงจร USB ทำงาน'],
  'ชิป USB-to-UART ต่างรุ่นทำงานเหมือนกันแต่ใช้ไดรเวอร์ต่างกัน และสาย USB ราคาถูกบางเส้นมีแต่สายไฟ ไม่มีสายข้อมูล'),
 ('บอร์ด ESP32 รีเซ็ตเองทุกครั้งที่สั่งรีเลย์และเปิด Wi-Fi พร้อมกัน โดย Serial Monitor แสดงข้อความ Brownout สาเหตุที่น่าจะเป็นที่สุดคือข้อใด',
  ['ไฟเลี้ยงตกชั่วขณะ เพราะแหล่งจ่ายจ่ายกระแสไม่พอ',
   'โค้ดมีคำสั่ง delay() มากเกินไป จน watchdog รีเซ็ตชิป',
   'ESP32 ไม่รองรับรีเลย์ ต้องใช้บอร์ด Arduino Uno แทน',
   'เซนเซอร์อุณหภูมิเสีย จึงส่งสัญญาณรีเซ็ตกลับมาที่บอร์ด'],
  'Brownout Detector เฝ้าแรงดันไฟเลี้ยง เมื่อต่ำกว่าเกณฑ์จะรีเซ็ตชิปเพื่อป้องกันการทำงานผิดเพี้ยน Wi-Fi และขดลวดรีเลย์ทำให้กระแสกระชากพร้อมกัน'),
 ('ข้อใดเรียงลำดับ "ชิป → โมดูล → บอร์ดพัฒนา" ของ ESP32 ได้ถูกต้อง',
  ['ชิป ESP32 → โมดูล WROOM-32 → บอร์ด DevKit',
   'บอร์ด DevKit → ชิป ESP32 → โมดูล WROOM-32 ที่อยู่ใต้ฝาโลหะ',
   'โมดูล WROOM-32 → ชิป ESP32 → บอร์ด DevKit ที่มีพอร์ต USB',
   'ทั้งสามคำหมายถึงสิ่งเดียวกัน ต่างกันแค่ชื่อเรียกทางการค้า'],
  'การรู้ระดับนี้ช่วยอ่าน datasheet ได้ถูก เช่น ขา GPIO6–11 ถูกใช้ภายในโมดูลเพื่อต่อกับ Flash'),
]
B['district3'] += [
 ('GPIO Matrix ของ ESP32 ช่วยนักออกแบบวงจรอย่างไร',
  ['ย้าย UART, I2C, SPI หรือ PWM ไปขาที่ต้องการด้วยซอฟต์แวร์',
   'เพิ่มจำนวนขาจริงของชิปเป็นสองเท่า โดยไม่ต้องเปลี่ยนไปใช้โมดูลรุ่นใหม่',
   'ทำให้ขา GPIO ทุกขาทนแรงดัน 5 V ได้เมื่อเปิดใช้งาน',
   'ใช้สลับสัญญาณ Wi-Fi ไปออกที่ขา GPIO แทนเสาอากาศบนโมดูล'],
  'ตัวอย่างเช่น Wire.begin(sda, scl) หรือ Serial2.begin(9600, SERIAL_8N1, rx, tx) ย้ายบัสไปยังขาที่สะดวกได้ ยกเว้นขาที่มีข้อจำกัดเฉพาะ'),
 ('ขั้นตอนการอัปโหลดโปรแกรมลง ESP32 ข้อใดถูกต้อง',
  ['คอมไพล์เป็น .bin → ส่งผ่าน USB-UART → เขียนลง Flash → รีเซ็ตแล้วรัน',
   'ส่งโค้ดภาษา C ผ่าน Wi-Fi → ESP32 คอมไพล์เอง → รันจาก SRAM ทันที',
   'คอมไพล์เป็น .bin → เขียนลง SRAM → โปรแกรมอยู่ถาวรแม้ปิดไฟ',
   'ถอดชิปออก → เขียนด้วยเครื่องเขียนภายนอก → ใส่ชิปกลับเข้าบอร์ดทุกครั้ง'],
  'ถ้าอัปโหลดค้างที่ Connecting... บางบอร์ดต้องกดปุ่ม BOOT (GPIO0) ค้างไว้เพื่อเข้าโหมดดาวน์โหลด'),
 ('ทีมต้องการทำกล้องตรวจจับใบหน้าบน ESP32 พร้อมเว็บเซิร์ฟเวอร์ ควรเลือกบอร์ดที่มีคุณสมบัติใดเพิ่ม',
  ['มี PSRAM เพิ่ม เพราะภาพจากกล้องและงาน AI ใช้หน่วยความจำมาก',
   'มี ADC ความละเอียดสูงกว่า 12 บิต เพื่ออ่านภาพจากกล้อง',
   'มี LED ที่ GPIO2 เพื่อใช้เป็นไฟแฟลชของกล้องตอนถ่ายภาพกลางคืน',
   'ไม่มีเสาอากาศ เพื่อลดสัญญาณรบกวนที่เข้าสู่เซนเซอร์ภาพ'],
  'SRAM ภายในของ ESP32 ราว 520 KB ไม่พอสำหรับบัฟเฟอร์ภาพ บอร์ดอย่าง ESP32-CAM จึงมี PSRAM ภายนอกเพิ่ม'),
]

STAR = star_table([
 ('PIN CHAMPION', 'อ่านขา ESP32 ขาดทุกยก พร้อมเดินสายโปรเจกต์จริงได้อย่างปลอดภัย'),
 ('GPIO GLADIATOR', 'แม่นยำสูง เหลืออีกจุดเดียวก็เต็ม ตรวจคำอธิบายข้อที่พลาด'),
 ('SIGNAL FIGHTER', 'ผ่านเกณฑ์ความเข้าใจพื้นฐาน ลองเล่นห้องทดลอง ADC กับกับดัก Wi-Fi อีกรอบ'),
 ('WIRE ROOKIE', 'เริ่มจับหลักได้ ควรทบทวนตารางขาห้ามใช้และขา Strapping'),
 ('BREADBOARD TRAINEE', 'พอมีพื้นฐาน แนะนำให้เล่นห้องทดลองให้ครบทั้ง 3 ยกก่อนสอบใหม่'),
 ('FIRST POWER-ON', 'ยังไม่คุ้นเนื้อหา ไม่เป็นไร เริ่มจากยกแรกแล้วตรวจขาทีละขา'),
])

BADGES = r"""[
  {id:'perfect',  name:'UNDEFEATED',      desc:'Posttest ถูกครบ 6 ข้อ',                  test:s => s.post === 6},
  {id:'zero2hero',name:'COMEBACK ROUND',  desc:'คะแนนเพิ่มขึ้น 3 ข้อขึ้นไปจาก Pretest',     test:s => (s.post - s.pre) >= 3},
  {id:'fast',     name:'FAST TRIGGER',    desc:'ตอบถูกภายใน 8 วินาที',                   test:s => s.fastCorrect},
  {id:'labrat',   name:'PIN INSPECTOR',   desc:'เล่นห้องทดลองครบทั้งสามยก',               test:s => s.labs.lab1.length >= 10 && s.labs.lab2.length >= 5 && s.labs.lab3.length >= 6},
  {id:'combo',    name:'COMBO BREAKER',   desc:'ตอบถูกติดกัน 5 ข้อขึ้นไป',               test:s => s.maxCombo >= 5},
  {id:'sweep',    name:'TRIPLE KO',       desc:'ได้ 2/2 ครบทั้งสามยก',                   test:s => s.postByD.district1 === 2 && s.postByD.district2 === 2 && s.postByD.district3 === 2}
]"""

ADVICE = r"""
  const tips=[];
  if(labCount('lab1')<10) tips.push('ตรวจขาบนบอร์ดให้ครบอย่างน้อย 10 ขา โดยเฉพาะ GPIO6–11, 12 และ 34–39 ซึ่งเป็นจุดที่ทำให้โปรเจกต์ล้มบ่อยที่สุด');
  if(labCount('lab2')<5) tips.push('ลองเปิด Wi-Fi แล้วอ่านค่าที่ขา ADC2 ในห้องทดลอง เพื่อจำให้ขึ้นใจว่าเซนเซอร์แอนะล็อกของงาน IoT ต้องอยู่บน ADC1');
  if(labCount('lab3')<6) tips.push('จับคู่โมดูลกับบัสให้ครบ แล้วนำตารางไปใช้วางแผนขาของโปรเจกต์กลุ่มทันที');
  if(postInfo.stars===6) tips.push('ได้ครบ 6 ดาวแล้ว ขั้นต่อไปคือทำ "ตารางจัดสรรขา (Pin Map)" ของโปรเจกต์กลุ่มให้ครบทุกอุปกรณ์ก่อนต่อวงจรจริง');
  return tips;
"""

CFG = {
    'filename': 'game2_pin_wars.html',
    'title': 'PIN WARS : สังเวียนขา ESP32',
    'brand': 'PIN WARS',
    'edition': 'ARENA EDITION',
    'desc': 'เกมทบทวนขา ESP32: ลอจิก 3.3 V ขาห้ามใช้ ขา Strapping ADC1/ADC2 PWM I2C SPI UART — CPE2422/2428 · ผศ.ดร.กุลวลัญช์ วรุณสิน มหาวิทยาลัยรามคำแหง',
    'ogdesc': 'สามยกในสังเวียนขา ESP32 เลือกขาให้ถูกก่อนวงจรจะพัง วัดผลก่อน-หลังเรียนด้วยระบบดาว 6 ดวง',
    'favicon': "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%23110906'/><rect x='28' y='18' width='44' height='64' rx='6' fill='none' stroke='%23ff7a30' stroke-width='7'/><circle cx='40' cy='38' r='6' fill='%2338bdf8'/><circle cx='60' cy='62' r='6' fill='%23fbbf24'/></svg>",
    'theme': THEME,
    'extra_css': EXTRA_CSS,
    'arcade_label': 'ด่านไต่อัฒจันทร์สังเวียน',
    'hero_svg': HERO,
    'subtitle': 'สวมบทบาท <b>นักสู้วงจร</b> ขึ้นสังเวียน 3 ยกกับบอร์ด ESP32 ยกแรกแยกขาปลอดภัยกับขาอันตราย ยกสองศึกดิจิทัลปะทะแอนะล็อกและกับดัก Wi-Fi ยกสุดท้ายศึกสายสื่อสาร I2C, SPI, UART และ 1-Wire สะสม XP และดาว วัดพัฒนาการก่อน–หลังเรียน',
    'login_tag': 'Fighter Registration',
    'features': '<span>CPE2422 · คลิปทบทวนที่ 2</span><span>GPIO · ADC · PWM · BUS</span><span>PRETEST / POSTTEST</span><span>ระบบดาว 6 ดวง</span><span>XP &amp; COMBO</span><span>ส่งออกคะแนน CSV</span>',
    'climb_text': 'ตัวละครไต่อัฒจันทร์ขึ้น 1 ชั้น ทันที',
    'zones_html': ZONES,
    'checks': [('Round 01', 'ขาไหนปลอดภัย'), ('Round 02', 'ดิจิทัลปะทะแอนะล็อก'), ('Round 03', 'ศึกสายสื่อสาร')],
    'post_desc': '6 ข้อใหม่ (ยกละ 2 ข้อ) เพื่อวัดความเข้าใจหลังผ่านครบทั้ง 3 ยกในสังเวียน',
    'report_tag': 'Fight Report',
    'course': COURSE.split(' · ')[0],
    'footer_line': 'เกมทบทวนคลิปที่ 2: ESP32 Explained — GPIO, Pins &amp; More — ภาคเรียนที่ 1/2569',
    'bank': bank_js(B),
    'skill_labels': "{district1:'ความปลอดภัยของขา', district2:'ดิจิทัล แอนะล็อก PWM', district3:'บัสสื่อสาร & ไร้สาย'}",
    'skey': 'cpe_pinwars_v1_state',
    'star_table': STAR,
    'navstops': navstops('R1 SAFE', 'R2 SIGNAL', 'R3 BUS'),
    'lock_msg': 'ยกนี้ยังไม่ปลดล็อก สู้ตามลำดับก่อนนะครับ',
    'act': {'floor': 'ชั้น', 'top': 'แชมป์สังเวียน', 'ground': 'ข้างเวที', 'theme': 'arena'},
    'pre_sub': 'นี่คือเส้นฐานของคุณ — เดี๋ยวเรามาวัดกันใหม่หลังสู้ครบทั้ง 3 ยก',
    'go_first': 'ขึ้นยกแรก',
    'lab_js': LAB_JS,
    'lab_wiring': LAB_WIRING,
    'init_extra': INIT_EXTRA,
    'badges': BADGES,
    'advice_js': ADVICE,
    'role': 'นักสู้วงจร',
    'filekey': 'CPE2422_G2_pinwars',
    'avatars': avatars('#24130b', ['#ff7a30', '#38bdf8', '#fbbf24', '#ef4444', '#7dd3fc', '#ffa26b']),
}
