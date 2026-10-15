/* ================================================================
   NEO PINOUT v1.0 — ผังขา ESP32 แบบเหมือนจริง (มุมมองด้านบน เสาอากาศอยู่ด้านบน)
   - ESP32-DevKitC V4 38 ขา (บอร์ดในคลิป ESP32 Explained) และ ESP32 DevKit V1 (DOIT) 30 ขา
   - NeoPin.detect(text)  -> รายการขาที่ถูกอ้างถึงในข้อความ
   - NeoPin.figure(el, pins) -> วาดผังแบบย่อ (เน้นเฉพาะขาที่อ้างถึง) ลงใน el
   - NeoPin.open(pins)     -> เปิดผังเต็มจอ แตะขาเพื่อดูรายละเอียด
   ข้อมูลขาอ้างอิง Espressif ESP32 Datasheet / ESP32-DevKitC V4 User Guide
   ================================================================ */
(function(){
  'use strict';
  var D=document;

  /* ---------- ข้อมูลหมวดขา ---------- */
  var CAT={
    safe :{c:'#22c55e',n:'ใช้งานทั่วไป (แนะนำ)'},
    input:{c:'#a855f7',n:'อินพุตอย่างเดียว'},
    strap:{c:'#f59e0b',n:'Strapping ระวังตอนบูต'},
    flash:{c:'#64748b',n:'ต่อ Flash ภายใน ห้ามใช้'},
    uart :{c:'#3b82f6',n:'UART0 / USB Serial'},
    pwr  :{c:'#ef4444',n:'ไฟเลี้ยง'},
    gnd  :{c:'#9aa3b5',n:'กราวด์ (GND)'},
    en   :{c:'#f97316',n:'รีเซ็ต (EN)'},
    part :{c:'#22d3ee',n:'ส่วนประกอบบนบอร์ด'}
  };
  /* ส่วนประกอบบนบอร์ด: [ชื่อ, คำอธิบายสั้น, รายละเอียด] */
  var PART={
    antenna:['เสาอากาศ PCB','Wi-Fi · BT 2.4 GHz','เสาอากาศลายทองแดงบนแผ่นวงจร รับส่ง Wi-Fi และ Bluetooth ย่าน 2.4 GHz ห้ามวางโลหะหรือสายไฟทับบริเวณนี้ และควรหันส่วนนี้ออกนอกกล่องโลหะ'],
    module :['โมดูล WROOM-32','ชิป+Flash+เสาอากาศ','ESP32-WROOM-32 รวมชิป ESP32, หน่วยความจำ Flash, คริสตัล 40 MHz และเสาอากาศไว้ด้วยกันใต้ฝาโลหะ ผ่านการรับรองคลื่นวิทยุแล้ว ผู้ผลิตบอร์ดจึงนำไปวางบนบอร์ดพัฒนาได้ทันที'],
    chip   :['ชิป ESP32','CPU 2 คอร์ 240 MHz','ชิป ESP32-D0WD อยู่ใต้ฝาโลหะของโมดูล มีซีพียู Xtensa LX6 2 คอร์ ความถี่สูงสุด 240 MHz พร้อม Wi-Fi, Bluetooth และวงจร ADC/DAC/PWM ในชิปเดียว'],
    sram   :['SRAM ในชิป','520 KB · ไฟดับข้อมูลหาย','SRAM ขนาด 520 KB อยู่ภายในชิป ESP32 ใช้เก็บตัวแปรระหว่างโปรแกรมทำงาน เร็วมาก แต่ข้อมูลหายเมื่อปิดไฟหรือรีเซ็ต'],
    flash  :['Flash 4 MB','เก็บโปรแกรม ไม่หาย','หน่วยความจำ Flash แบบ SPI (ทั่วไป 4 MB) อยู่ใต้ฝาโลหะ เก็บโปรแกรมและไฟล์ไว้แม้ปิดไฟ เชื่อมกับชิปผ่าน GPIO6–11 จึงห้ามนำขาเหล่านั้นไปใช้'],
    psram  :['PSRAM','เฉพาะรุ่น WROVER','หน่วยความจำทำงานเสริม 4–8 MB มีเฉพาะโมดูล WROVER (เช่น บอร์ดกล้อง ESP32-CAM) เหมาะกับงานภาพและ AI โมดูล WROOM-32 บนบอร์ดนี้ไม่มี PSRAM'],
    xtal   :['คริสตัล 40 MHz','นาฬิกาหลักของชิป','คริสตัลสร้างสัญญาณนาฬิกา 40 MHz ให้ชิปและวงจรวิทยุ อยู่ใต้ฝาโลหะของโมดูล'],
    usbuart:['ชิป USB→UART','CP2102 / CH340','ชิปแปลงสัญญาณ USB เป็น UART (CP2102, CH340 หรือ CH9102 ทำหน้าที่เดียวกัน) ใช้อัปโหลดโค้ดและ Serial Monitor ผ่าน GPIO1/GPIO3 ถ้าคอมพิวเตอร์มองไม่เห็นพอร์ต COM ให้ติดตั้งไดรเวอร์ให้ตรงรุ่นชิป หรือเปลี่ยนเป็นสาย USB ที่ส่งข้อมูลได้'],
    usb    :['พอร์ต USB','ไฟ 5 V + ข้อมูล','พอร์ต micro-USB (บางรุ่นเป็น USB-C) รับไฟ 5 V เข้าบอร์ดและรับส่งข้อมูลผ่านชิป USB→UART สายชาร์จบางเส้นมีแต่สายไฟ ไม่มีสายข้อมูล จึงอัปโหลดโค้ดไม่ได้'],
    reg    :['เรกูเลเตอร์','5 V → 3.3 V','เรกูเลเตอร์แบบ LDO (เช่น AMS1117-3.3) แปลงไฟ 5 V จาก USB/VIN เป็น 3.3 V เลี้ยงชิปและขา 3V3 พิกัดราว 0.8–1 A และร้อนขึ้นเมื่อโหลดมาก ห้ามดึงไฟจากขา 3V3 ไปขับมอเตอร์'],
    en     :['ปุ่ม EN','รีเซ็ตชิป','ปุ่ม EN ดึงขา CHIP_PU ลงกราวด์ เมื่อปล่อยชิปจะรีเซ็ตและเริ่มโปรแกรมใหม่จาก setup()'],
    boot   :['ปุ่ม BOOT','GPIO0 · โหมดอัปโหลด','ปุ่ม BOOT ต่อกับ GPIO0 ถ้าอัปโหลดค้างที่ "Connecting..." ให้กด BOOT ค้างไว้จนเริ่มเขียนโค้ด หลังบูตแล้วใช้เป็นปุ่มอินพุตได้'],
    pwr    :['LED ไฟเลี้ยง','แดง = มีไฟเข้า','LED สีแดงติดเมื่อบอร์ดได้รับไฟ ถ้าไม่ติดให้ตรวจสายและพอร์ต USB ก่อนตรวจอย่างอื่น'],
    modpad :['ขา 6–11 ที่โมดูล','ต่อ Flash · ไม่ออกหัวเข็ม','บนบอร์ด 30 ขา GPIO6–11 ไม่ได้ต่อออกมาที่หัวเข็ม แต่ยังอยู่ที่ขาด้านล่างของโมดูล WROOM-32 (ขาโมดูลที่ 17–22: SD2=GPIO9, SD3=GPIO10, CMD=GPIO11, CLK=GPIO6, SD0=GPIO7, SD1=GPIO8) ซึ่งต่อกับชิป Flash ภายใน จึงห้ามนำไปใช้'],
    led2   :['LED GPIO2','เฉพาะ DevKit V1','บอร์ด DevKit V1 (DOIT) มี LED สีฟ้าต่อกับ GPIO2 ใช้ทดสอบโปรแกรมไฟกะพริบได้ทันที ส่วน DevKitC ไม่มี LED ผู้ใช้']
  };
  function isPart(k){ return typeof k==='string'&&k.indexOf('p:')===0; }
  function pid(k){ return String(k).slice(2); }
  var G={
    0 :['strap','BOOT · ADC2 · T1','ขา Strapping ต่อกับปุ่ม BOOT ถ้าเป็น LOW ขณะเปิดเครื่อง ชิปจะเข้าโหมดอัปโหลดโค้ด ใช้อ่านปุ่มได้ แต่ห้ามมีวงจรภายนอกดึงลงตอนบูต'],
    1 :['uart','TX0 · USB Serial','UART0 ส่งข้อมูลไปยังชิป USB-to-UART ใช้กับ Serial Monitor และการอัปโหลดโค้ด ไม่ควรต่ออุปกรณ์อื่น'],
    2 :['strap','ADC2 · T2 · LED*','ขา Strapping ต้องเป็น LOW หรือปล่อยลอยตอนเข้าโหมดอัปโหลด บอร์ด DevKit V1 (DOIT) ต่อ LED สีฟ้าไว้ที่ขานี้ ส่วน DevKitC ไม่มี LED ผู้ใช้'],
    3 :['uart','RX0 · USB Serial','UART0 รับข้อมูลจากชิป USB-to-UART ไม่ควรต่ออุปกรณ์อื่น'],
    4 :['safe','ADC2 · T0','ใช้งานทั่วไปได้ดี: ดิจิทัล PWM และ 1-Wire (DHT22, DS18B20) แต่ ADC2 อ่านค่าไม่ได้ขณะเปิด Wi-Fi'],
    5 :['strap','VSPI CS','ขา Strapping (ส่งสัญญาณ PWM ช่วงบูต) เป็นขา CS เริ่มต้นของ SPI ใช้ได้แต่ระวังอุปกรณ์ที่ทำงานผิดเมื่อได้รับสัญญาณช่วงบูต'],
    6 :['flash','FLASH CLK','ต่อกับหน่วยความจำ Flash ภายในโมดูล ห้ามใช้ ถ้านำไปต่ออุปกรณ์ บอร์ดจะรีเซ็ตหรือค้าง'],
    7 :['flash','FLASH SD0','ต่อกับหน่วยความจำ Flash ภายในโมดูล ห้ามใช้'],
    8 :['flash','FLASH SD1','ต่อกับหน่วยความจำ Flash ภายในโมดูล ห้ามใช้'],
    9 :['flash','FLASH SD2','ต่อกับหน่วยความจำ Flash ภายในโมดูล ห้ามใช้'],
    10:['flash','FLASH SD3','ต่อกับหน่วยความจำ Flash ภายในโมดูล ห้ามใช้'],
    11:['flash','FLASH CMD','ต่อกับหน่วยความจำ Flash ภายในโมดูล ห้ามใช้'],
    12:['strap','ADC2 · T5 · HSPI MISO','ขา Strapping (MTDI) ต้องเป็น LOW ตอนบูต ถ้าถูกดึงเป็น HIGH บอร์ดจะบูตไม่ขึ้น ห้ามต่อ pull-up'],
    13:['safe','ADC2 · T4 · HSPI MOSI','ใช้งานทั่วไปได้ (ADC2 อ่านค่าไม่ได้ขณะเปิด Wi-Fi)'],
    14:['safe','ADC2 · T6 · HSPI CLK','ใช้งานได้ แต่ส่ง PWM สั้นๆ ช่วงบูต จึงไม่เหมาะกับรีเลย์ที่ต้องไม่กระตุก'],
    15:['strap','ADC2 · T3 · HSPI CS','ขา Strapping (MTDO) ส่ง PWM ช่วงบูต ถ้าเป็น LOW จะปิดข้อความบูตบน Serial'],
    16:['safe','RX2 · UART2','UART2 ฝั่งรับ เหมาะกับ GPS, PMS5003, LD2410 (บนโมดูล WROVER ใช้กับ PSRAM ห้ามใช้)'],
    17:['safe','TX2 · UART2','UART2 ฝั่งส่ง (บนโมดูล WROVER ใช้กับ PSRAM ห้ามใช้)'],
    18:['safe','VSPI SCK','สัญญาณนาฬิกาของ SPI เริ่มต้น ใช้งานทั่วไปได้ดี'],
    19:['safe','VSPI MISO','ขาข้อมูลเข้าของ SPI เริ่มต้น ใช้งานทั่วไปได้ดี'],
    21:['safe','I2C SDA','ขาข้อมูล I2C เริ่มต้นของ Arduino (Wire) เช่น OLED, BME280, BH1750, MPU6050'],
    22:['safe','I2C SCL','ขานาฬิกา I2C เริ่มต้นของ Arduino (Wire)'],
    23:['safe','VSPI MOSI','ขาข้อมูลออกของ SPI เริ่มต้น ใช้งานทั่วไปได้ดี'],
    25:['safe','DAC1 · ADC2','มี DAC 8 บิต สร้างแรงดันอนาล็อกจริงได้ ใช้ดิจิทัลและ PWM ได้ดี'],
    26:['safe','DAC2 · ADC2','มี DAC 8 บิต สร้างแรงดันอนาล็อกจริงได้ ใช้ดิจิทัลและ PWM ได้ดี'],
    27:['safe','ADC2 · T7','ใช้งานทั่วไปได้ดี (ADC2 อ่านค่าไม่ได้ขณะเปิด Wi-Fi)'],
    32:['safe','ADC1 · T9','ADC1 อ่านอนาล็อกได้แม้เปิด Wi-Fi เหมาะกับเซนเซอร์อนาล็อกในงาน IoT'],
    33:['safe','ADC1 · T8','ADC1 อ่านอนาล็อกได้แม้เปิด Wi-Fi เหมาะกับเซนเซอร์อนาล็อกในงาน IoT'],
    34:['input','ADC1 · INPUT ONLY','อินพุตอย่างเดียว ไม่มี pull-up/pull-down ภายใน เหมาะกับอ่านเซนเซอร์อนาล็อก (ADC1) ห้ามใช้ขับ LED'],
    35:['input','ADC1 · INPUT ONLY','อินพุตอย่างเดียว ไม่มี pull-up/pull-down ภายใน เหมาะกับอ่านเซนเซอร์อนาล็อก (ADC1)'],
    36:['input','VP · ADC1 · INPUT','SENSOR_VP อินพุตอย่างเดียว ไม่มี pull-up/pull-down ภายใน (ADC1 ช่อง 0)'],
    39:['input','VN · ADC1 · INPUT','SENSOR_VN อินพุตอย่างเดียว ไม่มี pull-up/pull-down ภายใน (ADC1 ช่อง 3)']
  };
  var SP={
    '3V3':['pwr','3.3 V OUT','ไฟ 3.3 V จากเรกูเลเตอร์บนบอร์ด ใช้เลี้ยงเซนเซอร์ 3.3 V (ระวังโหลดรวมเกินความสามารถของเรกูเลเตอร์)'],
    '5V' :['pwr','5 V · USB/VIN','ไฟ 5 V จากพอร์ต USB หรือป้อนไฟ 5 V เข้าที่ขานี้ ห้ามนำ 5 V ไปต่อเข้าขา GPIO'],
    'GND':['gnd','0 V','กราวด์ร่วม ทุกอุปกรณ์ในวงจรต้องต่อ GND ร่วมกับ ESP32'],
    'EN' :['en','RESET','Chip Enable ต่อกับปุ่ม EN ดึงเป็น LOW แล้วปล่อย = รีเซ็ตชิป']
  };
  function info(k){ if(isPart(k)){ var P=PART[pid(k)]; return P?['part',P[1],P[2]]:null; } return typeof k==='number'?G[k]:SP[k]; }
  function nameOf(k){ if(isPart(k)) return (PART[pid(k)]||[k])[0]; return typeof k==='number'?'GPIO'+k:k; }

  /* ---------- เลย์เอาต์ขาจริง (บนลงล่าง เมื่อเสาอากาศอยู่ด้านบน) ---------- */
  var BOARDS={
    c38:{t:'ESP32-DevKitC V4 · 38 ขา',s:'บอร์ดในคลิป ESP32 Explained',
      L:['3V3','EN',36,39,34,35,32,33,25,26,27,14,12,'GND',13,9,10,11,'5V'],
      R:['GND',23,22,1,3,21,'GND',19,18,5,17,16,4,0,2,15,8,7,6],
      SL:['3V3','EN','VP','VN','34','35','32','33','25','26','27','14','12','GND','13','D2','D3','CMD','5V'],
      SR:['GND','23','22','TX','RX','21','GND','19','18','5','17','16','4','0','2','15','D1','D0','CLK']},
    v30:{t:'ESP32 DevKit V1 (DOIT) · 30 ขา',s:'บอร์ดยอดนิยมในชุดทดลอง',
      L:['EN',36,39,34,35,32,33,25,26,27,14,12,13,'GND','5V'],
      R:[23,22,1,3,21,19,18,5,17,16,4,2,15,'GND','3V3'],
      SL:['EN','VP','VN','D34','D35','D32','D33','D25','D26','D27','D14','D12','D13','GND','VIN'],
      SR:['D23','D22','TX0','RX0','D21','D19','D18','D5','TX2','RX2','D4','D2','D15','GND','3V3']}
  };
  var VALID=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23,25,26,27,32,33,34,35,36,39];
  var boardSel='c38';
  try{ boardSel=localStorage.getItem('cpe2422_board')||'c38'; }catch(e){}
  if(!BOARDS[boardSel]) boardSel='c38';

  /* ---------- ตรวจจับการอ้างถึงขาในข้อความ ---------- */
  function addRange(set,a,b){ a=+a; b=+b; if(b<a||b-a>12) return; for(var i=a;i<=b;i++) if(VALID.indexOf(i)>=0) set.push(i); }
  function detect(text,force){
    text=String(text||'').replace(/\s+/g,' ');
    var out=[], m, ctx=!!force||/ESP32|GPIO|ขา/.test(text);
    var re1=/(?:GPIO|\bIO)\s?(\d{1,2})((?:\s*(?:\([^)]{1,10}\))?\s*(?:,|และ|หรือ|\/|–|-|~|ถึง)\s*(?:GPIO)?\s?\d{1,2}\b)*)/g;
    while((m=re1.exec(text))){
      var seq=(m[1]+m[2]).replace(/\([^)]*\)/g,' ').replace(/GPIO/g,' ');
      var parts=seq.split(/\s*(,|และ|หรือ|\/)\s*/);
      parts.forEach(function(p){ var r=/^(\d{1,2})\s*(?:–|-|~|ถึง)\s*(\d{1,2})$/.exec(p.trim()); if(r) addRange(out,r[1],r[2]); else { var n=parseInt(p,10); if(!isNaN(n)&&VALID.indexOf(n)>=0) out.push(n); } });
    }
    var re2=/ขา\s*(\d{1,2})\s*(?:–|-|ถึง)\s*(\d{1,2})/g; while((m=re2.exec(text))) addRange(out,m[1],m[2]);
    var re3=/(\d{1,2})\s*(?:–|-)\s*(\d{1,2})\s*ขา/g; while((m=re3.exec(text))) addRange(out,m[1],m[2]);
    var re4=/ขา\s*(?:GPIO\s?)?(\d{1,2})(?![\d.]|\s*(?:–|-)|\s*(?:ขา|มม|mm|V|โวลต์|ตัว|เส้น|บิต|นาที))/g; while((m=re4.exec(text))){ var n=+m[1]; if(VALID.indexOf(n)>=0) out.push(n); }
    if(ctx){
      if(/\b3V3\b|3\.3\s?V/.test(text)) out.push('3V3');
      if(/\bVIN\b|\b5\s?V\b/.test(text)) out.push('5V');
      if(/\bGND\b|กราวด์/.test(text)) out.push('GND');
      if(/\bI2C\b|\bSDA\b|\bSCL\b/.test(text)) out.push(21,22);
      if(/\bVSPI\b|\bSPI\b(?!\s*Flash)|\bMOSI\b|\bMISO\b/.test(text)) out.push(5,18,19,23);
      if(/\bDAC\b/.test(text)) out.push(25,26);
      if(/UART2|\bRX2\b|\bTX2\b/.test(text)) out.push(16,17);
      if(/UART0|\bTX0\b|\bRX0\b/.test(text)) out.push(1,3);
      if(/strapping/i.test(text)) out.push(0,2,5,12,15);
      if(/อินพุตอย่างเดียว|input[- ]only/i.test(text)) out.push(34,35,36,39);
      if(/ADC1/.test(text)) out.push(32,33,34,35,36,39);
      if(/ADC2/.test(text)) out.push(0,2,4,12,13,14,15,25,26,27);
      if(/ขา[^.]{0,24}Flash|Flash[^.]{0,24}ขา|SPI Flash/.test(text)) out.push(6,7,8,9,10,11);
      if(/\bBOOT\b/.test(text)) out.push(0);
      if(/\bEN\b/.test(text)) out.push('EN');
    }
    var board=!!force||/ESP32|บอร์ด|โมดูล|WROOM|WROVER|GPIO|DevKit|Arduino IDE/.test(text), pp=[];
    if(board){
      if(/เสาอากาศ|antenna|Bluetooth|\bBLE\b|2\.4\s?GHz/i.test(text)) pp.push('antenna');
      if(/WROOM|WROVER|ชิป\s*(?:ESP32\s*)?(?:→|->)\s*โมดูล|ฝาโลหะ|โมดูล ESP32|ESP32 Module/i.test(text)) pp.push('module');
      if(/ชิป ESP32|\bSoC\b|Xtensa|ดูอัลคอร์|dual[- ]core|2 คอร์|240\s?MHz|ซีพียู|\bCPU\b|ประมวลผล/i.test(text)) pp.push('chip');
      if(/\bSRAM\b|520\s?KB/.test(text)) pp.push('sram');
      if(/Flash/.test(text)) pp.push('flash');
      if(/PSRAM/.test(text)) pp.push('psram');
      if(/คริสตัล|crystal|40\s?MHz/i.test(text)) pp.push('xtal');
      if(/USB[- ]?to[- ]?UART|USB\s?→\s?UART|CP210[24]|CH340|CH9102|ไดรเวอร์|พอร์ต COM|\bCOM\d?\b|มองไม่เห็นพอร์ต/i.test(text)) pp.push('usbuart');
      if(/USB/.test(text)) pp.push('usb');
      if(/เรกูเลเตอร์|regulator|AMS1117|\bLDO\b/i.test(text)) pp.push('reg');
      if(/ปุ่ม\s?EN\b|ปุ่ม\s?RESET|ปุ่มรีเซ็ต|กด\s?EN\b|พอร์ต USB\s*ปุ่ม|ปุ่มบนบอร์ด/i.test(text)) pp.push('en');
      if(/ปุ่ม\s?BOOT|\bBOOT\b|โหมดอัปโหลด|download mode|Connecting\.\.\.|พอร์ต USB\s*ปุ่ม|ปุ่มบนบอร์ด/i.test(text)) pp.push('boot');
      if(/Power LED|LED ไฟเลี้ยง|ไฟ\s?Power|\bPWR\b|ไฟสถานะ/i.test(text)) pp.push('pwr');
      if(/LED_BUILTIN|LED บนบอร์ด|LED ผู้ใช้|GPIO2[^.]{0,30}LED|LED[^.]{0,30}GPIO2/.test(text)) pp.push('led2');
    }
    pp.forEach(function(x){ out.push('p:'+x); });
    var seen={}, res=[]; out.forEach(function(k){ var id=String(k); if(!seen[id]){ seen[id]=1; res.push(k); } });
    return res;
  }

  /* ---------- วาดบอร์ด (หน่วย 0.1 มม.) ---------- */
  var UID=0;
  var W=279, PITCH=25.4;
  function boardSVG(bk,opt){
    opt=opt||{}; var B=BOARDS[bk], n=B.L.length, id='np'+(++UID);
    var H=n===19?544:515, y0=n===19?44:52, xl=22, xr=W-22;
    var hl={}, parts=[]; (opt.pins||[]).forEach(function(k){ if(isPart(k)) parts.push(pid(k)); else hl[String(k)]=1; });
    if(bk!=='v30') parts=parts.filter(function(p){ return p!=='led2'; });
    if([6,7,8,9,10,11].some(function(k){ return hl[String(k)]&&B.L.indexOf(k)<0&&B.R.indexOf(k)<0; })&&parts.indexOf('modpad')<0) parts.push('modpad');
    var any=Object.keys(hl).length>0||parts.length>0, compact=!!opt.compact, hasParts=parts.length>0;
    var xray=parts.some(function(p){ return /^(chip|sram|flash|psram|xtal)$/.test(p); });
    var LBW=compact?(hasParts&&!opt.numbers?162:132):300;
    var vb=opt.quiz?[-34,-34,W+68,H+52]:(compact?[-LBW,-26,W+LBW*2,H+40]:[-LBW,-34,W+LBW*2,H+76]);
    var s='<svg class="np-svg" viewBox="'+vb.join(' ')+'" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ผังขา '+B.t+'">';
    s+='<defs>'+
      '<linearGradient id="'+id+'pcb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b1f29"/><stop offset=".55" stop-color="#0d1017"/><stop offset="1" stop-color="#161a23"/></linearGradient>'+
      '<linearGradient id="'+id+'sh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eef1f4"/><stop offset=".35" stop-color="#c3c9d1"/><stop offset=".6" stop-color="#e2e6ea"/><stop offset="1" stop-color="#a9b0b9"/></linearGradient>'+
      '<linearGradient id="'+id+'au" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6d77a"/><stop offset="1" stop-color="#b8892c"/></linearGradient>'+
      '<linearGradient id="'+id+'usb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8d949c"/><stop offset=".5" stop-color="#e3e7eb"/><stop offset="1" stop-color="#8d949c"/></linearGradient>'+
      '<filter id="'+id+'gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>'+
      '</defs>';
    /* PCB */
    s+='<rect x="0" y="0" width="'+W+'" height="'+H+'" rx="14" fill="url(#'+id+'pcb)" stroke="#05070b" stroke-width="3"/>';
    s+='<g stroke="#232a37" stroke-width="2" fill="none" opacity=".9"><path d="M60 300 H120 V330"/><path d="M220 300 H170 V345"/><path d="M80 420 H140 V470"/><path d="M200 400 V440 H160"/><path d="M45 270 V380"/><path d="M234 270 V360"/></g>';
    /* โมดูล WROOM-32 */
    var mx=49, mw=181, my=-14, mh=n===19?256:250;
    s+='<rect x="'+mx+'" y="'+my+'" width="'+mw+'" height="'+mh+'" rx="5" fill="#141821" stroke="#05070b" stroke-width="2"/>';
    /* ขาด้านล่างของโมดูล WROOM-32 (ขาโมดูล 15–24 จากซ้ายไปขวา) */
    var MPAD=['GND',13,9,10,11,6,7,8,15,2], onHdr=function(k){ return B.L.indexOf(k)>=0||B.R.indexOf(k)>=0; };
    var padHL=MPAD.map(function(k){ return typeof k==='number'&&k>=6&&k<=11&&hl[String(k)]&&!onHdr(k); });
    for(var c=0;c<10;c++){
      var pxx=mx+28+c*13;
      if(padHL[c]) s+='<circle cx="'+(pxx+3)+'" cy="'+(my+mh-2)+'" r="8" fill="#ff4d5e" opacity=".6" filter="url(#'+id+'gl)"/>';
      s+='<rect x="'+pxx+'" y="'+(my+mh-6)+'" width="6" height="7" fill="'+(padHL[c]?'#ff8a95':'url(#'+id+'au)')+'"/>';
      if(padHL[c]) s+='<text x="'+(pxx+3)+'" y="'+(my+mh+14)+'" text-anchor="middle" font-family="Arial" font-size="9" font-weight="700" fill="#ff8a95">'+MPAD[c]+'</text>';
    }
    s+='<path d="M'+(mx+18)+' '+(my+52)+' V'+(my+14)+' H'+(mx+48)+' V'+(my+44)+' H'+(mx+70)+' V'+(my+14)+' H'+(mx+92)+' V'+(my+44)+' H'+(mx+114)+' V'+(my+14)+' H'+(mx+136)+' V'+(my+44)+' H'+(mx+160)+' V'+(my+14)+'" fill="none" stroke="url(#'+id+'au)" stroke-width="6" stroke-linejoin="miter"/>';
    var sx=mx+11, sy=my+64, sw=mw-22, sh=mh-74;
    if(xray){
      /* มุมมองเอกซเรย์: เปิดฝาโลหะให้เห็นชิ้นส่วนภายใน */
      s+='<rect x="'+sx+'" y="'+sy+'" width="'+sw+'" height="'+sh+'" rx="4" fill="#0b2a33" stroke="#7d848d" stroke-width="1.5" stroke-dasharray="6 4"/>';
      s+='<text x="'+(sx+6)+'" y="'+(sy+14)+'" font-family="Arial" font-size="9.5" fill="#7fd6e6">มุมมองใต้ฝาโลหะ</text>';
      s+='<rect x="'+(mx+28)+'" y="'+(sy+30)+'" width="72" height="72" rx="4" fill="#26292f" stroke="#0a0a0a" stroke-width="2"/><circle cx="'+(mx+36)+'" cy="'+(sy+38)+'" r="3" fill="#555"/>'+
         '<text x="'+(mx+64)+'" y="'+(sy+64)+'" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#d8dce2">ESP32</text><text x="'+(mx+64)+'" y="'+(sy+78)+'" text-anchor="middle" font-family="Arial" font-size="8" fill="#9aa1a9">D0WD</text>';
      for(var t=0;t<6;t++){ s+='<rect x="'+(mx+34+t*11)+'" y="'+(sy+26)+'" width="5" height="4" fill="#b8892c"/><rect x="'+(mx+34+t*11)+'" y="'+(sy+102)+'" width="5" height="4" fill="#b8892c"/>'; }
      s+='<rect x="'+(mx+114)+'" y="'+(sy+32)+'" width="42" height="56" rx="3" fill="#1f2228" stroke="#0a0a0a" stroke-width="2"/><text x="'+(mx+135)+'" y="'+(sy+58)+'" text-anchor="middle" font-family="Arial" font-size="9" font-weight="700" fill="#d8dce2">FLASH</text><text x="'+(mx+135)+'" y="'+(sy+71)+'" text-anchor="middle" font-family="Arial" font-size="8" fill="#9aa1a9">4 MB</text>';
      for(var t2=0;t2<4;t2++){ s+='<rect x="'+(mx+109)+'" y="'+(sy+38+t2*13)+'" width="5" height="4" fill="#b8892c"/><rect x="'+(mx+156)+'" y="'+(sy+38+t2*13)+'" width="5" height="4" fill="#b8892c"/>'; }
      s+='<rect x="'+(mx+114)+'" y="'+(sy+100)+'" width="40" height="20" rx="8" fill="#c9ccd1" stroke="#6b7076"/><text x="'+(mx+134)+'" y="'+(sy+114)+'" text-anchor="middle" font-family="Arial" font-size="8" fill="#333">40MHz</text>';
      s+='<rect x="'+(mx+28)+'" y="'+(sy+118)+'" width="72" height="40" rx="3" fill="none" stroke="#7fd6e6" stroke-width="1.5" stroke-dasharray="4 3"/><text x="'+(mx+64)+'" y="'+(sy+136)+'" text-anchor="middle" font-family="Arial" font-size="8.5" fill="#7fd6e6">PSRAM</text><text x="'+(mx+64)+'" y="'+(sy+149)+'" text-anchor="middle" font-family="Arial" font-size="7.5" fill="#7fd6e6">(เฉพาะ WROVER)</text>';
    } else {
      s+='<rect x="'+sx+'" y="'+sy+'" width="'+sw+'" height="'+sh+'" rx="4" fill="url(#'+id+'sh)" stroke="#7d848d" stroke-width="1.5"/>';
      s+='<text x="'+(mx+mw/2)+'" y="'+(sy+44)+'" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="700" fill="#4a5059">ESP32-WROOM-32</text>';
      s+='<text x="'+(mx+mw/2)+'" y="'+(sy+70)+'" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="12" fill="#5d636c">Espressif · Wi-Fi + BT</text>';
      s+='<text x="'+(mx+mw/2)+'" y="'+(sy+sh-24)+'" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="22" font-weight="700" fill="#6b7179">C E</text>';
    }
    /* ชิ้นส่วนใต้โมดูล */
    var by=mh+my;
    s+='<g>'+
      '<rect x="160" y="'+(by+18)+'" width="58" height="30" rx="2" fill="#1d1f24" stroke="#000"/><rect x="166" y="'+(by+8)+'" width="46" height="12" fill="#9aa1a9"/>'+
      '<rect x="166" y="'+(by+48)+'" width="8" height="10" fill="#9aa1a9"/><rect x="185" y="'+(by+48)+'" width="8" height="10" fill="#9aa1a9"/><rect x="204" y="'+(by+48)+'" width="8" height="10" fill="#9aa1a9"/>'+
      '<text x="189" y="'+(by+38)+'" text-anchor="middle" font-family="Arial" font-size="8" fill="#9aa1a9">AMS1117</text>'+
      '<rect x="78" y="'+(by+70)+'" width="48" height="48" rx="3" fill="#1a1c21" stroke="#000"/><circle cx="85" cy="'+(by+77)+'" r="2.5" fill="#55595f"/>'+
      '<text x="102" y="'+(by+98)+'" text-anchor="middle" font-family="Arial" font-size="8" fill="#8b9097">'+(bk==='c38'?'CP2102':'CP2102')+'</text>'+
      '<rect x="150" y="'+(by+80)+'" width="14" height="8" fill="#c9a66b"/><rect x="150" y="'+(by+96)+'" width="14" height="8" fill="#c9a66b"/><rect x="176" y="'+(by+80)+'" width="14" height="8" fill="#1e1e1e" stroke="#bbb" stroke-width="1"/>'+
      '<rect x="62" y="'+(by+22)+'" width="14" height="8" fill="#c9a66b"/><rect x="88" y="'+(by+22)+'" width="14" height="8" fill="#1e1e1e" stroke="#bbb" stroke-width="1"/>'+
      '<rect x="206" y="'+(by+80)+'" width="12" height="7" rx="1" fill="#ff3b3b"/><circle cx="212" cy="'+(by+83)+'" r="11" fill="#ff3b3b" opacity=".35" filter="url(#'+id+'gl)"/>'+
      '<text x="212" y="'+(by+100)+'" text-anchor="middle" font-family="Arial" font-size="7.5" fill="#e8e8e8">PWR</text>'+
      (bk==='v30'?'<rect x="206" y="'+(by+112)+'" width="12" height="7" rx="1" fill="#3aa0ff"/><text x="212" y="'+(by+131)+'" text-anchor="middle" font-family="Arial" font-size="7.5" fill="#e8e8e8">IO2</text>':'')+
      '</g>';
    /* ปุ่ม EN / BOOT และพอร์ต USB */
    var bt=H-74;
    [[80,'EN'],[W-80,'BOOT']].forEach(function(b){
      s+='<rect x="'+(b[0]-18)+'" y="'+(bt+4)+'" width="36" height="36" rx="4" fill="#c7ccd2" stroke="#6e757d" stroke-width="1.5"/><circle cx="'+b[0]+'" cy="'+(bt+22)+'" r="11" fill="#2b2f36" stroke="#111"/>'+
         '<text x="'+b[0]+'" y="'+(bt-6)+'" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#f1f1f1">'+b[1]+'</text>';
    });
    s+='<rect x="'+(W/2-34)+'" y="'+(H-58)+'" width="68" height="66" rx="6" fill="url(#'+id+'usb)" stroke="#5b6168" stroke-width="2"/><rect x="'+(W/2-22)+'" y="'+(H+1)+'" width="44" height="6" rx="2" fill="#30353b"/>'+
       '<text x="'+(W/2)+'" y="'+(H-64)+'" text-anchor="middle" font-family="Arial" font-size="9" fill="#cfd3d8">micro-USB</text>';
    /* ขาและป้ายชื่อ */
    function side(list,silk,isL){
      list.forEach(function(k,i){
        var y=y0+i*PITCH, x=isL?xl:xr, key=String(k), inf=info(k)||['gnd','',''], cat=CAT[inf[0]], on=!!hl[key];
        var dim=any&&!on&&compact;
        s+='<g class="np-pin'+(on?' on':'')+(dim?' dim':'')+'" data-k="'+key+'" style="--pc:'+cat.c+'">';
        if(on) s+='<circle class="np-halo" cx="'+x+'" cy="'+y+'" r="16" fill="'+cat.c+'" opacity=".55" filter="url(#'+id+'gl)"/>';
        s+=(i===0?'<rect x="'+(x-9)+'" y="'+(y-9)+'" width="18" height="18" rx="2"':'<circle cx="'+x+'" cy="'+y+'" r="9.5"')+' fill="url(#'+id+'au)" stroke="#7a5a1c" stroke-width="1"/>';
        s+='<rect x="'+(x-3.6)+'" y="'+(y-3.6)+'" width="7.2" height="7.2" fill="#d9dde2" stroke="#6b7076" stroke-width=".8"/>';
        s+='<text x="'+(isL?x+15:x-15)+'" y="'+(y+3.6)+'" text-anchor="'+(isL?'start':'end')+'" font-family="Arial,Helvetica,sans-serif" font-size="10" font-weight="700" fill="#eef0f3">'+silk[i]+'</text>';
        if(opt.quiz){ s+='<circle class="np-qring" cx="'+x+'" cy="'+y+'" r="13" fill="none" stroke-width="3.5"/><rect class="np-hit" x="'+(isL?x-30:x-60)+'" y="'+(y-12.7)+'" width="90" height="25.4" fill="transparent"/></g>'; return; }
        if(inf[0]==='flash') s+='<path d="M'+(x-7)+' '+(y-7)+' L'+(x+7)+' '+(y+7)+' M'+(x+7)+' '+(y-7)+' L'+(x-7)+' '+(y+7)+'" stroke="#ff4d5e" stroke-width="2.4" opacity="'+(dim?'.3':'.9')+'"/>';
        /* ป้ายด้านนอก */
        var nm=nameOf(k), tg=inf[1], x1=isL?-14:W+14;
        if(compact){
          if(on||!any){
            var pw=on?112:100, fz=on?20:16, ppx=isL?x1-pw:x1;
            s+='<line x1="'+(isL?x-10:x+10)+'" y1="'+y+'" x2="'+x1+'" y2="'+y+'" stroke="'+cat.c+'" stroke-width="'+(on?2.6:1.2)+'"/>';
            s+='<rect class="np-pill" x="'+ppx+'" y="'+(y-12.2)+'" width="'+pw+'" height="24.4" rx="12.2" fill="'+cat.c+'" fill-opacity="'+(on?.3:.12)+'" stroke="'+cat.c+'" stroke-width="'+(on?2.2:1)+'"/>';
            s+='<text class="np-nm" x="'+(ppx+pw/2)+'" y="'+(y+6.5)+'" text-anchor="middle" font-size="'+fz+'" font-weight="700">'+nm+'</text>';
          } else if(!hasParts){
            s+='<text class="np-nm" x="'+(isL?x1:x1)+'" y="'+(y+4.5)+'" text-anchor="'+(isL?'end':'start')+'" font-size="13" font-weight="600">'+nm+'</text>';
          }
        } else {
          var nmW=80, pillW=nmW+tg.length*7.3+20, px=isL?x1-pillW:x1, on2=on;
          s+='<line x1="'+(isL?x-10:x+10)+'" y1="'+y+'" x2="'+x1+'" y2="'+y+'" stroke="'+cat.c+'" stroke-width="'+(on2?2.4:1.2)+'" opacity="'+(on2?1:.55)+'"/>';
          s+='<rect class="np-pill" x="'+px+'" y="'+(y-11.5)+'" width="'+pillW+'" height="23" rx="11.5" fill="'+cat.c+'" fill-opacity="'+(on2?.24:.1)+'" stroke="'+cat.c+'" stroke-opacity="'+(on2?1:.45)+'" stroke-width="'+(on2?2:1)+'"/>';
          s+='<circle cx="'+(isL?x1-pillW+12:x1+12)+'" cy="'+y+'" r="4.5" fill="'+cat.c+'"/>';
          var tx=isL?x1-pillW+22:x1+22;
          s+='<text class="np-nm" x="'+tx+'" y="'+(y+5.6)+'" font-size="16" font-weight="700">'+nm+'</text>';
          s+='<text class="np-tg" x="'+(tx+nmW-8)+'" y="'+(y+4.6)+'" font-size="12.5" fill="'+cat.c+'">'+tg+'</text>';
        }
        s+='<rect class="np-hit" x="'+(isL?-LBW:x-14)+'" y="'+(y-12.7)+'" width="'+(LBW+(isL?x+14:W-x+14))+'" height="25.4" fill="transparent"/>';
        s+='</g>';
      });
    }
    side(B.L,B.SL,true); side(B.R,B.SR,false);
    /* ส่วนประกอบที่อ้างถึง: กรอบเรืองแสง + ป้ายชี้ (โหมดย่อ) หรือหมายเลข (โหมดเต็ม) */
    var bt2=H-74, by2=mh+my;
    var BOX={
      antenna:[mx+8,my+4,mw-16,54], module:[mx-3,my-3,mw+6,mh+6],
      chip:xray?[mx+24,sy+22,80,88]:[sx,sy,sw,sh], sram:xray?[mx+24,sy+22,80,88]:[sx,sy,sw,sh],
      flash:xray?[mx+106,sy+28,58,64]:[sx,sy,sw,sh], psram:xray?[mx+24,sy+114,80,48]:[sx,sy,sw,sh], xtal:xray?[mx+110,sy+96,48,28]:[sx,sy,sw,sh],
      usbuart:[72,by2+64,60,60], usb:[W/2-40,H-62,80,76], reg:[154,by2+2,70,62],
      en:[58,bt2,44,44], boot:[W-102,bt2,44,44], modpad:[mx+50,my+mh-12,84,30], pwr:[198,by2+72,28,34], led2:[198,by2+104,28,34]
    };
    var occ={L:[],R:[]};
    Object.keys(hl).forEach(function(k){ [['L',B.L],['R',B.R]].forEach(function(sd){ sd[1].forEach(function(x,i){ if(String(x)===k) occ[sd[0]].push([y0+i*PITCH-14,y0+i*PITCH+14]); }); }); });
    function free(sd,a,b){ return occ[sd].every(function(r){ return b<r[0]-3||a>r[1]+3; }); }
    var top=-20, bot=H+10, CH=46;
    parts.forEach(function(pk,ix){
      var bx=BOX[pk]; if(!bx) return; var P=PART[pk], c=CAT.part.c, cx=bx[0]+bx[2]/2, cy=bx[1]+bx[3]/2;
      s+='<g class="np-part on" data-k="p:'+pk+'">';
      s+='<rect class="np-pglow" x="'+bx[0]+'" y="'+bx[1]+'" width="'+bx[2]+'" height="'+bx[3]+'" rx="6" fill="'+c+'" fill-opacity=".14" stroke="'+c+'" stroke-width="3" filter="url(#'+id+'gl)"/>';
      s+='<rect x="'+bx[0]+'" y="'+bx[1]+'" width="'+bx[2]+'" height="'+bx[3]+'" rx="6" fill="'+c+'" fill-opacity=".08" stroke="'+c+'" stroke-width="2.4"/>';
      if(compact&&!opt.numbers){
        var pref=cx<W/2?'L':'R', alt=pref==='L'?'R':'L', sd=null, yy=null;
        for(var d=0;d<700&&sd==null;d+=6){ [cy+d,cy-d].some(function(t){ var a=t-CH/2,b=t+CH/2; if(a<top||b>bot) return false;
          if(free(pref,a,b)){ sd=pref; yy=t; return true; } if(d>60&&free(alt,a,b)){ sd=alt; yy=t; return true; } return false; }); }
        if(sd==null){ sd=pref; yy=cy; }
        occ[sd].push([yy-CH/2,yy+CH/2]);
        var isL=sd==='L', CW=LBW-14, x1=isL?-10:W+10, bxX=isL?x1-CW:x1, ex=isL?bx[0]:bx[0]+bx[2];
        if((isL&&cx>W/2)||(!isL&&cx<W/2)) ex=cx;
        s+='<polyline points="'+ex+','+cy+' '+(isL?Math.min(ex,-2):Math.max(ex,W+2))+','+cy+' '+x1+','+yy+'" fill="none" stroke="'+c+'" stroke-width="2.4"/>';
        s+='<circle cx="'+ex+'" cy="'+cy+'" r="4.5" fill="'+c+'"/>';
        s+='<rect class="np-pill" x="'+bxX+'" y="'+(yy-CH/2)+'" width="'+CW+'" height="'+CH+'" rx="12" fill="'+c+'" fill-opacity=".2" stroke="'+c+'" stroke-width="2.2"/>';
        s+='<text class="np-nm" x="'+(bxX+CW/2)+'" y="'+(yy-2)+'" text-anchor="middle" font-size="17" font-weight="700">'+P[0]+'</text>';
        s+='<text class="np-tg" x="'+(bxX+CW/2)+'" y="'+(yy+15)+'" text-anchor="middle" font-size="12" fill="'+c+'">'+P[1]+'</text>';
      } else {
        var lft=/^(sram|module|en)$/.test(pk), btm=/^(usb|psram)$/.test(pk), nx=lft?bx[0]+4:bx[0]+bx[2]-4, ny=btm?bx[1]+bx[3]-4:bx[1]+4;
        s+='<circle cx="'+nx+'" cy="'+ny+'" r="13" fill="'+c+'" stroke="#05070b" stroke-width="2"/><text x="'+nx+'" y="'+(ny+5)+'" text-anchor="middle" font-size="15" font-weight="700" fill="#05070b">'+(ix+1)+'</text>';
      }
      s+='</g>';
    });
    if(!opt.quiz&&!(hasParts&&parts.indexOf('antenna')>=0)) s+='<text x="'+(W/2)+'" y="-18" text-anchor="middle" font-size="12" class="np-cap">เสาอากาศ PCB (ด้านบน)</text>';
    s+='</svg>';
    return s;
  }

  /* ---------- ผังแบบย่อในสไลด์ ---------- */
  function figure(el,pins){
    if(!el) return; el._pins=pins||[];
    var pn=el._pins.filter(function(k){ return !isPart(k); }), pt=el._pins.filter(isPart);
    if(boardSel!=='v30') pt=pt.filter(function(k){ return k!=='p:led2'; });
    var chip=function(k){ var c=CAT[(info(k)||['gnd'])[0]].c; return '<i style="--pc:'+c+'">'+nameOf(k)+'</i>'; };
    var chips=pt.map(chip).join('')+(pn.length>14?'<i>'+pn.length+' ขา</i>':pn.map(chip).join(''));
    el.innerHTML='<div class="np-fig-h"><b>'+(pt.length?'บนบอร์ดจริง':'ขาบนบอร์ดจริง')+'</b><button type="button" class="np-zoom" aria-label="ขยายผังเต็ม">ขยาย ⤢</button><div class="np-chips">'+chips+'</div></div>'+
      '<div class="np-fig-b" title="แตะเพื่อขยายผังเต็มและดูรายละเอียด">'+boardSVG(boardSel,{pins:el._pins,compact:true})+'</div>';
  }

  /* ---------- ผังเต็มจอ ---------- */
  var M=null, cur=[], selK=null, allParts=false;
  function legend(){ return Object.keys(CAT).map(function(k){ return '<span><i style="background:'+CAT[k].c+'"></i>'+CAT[k].n+'</span>'; }).join(''); }
  function render(){
    if(!M) return; var B=BOARDS[boardSel];
    M.querySelector('.np-sel').innerHTML=Object.keys(BOARDS).map(function(k){ return '<button type="button" data-b="'+k+'" class="'+(k===boardSel?'on':'')+'">'+(k==='c38'?'38 ขา · DevKitC':'30 ขา · DevKit V1')+'</button>'; }).join('');
    M.querySelector('.np-sub').textContent=B.t+' — '+B.s;
    var narrow=!!(window.matchMedia&&matchMedia('(max-width:700px)').matches);
    var shown=allParts?cur.filter(function(k){ return !isPart(k); }).concat(Object.keys(PART).map(function(x){ return 'p:'+x; })):cur;
    M.querySelector('.np-board').innerHTML=boardSVG(boardSel,{pins:shown,compact:narrow,numbers:allParts});
    var pn=cur.filter(function(k){ return !isPart(k); }), pt=cur.filter(isPart);
    if(boardSel!=='v30') pt=pt.filter(function(k){ return k!=='p:led2'; });
    var miss=pn.filter(function(k){ return B.L.indexOf(k)<0&&B.R.indexOf(k)<0; });
    var btn=function(k,i){ return '<button type="button" data-k="'+k+'" style="--pc:'+CAT[(info(k)||['gnd'])[0]].c+'">'+(isPart(k)?(i+1)+'. ':'')+nameOf(k)+'</button>'; };
    var ptl=allParts?Object.keys(PART).filter(function(x){ return boardSel==='v30'||x!=='led2'; }).map(function(x){ return 'p:'+x; }):pt;
    M.querySelector('.np-hl').innerHTML=
      (ptl.length?'<b>'+(allParts?'ส่วนประกอบทั้งหมดบนบอร์ด':'ส่วนประกอบที่อ้างถึง')+'</b>'+ptl.map(btn).join(''):'')+
      (pn.length?'<b>ขาที่อ้างถึงในหน้านี้</b>'+pn.map(function(k){ return btn(k); }).join(''):'')+
      (!cur.length?'<b>แตะขาหรือชิ้นส่วนใดก็ได้บนบอร์ด</b>':'')+
      '<b></b><button type="button" class="np-allparts">'+(allParts?'ซ่อนส่วนประกอบ':'แสดงส่วนประกอบทั้งหมด')+'</button>'+
      (miss.length?'<small>บอร์ดแบบนี้ไม่มีขา '+miss.map(nameOf).join(', ')+' ที่หัวเข็ม'+(miss.every(function(k){ return k>=6&&k<=11; })?' แต่ยังอยู่ที่ขาด้านล่างของโมดูล (กรอบสีแดง) และต่อกับ Flash ภายใน':' ให้ใช้งาน')+'</small>':'');
    show(selK!=null?selK:(pt.length?pt[0]:(pn.length?pn[0]:null)));
  }
  function show(k){
    if(!M) return; selK=k; var box=M.querySelector('.np-info');
    Array.prototype.forEach.call(M.querySelectorAll('.np-board .np-pin,.np-board .np-part'),function(g){ g.classList.toggle('sel',g.getAttribute('data-k')===String(k)); });
    if(k==null){ box.innerHTML='<p class="np-hint">แตะที่ขา ป้ายชื่อ หรือชิ้นส่วนบนบอร์ด เพื่อดูหน้าที่และข้อควรระวัง</p>'; return; }
    var inf=info(k); if(!inf){ box.innerHTML=''; return; } var cat=CAT[inf[0]];
    box.innerHTML='<div class="np-ititle" style="--pc:'+cat.c+'"><b>'+nameOf(k)+'</b><span>'+cat.n+'</span></div><div class="np-itag">'+inf[1]+'</div><p>'+inf[2]+'</p>';
  }
  function build(){
    if(M) return M;
    M=D.createElement('div'); M.id='npModal'; M.setAttribute('role','dialog'); M.setAttribute('aria-modal','true'); M.setAttribute('aria-label','ผังขา ESP32');
    M.innerHTML='<div class="np-card"><div class="np-head"><div><b>ผังขา ESP32 แบบเหมือนจริง</b><div class="np-sub"></div></div><div class="np-sel"></div><button type="button" class="np-x" aria-label="ปิด">✕</button></div>'+
      '<div class="np-body"><div class="np-board"></div><aside><div class="np-info"></div><div class="np-hl"></div><div class="np-leg">'+legend()+'</div></aside></div></div>';
    D.body.appendChild(M);
    M.addEventListener('click',function(e){
      if(e.target===M||e.target.closest('.np-x')){ close(); return; }
      var b=e.target.closest('[data-b]'); if(b){ boardSel=b.getAttribute('data-b'); try{ localStorage.setItem('cpe2422_board',boardSel); }catch(x){} render(); refreshFigs(); return; }
      if(e.target.closest('.np-allparts')){ allParts=!allParts; selK=null; render(); return; }
      var p=e.target.closest('[data-k]'); if(p){ var k=p.getAttribute('data-k'); show(/^\d+$/.test(k)?+k:k); try{ SFX.play('select'); }catch(x){} }
    });
    return M;
  }
  function open(pins){ build(); cur=pins||[]; selK=null; allParts=false; render(); M.classList.add('show'); D.body.classList.add('np-open'); var x=M.querySelector('.np-x'); if(x) x.focus(); }
  function close(){ if(M){ M.classList.remove('show'); D.body.classList.remove('np-open'); } }
  D.addEventListener('keydown',function(e){ if(e.key==='Escape'&&M&&M.classList.contains('show')){ e.stopPropagation(); e.preventDefault(); close(); } },true);
  function refreshFigs(){ Array.prototype.forEach.call(D.querySelectorAll('.np-fig'),function(f){ figure(f,f._pins); }); }

  window.NeoPin={isPart:isPart,detect:detect,figure:figure,open:open,close:close,name:nameOf,svg:boardSVG};
})();
