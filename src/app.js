/* ---------- Fotos für "Unsere Ergebnisse": Dateien in den Ordner fotos/ legen und hier eintragen ----------
   orte: kurve, perspektive, erwartungen, korridor, beduerfnisse, skillwill, augenhoehe, fragen, grow, schwierig  */
const ERGEBNISSE = [
  // { titel: "Unsere Veränderungskurve", bild: "fotos/kurve.jpg", orte: ["kurve"] },
];
const FOLIEN = 70; // Anzahl der Folienbilder in folien/

/* ---------- Speicher (nur auf diesem Gerät) ---------- */
const KEY = 'erstes-mal-fuehren-begleitraum-v1';
let S = (()=>{ try{ return JSON.parse(localStorage.getItem(KEY)) || {}; }catch(e){ return {}; } })();
function save(){ try{ localStorage.setItem(KEY, JSON.stringify(S)); }catch(e){} }
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const $ = (s, r=document) => r.querySelector(s);
function toast(t){ const el=$('#toast'); el.textContent=t; el.classList.add('on'); clearTimeout(toast.t); toast.t=setTimeout(()=>el.classList.remove('on'),1600); }
async function copy(text){ try{ await navigator.clipboard.writeText(text); toast('Kopiert'); }catch(e){ const ta=document.createElement('textarea'); ta.value=text; document.body.appendChild(ta); ta.select(); try{ document.execCommand('copy'); toast('Kopiert'); }catch(_){ toast('Bitte markieren und kopieren'); } ta.remove(); } }
const getP = (path) => path.split('.').reduce((o,k)=>o&&o[k], S);
function setP(path, v){ const ks=path.split('.'); let o=S; ks.slice(0,-1).forEach(k=>{ if(typeof o[k]!=='object'||!o[k]) o[k]={}; o=o[k]; }); o[ks.at(-1)]=v; save(); }

/* ---------- Router ---------- */
function route(){
  const raw = (location.hash || '#start').slice(1);
  const [id, query] = raw.split('?');
  const page = document.getElementById('p-' + id) ? id : 'start';
  document.querySelectorAll('section.page').forEach(s => s.classList.toggle('show', s.id === 'p-' + page));
  document.querySelectorAll('nav.side a').forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + page));
  const qp = new URLSearchParams(query || '');
  const sub = qp.get('sub'); if (sub) { const nav = document.querySelector('#p-' + page + ' .subnav[id]'); if (nav) showSub(nav, sub); }
  if (page === 'startplan') { const st = parseInt(qp.get('step'), 10); if (!isNaN(st)) { S.step = Math.max(0, Math.min(STEPS.length - 1, st - 1)); save(); } renderWiz(); }
  document.getElementById('side').classList.remove('open');
  window.scrollTo(0, 0);
}
function toggleNav(){ document.getElementById('side').classList.toggle('open'); }
document.addEventListener('click', e => { const side = $('#side'); if (side.classList.contains('open') && !side.contains(e.target) && !e.target.closest('.topbar')) side.classList.remove('open'); });
window.addEventListener('hashchange', route);
function showSub(nav, sub){
  nav.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.sub === sub));
  nav.closest('section').querySelectorAll('.sub').forEach(s => s.classList.toggle('show', s.id === 'sub-' + sub));
}
document.querySelectorAll('.subnav[id]').forEach(nav => nav.addEventListener('click', e => { const b = e.target.closest('button[data-sub]'); if (b) showSub(nav, b.dataset.sub); }));

/* ---------- Lightbox ---------- */
function zoom(src){ const lb=$('#lightbox'); lb.querySelector('img').src=src; lb.classList.add('on'); }
document.addEventListener('click', e => { const z = e.target.closest('[data-zoom]'); if (z) zoom(z.dataset.zoom); });
document.addEventListener('keydown', e => { if (e.key==='Escape') $('#lightbox').classList.remove('on'); });

