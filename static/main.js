/* ── TRESDB — main.js ──────────────────────────────── */

const TAB_COLORS = {
  avl:  'var(--avl)',
  rn:   'var(--rn-red)',
  b:    'var(--b-tree)',
  bmas: 'var(--bplus)',
};

const CHIP_EXAMPLES = {
  INSERT: 'INSERT nombre:Ana edad:25 ciudad:Bogotá',
  SELECT: 'SELECT nombre = Ana',
  RANGE:  'RANGE edad 20 30',
  DELETE: 'DELETE nombre = Ana',
  INDEX:  'INDEX ciudad',
  HELP:   'HELP TREES',
};

let tabActual = 'avl';

function cambiarModo(valor) {
  if (valor === 'auto') {
    ejecutarSilencioso('USE TREE auto');
    return;
  }
  // cambia el tab visual y notifica al backend
  setTab(valor);
  ejecutarSilencioso(`USE TREE ${valor}`);
}

async function ejecutarSilencioso(cmd) {
  try {
    await fetch('/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comando: cmd })
    });
  } catch(e) {}
}

/* ── TEMA ──────────────────────────────────────────── */
function initTheme() {
  if (localStorage.getItem('theme') === 'light') {
    document.documentElement.classList.add('light');
    document.getElementById('theme-icon').textContent = '☀️';
  }
}

function toggleTheme() {
  const root = document.documentElement;
  const isLight = root.classList.toggle('light');
  document.getElementById('theme-icon').textContent = isLight ? '☀️' : '🌙';
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
}

function toggleAbout() {
  const modal = document.getElementById('modal-about');
  modal.style.display = modal.style.display === 'none' ? 'flex' : 'none';
}

/* ── TABS ──────────────────────────────────────────── */
function setTab(tab) {
  tabActual = tab;
  document.querySelectorAll('.tab').forEach(t => {
    t.classList.toggle('active', t.dataset.tab === tab);
  });
  mostrarArbolActual();
}

/* ── ÁRBOL EN VISUALIZADOR ─────────────────────────── */
async function mostrarArbolActual() {
  const badge = document.getElementById('op-badge');
  badge.textContent = 'LOADING...';
  badge.style.display = 'block';

  try {
    const res  = await fetch(`/tree/${tabActual}`);
    const data = await res.json();
    const disp = document.getElementById('tree-display');
    const empty = document.getElementById('tree-empty');

    if (data.lineas && data.lineas.length > 0) {
      disp.innerHTML = colorearArbol(data.lineas.join('\n'), tabActual);
      disp.style.display = 'block';
      empty.style.display = 'none';
    } else {
      disp.style.display = 'none';
      empty.style.display = 'flex';
    }
  } catch(e) {
    console.error(e);
  } finally {
    badge.style.display = 'none';
  }
}

function colorearArbol(texto, tab) {
  const seguro = texto
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  if (tab === 'rn') {
    return seguro
      .replace(/\[(\d+)\|R\]/g, '<span class="nr">[$1|R]</span>')
      .replace(/\[(\d+)\|N\]/g, '<span class="nn">[$1|N]</span>');
  }
  if (tab === 'avl') {
    return seguro.replace(/\[(\d+)\]/g, '<span class="na">[$1]</span>');
  }
  if (tab === 'b') {
    return seguro.replace(/\[([^\]]+)\]/g, '<span class="nb">[$1]</span>');
  }
  if (tab === 'bmas') {
    return seguro
      .replace(/\[I\]/g, '<span class="nn">[I]</span>')
      .replace(/\[H\]/g, '<span class="np">[H]</span>')
      .replace(/→/g, '<span class="na">→</span>');
  }
  return seguro;
}

