const API = 'http://localhost:8000';
let currentPage = 'dashboard';
let editingId = null;
let modalEndpoint = null;
let modalCfg = null;

// ── CONFIGURACIÓN POR ENDPOINT REAL ──────────────────────────────────────────
const PAGES = {

  buses: {
    label: 'Buses', icon: '🚌', crud: true,
    endpoint: '/buses', pk: 'id_bus',
    headers: ['ID','Placa','Capacidad','Estado','Empresa','Terminal'],
    display: r => [r.id_bus, r.placa, r.capacidad, estadoBadge(r.estado), r.id_empresa??'-', r.id_terminal??'-'],
    rawHtml: true,
    fields: [
      { key:'placa',       label:'Placa',       type:'text',   required:true },
      { key:'capacidad',   label:'Capacidad',   type:'number', required:true },
      { key:'estado',      label:'Estado',      type:'select', required:true,
        options:['Activo','Inactivo','Mantenimiento','En servicio'] },
      { key:'id_empresa',  label:'ID Empresa',  type:'number' },
      { key:'id_terminal', label:'ID Terminal', type:'number' },
    ],
  },

  conductores: {
    label: 'Conductores', icon: '👤', crud: true,
    endpoint: '/conductores', pk: 'id_conductor',
    headers: ['ID','Nombres','Licencia','Teléfono','Fecha Ingreso'],
    display: r => [r.id_conductor, r.nombres, r.licencia, r.telefono??'-', r.fecha_ingreso],
    fields: [
      { key:'nombres',       label:'Nombres',       type:'text', required:true },
      { key:'licencia',      label:'Licencia',      type:'text', required:true },
      { key:'telefono',      label:'Teléfono',      type:'text' },
      { key:'fecha_ingreso', label:'Fecha Ingreso', type:'date', required:true },
    ],
  },

  pasajeros: {
    label: 'Pasajeros', icon: '🧑', crud: true,
    endpoint: '/pasajeros', pk: 'id_pasajero',
    headers: ['ID','Nombres','Correo','Teléfono'],
    display: r => [r.id_pasajero, r.nombres, r.correo, r.telefono],
    fields: [
      { key:'nombres',  label:'Nombres',  type:'text',  required:true },
      { key:'correo',   label:'Correo',   type:'email', required:true },
      { key:'telefono', label:'Teléfono', type:'text',  required:true },
    ],
  },

  incidencias: {
    label: 'Incidencias', icon: '⚠️', crud: true,
    endpoint: '/incidencias', pk: 'id_incidencia',
    headers: ['ID','Bus','Centro','Pasajero','Tipo','Fecha','Descripción'],
    display: r => [r.id_incidencia, r.id_bus, r.id_centro, r.id_pasajero, r.tipo, fmtDate(r.fecha_reporte), String(r.descripcion).substring(0,45)+'…'],
    fields: [
      { key:'id_bus',      label:'ID Bus',      type:'number', required:true },
      { key:'id_centro',   label:'ID Centro',   type:'number', required:true },
      { key:'id_pasajero', label:'ID Pasajero', type:'number', required:true },
      { key:'tipo',        label:'Tipo',        type:'select', required:true,
        options:['Retraso','Exceso de velocidad','Bus en mal estado','Conductor en mal estado','Choque','Otro'] },
      { key:'descripcion', label:'Descripción', type:'textarea', required:true, full:true },
    ],
  },

  empresas: {
    label: 'Empresas', icon: '🏢', crud: true,
    endpoint: '/empresas', pk: 'id_empresa',
    headers: ['ID','Nombre','RUC','Teléfono','Correo'],
    display: r => [r.id_empresa, r.nombre, r.ruc, r.telefono??'-', r.correo??'-'],
    fields: [
      { key:'nombre',   label:'Nombre',   type:'text',  required:true },
      { key:'ruc',      label:'RUC',      type:'text',  required:true },
      { key:'telefono', label:'Teléfono', type:'text' },
      { key:'correo',   label:'Correo',   type:'email' },
    ],
  },

  // ── Solo lectura ──
  rutas: {
    label: 'Rutas', icon: '🗺️', crud: false,
    endpoint: '/rutas', pk: 'id_ruta',
    headers: ['ID','Nombre Ruta','Código','Tiempo Est. (min)','Empresa'],
    display: r => [r.id_ruta, r.nombre_ruta, r.codigo_ruta, r.tiempo_estimado??'-', r.id_empresa??'-'],
  },
  terminales: {
    label: 'Terminales', icon: '🏛️', crud: false,
    endpoint: '/terminales', pk: 'id_terminal',
    headers: ['ID','Nombre','Distrito','Capacidad'],
    display: r => [r.id_terminal, r.nombre, r.distrito, r.capacidad??'-'],
  },
  paraderos: {
    label: 'Paraderos', icon: '📍', crud: false,
    endpoint: '/paraderos', pk: 'id_paradero',
    headers: ['ID','Nombre','Dirección'],
    display: r => [r.id_paradero, r.nombre, r.direccion],
  },
  horarios: {
    label: 'Horarios', icon: '🕐', crud: false,
    endpoint: '/horarios', pk: 'id_horario',
    headers: ['ID','Hora Salida','Hora Llegada','Ruta'],
    display: r => [r.id_horario, r.hora_salida, r.hora_llegada, r.id_ruta],
  },
  notificaciones: {
    label: 'Notificaciones', icon: '🔔', crud: false,
    endpoint: '/notificaciones', pk: 'id_notificacion',
    headers: ['ID','Tipo','Mensaje'],
    display: r => [r.id_notificacion ?? r.id, r.tipo, String(r.mensaje).substring(0,60)+'…'],
  },
  'registro-control': {
    label: 'Registros Control', icon: '📝', crud: false,
    endpoint: '/registro-control', pk: 'id_registro',
    headers: ['ID','Bus','Retraso (min)','Observación'],
    display: r => [r.id_registro ?? r.id, r.id_bus, r.retraso_minutos ?? r.retraso, String(r.observacion).substring(0,60)+'…'],
  },
};

