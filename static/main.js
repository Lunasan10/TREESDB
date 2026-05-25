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
  UPDATE: 'UPDATE nombre = Ana SET edad:26 ciudad:Medellín',
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
  mostrarArbolActual();
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
  mostrarArbolActual(false);
}

/* ── ÁRBOL EN VISUALIZADOR ─────────────────────────── */
async function mostrarArbolActual(animar = false) {
  const badge = document.getElementById('op-badge');
  const disp  = document.getElementById('tree-display');
  const empty = document.getElementById('tree-empty');

  if (animar) {
    badge.style.display = 'block';
  }

  try {
    const res  = await fetch(`/tree-json/${tabActual}`);
    const data = await res.json();

    if (data.arbol) {
      const svg = renderizarSVG(data.arbol, tabActual);
      disp.innerHTML = svg || '';
      disp.style.display = 'block';
      empty.style.display = 'none';
    } else {
      disp.style.display = 'none';
      empty.style.display = 'flex';
    }
  } catch(e) {
    console.error('[TRESDB] Error renderizando árbol:', e);
  } finally {
    setTimeout(() => { badge.style.display = 'none'; }, 500);
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
  const badgeTextos = {
  INSERT: '🌱 INSERTANDO...',
  SELECT: '🔍 BUSCANDO...',
  DELETE: '🍂 ELIMINANDO...',
  RANGE:  '↔ RANGO...',
  INDEX:  '📌 INDEXANDO...',
  };
  badge.textContent = badgeTextos[op] || '⚙️ PROCESANDO...';
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
    setTimeout(() => mostrarArbolActual(true), 200)
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
    div.innerHTML = renderHelp(data.mensaje);
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

function renderHelp(texto) {
  const lineas = texto.split('\n');
  let html = '<div class="help-panel">';

  lineas.forEach(linea => {
    const t = linea.trim();
    if (!t) {
      html += '<div class="help-space"></div>';
    } else if (t.startsWith('🌿') || t.startsWith('🌳')) {
      html += `<div class="help-title">${escapeHtml(t)}</div>`;
    } else if (t.startsWith('🌱') || t.startsWith('🔍') ||
               t.startsWith('🍂') || t.startsWith('↔')  ||
               t.startsWith('📌') || t.startsWith('AVL') ||
               t.startsWith('R-N') || t.startsWith('B+') ||
               t.startsWith('B ')) {
      const [cmd, ...resto] = t.split('→');
      html += `<div class="help-row">
        <span class="help-cmd">${escapeHtml(cmd.trim())}</span>
        ${resto.length ? `<span class="help-desc">→ ${escapeHtml(resto.join('→').trim())}</span>` : ''}
      </div>`;
    } else if (t.includes('INSERT') || t.includes('SELECT') ||
               t.includes('RANGE')  || t.includes('DELETE') ||
               t.includes('INDEX')  || t.includes('SHOW')   ||
               t.includes('USE')    || t.includes('INFO')   ||
               t.includes('HELP')) {
      html += `<div class="help-example"><span class="help-prompt">~</span> ${escapeHtml(t)}</div>`;
    } else {
      html += `<div class="help-line">${escapeHtml(t)}</div>`;
    }
  });

  html += '</div>';
  return html;
}

/* ── LOG ───────────────────────────────────────────── */
function agregarLog(cmd, data) {
  const op     = cmd.split(' ')[0].toLowerCase();
  const pillar = data.error ? 'error' : op;
  const n      = data.datos ? data.datos.length : 0;
  const hora   = new Date().toLocaleTimeString('es-CO', { hour12: false });
  const arbol  = data.arbol ? `<span class="log-arbol">${data.arbol}</span>` : '';
  const result = data.error
    ? data.error
    : data.mensaje
      ? data.mensaje
      : `${n} resultado(s)`;

  const entry = document.createElement('div');
  entry.className = 'log-entry fade-in';
  entry.innerHTML = `
    <div class="log-top">
      <span class="log-pill pill-${pillar}">${op.toUpperCase()}</span>
      <span class="log-cmd">${escapeHtml(cmd)}</span>
      <span class="log-time">${hora}</span>
    </div>
    <div class="log-result">${escapeHtml(result)} ${arbol}</div>
  `;

  const container = document.getElementById('log-entries');
  container.insertBefore(entry, container.firstChild);
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

/* ── SVG RENDERER ──────────────────────────────────── */

const SVG_CONFIG = {
  nodeR:    20,      // radio del nodo
  levelH:   70,      // altura entre niveles
  minSep:   52,      // separación mínima entre nodos
  padX:     40,
  padY:     50,
};

// ── Calcular posiciones x,y de cada nodo ─────────────

function calcularPosiciones(nodo, profundidad = 0, contador = { val: 0 }, tab = 'avl') {
  if (!nodo) return null;

  const izq = calcularPosiciones(nodo.izquierda || null, profundidad + 1, contador, tab);
  const sep = SVG_CONFIG.minSep * (tab === 'rn' ? 1.8 : 1);
  const x   = contador.val * sep;
  contador.val++;
  const der = calcularPosiciones(nodo.derecha || null, profundidad + 1, contador, tab);

  return { ...nodo, x, y: profundidad * SVG_CONFIG.levelH, izquierda: izq, derecha: der };
}

function calcularPosicionesB(nodo, profundidad = 0, contador = { val: 0 }) {
  if (!nodo) return null;
  const hijos = (nodo.hijos || []).map(h => calcularPosicionesB(h, profundidad + 1, contador));
  const x = contador.val * SVG_CONFIG.minSep * 1.8;
  contador.val++;
  return { ...nodo, x, y: profundidad * SVG_CONFIG.levelH, hijos };
}

function bbox(nodo, tipo) {
  // encontrar ancho y alto total del árbol
  let minX = Infinity, maxX = -Infinity, maxY = 0;
  function walk(n) {
    if (!n) return;
    if (n.x < minX) minX = n.x;
    if (n.x > maxX) maxX = n.x;
    if (n.y > maxY) maxY = n.y;
    if (tipo === 'b' || tipo === 'bmas') {
      (n.hijos || []).forEach(walk);
    } else {
      walk(n.izquierda);
      walk(n.derecha);
    }
  }
  walk(nodo);
  return { minX, maxX, maxY };
}

// ── Renderizar SVG ────────────────────────────────────

function renderizarSVG(arbol, tab) {
  if (!arbol) return null;

  const cfg   = SVG_CONFIG;
  const esB   = tab === 'b' || tab === 'bmas';
  const nodos = esB
    ? calcularPosicionesB(arbol)
    : calcularPosiciones(arbol, 0, { val: 0 }, tab);

  const { minX, maxX, maxY } = bbox(nodos, tab);
  const offsetX = cfg.padX - minX;
  const W = maxX - minX + cfg.padX * 2 + cfg.nodeR * 4;
  const H = maxY + cfg.padY * 2 + cfg.nodeR * 2;

  let edges = '';
  let nodes = '';

  function colorNodo(n) {
    const isDark = !document.documentElement.classList.contains('light');

    if (tab === 'avl') return {
      fill:   isDark ? '#1e3a28' : '#e8f5ee',
      stroke: 'var(--avl)',
      text:   'var(--avl)'
    };
    if (tab === 'rn') return n.color === 'R'
      ? { fill: isDark ? '#3a0a0a' : '#fde8e8', stroke: 'var(--rn-red)', text: 'var(--rn-red)' }
      : { fill: isDark ? '#1a1a2e' : '#e8e8f0', stroke: 'var(--rn-black)', text: 'var(--rn-black)' };
    if (tab === 'b') return {
      fill:   isDark ? '#2a1e0a' : '#fdf3e0',
      stroke: 'var(--b-tree)',
      text:   'var(--b-tree)'
    };
    if (tab === 'bmas') return n.hoja
      ? { fill: isDark ? '#0a1e2a' : '#e0f0f8', stroke: 'var(--bplus)', text: 'var(--bplus)' }
      : { fill: isDark ? '#1a2a1e' : '#e8f5ee', stroke: 'var(--avl)',   text: 'var(--avl)' };
    return { fill: isDark ? '#1e3a28' : '#e8f5ee', stroke: 'var(--accent)', text: 'var(--accent)' };
  }

  function dibujarArista(x1, y1, x2, y2, color) {
    edges += `<line 
      x1="${x1 + offsetX}" y1="${y1 + cfg.padY}" 
      x2="${x2 + offsetX}" y2="${y2 + cfg.padY}"
      stroke="${color}" stroke-width="1.5" opacity=".6"
      marker-end="url(#arrow-${tab})"/>`;
  }

  function dibujarNodoBinario(n) {
    if (!n) return;
    const cx = n.x + offsetX;
    const cy = n.y + cfg.padY;
    const c  = colorNodo(n);
    const height = tab === 'rn' ? 44 : cfg.nodeR * 2;

    if (n.izquierda) {
      const yOrigen = n.y + height / 2;
      const yDestino = n.izquierda.y - (tab === 'rn' ? height / 2 : cfg.nodeR);
      dibujarArista(n.x, yOrigen, n.izquierda.x, yDestino, c.stroke);
      dibujarNodoBinario(n.izquierda);
    }
    if (n.derecha) {
      const yOrigen = n.y + height / 2;
      const yDestino = n.derecha.y - (tab === 'rn' ? height / 2 : cfg.nodeR);
      dibujarArista(n.x, yOrigen, n.derecha.x, yDestino, c.stroke);
      dibujarNodoBinario(n.derecha);
    }

    if (tab === 'rn') {
      const texto = String(n.clave);
      const partes = texto.split(/:(.+)/);
      const tipo = partes[0] || texto;
      const valor = partes[1] !== undefined ? partes[1] : tipo;
      const boxW = Math.max(cfg.nodeR * 3.5, Math.max(tipo.length * 8, valor.length * 9) + 18);
      const boxH = height;
      const x0 = cx - boxW / 2;
      const y0 = cy - boxH / 2;

      nodes += `
        <g class="svg-node" style="animation-delay:${Math.random() * 300}ms">
          <rect x="${x0}" y="${y0}" width="${boxW}" height="${boxH}" rx="8"
            fill="${c.fill}" stroke="${c.stroke}" stroke-width="1.5"/>
          <text x="${cx}" y="${cy - 6}" text-anchor="middle"
            font-size="9" fill="${c.text}" font-family="JetBrains Mono"
            font-weight="700">${escapeHtml(tipo)}</text>
          <text x="${cx}" y="${cy + 12}" text-anchor="middle"
            font-size="10" fill="${c.text}" font-family="JetBrains Mono"
            font-weight="600">${escapeHtml(valor)}</text>
        </g>`;
      return;
    }

    // etiqueta superior (fb)
    const etiqueta = tab === 'avl' ? String(n.fb) : '';

    nodes += `
      <g class="svg-node" style="animation-delay:${Math.random() * 300}ms">
        ${etiqueta ? `<text x="${cx}" y="${cy - cfg.nodeR - 5}"
          text-anchor="middle" font-size="10" fill="${c.stroke}"
          font-family="JetBrains Mono">${etiqueta}</text>` : ''}
        <circle cx="${cx}" cy="${cy}" r="${cfg.nodeR}"
          fill="${c.fill}" stroke="${c.stroke}" stroke-width="1.5"/>
        <text x="${cx}" y="${cy + 4}" text-anchor="middle"
          dominant-baseline="middle"
          font-size="11" fill="${c.text}" font-family="JetBrains Mono"
          font-weight="600">${escapeHtml(String(n.clave))}</text>
      </g>`;
  }

  function dibujarNodoB(n) {
    if (!n) return;
    const c      = colorNodo(n);
    const nClaves = n.claves.length;
    const boxW   = Math.max(nClaves * 32, 48);
    const boxH   = 32;
    const cx     = n.x + offsetX;
    const cy     = n.y + cfg.padY;

    // aristas a hijos
    (n.hijos || []).forEach(h => {
      if (h) {
        const boxH = 32;
        dibujarArista(n.x, n.y + boxH / 2, h.x, h.y - boxH / 2, c.stroke);
        dibujarNodoB(h);
      }
    });

    // rectángulo del nodo
    nodes += `
      <g class="svg-node" style="animation-delay:${Math.random() * 300}ms">
        <rect x="${cx - boxW/2}" y="${cy - boxH/2}" 
          width="${boxW}" height="${boxH}" rx="4"
          fill="${c.fill}" stroke="${c.stroke}" stroke-width="1.5"/>`;

    // divisores y claves
    n.claves.forEach((clave, i) => {
      const kx = cx - boxW/2 + (i + 0.5) * (boxW / nClaves);
      nodes += `<text x="${kx}" y="${cy + 5}" text-anchor="middle"
        font-size="11" fill="${c.text}" font-family="JetBrains Mono"
        font-weight="600">${escapeHtml(String(clave))}</text>`;
      if (i < nClaves - 1) {
        const divX = cx - boxW/2 + (i + 1) * (boxW / nClaves);
        nodes += `<line x1="${divX}" y1="${cy - boxH/2 + 4}" 
          x2="${divX}" y2="${cy + boxH/2 - 4}"
          stroke="${c.stroke}" stroke-width="1" opacity=".4"/>`;
      }
    });

    // etiqueta tipo hoja/interno
    if (tab === 'bmas') {
      const label  = n.hoja ? 'HOJA' : 'INT';
      const labelC = n.hoja ? 'var(--bplus)' : 'var(--avl)';
      nodes += `<text x="${cx}" y="${cy - boxH / 2 - 5}"
        text-anchor="middle" font-size="8" fill="${labelC}"
        font-family="JetBrains Mono" opacity=".8">${label}</text>`;
    }

    nodes += `</g>`;
  }

  // construir SVG completo
  const arrowColor = tab === 'rn' ? 'var(--rn-red)'
    : tab === 'b' ? 'var(--b-tree)'
    : tab === 'bmas' ? 'var(--bplus)'
    : 'var(--avl)';

  if (esB) dibujarNodoB(nodos);
  else     dibujarNodoBinario(nodos);

  return `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}"
    xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="arrow-${tab}" viewBox="0 0 10 10" refX="8" refY="5"
        markerWidth="5" markerHeight="5" orient="auto">
        <path d="M1,1 L8,5 L1,9" fill="none" 
          stroke="${arrowColor}" stroke-width="1.5" 
          stroke-linecap="round" stroke-linejoin="round"/>
      </marker>
    </defs>
    ${edges}
    ${nodes}
  </svg>`;
}

/* ── RESIZE HANDLE ─────────────────────────────────── */
function initResize() {
  const handle   = document.getElementById('resize-handle');
  const logPanel = document.getElementById('log-panel');
  let dragging   = false;
  let startX, startW;

  handle.addEventListener('mousedown', e => {
    dragging = true;
    startX   = e.clientX;
    startW   = logPanel.offsetWidth;
    handle.classList.add('dragging');
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  });

  document.addEventListener('mousemove', e => {
    if (!dragging) return;
    const delta = startX - e.clientX;  // arrastrar izquierda = panel más ancho
    const newW  = Math.min(500, Math.max(150, startW + delta));
    logPanel.style.width = newW + 'px';
  });

  document.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    handle.classList.remove('dragging');
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
  });
}

// llamar en DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  actualizarStats();
  mostrarArbolActual();
  initResize();  // ← agregar esta línea
  document.getElementById('cmd-input')
    .addEventListener('keydown', e => { if (e.key === 'Enter') ejecutar(); });
});

document.addEventListener('click', e => {
  console.log('click en:', e.target.id || e.target.tagName);
});