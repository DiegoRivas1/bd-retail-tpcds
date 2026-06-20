// dashboard.js
// Logica del dashboard: pipeline agéntico, fetch al backend y render de resultados.

const inputEl    = document.getElementById('input-pregunta');
const btnEnviar  = document.getElementById('btn-enviar');
const resultArea = document.getElementById('result-area');

const PASOS = ['step-pregunta', 'step-intencion', 'step-sql', 'step-spark', 'step-resultado'];

function cargarPregunta(texto) {
    inputEl.value = texto;
    inputEl.focus();
}

function resetPipeline() {
    PASOS.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('active', 'completed');
    });
}

function activarPaso(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('active');
}

function completarPaso(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.remove('active');
        el.classList.add('completed');
    }
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function toggleSqlBlock(headerEl) {
    const bodyEl    = headerEl.nextElementSibling;
    const arrowSpan = headerEl.querySelector('span:last-child');
    if (!bodyEl) return;
    bodyEl.classList.toggle('open');
    if (arrowSpan) arrowSpan.textContent = bodyEl.classList.contains('open') ? '▲' : '▼';
}

function renderError(mensaje) {
    resultArea.innerHTML = `
        <div class="empty-state" style="
            color: var(--error-red);
            background: var(--error-bg);
            border: 1px solid rgba(255,92,110,0.2);
            border-radius: var(--radius-lg);
            padding: 24px;
        ">
            <div>Error en la consulta agéntica</div>
            <div style="font-size:12px; opacity:0.8;">${escapeHtml(mensaje)}</div>
        </div>`;
}

function renderResultado(datos) {
    const intencion = datos.intencion || 'analytics';
    const total     = datos.total     || 0;
    const columnas  = datos.columnas  || [];
    const filas     = datos.filas     || [];
    const sql       = datos.sql       || '';

    const metaHtml = `
        <div class="result-meta">
            <span class="badge badge-intent">${escapeHtml(intencion)}</span>
            <span class="badge badge-count">${total.toLocaleString()} registros</span>
        </div>`;

    const sqlHtml = `
        <div class="sql-card">
            <div class="sql-header" onclick="toggleSqlBlock(this)">
                <span>SQL generado</span>
                <span>▼</span>
            </div>
            <div class="sql-body">
                <pre style="margin:0;">${escapeHtml(sql)}</pre>
            </div>
        </div>`;

    if (!filas.length) {
        resultArea.innerHTML = metaHtml + sqlHtml + `
            <div class="empty-state" style="padding:24px;">
                La consulta no retorno resultados.
            </div>`;
        return;
    }

    const encabezados = columnas.map(c => `<th>${escapeHtml(c)}</th>`).join('');

    const filasHtml = filas.map(fila => {
        const celdas = columnas.map(col => {
            const val      = fila[col];
            const esNumero = typeof val === 'number';
            const display  = val === null || val === undefined
                ? '—'
                : esNumero
                    ? Number(val).toLocaleString('es-PE')
                    : val;
            const clase = esNumero ? ' class="number-cell"' : '';
            return `<td${clase}>${escapeHtml(String(display))}</td>`;
        }).join('');
        return `<tr>${celdas}</tr>`;
    }).join('');

    const tablaHtml = `
        <div class="table-wrapper">
            <table>
                <thead><tr>${encabezados}</tr></thead>
                <tbody>${filasHtml}</tbody>
            </table>
        </div>`;

    resultArea.innerHTML = metaHtml + sqlHtml + tablaHtml;
}

async function enviarConsulta() {
    const pregunta = inputEl.value.trim();
    if (!pregunta) return;

    btnEnviar.disabled = true;
    btnEnviar.innerHTML = '<span>Procesando...</span>';
    resultArea.innerHTML = '';
    resetPipeline();

    activarPaso('step-pregunta');
    await delay(220);
    completarPaso('step-pregunta');

    activarPaso('step-intencion');
    await delay(280);
    completarPaso('step-intencion');

    activarPaso('step-sql');

    let datos;
    try {
        const fetchPromise   = fetch('/consulta', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta }),
        });
        const timeoutPromise = new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Tiempo de espera agotado (120s)')), 120000)
        );

        const respuesta = await Promise.race([fetchPromise, timeoutPromise]);

        completarPaso('step-sql');
        activarPaso('step-spark');
        await delay(260);
        completarPaso('step-spark');

        activarPaso('step-resultado');
        datos = await respuesta.json();
        await delay(180);
        completarPaso('step-resultado');

    } catch (err) {
        completarPaso('step-sql');
        completarPaso('step-spark');
        completarPaso('step-resultado');
        renderError(err.message || 'Error de conexion con el servidor.');
        btnEnviar.disabled = false;
        btnEnviar.innerHTML = '<span>Consultar</span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';
        return;
    }

    btnEnviar.disabled = false;
    btnEnviar.innerHTML = '<span>Consultar</span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';

    if (!datos.exito) {
        renderError(datos.mensaje || datos.error || 'El agente no pudo generar SQL valido.');
        return;
    }

    renderResultado(datos);
}

window.cargarPregunta  = cargarPregunta;
window.enviarConsulta  = enviarConsulta;
window.toggleSqlBlock  = toggleSqlBlock;
