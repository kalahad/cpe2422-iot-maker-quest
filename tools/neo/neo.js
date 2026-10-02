/* ================================================================
   NEO ARCADE v1.0 — UX ชั้นใหม่ของ IoT Maker Quest (โหลดหลัง CORE)
   1) เวทีจอเดียว  2) หน้าแรกแบ่งซ้าย-ขวา  3) Mission Briefing + นับถอยหลัง
   4) หน้าทฤษฎีเป็นสไลด์การ์ด (Big Idea · ตัวเลขต้องจำ · เจาะลึก · กับดัก · Lab · Boss Check)
   5) หน้าสรุปภารกิจจอเดียวแบบ minimal
   ================================================================ */
(function(){
  'use strict';
  var D=document, CARDS=window.NEO_CARDS||{};
  var REDUCE=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
  function q(s,r){ return (r||D).querySelector(s); }
  function qa(s,r){ return Array.prototype.slice.call((r||D).querySelectorAll(s)); }
  function h(tag,cls,html){ var e=D.createElement(tag); if(cls) e.className=cls; if(html!=null) e.innerHTML=html; return e; }
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function sfx(n){ try{ SFX.play(n); }catch(e){} }
  function xp(n){ try{ addXp(n); }catch(e){} }

  /* ---------- 1) ความสูงแถบบน -> ตัวแปร --tbh ---------- */
  function setTbh(){
    var t=q('#topbar'), on=t&&t.classList.contains('show');
    D.documentElement.style.setProperty('--tbh',(on?t.offsetHeight:0)+'px');
    D.body.classList.toggle('neo-wel',!on);
  }

  /* ---------- 2) หน้าแรก ---------- */
  function welcome(){
    var w=q('#scr-welcome'); if(!w||q('.neo-wel-grid',w)) return;
    var hero=q('.hero',w), art=q('.cityart',hero), t=q('.title',hero), sub=q('.subtitle',hero), card=q('.login-card',hero);
    var grid=h('div','neo-wel-grid'), L=h('div','neo-wel-left'), R=h('div','neo-wel-right');
    L.appendChild(h('div','neo-kicker','CPE2422 · IoT MAKER QUEST'+(CARDS.stage?' · '+esc(CARDS.stage):'')));
    if(art) L.appendChild(art); if(t) L.appendChild(t); if(sub) L.appendChild(sub);
    L.appendChild(h('div','neo-chips','<span><b>3</b> ด่านย่อย</span><span><b>3</b> ห้องทดลอง</span><span><b>6</b> ดาว Pre → Post</span><span><b>~20</b> นาที</span>'));
    if(card) R.appendChild(card);
    grid.appendChild(L); grid.appendChild(R); hero.appendChild(grid);
    var st=q('#btnStart'); if(st){ st.classList.add('neo-pulse'); st.textContent='เริ่มภารกิจ ▶'; }
  }

  /* ---------- 3) Mission Briefing ---------- */
  var IC={
    tap:'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 26V10a4 4 0 0 1 8 0v12"/><path d="M28 20a4 4 0 0 1 8 0v4a4 4 0 0 1 8 0v8c0 7-5 12-12 12h-2c-5 0-8-2-11-6l-6-8a4 4 0 0 1 6-5l3 3"/><path d="M12 8l-3-3M8 16H4M36 6l3-3"/></svg>',
    up:'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M24 40V10M12 22l12-12 12 12"/><path d="M8 44h32"/></svg>',
    shield:'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M24 4l16 6v12c0 10-7 18-16 22C15 40 8 32 8 22V10z"/><path d="M17 24l5 5 9-10"/></svg>'
  };
  function brief(kind){
    var sec=q(kind==='pre'?'#scr-pretest':'#scr-posttest'); if(!sec||q('.neo-brief',sec)) return;
    var p=q('.panel',sec), launch=q(kind==='pre'?'#preLaunch':'#postLaunch',p);
    var b=h('div','neo-brief');
    b.innerHTML=
      '<span class="tag">Mission Briefing · '+(kind==='pre'?'Pretest':'Posttest')+'</span>'+
      '<h2>'+(kind==='pre'?'วัดพลังก่อนลุย!':'บอสด่านสุดท้าย!')+'</h2>'+
      '<div class="neo-stats"><div><b>6</b><small>ข้อ</small></div><div><b>~3</b><small>นาที</small></div><div><b>'+(kind==='pre'?'0':'NEW')+'</b><small>'+(kind==='pre'?'ผลต่อเกรด':'ไม่ซ้ำ Pretest')+'</small></div></div>'+
      '<div class="neo-rules">'+
        '<div class="neo-rule" style="--k:var(--n-a)">'+IC.tap+'<h4>แตะตอบ</h4><p>ไม่ต้องบังคับตัวละคร</p></div>'+
        '<div class="neo-rule" style="--k:var(--n-c)">'+IC.up+'<h4>ถูก = ไต่ขึ้น</h4><p>ติดกันได้ Combo</p></div>'+
        '<div class="neo-rule" style="--k:var(--n-b)">'+IC.shield+'<h4>ผิด = ไม่ตาย</h4><p>อ่านเฉลยแล้วไปต่อ</p></div>'+
      '</div>';
    var row=h('div','btn-row'); launch.classList.add('neo-pulse'); launch.style.flex='0 1 auto';
    launch.textContent=kind==='pre'?'พร้อมแล้ว ลุย! ▶':'ท้าบอส ▶'; row.appendChild(launch); b.appendChild(row);
    while(p.firstChild) p.removeChild(p.firstChild);
    p.appendChild(b);
  }
  function countdown(kind){
    var ov=q('#neoCount'); if(!ov){ ov=h('div','',''); ov.id='neoCount'; D.body.appendChild(ov); }
    if(REDUCE){ startTest(kind); return; }
    var seq=['3','2','1','GO!'], i=0; ov.classList.add('show');
    (function step(){
      if(i>=seq.length){ ov.classList.remove('show'); startTest(kind); return; }
      ov.innerHTML='<b>'+seq[i]+'</b>'; sfx(i<3?'tick':'unlock'); i++; setTimeout(step,i<4?620:520);
    })();
  }
  D.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('#preLaunch,#postLaunch'); if(!b) return;
    e.stopPropagation(); e.preventDefault(); sfx('click'); countdown(b.id==='preLaunch'?'pre':'post');
  },true);

  /* ---------- 4) หน้าทฤษฎี -> สไลด์ ---------- */
  var decks={};
  function slide(label,nodes,extraHtml){
    var s=h('div','neo-slide'), inn=h('div','neo-in'); s.appendChild(h('div','neo-slabel',label)); s.appendChild(inn);
    if(extraHtml) inn.insertAdjacentHTML('beforeend',extraHtml);
    (nodes||[]).forEach(function(n){ inn.appendChild(n); });
    s._in=inn; return s;
  }
  /* แบ่งตารางยาวเป็นหลายใบ (ไม่เกิน ROWS แถวต่อสไลด์) */
  var ROWS=5;
  function isData(r){ return !!r.querySelector('td'); }
  function splitTables(kids){
    var out=[];
    kids.forEach(function(k){
      var t=k.classList&&k.classList.contains('tbl-wrap')?q('table',k):null, rows=t?qa('tr',t).filter(isData):[];
      if(!t||rows.length<=ROWS+1){ out.push(k); return; }
      var parts=Math.ceil(rows.length/ROWS), per=Math.ceil(rows.length/parts);
      for(var p=0;p<parts;p++){
        var c=k.cloneNode(true), cr=qa('tr',c).filter(isData);
        cr.forEach(function(r,ri){ if(ri<p*per||ri>=(p+1)*per) r.parentNode.removeChild(r); });
        if(p>0){ var th=q('th',c); if(th) th.textContent+=' (ต่อ '+(p+1)+'/'+parts+')'; }
        out.push(c);
      }
    });
    return out;
  }
  /* ย่อเนื้อหาอัตโนมัติให้พอดีหนึ่งจอ */
  function fit(s){
    var inn=s._in; if(!inn) return; inn.style.zoom=''; var z=1;
    while(s.scrollHeight>s.clientHeight+2 && z>0.66){ z-=0.06; inn.style.zoom=z.toFixed(2); }
  }
  function deckify(n){
    var sec=q('#scr-lesson'+n); if(!sec) return;
    var panel=q('.panel',sec); if(!panel||q('.neo-deck',panel)) return;
    var c=CARDS['z'+n]||{}, kids=splitTables(Array.prototype.slice.call(panel.children));
    var tag=kids[0]&&kids[0].classList.contains('tag')?kids.shift():null;
    var h2=kids[0]&&kids[0].tagName==='H2'?kids.shift():null;
    var qi=-1; kids.forEach(function(k,i){ if(k.querySelector&&k.querySelector('[data-quiz]')) qi=i; });
    var quizRow=qi>=0?kids.splice(qi,1)[0]:null;
    var li=-1; kids.forEach(function(k,i){ if(li<0&&k.tagName==='H3'&&/ห้องทดลอง/.test(k.textContent)) li=i; });
    var pre=li>=0?kids.slice(0,li):kids, lab=li>=0?kids.slice(li):[];
    var slides=[], intro=[], deep=[], facts=[];
    pre.forEach(function(k){
      if(k.classList.contains('keyfact')) facts.push(k);
      else if(k.classList.contains('tbl-wrap')||k.classList.contains('codebox')||k.classList.contains('divfig')) deep.push([k]);
      else if(!deep.length) intro.push(k);
      else deep[deep.length-1].push(k);
    });
    slides.push(slide('01 · BIG IDEA',intro,c.big?'<p class="neo-big">'+c.big+'</p>':''));
    if(c.nums&&c.nums.length) slides.push(slide('02 · ตัวเลขต้องจำ',[],'<div class="neo-nums">'+c.nums.map(function(x){return '<div class="neo-num"><b>'+x[0]+'</b><span>'+x[1]+'</span></div>';}).join('')+'</div>'));
    deep.forEach(function(g,i){ slides.push(slide('เจาะลึก '+(i+1)+'/'+deep.length,g)); });
    if(facts.length) slides.push(slide('จำให้ขึ้นใจ',facts));
    if(c.traps&&c.traps.length) slides.push(slide('กับดักออกสอบ · แตะการ์ดเพื่อพลิก',[],'<div class="neo-traps">'+c.traps.map(function(x){
      return '<button type="button" class="neo-flip"><div class="in"><div class="f"><em>ความเชื่อผิด</em><p>'+x[0]+'</p><small>แตะเพื่อดูความจริง</small></div><div class="k"><em>ความจริง</em><p>'+x[1]+'</p></div></div></button>';}).join('')+'</div>'));
    var labs=[]; lab.forEach(function(k){ if(k.tagName==='H3'&&/ห้องทดลอง/.test(k.textContent)) labs.push([k]); else if(labs.length) labs[labs.length-1].push(k); });
    labs.forEach(function(g,i){ slides.push(slide('LAB '+(i+1)+(labs.length>1?'/'+labs.length:'')+' · ลงมือเล่น',g)); });
    var boss=slide('BOSS CHECK · ตอบให้ถูกแล้วไปด่านฝึกหัด',[],'<div class="neo-boss" data-d="district'+n+'"></div>');
    var qb=quizRow?q('[data-quiz]',quizRow):null; if(qb){ qb.classList.add('neo-pulse','neo-go'); qb.textContent='ไปด่านฝึกหัด ▶'; }
    slides.push(boss);
    var deck=h('div','neo-deck'), head=h('div','neo-dhead'), stage=h('div','neo-stage'), prog=h('div','neo-prog');
    if(tag) head.appendChild(tag); if(h2) head.appendChild(h2); head.appendChild(prog);
    slides.forEach(function(s){ stage.appendChild(s); prog.appendChild(h('i')); });
    var foot=h('div','neo-dfoot','<button type="button" class="btn neo-prev">◀ ย้อน</button><span class="sp"></span><button type="button" class="btn primary neo-next">ถัดไป ▶</button>');
    if(qb) foot.appendChild(qb);
    deck.appendChild(head); deck.appendChild(stage); deck.appendChild(foot);
    while(panel.firstChild) panel.removeChild(panel.firstChild);
    panel.appendChild(deck);
    var st={n:n,i:0,slides:slides,prog:prog,foot:foot,seen:{},qb:qb};
    decks[n]=st;
    q('.neo-prev',foot).addEventListener('click',function(){ go(n,st.i-1); });
    q('.neo-next',foot).addEventListener('click',function(){ go(n,st.i+1); });
    var x0=null; stage.addEventListener('touchstart',function(e){ x0=e.touches[0].clientX; },{passive:true});
    stage.addEventListener('touchend',function(e){ if(x0==null) return; var dx=e.changedTouches[0].clientX-x0; x0=null;
      if(Math.abs(dx)>60 && !(e.target.closest&&e.target.closest('input,.neo-flip'))) go(n,st.i+(dx<0?1:-1)); },{passive:true});
    slides.forEach(attachPin);
    stage.addEventListener('click',pinClick);
    boss.querySelector('.neo-boss').addEventListener('click',bossClick);
    renderBoss(boss.querySelector('.neo-boss'));
    go(n,0,true);
  }
  function go(n,i,silent){
    var st=decks[n]; if(!st) return; var N=st.slides.length;
    i=Math.max(0,Math.min(N-1,i));
    st.slides.forEach(function(s,k){ s.classList.toggle('on',k===i); s.classList.toggle('prev',k<i); if(k===i) s.scrollTop=0; });
    Array.prototype.forEach.call(st.prog.children,function(b,k){ b.classList.toggle('on',k<=i); });
    q('.sp',st.foot).textContent=(i+1)+' / '+N+' · ปัด หรือกด ← →';
    q('.neo-prev',st.foot).style.visibility=i?'visible':'hidden';
    q('.neo-next',st.foot).style.display=i<N-1?'':'none';
    if(st.qb) st.qb.style.display=i===N-1?'':'none';
    setTimeout(markTop,30);
    fit(st.slides[i]); if(st.slides[i]._in) setTimeout(function(){ fit(st.slides[i]); },380);
    if(!silent && i!==st.i) sfx('select');
    if(!silent && !st.seen[i]){ st.seen[i]=1; if(i>0) xp(3); }
    st.i=i;
  }
  /* ผังขา ESP32 ประกอบทุกสไลด์ที่อ้างถึงขา */
  function attachPin(sl){
    if(!window.NeoPin||!sl||!sl._in) return;
    var pins=NeoPin.detect(sl._in.textContent), fig=q('.np-fig',sl), chip=q('.np-chip',sl);
    if(!pins.length){ sl.classList.remove('np-has'); if(fig) fig.remove(); if(chip) chip.remove(); return; }
    sl.classList.add('np-has');
    if(!fig){ fig=h('div','np-fig'); sl.appendChild(fig); }
    if(!chip){ chip=h('button','np-chip','ดูบนบอร์ดจริง ('+pins.length+')'); chip.type='button'; sl.insertBefore(chip,sl._in); }
    else chip.textContent='ดูบนบอร์ดจริง ('+pins.length+')';
    sl._pins=pins; NeoPin.figure(fig,pins);
    if(!sl._focusBound){ sl._focusBound=1; bindFocus(sl); }
  }
  /* ชี้/แตะแถวตาราง หรือกล่องข้อความ -> ภาพบอร์ดเน้นเฉพาะสิ่งที่แถวนั้นพูดถึง */
  function bindFocus(sl){
    var inn=sl._in, last=null, tmr=null;
    function apply(el){
      if(el===last) return; last=el;
      qa('.np-focus',inn).forEach(function(x){ x.classList.remove('np-focus'); });
      var f=q('.np-fig',sl); if(!f||!sl.classList.contains('np-has')) return;
      if(!el){ NeoPin.figure(f,sl._pins); return; }
      var k=NeoPin.detect(el.textContent,true);
      if(!k.length){ NeoPin.figure(f,sl._pins); return; }
      el.classList.add('np-focus'); NeoPin.figure(f,k);
    }
    inn.addEventListener('pointerover',function(e){
      var el=e.target.closest('tr,.keyfact,li,.neo-num,.neo-flip,.codebox,.neo-in>p');
      if(el&&el.querySelector('th')&&!el.querySelector('td')) el=null;
      clearTimeout(tmr); tmr=setTimeout(function(){ apply(el&&inn.contains(el)?el:null); },70);
    });
    inn.addEventListener('pointerleave',function(){ clearTimeout(tmr); tmr=setTimeout(function(){ apply(null); },120); });
  }
  function pinClick(e){
    if(!window.NeoPin) return;
    var sl=e.target.closest('.neo-slide'); if(!sl) return;
    if(e.target.closest('.np-zoom,.np-fig-b')){ var f=q('.np-fig',sl); sfx('click'); NeoPin.open(f?f._pins:sl._pins); return; }
    if(e.target.closest('.np-chip')){ sfx('click'); NeoPin.open(sl._pins||[]); return; }
    var b=e.target.closest('button,[data-pin]'); if(!b||!sl.classList.contains('np-has')) return;
    setTimeout(function(){
      var pins=NeoPin.detect(b.textContent,true);
      if(!pins.length){ var t=qa('.status-line,.ex,[aria-live],.readout,.out',sl).map(function(x){ return x.textContent; }).join(' '); pins=NeoPin.detect(t,true); }
      if(pins.length){ var f=q('.np-fig',sl); if(f) NeoPin.figure(f,pins); sl._pins=pins; }
    },90);
  }
  function visiblePins(){
    if(!window.NeoPin) return [];
    var ac=q('#arcade'), t='';
    if(ac&&ac.classList.contains('show')) t=(q('#acQCard')||{}).textContent||'';
    else { var a=q('.screen.active'); if(a){ var on=q('.neo-slide.on',a); t=on?(on._pins?'':(on.textContent)):a.textContent; if(on&&on._pins) return on._pins; } }
    return NeoPin.detect(t);
  }
  function pinButtons(){
    var tb=q('#topbar .tb-right'), snd=q('#btnSound');
    if(tb&&!q('#btnPin')){ var b=h('button','icon-btn','PIN<b></b>'); b.id='btnPin'; b.title='ผังขา ESP32 แบบเหมือนจริง'; b.setAttribute('aria-label','เปิดผังขา ESP32'); tb.insertBefore(b,snd||tb.firstChild);
      b.addEventListener('click',function(){ sfx('click'); NeoPin.open(visiblePins()); }); }
    var hud=q('#arcade .ac-hud'), ex=q('#acExit');
    if(hud&&!q('#acPin')){ var a=h('button','icon-btn ac-exit','ผังขา<b></b>'); a.id='acPin'; a.title='ผังขา ESP32'; hud.insertBefore(a,ex);
      a.addEventListener('click',function(e){ e.stopPropagation(); sfx('click'); NeoPin.open(NeoPin.detect((q('#acQCard')||{}).textContent||'')); }); }
    var card=q('#acQCard');
    if(card&&window.MutationObserver){ new MutationObserver(function(){ mark(q('#acPin'),NeoPin.detect(card.textContent)); }).observe(card,{childList:true,subtree:true,characterData:true}); }
  }
  function mark(btn,pins){ if(!btn) return; btn.classList.toggle('np-has',pins.length>0); var b=q('b',btn); if(b) b.textContent=pins.length||''; }
  function markTop(){ mark(q('#btnPin'),visiblePins()); }

  /* Boss check: คำถาม 1 ข้อจากคลังของด่านย่อยนั้น */
  function renderBoss(box){
    var d=box.getAttribute('data-d'), pool=(typeof BANK!=='undefined'&&BANK[d])||[]; if(!pool.length) return;
    var src=pool[Math.floor(Math.random()*pool.length)], qq=(typeof randomizeChoices==='function')?randomizeChoices(src):src;
    box._q=qq; box._done=false;
    box.innerHTML='<div class="q">'+qq.q+'</div><div class="opts">'+qq.c.map(function(c,i){ return '<button type="button" data-bi="'+i+'">'+c+'</button>'; }).join('')+
      '</div><div class="ex"></div><div style="text-align:center"><button type="button" class="btn sm neo-reboss">สุ่มคำถามใหม่</button></div>';
    var bs=box.closest('.neo-slide'); if(bs) attachPin(bs);
  }
  function bossClick(e){
    var box=e.currentTarget, rb=e.target.closest('.neo-reboss'); if(rb){ sfx('click'); renderBoss(box); return; }
    var b=e.target.closest('[data-bi]'); if(!b||box._done) return;
    box._done=true; var i=+b.getAttribute('data-bi'), ok=i===box._q.a;
    qa('[data-bi]',box).forEach(function(x){ if(+x.getAttribute('data-bi')===box._q.a) x.classList.add('ok'); });
    if(!ok) b.classList.add('bad');
    var ex=q('.ex',box); ex.innerHTML=(ok?'<b>ถูกต้อง! +10 XP</b> · ':'<b>เกือบแล้ว</b> · ')+box._q.e; ex.classList.add('show'); fit(box.closest('.neo-slide'));
    sfx(ok?'correct':'wrong'); if(ok) xp(10);
  }
  D.addEventListener('click',function(e){ var f=e.target.closest&&e.target.closest('.neo-flip'); if(f){ f.classList.toggle('open'); sfx('select'); if(!f._x){ f._x=1; xp(2);} } });
  D.addEventListener('keydown',function(e){
    if(e.target.tagName==='INPUT') return; try{ if(AC&&AC.on) return; }catch(x){}
    var a=q('.screen.active'); if(!a) return; var m=/^scr-lesson(\d)$/.exec(a.id); if(!m) return;
    var st=decks[+m[1]]; if(!st) return;
    if(e.key==='ArrowRight'){ e.preventDefault(); go(st.n,st.i+1); } else if(e.key==='ArrowLeft'){ e.preventDefault(); go(st.n,st.i-1); }
  });

  /* ---------- 5) สรุปภารกิจ ---------- */
  var BADGE_IC='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 2l3 6 6.5 1-4.7 4.6 1.1 6.4L12 17l-5.9 3 1.1-6.4L2.5 9 9 8z"/></svg>';
  function summary(){
    var sec=q('#scr-summary'); if(!sec) return; var panel=q('.panel',sec);
    var old=q('#neoSum',panel); if(old) old.remove();
    var pre=+(state.pre||0), post=+(state.post||0), max=6, pc=Math.round(post/max*100), dl=post-pre;
    var info=(typeof starInfo==='function')?starInfo(post):{rank:''};
    var id=(window.GNRID&&GNRID.get())||{sid:'—'}, nick=state.name||'ผู้เล่น';
    var ds=['district1','district2','district3'];
    var weak=(typeof weakestDistrict==='function')?weakestDistrict():'district1';
    var skills=ds.map(function(d){ var a=state.preByD[d]||0, b=state.postByD[d]||0;
      return '<div class="skill"><span>'+esc(SKILL_LABELS[d])+'</span><em>'+b+'/2</em><div class="tr"><i class="pre" style="width:'+(a*50)+'%"></i><i class="post" style="width:0" data-w="'+(b*50)+'"></i></div></div>'; }).join('');
    var badges=(typeof BADGE_DEFS!=='undefined'?BADGE_DEFS:[]).map(function(bd){ var ok=false; try{ ok=!!bd.test(state); }catch(e){}
      return '<div class="bd '+(ok?'on':'off')+'" data-t="'+esc(bd.name+' — '+bd.desc)+'">'+BADGE_IC+'</div>'; }).join('');
    var nb=(typeof BADGE_DEFS!=='undefined'?BADGE_DEFS:[]).filter(function(bd){ try{ return bd.test(state); }catch(e){ return false; } }).length;
    var cheer = pc>=100?['สมบูรณ์แบบ! เคลียร์ครบทุกข้อ','ท้าตัวเองต่อด้วยการเล่นซ้ำเพื่อเจอคำถามชุดใหม่']:
                pc>=67 ?['เกือบเต็มแล้ว อีกนิดเดียว','เก็บ '+SKILL_LABELS[weak]+' ให้ครบ แล้วกลับมาท้าบอสอีกรอบ']:
                pc>=34 ?['มาถูกทางแล้ว ไปต่อ!','เริ่มทบทวนจาก '+SKILL_LABELS[weak]+' ทีละสไลด์ แล้วลองใหม่']:
                        ['จุดเริ่มต้นของทุกแชมป์','กลับไปเล่นห้องทดลองของ '+SKILL_LABELS[weak]+' ให้ครบ แล้วกลับมาวัดพลังใหม่'];
    var R=54, C=2*Math.PI*R;
    var box=h('div',''); box.id='neoSum';
    box.innerHTML=
      '<div class="sh"><span class="tag">Mission Complete</span><h2>'+esc(q('#topbar .brand span')?q('#topbar .brand span').textContent:'')+'</h2><span class="who">'+esc(nick)+' · '+esc(id.sid||'—')+'</span></div>'+
      '<div class="card c1"><div class="ring"><svg viewBox="0 0 140 140"><defs><linearGradient id="neoRg" x1="0" x2="1"><stop offset="0" stop-color="var(--n-a)"/><stop offset="1" stop-color="var(--n-b)"/></linearGradient></defs>'+
        '<circle cx="70" cy="70" r="'+R+'" fill="none" stroke="var(--n-glass2)" stroke-width="12"/>'+
        '<circle class="arc" cx="70" cy="70" r="'+R+'" fill="none" stroke="url(#neoRg)" stroke-width="12" stroke-linecap="round" transform="rotate(-90 70 70)" stroke-dasharray="'+C.toFixed(1)+'" stroke-dashoffset="'+C.toFixed(1)+'" style="transition:stroke-dashoffset 1.2s cubic-bezier(.2,.8,.2,1);filter:drop-shadow(0 0 6px var(--n-a))"/></svg>'+
        '<div class="mid"><div><b class="cnt">0</b><small>/ 6 POST</small></div></div></div>'+
        '<div class="rank">'+esc(info.rank||'')+'</div>'+
        '<div class="delta">Pre '+pre+' → Post '+post+' <span class="'+(dl>=0?'up':'dn')+'">'+(dl>=0?'+':'')+dl+'</span></div></div>'+
      '<div class="card c2"><h4>ทักษะรายด่าน</h4>'+skills+'<div class="legend">แถบเทา = ก่อนเรียน · แถบสี = หลังเรียน</div>'+
        '<div class="stats"><div><b>'+state.xp+'</b><small>XP</small></div><div><b>'+state.maxCombo+'</b><small>Combo สูงสุด</small></div><div><b>'+nb+'/6</b><small>เหรียญ</small></div></div></div>'+
      '<div class="card c3"><div class="cheer">'+esc(cheer[0])+'<small>'+esc(cheer[1])+'</small></div><h4>เหรียญตรา</h4><div class="badges">'+badges+'</div></div>'+
      '<div class="act"><button type="button" class="btn primary neo-review">ทบทวน: '+esc(SKILL_LABELS[weak])+' ▶</button>'+
        '<button type="button" class="icon-btn neo-again" title="เล่นใหม่">เล่นใหม่</button>'+
        '<button type="button" class="icon-btn neo-csv" title="บันทึกคะแนน CSV">CSV</button>'+
        '<a class="icon-btn" href="index.html" title="หน้าแผนที่ภารกิจ">แผนที่</a></div>';
    panel.appendChild(box);
    q('.neo-review',box).onclick=function(){ sfx('click'); goto_(DISTRICT_SCREEN[weak]); };
    q('.neo-again',box).onclick=function(){ var b=q('#btnAgain'); if(b) b.click(); };
    q('.neo-csv',box).onclick=function(){ try{ exportCSV(); }catch(e){} };
    requestAnimationFrame(function(){ setTimeout(function(){
      q('.arc',box).style.strokeDashoffset=(C*(1-post/max)).toFixed(1);
      qa('.tr .post',box).forEach(function(i){ i.style.width=i.getAttribute('data-w')+'%'; });
      var cn=q('.cnt',box), k=0; (function up(){ cn.textContent=k; if(k<post){ k++; setTimeout(up,REDUCE?0:160); } })();
    },80); });
  }

  /* ---------- ห่อฟังก์ชันของเกม ---------- */
  if(typeof goto_==='function'){
    var _g=goto_;
    goto_=function(id){ var r=_g.apply(this,arguments); setTbh(); setTimeout(markTop,80);
      var m=/^scr-lesson(\d)$/.exec(id); if(m&&decks[+m[1]]&&decks[+m[1]].i===decks[+m[1]].slides.length-1) go(+m[1],0,true);
      if(m&&decks[+m[1]]){ var st=decks[+m[1]]; setTimeout(function(){ fit(st.slides[st.i]); },60); }
      return r; };
  }
  if(typeof showSummary==='function'){
    var _s=showSummary;
    showSummary=function(){ var r=_s.apply(this,arguments); try{ summary(); }catch(e){ console.warn('neo summary',e); } return r; };
  }
  window.addEventListener('resize',function(){ setTbh(); var a=q('.screen.active'), m=a&&/^scr-lesson(\d)$/.exec(a.id); if(m&&decks[+m[1]]){ var st=decks[+m[1]]; fit(st.slides[st.i]); } });

  welcome(); brief('pre'); brief('post'); [1,2,3].forEach(deckify); try{ pinButtons(); }catch(e){ console.warn('neo pin',e); } setTbh();
  if(window.MutationObserver){ var tb=q('#topbar'); if(tb) new MutationObserver(setTbh).observe(tb,{attributes:true,attributeFilter:['class']}); }
})();
