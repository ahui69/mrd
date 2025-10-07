const BASE = location.origin;
const AUTH_TOKEN = localStorage.getItem('AUTH_TOKEN') || 'changeme';

const els = {
  app: document.getElementById('app'),
  sidebar: document.getElementById('sidebar'),
  toggleSidebar: document.getElementById('toggleSidebar'),
  newChat: document.getElementById('newChat'),
  reloadPkg: document.getElementById('reloadPkg'),
  historyList: document.getElementById('historyList'),
  chat: document.getElementById('chat'),
  composer: document.getElementById('composer'),
  input: document.getElementById('message'),
  mic: document.getElementById('mic'),
  fileInput: document.getElementById('fileInput'),
  typing: document.getElementById('typing'),
};

let currentChatId = null;
let chats = loadChats();
let pendingFiles = []; // files selected but not sent yet
let lastActiveTs = Date.now();

function loadChats(){
  try { return JSON.parse(localStorage.getItem('CHATS')||'[]'); } catch(e){ return []; }
}
function saveChats(){ localStorage.setItem('CHATS', JSON.stringify(chats)); }

function createChat(){
  const id = 'chat-' + Date.now();
  const chat = { id, title: 'Nowa rozmowa', messages: [], createdAt: Date.now() };
  chats.unshift(chat); saveChats();
  currentChatId = id; renderHistory(); renderChat();
}
function getChat(){ return chats.find(c => c.id === currentChatId); }
function setTitleFromFirstAssistant(text){
  const chat = getChat(); if(!chat) return;
  if(!chat.title || chat.title === 'Nowa rozmowa'){
    chat.title = (text||'Asystent').slice(0, 48);
    saveChats(); renderHistory();
  }
}

function renderHistory(){
  els.historyList.innerHTML = '';
  chats.forEach(c => {
    const item = document.createElement('div');
    item.className = 'item';
    const btn = document.createElement('button');
    btn.textContent = c.title || 'Rozmowa';
    btn.onclick = () => { currentChatId = c.id; renderChat(); };
    const del = document.createElement('button');
    del.textContent = '✕';
    del.onclick = () => { chats = chats.filter(x => x.id !== c.id); saveChats(); if(currentChatId===c.id) currentChatId=null; renderHistory(); renderChat(); };
    item.append(btn, del); els.historyList.appendChild(item);
  });
}

function renderChat(){
  const chat = getChat();
  els.chat.innerHTML = '';
  (chat?.messages || []).forEach(m => addMsg(m.role, m.content));
}

function addMsg(role, content){
  const div = document.createElement('div');
  div.className = 'msg ' + (role === 'user' ? 'user' : 'assistant');
  div.textContent = content;
  els.chat.appendChild(div);
  els.chat.scrollTop = els.chat.scrollHeight;
}

function setTyping(state){
  els.typing.classList.toggle('hidden', !state);
  els.chat.setAttribute('aria-busy', state ? 'true' : 'false');
}

function toAssistantPayload(){
  const chat = getChat();
  const messages = (chat?.messages||[]).map(m => ({role:m.role, content:m.content}));
  return {
    user: 'user',
    messages,
    allow_research: true,
    allow_news: true,
    allow_sports: true,
    save_memory: true,
    topk: 8,
  };
}

async function callAssistant(){
  const payload = toAssistantPayload();
  // Try streaming first
  try{
    const res = await fetch(`${BASE}/api/assistant/stream`,{
      method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${AUTH_TOKEN}`},
      body: JSON.stringify(payload)
    });
    if(!res.ok) throw new Error(await res.text());
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let acc = '';
    let full = '';
    setTyping(true);
    while(true){
      const {done, value} = await reader.read();
      if(done) break;
      acc += dec.decode(value, {stream:true});
      const chunks = acc.split("\n\n");
      acc = chunks.pop();
      for(const ch of chunks){
        if(!ch.startsWith('data:')) continue;
        const json = ch.slice(5).trim();
        if(!json) continue;
        try{
          const obj = JSON.parse(json);
          if(obj.delta){
            full += obj.delta;
            appendOrUpdateAssistant(full);
          }
        }catch{}
      }
    }
    setTyping(false);
    return {ok:true, answer: full};
  }catch(err){
    const res = await fetch(`${BASE}/api/assistant/chat`,{
      method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${AUTH_TOKEN}`},
      body: JSON.stringify(payload)
    });
    if(!res.ok){ throw new Error(await res.text()); }
    return await res.json();
  }
}

