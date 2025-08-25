// frontend/assets/app.js
// Krav: frontend/assets/config.js definerer const API_BASE = "http://127.0.0.1:8000" (eller din Render-URL)

const $ = (s)=>document.querySelector(s);

img.onload = ()=>{
  state.imgNatural.w = img.naturalWidth;
  state.imgNatural.h = img.naturalHeight;
  computeScale();

  // NYT: giv overlay samme størrelse som billedet
  const overlay = document.getElementById('overlay');
  overlay.style.width  = img.clientWidth + 'px';
  overlay.style.height = img.clientHeight + 'px';

  renderOverlay();
};

const state = {
  editor: false,
  imagesBase: localStorage.getItem('imagesBase') || './images',
  opgaveNr: 1,
  totalOpgaver: 20,
  questions: [],        // spørgsmål for valgt opgaveNr
  layout: {},           // { "1.1": [ {x,y,w,h,type?} ] }
  answers: JSON.parse(localStorage.getItem('answers') || '{}'),
  imgNatural: { w: 0, h: 0 },
  scale: 1
};

function pad2(n){ return String(n).padStart(2,'0'); }
function computeScale(){
  const img = $('#opgaveImg');
  state.scale = img.clientWidth / (state.imgNatural.w || img.clientWidth);
}
function setTitle(){ $('#title')?.textContent = `Opgavesæt – Opgave ${state.opgaveNr}`; }

async function fetchJSON(url){
  const r = await fetch(url);
  if(!r.ok) throw new Error(`${r.status}: ${await r.text()}`);
  return r.json();
}

async function loadQuestions(){
  const list = await fetchJSON(`${API_BASE}/questions?assignment_id=1&opgave_nr=${state.opgaveNr}`);
  state.questions = list;
  renderQnList();
  renderImage();
}

async function loadLayout(){
  const data = await fetchJSON(`${API_BASE}/layout/1`);
  state.layout = data.layout || {};
  renderOverlay();
}

function renderQnList(){
  const box = $('#qnList'); if(!box) return;
  box.innerHTML = '';
  state.questions.forEach(q=>{
    const el = document.createElement('div');
    el.className = 'qn';
    el.innerHTML = `
      <div class="row">
        <div>
          <strong>${q.question_number}</strong>
          <div class="meta">${(q.prompt||'').slice(0,120)}</div>
        </div>
        <div class="actions"></div>
      </div>`;
    const actions = el.querySelector('.actions');
    const addBtn = document.createElement('button');
    addBtn.textContent = '+ felt';
    addBtn.title = 'Tilføj felt på billedet';
    addBtn.onclick = ()=> addField(q.question_number);
    actions.appendChild(addBtn);
    box.appendChild(el);
  });
}

function renderImage(){
  const img = $('#opgaveImg');
  if(!img) return;
  img.src = `${state.imagesBase}/opgave_${pad2(state.opgaveNr)}.png`;
  img.onload = ()=>{
    state.imgNatural.w = img.naturalWidth;
    state.imgNatural.h = img.naturalHeight;
    computeScale();
    renderOverlay();
  };
}

function addField(qn){
  if(!state.layout[qn]) state.layout[qn] = [];
  state.layout[qn].push({ x:40, y:40, w:220, h:40, type:'text' });
  renderOverlay();
  // (valgfrit) gem layout ved hvert trin: saveLayout();
}

function renderOverlay(){
  const overlay = $('#overlay'); if(!overlay) return;
  overlay.innerHTML = '';
  state.questions.forEach(q=>{
    const rects = state.layout[q.question_number] || [];
    rects.forEach((r, idx)=>{
      const d = document.createElement('div');
document.getElementById('saveLayout')?.addEventListener('click', saveLayout);

document.getElementById('autoLayout')?.addEventListener('click', async () => {
  try {
    const params = new URLSearchParams({
      opgave_nr: String(state.opgaveNr),
      start_x: '40',
      start_y: '80',
      width: '300',
      height: '40',
      gap: '50'
    });
    const res = await fetch(`${API_BASE}/layout/1/autogen?` + params.toString(), { method: 'POST' });
    const data = await res.json();
    if (!res.ok || data.ok === false) throw new Error(data.error || 'Ukendt fejl');
    // hent layout igen og tegn felter
    await loadLayout();
    alert('Auto-layout oprettet for opgave ' + state.opgaveNr);
  } catch (e) {
    alert('Kunne ikke autolave layout: ' + e.message);
  }
});