/* ---------- Fotos ---------- */
(function(){
  const g = $('#gallery');
  const fig = f => `<figure><img loading="lazy" src="${f.bild}" alt="${esc(f.titel)}" data-zoom="${f.bild}"><figcaption>${esc(f.titel)}</figcaption></figure>`;
  g.innerHTML = ERGEBNISSE.length ? `<div class="gallery">${ERGEBNISSE.map(fig).join('')}</div>` : `<div class="empty">Nach dem Training findest du hier die Fotos unserer Flipcharts und Pinnwände.</div>`;
  document.querySelectorAll('.unsere-fotos[data-ort]').forEach(el => {
    const fs = ERGEBNISSE.filter(f => (f.orte||[]).includes(el.dataset.ort));
    if (fs.length) el.innerHTML = `<div class="fcbox"><span class="eyebrow">Unsere Ergebnisse</span><div class="gallery">${fs.map(fig).join('')}</div></div>`;
  });
})();

/* ---------- Bedürfnisse ---------- */
const NEEDS=[
 {t:"Bindung",hear:"Ich gehöre dazu und kann mich auf andere verlassen.",q:"Zugehörigkeit, Verbundenheit und Unterstützung durch andere Menschen. Erfüllte Bindung gibt Sicherheit und Vertrauen.",fix:"Echtes Interesse aneinander, gemeinsame Rituale, niemand wird übergangen.",miss:"Rückzug, Grüppchen, Gespräche nur noch über Dritte."},
 {t:"Orientierung und Kontrolle",hear:"Ich verstehe, was passiert, und kann mitgestalten.",q:"Klarheit, Stabilität und das Gefühl, Situationen verstehen und beeinflussen zu können.",fix:"Klare Zuständigkeiten, früh informieren, Entscheidungen erklären.",miss:"Gerüchte, viele Rückfragen, Festhalten am Alten."},
 {t:"Selbstwertschutz und Selbstwerterhöhung",hear:"Ich werde gesehen und kann wachsen.",q:"Anerkennung, Respekt und Wertschätzung. Und die Möglichkeit, an Herausforderungen zu wachsen.",fix:"Anerkennung konkret aussprechen, Kritik unter vier Augen, Neues zutrauen.",miss:"Rechtfertigen, Verteidigen, Kränkung, Rückzug aus Verantwortung."},
 {t:"Lustgewinn und Unlustvermeidung",hear:"Die Arbeit macht auch Freude.",q:"Angenehme Erfahrungen suchen, Belastendes vermeiden. Das sorgt für Wohlbefinden und Gleichgewicht.",fix:"Erfolge feiern, Ärgernisse abbauen, Humor zulassen.",miss:"Lustlosigkeit, Dienst nach Vorschrift, Gereiztheit."},
 {t:"Kohärenz",hear:"Was ich tue, ergibt Sinn.",q:"Sinn, Zusammenhang und Stimmigkeit. Was ich tue, passt zu meinen Werten.",fix:"Das Wozu klären, Widersprüche offen ansprechen.",miss:"Zynismus, „Das bringt doch eh nichts“."}];
$('#needs').innerHTML = NEEDS.map((n,i)=>`<div class="need"><span class="k">${i+1} · ${esc(n.t)}</span><span class="hear">${esc(n.hear)}</span><p>${esc(n.q)}</p><div class="help"><b>Im Team erfüllt, wenn …</b>${esc(n.fix)}</div><div class="help" style="background:#FAE6E6;margin-top:0"><b style="color:#CB0101">Woran man merkt, dass es fehlt</b>${esc(n.miss)}</div></div>`).join('');

/* ---------- Startplan ---------- */
const STEPS=["Meine Situation","Mein Team in der Veränderung","Erwartungen klären","Mein Führungskorridor","Fünf Grundbedürfnisse","Meine Matrix","Mein Gespräch","Meine ersten Schritte","Zusammenfassung"];
const QUADS=[
 {k:"b",t:"Kann und will",c:"qb"},
 {k:"a",t:"Kann, will gerade nicht",c:"qa"},
 {k:"d",t:"Will, kann noch nicht",c:"qd"},
 {k:"c",t:"Kann noch nicht, will gerade nicht",c:"qc"}];