function appendOrUpdateAssistant(text){
  const nodes = [...els.chat.querySelectorAll('.msg.assistant')];
  let div = nodes[nodes.length-1];
  if(!div){
    div = document.createElement('div');
    div.className = 'msg assistant';
    els.chat.appendChild(div);
  }
  div.textContent = text;
  els.chat.scrollTop = els.chat.scrollHeight;
}

async function uploadFiles(files){
  const fd = new FormData();
  [...files].forEach(f => fd.append('files', f));
  const res = await fetch(`${BASE}/api/files/upload`,{
    method:'POST', headers:{'Authorization':`Bearer ${AUTH_TOKEN}`}, body: fd
  });
  if(!res.ok) throw new Error(await res.text());
  return await res.json();
}

// Mic: real-time Polish STT
let recog = null; let recognizing=false;
function supportsWebkitSTT(){ return 'webkitSpeechRecognition' in window; }
function startRec(){
  if(!supportsWebkitSTT()){ alert('STT nieobsługiwane w tej przeglądarce'); return; }
  recog = new webkitSpeechRecognition();
  recog.continuous = true; recog.interimResults = true; recog.lang = 'pl-PL';
  recognizing=true; els.mic.classList.add('on');
  recog.onresult = (e)=>{
    let interim=''; let final='';
    for(let i=e.resultIndex;i<e.results.length;i++){
      const r = e.results[i];
      if(r.isFinal) final += r[0].transcript; else interim += r[0].transcript;
    }
    const base = (els.input.dataset.base||'');
    els.input.value = (base + ' ' + final + ' ' + interim).trim();
  };
  recog.onend = ()=>{ recognizing=false; els.mic.classList.remove('on'); };
  recog.start();
}
function stopRec(){ if(recognizing && recog){ recog.stop(); recognizing=false; els.mic.classList.remove('on'); } }

// Events
els.toggleSidebar.onclick = ()=>{ els.app.classList.toggle('sidebar-open'); };
els.newChat.onclick = ()=>{ createChat(); };
els.reloadPkg.onclick = async ()=>{
  // Refresh knowledge on startup placeholder: ping /api/health
  await fetch(`${BASE}/api/health`);
  alert('Pakiet odświeżony.');
};

els.composer.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const txt = els.input.value.trim();
  if(!txt && pendingFiles.length===0) return;
  lastActiveTs = Date.now();
  if(!currentChatId) createChat();
  const chat = getChat();

  // Attach selected files first (metadata only)
  if(pendingFiles.length>0){
    try{
      const up = await uploadFiles(pendingFiles);
      const items = up.files||[];
      const lines = items.map(it=>`[plik] ${it.name} — ${it.url}`).join('\n');
      chat.messages.push({role:'user', content: `Pliki załączone:\n${lines}`});
      addMsg('user', `Pliki załączone:\n${lines}`);
      pendingFiles = []; els.fileInput.value='';
    }catch(err){ console.error(err); alert('Błąd uploadu plików'); }
  }

  if(txt){ chat.messages.push({role:'user', content: txt}); addMsg('user', txt); els.input.value=''; els.input.dataset.base=''; }

  try{
    setTyping(true);
    const res = await callAssistant();
    const answer = res.answer || '';
    chat.messages.push({role:'assistant', content: answer});
    addMsg('assistant', answer);
    setTitleFromFirstAssistant(answer);
    saveChats();
  }catch(err){
    console.error(err);
    addMsg('assistant', 'Błąd: ' + (''+err.message).slice(0,200));
  }finally{ setTyping(false); }
});