const REPORTS = [
  {
    id: 'conductores', title: '🧑‍✈️ Conductores con Asignaciones',
    endpoint: '/reportes/conductores',
    joins: 'conductor → asignacion_conductor → bus',
    desc: 'Conductores con al menos 1 asignación. GROUP BY + HAVING + JOIN de 3 tablas.',
  },
  {
    id: 'incidencias', title: '⚠️ Tipos de Incidencias por Empresa',
    endpoint: '/reportes/incidencias',
    joins: 'incidencia → bus → empresa_transporte',
    desc: 'Tipos de incidencia agrupados por empresa. GROUP BY + HAVING + JOIN de 3 tablas.',
  },
  {
    id: 'retrasos', title: '⏱️ Buses con Retraso',
    endpoint: '/reportes/retrasos',
    joins: 'bus → registro_control → empresa_transporte',
    desc: 'Buses con retraso > 0 y cálculo de retraso ajustado (+10 min). JOIN de 3 tablas.',
  },
  {
    id: 'empresas', title: '🏢 Incidencias y Retrasos por Empresa',
    endpoint: '/reportes/empresas',
    joins: 'empresa_transporte → bus → incidencia → registro_control',
    desc: 'Total de incidencias y promedio de retraso por empresa. JOIN de 4 tablas.',
  },
];