const P = () => S.plan || (S.plan = {team:[]});
function field(path, label, ph='', area=false, hint=''){
  const v = esc(getP('plan.'+path) || ''); const id='f-'+path.replace(/\W/g,'-');
  return `<label class="l" for="${id}">${label}</label>${hint?`<p class="hint">${hint}</p>`:''}${area?`<textarea id="${id}" data-save="plan.${path}" placeholder="${esc(ph)}">${v}</textarea>`:`<input type="text" id="${id}" data-save="plan.${path}" placeholder="${esc(ph)}" value="${v}">`}`;
}
function matrix(){
  const tm=(P().team||[]).filter(m=>m.kz);
  const cell=q=>`<div class="${q.c}"><b>${q.t}</b><div class="chips">${tm.filter(m=>m.q===q.k).map(m=>`<span>${esc(m.kz)}</span>`).join('')}</div></div>`;
  const by=k=>QUADS.find(q=>q.k===k);
  return `<div class="sw"><div class="ax-y">Können ↑</div><div class="q">${cell(by('a'))}${cell(by('b'))}${cell(by('c'))}${cell(by('d'))}</div><div></div><div class="ax-x">Wollen →</div></div>`;
}
function stepBody(i){
  const p=P();
  switch(i){
    case 0: return `<h3>Meine Situation</h3><p class="hint">Ein paar Sätze, damit du später siehst, wo du gestartet bist.</p>${field('rolle','Meine Rolle und mein Team','Ich führe … Personen im Bereich …')}${field('seit','Seit wann bin ich Führungskraft?','zum Beispiel seit 1. September')}${field('herkunft','Woher komme ich?','aus dem eigenen Team, aus einem anderen Bereich, von außen')}${field('fuehrung','Führen heißt für mich …','',true)}${field('anliegen','Was will ich aus diesen zwei Tagen mitnehmen?','Meine Hashtags: #… #…',true)}`;
    case 1: return `<h3>Mein Team in der Veränderung</h3><p class="hint">Denk an die Veränderungskurve.</p>${field('kurve.team','Wo steht mein Team gerade?','zum Beispiel Widerstand, rationale Einsicht …')}${field('kurve.ich','Wo stehe ich selbst?')}${field('kurve.braucht','Was braucht mein Team jetzt von mir?','',true)}`;
    case 2: return `<h3>Erwartungen klären</h3>${field('erw.fragen','Welche Fragen hat mein Team wahrscheinlich?','Urlaub, Homeoffice, Erreichbarkeit, Entscheidungen …',true)}${field('erw.antworten','Meine Antworten darauf','',true,'Und ehrlich: Was weiß ich noch nicht, bis wann kläre ich es?')}${field('erw.ich','Was erwarte ich von meinem Team?','',true)}${field('erw.fk','Was muss ich mit meiner eigenen Führungskraft klären?','',true)}${field('erw.termin','Wann führe ich das Erwartungsgespräch?')}`;
    case 3: return `<h3>Mein Führungskorridor</h3>${field('korr.ziele','1 · Welche Ziele habe ich für meinen Bereich?','',true)}${field('korr.erw','2 · Was erwarte ich, damit wir die Ziele erreichen?','',true)}${field('korr.werte','3 · Welche Werte und Prinzipien gelten für unsere Zusammenarbeit?','',true)}${field('korr.komm','4 · Welche Kommunikation braucht es dafür?','Teamrunde, Einzelgespräche, Kanäle …',true)}`;
    case 4: return `<h3>Fünf Grundbedürfnisse</h3><p class="hint">Was tust du konkret, um jedes Bedürfnis in deinem Team zu stärken?</p>${NEEDS.map((n,k)=>field('need.'+k,`${k+1} · ${n.t}`,'Ab Montag werde ich …')).join('')}`;
    case 5: return `<h3>Meine Matrix</h3><p class="hint">Erst dein Führungsverhalten und deine Fragen pro Feld. Dann ordnest du dein Team ein, mit Kürzeln statt Namen.</p>
      ${QUADS.map(q=>`<div class="player"><div class="lbl" style="margin-top:0">${q.t}</div>${field('sw.'+q.k+'.tun','So führe ich hier','',true)}${field('sw.'+q.k+'.fragen','Das frage ich','',true)}</div>`).join('')}
      <h3 style="margin-top:20px">Mein Team</h3><p class="hint">Bis zu zwölf Personen. Denk an eine konkrete Aufgabe.</p>
      <div id="tlist">${(p.team||[]).map((m,k)=>`<div class="player"><div class="top"><input type="text" placeholder="Kürzel" value="${esc(m.kz)}" data-tm="${k}" data-f="kz"><button class="x" data-del="${k}" aria-label="Entfernen">×</button></div><div class="lbl">Bei welcher Aufgabe?</div><input type="text" value="${esc(m.aufgabe)}" data-tm="${k}" data-f="aufgabe"><div class="lbl">Feld</div><select data-tm="${k}" data-f="q"><option value="">bitte wählen</option>${QUADS.map(q=>`<option value="${q.k}" ${m.q===q.k?'selected':''}>${esc(q.t)}</option>`).join('')}</select><div class="lbl">Was will ich von dieser Person wissen?</div><input type="text" value="${esc(m.frage)}" data-tm="${k}" data-f="frage"></div>`).join('')}</div>
      ${(p.team||[]).length<12?'<button class="btn ghost small" id="addTm">+ Person hinzufügen</button>':''}<h3 style="margin-top:20px">Dein Team auf einen Blick</h3><div id="mx">${matrix()}</div>`;
    case 6: return `<h3>Mein Gespräch</h3>${field('g.mit','Mit wem? (Kürzel)')}${field('g.anlass','Worum geht es?','',true)}${field('g.G','Ziel · Was soll am Ende klar sein?','',true)}${field('g.R','Realität · Wie sehe ich die Situation? Was vermute ich zur Sicht der anderen Person?','',true)}${field('g.O','Möglichkeiten · Welche Fragen stelle ich? Was biete ich an?','',true)}${field('g.W','Vereinbarung · Was soll bis wann passieren?','',true)}${field('g.einstieg','Mein erster Satz','Ich möchte heute mit dir über … sprechen.')}
      <h3 style="margin-top:22px">Falls es blockiert</h3>${field('g.weiss','Ich weiß …')}${field('g.wichtig','Mir ist wichtig …')}${field('g.offen','Ich bin offen …')}`;
    case 7: return `<h3>Meine ersten Schritte</h3><p class="hint">Was tust du in den nächsten 30 Tagen? Möglichst konkret, mit Datum.</p>${field('s.1','Schritt 1')}${field('s.1w','Bis wann?')}${field('s.2','Schritt 2')}${field('s.2w','Bis wann?')}${field('s.3','Schritt 3')}${field('s.3w','Bis wann?')}${field('s.buddy','Mein Transfer-Buddy aus der Gruppe')}${field('s.satz','Mein wichtigster Satz aus den zwei Tagen','',true)}`;
    case 8: return `<h3>Zusammenfassung</h3>${summary()}<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px"><button class="btn" id="pdf">Als PDF sichern</button><button class="btn ghost" id="cpy">Als Text kopieren</button></div><p class="hint" style="margin-top:10px">Beim PDF öffnet sich das Drucken-Fenster. Wähle dort „Als PDF sichern“.</p>`;
  }
}
function line(label,v){ return v?`<p><b>${label}:</b> ${esc(v).replace(/\n/g,'<br>')}</p>`:''; }
function summary(){
  const p=P(), g=p.g||{}, s=p.s||{};
  let h=`<h3>Meine Situation</h3>${line('Rolle und Team',p.rolle)}${line('Führungskraft seit',p.seit)}${line('Herkunft',p.herkunft)}${line('Führen heißt für mich',p.fuehrung)}${line('Mein Anliegen',p.anliegen)}`;
  h+=`<h3>Mein Team in der Veränderung</h3>${line('Team',p.kurve?.team)}${line('Ich',p.kurve?.ich)}${line('Was mein Team braucht',p.kurve?.braucht)}`;
  h+=`<h3>Erwartungen</h3>${line('Fragen meines Teams',p.erw?.fragen)}${line('Meine Antworten',p.erw?.antworten)}${line('Was ich erwarte',p.erw?.ich)}${line('Mit meiner Führungskraft klären',p.erw?.fk)}${line('Erwartungsgespräch',p.erw?.termin)}`;
  h+=`<h3>Mein Führungskorridor</h3>${line('Ziele',p.korr?.ziele)}${line('Erwartungen',p.korr?.erw)}${line('Werte und Prinzipien',p.korr?.werte)}${line('Kommunikation',p.korr?.komm)}`;
  h+=`<h3>Grundbedürfnisse</h3>${NEEDS.map((n,k)=>line(n.t,p.need?.[k])).join('')}`;
  h+=`<h3>Meine Matrix</h3>${QUADS.map(q=>line(q.t+', so führe ich',p.sw?.[q.k]?.tun)+line(q.t+', das frage ich',p.sw?.[q.k]?.fragen)).join('')}`;
  const tm=(p.team||[]).filter(m=>m.kz).map(m=>`${esc(m.kz)}${m.aufgabe?' bei '+esc(m.aufgabe):''}${m.q?': '+esc(QUADS.find(q=>q.k===m.q).t):''}${m.frage?' · Frage: '+esc(m.frage):''}`).join('<br>');
  if(tm) h+=`<p><b>Mein Team:</b><br>${tm}</p>`;
  h+=`<h3>Mein Gespräch</h3>${line('Mit',g.mit)}${line('Anlass',g.anlass)}${line('Ziel',g.G)}${line('Realität',g.R)}${line('Möglichkeiten',g.O)}${line('Vereinbarung',g.W)}${line('Erster Satz',g.einstieg)}${line('Ich weiß',g.weiss)}${line('Mir ist wichtig',g.wichtig)}${line('Ich bin offen',g.offen)}`;
  const W=S.wandel||{}, D=S.druck||{};
  if(W.v||W.u||W.k||W.a) h+=`<h3>Meine Antwort auf VUKA</h3>${line('Vision',W.v)}${line('Verstehen',W.u)}${line('Klarheit',W.k)}${line('Agilität',W.a)}`;
  if(D.lassen||D.abgeben||D.planen) h+=`<h3>Meine Prioritäten</h3>${line('Das lasse ich',D.lassen)}${line('Das gebe ich ab',D.abgeben)}${line('Feste Zeit für',D.planen)}`;
  h+=`<h3>Meine ersten Schritte</h3>${[1,2,3].map(n=>s[n]?line('Schritt '+n,s[n]+(s[n+'w']?' (bis '+s[n+'w']+')':'')):'').join('')}${line('Transfer-Buddy',s.buddy)}${line('Mein wichtigster Satz',s.satz)}`;
  return h;
}
function renderWiz(){
  const i = S.step || 0;
  $('#steps').innerHTML = STEPS.map((_,k)=>`<i class="${k<=i?'on':''}"></i>`).join('');
  $('#stepname').textContent = `Schritt ${i+1} von ${STEPS.length} · ${STEPS[i]}`;
  $('#wiz').innerHTML = stepBody(i);
  $('#wPrev').style.visibility = i===0?'hidden':'visible';
  $('#wNext').style.visibility = i===STEPS.length-1?'hidden':'visible';
  bindInputs($('#wiz'));
  const p=P();
  const redraw=()=>{ const mx=$('#mx'); if(mx) mx.innerHTML=matrix(); };
  $('#wiz').querySelectorAll('[data-tm]').forEach(inp=>inp.addEventListener(inp.tagName==='SELECT'?'change':'input',()=>{ p.team[inp.dataset.tm][inp.dataset.f]=inp.value; save(); redraw(); }));
  $('#wiz').querySelectorAll('[data-del]').forEach(b=>b.addEventListener('click',()=>{ p.team.splice(+b.dataset.del,1); save(); renderWiz(); }));
  const add=$('#addTm'); if(add) add.addEventListener('click',()=>{ (p.team||(p.team=[])).push({kz:''}); save(); renderWiz(); const ins=$('#wiz').querySelectorAll('[data-f="kz"]'); ins[ins.length-1]?.focus(); });
  const pdf=$('#pdf'); if(pdf) pdf.addEventListener('click',()=>{ $('#print-area').innerHTML=`<h2>Mein Startplan · Das erste Mal führen 1</h2>`+summary()+`<p style="margin-top:16px;color:#666">Susanne Tours · susannetours.com</p>`; document.body.classList.add('printing'); window.print(); setTimeout(()=>document.body.classList.remove('printing'),500); });
  const cpy=$('#cpy'); if(cpy) cpy.addEventListener('click',()=>{ const d=document.createElement('div'); d.innerHTML=summary(); copy(d.innerText); });
}
$('#wPrev').addEventListener('click',()=>{ S.step=Math.max(0,(S.step||0)-1); save(); renderWiz(); window.scrollTo(0,0); });
$('#wNext').addEventListener('click',()=>{ S.step=Math.min(STEPS.length-1,(S.step||0)+1); save(); renderWiz(); window.scrollTo(0,0); });