els.fileInput.addEventListener('change', (e)=>{
  pendingFiles = [...(e.target.files||[])];
  const q = document.getElementById('fileQueue');
  q.innerHTML = '';
  pendingFiles.forEach((f, idx)=>{
    const it = document.createElement('div'); it.className='q-item';
    const name = document.createElement('span'); name.textContent = `${f.name} (${Math.round(f.size/1024)} KB)`;
    const rm = document.createElement('span'); rm.className='rm'; rm.textContent='✕';
    rm.onclick = ()=>{ pendingFiles.splice(idx,1); els.fileInput.value=''; const evt = new Event('change'); els.fileInput.dispatchEvent(evt); };
    if(f.type.startsWith('image/')){
      const img = document.createElement('img'); img.style.height='28px'; img.style.borderRadius='4px';
      const reader = new FileReader(); reader.onload = ev=>{ img.src = ev.target.result; }; reader.readAsDataURL(f);
      it.appendChild(img);
    }
    it.append(name, rm); q.appendChild(it);
  });
});

els.mic.addEventListener('click', ()=>{
  if(recognizing) stopRec(); else startRec();
});

// Startup
(function init(){
  // Always load current package (ping backend and prepare empty chat)
  renderHistory();
  // Session restore: jeśli ostatnia aktywność > 60 minut, zacznij świeżo
  const last = Number(localStorage.getItem('LAST_ACTIVE_TS')||'0');
  if(!chats.length || (Date.now()-last) > 60*60*1000){
    chats = []; saveChats(); createChat();
  } else {
    currentChatId = (chats[0] && chats[0].id) || null;
    if(!currentChatId) createChat(); else renderChat();
  }
  setInterval(()=>localStorage.setItem('LAST_ACTIVE_TS', String(lastActiveTs)), 5000);
})();