// ── HELPERS ───────────────────────────────────────────────────────────────────
function fmtDate(d) {
  if (!d) return '-';
  try { return new Date(d).toLocaleString('es-PE', { dateStyle:'short', timeStyle:'short' }); }
  catch { return d; }
}
function estadoBadge(e) {
  const m = { 'Activo':'badge-green','Inactivo':'badge-red','Mantenimiento':'badge-yellow','En servicio':'badge-blue' };
  return `<span class="badge ${m[e]||'badge-blue'}">${e}</span>`;
}
function esc(s) {
  return String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
function toast(msg, type='ok') {
  const t = document.getElementById('toast');
  t.textContent = msg; t.className = `show ${type}`;
  setTimeout(() => t.className = '', 3000);
}

// ── API ───────────────────────────────────────────────────────────────────────
async function apiFetch(path, opts={}) {
  const res = await fetch(API + path, {
    headers: { 'Content-Type': 'application/json' }, ...opts
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt || res.statusText);
  }
  return res.json();
}

// ── NAVIGATE ──────────────────────────────────────────────────────────────────
function navigate(page) {
  currentPage = page;
  document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
  const btn = [...document.querySelectorAll('.nav-item')].find(b => b.getAttribute('onclick')?.includes(`'${page}'`));
  if (btn) btn.classList.add('active');
  const labels = { dashboard:'Dashboard', reportes:'Reportes SQL', ...Object.fromEntries(Object.entries(PAGES).map(([k,v])=>[k,v.label])) };
  document.getElementById('page-title').textContent = labels[page] || page;

  if (page === 'dashboard') renderDashboard();
  else if (page === 'reportes') renderReportes();
  else renderTable(page);
}

// ── DASHBOARD ─────────────────────────────────────────────────────────────────
async function renderDashboard() {
  const c = document.getElementById('content');
  c.innerHTML = '<div class="loading"><span class="spinner"></span> Cargando estadísticas...</div>';
  const keys = ['buses','conductores','pasajeros','incidencias','empresas','rutas','terminales','paraderos'];
  const counts = {};
  await Promise.all(keys.map(async k => {
    try { const d = await apiFetch(PAGES[k].endpoint); counts[k] = Array.isArray(d) ? d.length : '—'; }
    catch { counts[k] = '—'; }
  }));
  c.innerHTML = `
    <div class="cards">
      ${keys.map(k => `
        <div class="card" onclick="navigate('${k}')">
          <div class="card-icon">${PAGES[k].icon}</div>
          <div class="card-num">${counts[k]}</div>
          <div class="card-label">${PAGES[k].label}</div>
        </div>`).join('')}
    </div>
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px">
      <h3 style="font-size:13px;margin-bottom:14px;color:var(--text-muted)">ACCESOS RÁPIDOS</h3>
      <div style="display:flex;flex-wrap:wrap;gap:10px">
        <button class="btn btn-primary" onclick="navigate('buses')">🚌 Gestionar Buses</button>
        <button class="btn btn-primary" onclick="navigate('conductores')">👤 Gestionar Conductores</button>
        <button class="btn btn-blue" onclick="navigate('incidencias')">⚠️ Ver Incidencias</button>
        <button class="btn btn-edit" onclick="navigate('reportes')">📊 Ver Reportes</button>
      </div>
    </div>`;
}

// ── TABLA ─────────────────────────────────────────────────────────────────────
async function renderTable(page) {
  const cfg = PAGES[page];
  const c = document.getElementById('content');
  c.innerHTML = '<div class="loading"><span class="spinner"></span> Cargando datos...</div>';
  let data = [];
  try {
    data = await apiFetch(cfg.endpoint);
    if (!Array.isArray(data)) data = [];
  } catch(e) {
    c.innerHTML = `<div class="empty">
      <div style="font-size:36px;margin-bottom:10px">⚠️</div>
      <p>No se pudo conectar a <code>${cfg.endpoint}</code></p>
      <small style="color:var(--text-muted)">${e.message}</small>
      <br><button class="btn btn-primary" style="margin-top:14px" onclick="renderTable('${page}')">Reintentar</button>
    </div>`;
    return;
  }

  const rows = data.map(r => {
    const cells = cfg.display(r);
    const pk = r[cfg.pk];
    const acciones = cfg.crud
      ? `<td style="white-space:nowrap">
           <button class="btn btn-edit" onclick='openEdit("${page}", ${pk})'>✏️ Editar</button>
           <button class="btn btn-danger" onclick='deleteRecord("${page}", ${pk})' style="margin-left:4px">🗑️</button>
         </td>`
      : '<td><span style="color:var(--text-muted);font-size:11px">solo lectura</span></td>';
    return `<tr>${cells.map((v,i) => cfg.rawHtml && i>0 ? `<td>${v}</td>` : `<td>${esc(v)}</td>`).join('')}${acciones}</tr>`;
  }).join('');

  const readonlyTag = !cfg.crud ? `<span class="readonly-badge">solo lectura</span>` : '';

  c.innerHTML = `
    <div class="toolbar">
      ${cfg.crud ? `<button class="btn btn-primary" onclick='openCreate("${page}")'>+ Nuevo</button> <button class="btn btn-blue" onclick="exportCSV("${page}")'> Exportar CSV </button> ` : ''}
      <input class="search-box" type="text" placeholder="Buscar..." oninput="filterTable(this.value)">
      <span style="color:var(--text-muted);font-size:12px">${data.length} registros ${readonlyTag}</span>
    </div>
    <div class="table-wrap">
      <table id="data-table">
        <thead><tr>${cfg.headers.map(h=>`<th>${h}</th>`).join('')}<th>Acciones</th></tr></thead>
        <tbody>${rows || `<tr><td colspan="${cfg.headers.length+1}" style="text-align:center;padding:30px;color:var(--text-muted)">Sin registros</td></tr>`}</tbody>
      </table>
    </div>`;
}

function filterTable(val) {
  document.querySelectorAll('#data-table tbody tr').forEach(r => {
    r.style.display = r.textContent.toLowerCase().includes(val.toLowerCase()) ? '' : 'none';
  });
}

// ── MODAL ─────────────────────────────────────────────────────────────────────
function buildForm(cfg, record={}) {
  const half = cfg.fields.filter(f => !f.full && f.type !== 'textarea');
  const full  = cfg.fields.filter(f =>  f.full || f.type === 'textarea');
  let html = '<div class="form-grid">';
  half.forEach(f => {
    html += `<div class="form-group"><label>${f.label}${f.required?' *':''}</label>${buildInput(f, record[f.key]??'')}</div>`;
  });
  html += '</div>';
  full.forEach(f => {
    html += `<div class="form-group" style="margin-top:12px"><label>${f.label}${f.required?' *':''}</label>${buildInput(f, record[f.key]??'')}</div>`;
  });
  return html;
}

function buildInput(f, val) {
  const id = `f_${f.key}`;
  if (f.type === 'select') {
    return `<select id="${id}" name="${f.key}">
      <option value="">Seleccionar...</option>
      ${f.options.map(o=>`<option value="${o}" ${val===o?'selected':''}>${o}</option>`).join('')}
    </select>`;
  }
  if (f.type === 'textarea') {
    return `<textarea id="${id}" name="${f.key}">${esc(val)}</textarea>`;
  }
  const v = f.type === 'datetime-local' && val ? String(val).substring(0,16) : val;
  return `<input id="${id}" type="${f.type}" value="${esc(v)}" ${f.required?'required':''}>`;
}

function openCreate(page) {
  const cfg = PAGES[page];
  editingId = null; modalEndpoint = cfg.endpoint; modalCfg = cfg;
  document.getElementById('modal-title').textContent = `Nuevo — ${cfg.label}`;
  document.getElementById('modal-body').innerHTML = buildForm(cfg);
  document.getElementById('modal').classList.add('open');
}

async function openEdit(page, id) {
  const cfg = PAGES[page];
  editingId = id; modalEndpoint = cfg.endpoint; modalCfg = cfg;
  document.getElementById('modal-title').textContent = `Editar — ${cfg.label} #${id}`;
  document.getElementById('modal-body').innerHTML = '<div class="loading"><span class="spinner"></span></div>';
  document.getElementById('modal').classList.add('open');
  try {
    const rec = await apiFetch(`${cfg.endpoint}/${id}`);
    document.getElementById('modal-body').innerHTML = buildForm(cfg, rec);
  } catch(e) {
    document.getElementById('modal-body').innerHTML = `<p style="color:var(--danger)">Error al cargar: ${e.message}</p>`;
  }
}

function closeModal() {
  document.getElementById('modal').classList.remove('open');
  editingId = null; modalEndpoint = null; modalCfg = null;
}

async function saveRecord() {
  const body = {};
  modalCfg.fields.forEach(f => {
    const el = document.getElementById(`f_${f.key}`);
    if (!el) return;
    const v = el.value.trim();
    if (v === '') { body[f.key] = null; return; }
    body[f.key] = f.type === 'number' ? Number(v) : v;
  });

  for (const f of modalCfg.fields.filter(f => f.required)) {
    if (body[f.key] === null || body[f.key] === undefined || body[f.key] === '') {
      toast(`"${f.label}" es obligatorio`, 'err'); return;
    }
  }

  const btn = document.getElementById('modal-save');
  btn.disabled = true; btn.textContent = 'Guardando...';
  try {
    if (editingId) {
      await apiFetch(`${modalEndpoint}/${editingId}`, { method:'PUT', body: JSON.stringify(body) });
      toast('✅ Registro actualizado');
    } else {
      await apiFetch(modalEndpoint, { method:'POST', body: JSON.stringify(body) });
      toast('✅ Registro creado');
    }
    closeModal();
    renderTable(currentPage);
  } catch(e) {
    toast('❌ ' + e.message, 'err');
  } finally {
    btn.disabled = false; btn.textContent = 'Guardar';
  }
}

async function deleteRecord(page, id) {
  if (!confirm(`¿Eliminar registro #${id}? No se puede deshacer.`)) return;
  try {
    await apiFetch(`${PAGES[page].endpoint}/${id}`, { method:'DELETE' });
    toast('🗑️ Eliminado');
    renderTable(page);
  } catch(e) {
    toast('❌ ' + e.message, 'err');
  }
}

// ── REPORTES ──────────────────────────────────────────────────────────────────
function renderReportes() {
  const c = document.getElementById('content');
  c.innerHTML = `
    <p style="color:var(--text-muted);font-size:13px;margin-bottom:20px">
      Consultas SQL con GROUP BY / HAVING y JOIN de 3+ tablas. Haz clic en "Ejecutar" para ver los resultados.
    </p>
    <div class="report-grid">
      ${REPORTS.map(r => `
        <div class="report-card">
          <h4>${r.title}</h4>
          <div class="joins">🔗 ${r.joins}</div>
          <p>${r.desc}</p>
          <button class="btn btn-blue" style="font-size:12px;padding:7px 14px" onclick='runReport("${r.id}", "${r.endpoint}")'>▶ Ejecutar consulta</button>
          <div class="report-result" id="rpt_${r.id}"></div>
        </div>`).join('')}
    </div>`;
}

async function runReport(id, endpoint) {
  const el = document.getElementById(`rpt_${id}`);
  el.style.display = 'block';
  el.innerHTML = '<span class="spinner"></span> Ejecutando...';
  try {
    const data = await apiFetch(endpoint);
    if (!Array.isArray(data) || data.length === 0) {
      el.innerHTML = '<p style="color:var(--text-muted)">Sin resultados.</p>'; return;
    }
    const cols = Object.keys(data[0]);
    el.innerHTML = `<table>
      <thead><tr>${cols.map(c=>`<th>${c}</th>`).join('')}</tr></thead>
      <tbody>${data.map(row=>`<tr>${cols.map(c=>`<td>${esc(row[c])}</td>`).join('')}</tr>`).join('')}</tbody>
    </table>`;
  } catch(e) {
    el.innerHTML = `<p style="color:var(--danger)">⚠️ ${e.message}<br><small>Verifica que FastAPI esté corriendo en localhost:8000</small></p>`;
  }
}

// ── STATUS ────────────────────────────────────────────────────────────────────
async function checkApi() {
  const el = document.getElementById('api-status');
  try {
    await apiFetch('/');
    el.textContent = '🟢 FastAPI conectada';
  } catch {
    el.textContent = '🔴 FastAPI no disponible';
  }
}

document.getElementById('modal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

checkApi();
navigate('dashboard');