/* ---------- Eingaben speichern ---------- */
function bindInputs(root){
  root.querySelectorAll('[data-save]').forEach(el=>{
    if (el.dataset.bound) return; el.dataset.bound='1';
    const v=getP(el.dataset.save); if (v!=null && el.value==='') el.value=v;
    el.addEventListener('input',()=>{ setP(el.dataset.save, el.value); });
  });
}

bindInputs(document);

/* ---------- Satzstarter ---------- */
const SENT=[
 ["Ein schwieriges Gespräch eröffnen",["Ich möchte heute mit dir über etwas sprechen, das mir wichtig ist.","Ich habe ein Thema, das mir nicht leicht fällt. Ich spreche es trotzdem an, weil mir an unserer Zusammenarbeit liegt.","Ich will nicht um den heißen Brei herumreden. Es geht um …","Hast du gerade zehn Minuten? Mir ist etwas aufgefallen, das ich mit dir klären möchte."]],
 ["Kritik ansprechen",["Mir ist aufgefallen, dass … Wie siehst du das?","In den letzten zwei Wochen ist dreimal … passiert. Das hat dazu geführt, dass …","Ich habe beobachtet, dass … Bei mir kommt das so an: … Ich wünsche mir, dass …","Mir geht es nicht um Schuld. Mir geht es darum, wie wir das künftig lösen.","Ich schätze deine Arbeit bei … Genau deshalb spreche ich offen an, was mir bei … fehlt.","Was brauchst du, damit das ab jetzt klappt?"]],
 ["Wenn jemand nicht redet",["Mir fällt auf, dass du gerade sehr still bist. Ist etwas?","Ich weiß, dass … Mir ist wichtig, dass … Ich bin offen für …","Liegt es eher an der Aufgabe, an der Zusammenarbeit oder an etwas ganz anderem?","Du musst mir das nicht jetzt sagen. Lass uns am … noch einmal darüber sprechen.","Ich brauche von dir bis … eine klare Rückmeldung, ob das klappt."]],
 ["Wenn es emotional wird",["Das ist wichtig. Was muss ich verstehen?","Ich merke, dass dich das sehr beschäftigt. Erzähl mir mehr.","Lass uns kurz durchatmen. Magst du einen Kaffee?","Wie sähe ein guter Weg für dich aus?"]],
 ["Erwartungen klären",["Mir ist in der Zusammenarbeit besonders wichtig, dass …","Was brauchst du von mir, damit du gut arbeiten kannst?","Was soll so bleiben, wie es ist? Was soll sich ändern?","Das weiß ich heute noch nicht. Ich sage dir bis … Bescheid."]],
 ["Vereinbaren und nachfassen",["Lass uns kurz festhalten: Du machst … bis … Ich mache …","Wann schauen wir wieder gemeinsam drauf?","Danke für das offene Gespräch gestern. Hier noch einmal kurz, was wir vereinbart haben: …"]]];