// Learn (research)
document.getElementById('learnBtn').addEventListener('click', async ()=>{
  const q = document.getElementById('learnInput').value.trim();
  if(!q) return;
  if(!currentChatId) createChat();
  const chat = getChat();
  chat.messages.push({role:'user', content: q}); addMsg('user', q); saveChats();
  setTyping(true);
  try{
    const payload = toAssistantPayload();
    payload.force_intent = 'research';
    const res = await fetch(`${BASE}/api/assistant/chat`,{
      method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${AUTH_TOKEN}`}, body: JSON.stringify(payload)
    });
    const j = await res.json();
    const answer = j.answer || '';
    chat.messages.push({role:'assistant', content: answer}); addMsg('assistant', answer); saveChats();
  }catch(e){ addMsg('assistant', 'Błąd nauki: '+e.message); }
  finally{ setTyping(false); }
});

// Map
document.getElementById('mapBtn').addEventListener('click', async ()=>{
  const o = document.getElementById('origin').value.trim();
  const d = document.getElementById('destination').value.trim();
  if(!o || !d) return;
  try{
    const url = `${BASE}/api/travel/map/static?origin=${encodeURIComponent(o)}&destination=${encodeURIComponent(d)}&size=800x400`;
    const img = document.getElementById('mapImg');
    img.src = url; img.style.display = 'block';
    // Doklej do czatu
    addMsg('assistant', `Mapa trasy: ${o} → ${d}`);
    const imgNode = document.createElement('img'); imgNode.src = url; imgNode.style.maxWidth = '100%';
    const holder = document.createElement('div'); holder.className = 'msg assistant'; holder.appendChild(imgNode); els.chat.appendChild(holder);
    els.chat.scrollTop = els.chat.scrollHeight;
    // Interaktywna mapa: Leaflet + MapTiler/OSM
    const mapDiv = document.getElementById('leafletMap'); mapDiv.style.display='block';
    if(window._leafletMap){ window._leafletMap.remove(); }
    const map = L.map('leafletMap').setView([52.0, 19.0], 5);
    window._leafletMap = map;
    const resPkg = await fetch(`${BASE}/api/system/package`, {headers:{'Authorization':`Bearer ${AUTH_TOKEN}`}});
    const pkg = await resPkg.json();
    const key = (((pkg||{}).package||{}).maptiler_key)||'';
    const tileUrl = key ? `https://api.maptiler.com/maps/streets/256/{z}/{x}/{y}.png?key=${key}` : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    L.tileLayer(tileUrl, {maxZoom: 19}).addTo(map);
    // Geokodowanie origin/destination
    const go = await fetch(`${BASE}/api/travel/geocode?q=${encodeURIComponent(o)}`, {headers:{'Authorization':`Bearer ${AUTH_TOKEN}`}}).then(r=>r.json());
    const gd = await fetch(`${BASE}/api/travel/geocode?q=${encodeURIComponent(d)}`, {headers:{'Authorization':`Bearer ${AUTH_TOKEN}`}}).then(r=>r.json());
    const p1 = (go.items&&go.items[0]) ? [go.items[0].lat, go.items[0].lon] : [0,0];
    const p2 = (gd.items&&gd.items[0]) ? [gd.items[0].lat, gd.items[0].lon] : [0,0];
    L.marker(p1).addTo(map).bindPopup(o);
    L.marker(p2).addTo(map).bindPopup(d);
    const group = new L.featureGroup([L.marker(p1), L.marker(p2)]);
    map.fitBounds(group.getBounds().pad(0.3));
  }catch(e){ addMsg('assistant','Błąd mapy: '+e.message); }
});

// Memory panel actions
document.getElementById('memStmBtn').addEventListener('click', async ()=>{
  try{
    const r = await fetch(`${BASE}/api/memory/context`, {headers:{'Authorization':`Bearer ${AUTH_TOKEN}`}});
    const j = await r.json();
    const list = document.getElementById('memList');
    list.innerHTML = '<b>STM:</b><br>' + (j.items||[]).map(x=>`${x.role}: ${x.content}`).join('<br>');
  }catch(e){ alert('STM błąd'); }
});

document.getElementById('memSearchBtn').addEventListener('click', async ()=>{
  const q = document.getElementById('memQuery').value.trim(); if(!q) return;
  try{
    const r = await fetch(`${BASE}/api/ltm/search?q=${encodeURIComponent(q)}`, {headers:{'Authorization':`Bearer ${AUTH_TOKEN}`}});
    const j = await r.json();
    const list = document.getElementById('memList');
    list.innerHTML = '<b>LTM:</b><br>' + (j.items||[]).map(x=>`${(x.id||'').slice(0,6)} ${x.text}`).join('<br>');
  }catch(e){ alert('LTM błąd'); }
});

document.getElementById('memReindexBtn').addEventListener('click', async ()=>{
  try{
    await fetch(`${BASE}/api/ltm/reindex`, {method:'POST', headers:{'Authorization':`Bearer ${AUTH_TOKEN}`}});
    alert('Zreindeksowano LTM');
  }catch(e){ alert('Błąd reindex'); }
});

document.getElementById('memSaveLastBtn').addEventListener('click', async ()=>{
  const nodes = [...els.chat.querySelectorAll('.msg.assistant')];
  const last = nodes[nodes.length-1]; if(!last) return alert('Brak odpowiedzi');
  const text = last.textContent || '';
  try{
    await fetch(`${BASE}/api/ltm/add`, {method:'POST', headers:{'Authorization':`Bearer ${AUTH_TOKEN}`, 'Content-Type':'application/json'}, body: JSON.stringify({text, tags:'chat,manual', conf:0.72})});
    alert('Zapisano do LTM');
  }catch(e){ alert('Błąd zapisu LTM'); }
});
