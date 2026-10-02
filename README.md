# CPE2422/2428 · IoT Maker Quest

ชุดเกมบทเรียนอินเทอร์แอคทีฟ 4 ด่าน สำหรับวิชา **CPE2422 อิเล็กทรอนิกส์วิศวกรรม** และ **CPE2428 ปฏิบัติการอิเล็กทรอนิกส์วิศวกรรม**
คณะวิศวกรรมศาสตร์ มหาวิทยาลัยรามคำแหง ภาคเรียนที่ 1/2569 — เล่นได้ทันทีบนเบราว์เซอร์มือถือ ไม่ต้องติดตั้งแอป

**เข้าเล่น:** `https://<ชื่อบัญชี>.github.io/cpe2422-iot-maker-quest/` (เติมหลังเปิด GitHub Pages)

## รายชื่อด่าน

| ด่าน | ชื่อ | เนื้อหา | ห้องทดลองที่กดเล่นได้ | คลังข้อสอบ |
|---|---|---|---|---|
| 1 | BRAIN CORE | คลิป 1: MCU กับ MPU · Flash/SRAM/EEPROM · ADC · setup/loop · millis · Interrupt · Watchdog | Device Sorter · Chip X-Ray + เครื่องแปลง ADC · Loop Simulator | 39 ข้อ |
| 2 | PIN WARS | คลิป 2: บอร์ด ESP32 · 3.3 V · ขาห้ามใช้/Strapping/อินพุตอย่างเดียว · ADC1/ADC2 · PWM/DAC · I2C/SPI/UART/1-Wire | Pin Inspector 27 ขา · ADC + กับดัก Wi-Fi + INPUT_PULLUP · Bus Matchmaker | 42 ข้อ |
| 3 | SENSOR HUNTER | คลิป 3: เซนเซอร์ 38 ชนิด · AO/DO · วงจรแบ่งแรงดัน · HX711/RC522/Relay | Sensor Dex 38 ใบ · Ultrasonic + PIR/เรดาร์ · Divider Builder | 42 ข้อ |
| 4 | PROJECT LAUNCHPAD | โปรเจกต์ S1–S7: IPO · ตัวขับโหลด · Hysteresis · แจ้งเตือน IoT · ค่ามาตรฐาน | Project Builder · Driver Chooser · Hysteresis Simulator | 36 ข้อ |

## คุณสมบัติ (สืบทอดจาก GNR1007 Learning Game Series UI v7.0)

- ลงทะเบียนด้วยรหัสนักศึกษา 10 หลัก (หรือรหัสลับผู้สอน) + ชื่อเล่น · หน้าแผนที่ภารกิจแสดงดาวสะสมและด่านถัดไป
- CLIMB MODE แตะอย่างเดียว · Pretest/Posttest ด่านย่อยละ 2 ข้อ ไม่ซ้ำกัน · สลับตัวเลือกทุกครั้ง
- เรดาร์ Pre vs Post · เหรียญตรา 6 ใบ · คำแนะนำเฉพาะบุคคล · ส่งออก CSV สำหรับผู้สอน · โหมดมืด/สว่าง
- ธีม NEO ARCADE: ทุกหน้าแสดงจบในจอเดียว (ไม่ต้องเลื่อน) รองรับมือถือ–จอใหญ่ · ทฤษฎีเป็นสไลด์การ์ดทีละใบ + Boss Check · สีประจำด่านแยกกัน 4 โทน
- ส่วนประกอบบนบอร์ด: เมื่อเนื้อหาพูดถึงชิป USB→UART, Flash, SRAM, PSRAM, เรกูเลเตอร์, เสาอากาศ, ปุ่ม EN/BOOT, พอร์ต USB หรือ LED ภาพบอร์ดจะกรอบเรืองแสงและป้ายชี้ตำแหน่งจริง (เปิดมุมมองใต้ฝาโลหะเมื่ออ้างถึงชิ้นส่วนภายในโมดูล) · ชี้/แตะแถวตารางเพื่อเน้นเฉพาะเรื่องนั้น
- ผังขา ESP32 แบบเหมือนจริง: ทุกสไลด์ที่อ้างถึงขาจะแสดงบอร์ดประกอบและเน้นขานั้น · ปุ่ม PIN บนแถบบนและในด่านอาร์เคดเปิดผังเต็มจอ แตะขาเพื่อดูหน้าที่/ข้อควรระวัง · สลับได้ระหว่าง ESP32-DevKitC V4 38 ขา (บอร์ดในคลิป) และ DevKit V1 30 ขา (ข้อมูลขาตาม Espressif DevKitC V4 User Guide)
- ไฟล์ HTML เดียวจบต่อด่าน ไม่มี backend · ผลคะแนนเก็บใน `localStorage` แยกตามรหัสนักศึกษา (คีย์ `cpe2422_*` ไม่ชนกับ GNR1007)

## วิธีสร้างใหม่หลังแก้เนื้อหา (สำหรับผู้ดูแล)

```bash
python3 tools/cpe_build.py            # สร้าง game1–4 จาก tools/games_src/*.py + template_game4.html
python3 tools/cpe_core/apply_core.py . # ติดตั้งชั้น UI v7.0 (ลงทะเบียน แผนที่ ธีม) ลงทุกเกม
python3 tools/neo/apply_neo.py .       # ติดตั้งชั้น NEO ARCADE (จอเดียวไม่ต้องเลื่อน · สไลด์การ์ดทฤษฎี · Mission Briefing · สรุปภารกิจ)
                                       # เนื้อหาการ์ด (BIG IDEA / ตัวเลข / กับดัก) แก้ที่ tools/games_src/neo_cards.py
                                       # ผังขา ESP32 และข้อมูลขาแต่ละขา แก้ที่ tools/neo/pinout.js
python3 tools/make_index.py            # สร้าง index.html
python3 tools/make_answer_key.py       # สร้างคลังข้อสอบ+เฉลย ไว้นอก repo (ห้ามเผยแพร่)
python3 tools/qa_headless.py game1_brain_core.html   # ทดสอบเล่นอัตโนมัติ (ต้องมี playwright)
```

แก้ข้อสอบ/บทเรียน/ห้องทดลองที่ `tools/games_src/gN_*.py` (ตัวเลือกแรกของแต่ละข้อคือคำตอบที่ถูก เอนจินสลับให้เอง)
ชื่อไฟล์เกมคงที่ตลอดเทอม เพื่อให้ URL และ QR code ที่แจกไปแล้วยังใช้ได้

## เครดิต

ผศ.ดร.กุลวลัญช์ วรุณสิน · สาขาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยรามคำแหง
อ้างอิงเนื้อหาคลิป: The Brain Behind Everything (Mechatinker) · ESP32 Explained (Technifyi) · 38 Arduino Sensors You Should Know