/* ── QUERY ─────────────────────────────────────────── */
async function ejecutar() {
  const input = document.getElementById('cmd-input');
  const cmd   = input.value.trim();
  if (!cmd) return;

  const badge = document.getElementById('op-badge');
  const op    = cmd.split(' ')[0].toUpperCase();
  badge.textContent = op + 'ING...';
  badge.style.display = 'block';

  try {
    const res  = await fetch('/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comando: cmd })
    });
    const data = await res.json();

    input.value = '';
    mostrarResultado(data, cmd);
    agregarLog(cmd, data);
    actualizarStats();
    setTimeout(mostrarArbolActual, 200);
  } catch(e) {
    mostrarResultado({ error: 'Error de conexión con el servidor' }, cmd);
  } finally {
    setTimeout(() => { badge.style.display = 'none'; }, 600);
  }
}

/* ── RESULTADO ─────────────────────────────────────── */
function mostrarResultado(data, cmd) {
  const div = document.getElementById('resultado-panel');

  // use_tree primero — cambia tab y muestra mensaje
  if (data.tipo === 'use_tree') {
    if (data.arbol && data.arbol !== 'auto') {
      setTab(data.arbol);
    }
    div.innerHTML = `<span class="msg-ok">✅ ${escapeHtml(data.mensaje)}</span>`;
    return;
  }

  if (data.error) {
    div.innerHTML = `<span class="msg-err">❌ ${escapeHtml(data.error)}</span>`;
    return;
  }

  if (data.tipo === 'help') {
    div.innerHTML = `<span class="msg-info">${escapeHtml(data.mensaje)}</span>`;
    return;
  }

  if (data.mensaje) {
    div.innerHTML = `<span class="msg-ok">✅ ${escapeHtml(data.mensaje)}</span>`;
    return;
  }

  if (!data.datos || data.datos.length === 0) {
    div.innerHTML = `<span class="msg-empty">Sin resultados para este query.</span>`;
    return;
  }

  const cols = Object.keys(data.datos[0]);
  let html = `<table><thead><tr>${cols.map(c => `<th>${escapeHtml(c)}</th>`).join('')}</tr></thead><tbody>`;
  data.datos.forEach(r => {
    html += `<tr>${cols.map(c => `<td>${escapeHtml(String(r[c] ?? ''))}</td>`).join('')}</tr>`;
  });
  html += '</tbody></table>';
  div.innerHTML = html;
}

/* ── LOG ───────────────────────────────────────────── */
function agregarLog(cmd, data) {
  const op     = cmd.split(' ')[0].toLowerCase();
  const pillar = data.error ? 'error' : op;
  const n      = data.datos ? data.datos.length : 0;
  const hora   = new Date().toLocaleTimeString('es-CO', { hour12: false });
  const result = data.error
    ? data.error.substring(0, 40)
    : data.mensaje
      ? data.mensaje.substring(0, 40)
      : `${n} resultado(s)`;

  const entry = document.createElement('div');
  entry.className = 'log-entry fade-in';
  entry.innerHTML = `
    <div class="log-top">
      <span class="log-pill pill-${pillar}">${op.toUpperCase()}</span>
      <span class="log-cmd">${escapeHtml(cmd)}</span>
      <span class="log-time">${hora}</span>
    </div>
    <div class="log-result">${escapeHtml(result)}</div>
  `;

  const container = document.getElementById('log-entries');
  container.insertBefore(entry, container.firstChild);

  // máximo 50 entradas
  while (container.children.length > 50) {
    container.removeChild(container.lastChild);
  }
}

/* ── STATS ─────────────────────────────────────────── */
async function actualizarStats() {
  try {
    const res  = await fetch('/info');
    const data = await res.json();
    document.getElementById('s-registros').textContent = data.registros;
    document.getElementById('s-altura').textContent    = data.altura_avl;
    document.getElementById('s-indices').textContent   =
      data.indices.length ? data.indices.join(', ') : 'ninguno';
  } catch(e) {}
}

/* ── CHIPS ─────────────────────────────────────────── */
function usarChip(cmd) {
  const input = document.getElementById('cmd-input');
  input.value = CHIP_EXAMPLES[cmd] || cmd;
  input.focus();
}

/* ── UTILS ─────────────────────────────────────────── */
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ── INIT ──────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  actualizarStats();
  mostrarArbolActual();

  document.getElementById('cmd-input')
    .addEventListener('keydown', e => { if (e.key === 'Enter') ejecutar(); });
});