$('#sentences').innerHTML = SENT.map(([t,arr])=>`<div class="card"><h3>${esc(t)}</h3>${arr.map(s=>`<div class="sent"><q>${esc(s)}</q><button class="btn ghost small" data-copy="${esc(s)}" aria-label="Kopieren">Kopieren</button></div>`).join('')}</div>`).join('');
$('#sentences').addEventListener('click',e=>{ const b=e.target.closest('[data-copy]'); if(b) copy(b.dataset.copy); });

/* ---------- Nach dem Training ---------- */
const WEEKS=[["e1","Woche 1","Mit deiner eigenen Führungskraft klären: Ziele, Spielraum, Entscheidungen."],["e2","Woche 1","Die Alltagsfragen deines Teams beantworten: Urlaub, Homeoffice, Erreichbarkeit."],["e3","Woche 2","Erwartungsgespräche führen, im Team oder einzeln."],["e4","Woche 2","Deinen Führungskorridor im Team vorstellen."],["e5","Woche 3","Regelmäßige Einzelgespräche einplanen und das erste führen."],["e6","Woche 3","Das aufgeschobene Gespräch führen, mit deinem Gesprächsplan."],["e7","Woche 4","Deine Matrix noch einmal anschauen: Wer hat sich bewegt?"],["e8","Woche 4","Deinem Transfer-Buddy schreiben: Was hat geklappt, was nicht?"]];
const wk = S.weeks || (S.weeks = {});
$('#checklist').innerHTML = `<h3>Deine ersten 30 Tage</h3>` + WEEKS.map(([k,w,t])=>`<label class="check"><input type="checkbox" data-week="${k}" ${wk[k]?'checked':''}><span><b>${w}:</b> ${t}</span></label>`).join('');
$('#checklist').querySelectorAll('[data-week]').forEach(c=>c.addEventListener('change',()=>{ wk[c.dataset.week]=c.checked; save(); }));

/* ---------- Folien ---------- */
(function(){const N=FOLIEN,src=i=>"folien/"+String(i+1).padStart(2,"0")+".jpg";let cur=0;
const g=$('#folGrid');g.innerHTML=Array.from({length:N},(_,i)=>`<button type="button" data-f="${i}"><img loading="lazy" src="${src(i)}" alt="Folie ${i+1}"><span>Folie ${i+1}</span></button>`).join('');
const v=$('#folView'),im=$('#folImg'),c=$('#folCount');
function go(n){cur=Math.max(0,Math.min(N-1,n));im.src=src(cur);im.alt="Folie "+(cur+1);c.textContent=String(cur+1);[cur+1,cur-1].forEach(k=>{if(k>=0&&k<N){new Image().src=src(k)}});}
function open(n){v.classList.add("on");document.body.style.overflow="hidden";go(n);}
function close(){v.classList.remove("on");document.body.style.overflow="";if(document.fullscreenElement)document.exitFullscreen?.();}
g.addEventListener("click",e=>{const b=e.target.closest("[data-f]");if(b)open(+b.dataset.f);});
$('#folStart').onclick=()=>open(0);
$('#folPrev').onclick=e=>{e.stopPropagation();go(cur-1)};
$('#folNext').onclick=e=>{e.stopPropagation();go(cur+1)};
$('#folClose').onclick=close;
$('#folFs').onclick=e=>{e.stopPropagation();const fe=document.fullscreenElement||document.webkitFullscreenElement;if(!fe){(v.requestFullscreen||v.webkitRequestFullscreen||function(){}).call(v);}else{(document.exitFullscreen||document.webkitExitFullscreen).call(document);}};
im.onclick=e=>{const r=im.getBoundingClientRect();go(e.clientX>r.left+r.width/3?cur+1:cur-1);};
addEventListener("keydown",e=>{if(!v.classList.contains("on"))return;if(["ArrowRight","PageDown"," ","Enter"].includes(e.key)){e.preventDefault();go(cur+1)}else if(["ArrowLeft","PageUp","Backspace"].includes(e.key)){e.preventDefault();go(cur-1)}else if(e.key==="Escape"){close()}});
let tx=null;v.addEventListener("touchstart",e=>tx=e.touches[0].clientX,{passive:true});v.addEventListener("touchend",e=>{if(tx===null)return;const d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50)go(d<0?cur+1:cur-1);tx=null;});
})();

route();
