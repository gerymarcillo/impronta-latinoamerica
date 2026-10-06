# -*- coding: utf-8 -*-
"""
GENERADOR DEL INDEX.HTML - VERSIÓN DESDE CERO
Proyecto: ECT-UNESUM-2026
- Portada con impronta (docente + IA)
- Login con código del proyecto
- Validación de códigos integrada
- DOS imágenes de portada: principal (grande) + secundaria (pequeña)
"""

from pathlib import Path

HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>El Conocimiento Transforma - UNESUM</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,sans-serif;background:#1e1e2e;color:#ecf0f1;min-height:100vh;padding:20px}
.container{max-width:1100px;margin:0 auto}

/* PORTADA */
.portada{min-height:95vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 20px}

/* CONTENEDOR DE IMÁGENES DE PORTADA */
.portada-imagenes{display:flex;align-items:center;justify-content:center;gap:20px;margin-bottom:25px;flex-wrap:wrap}
.portada-imagen-principal{max-width:400px;width:100%;border-radius:15px;box-shadow:0 20px 60px rgba(243,156,18,0.3);border:3px solid #f39c12}
.portada-imagen-secundaria{max-width:200px;width:100%;border-radius:12px;box-shadow:0 15px 40px rgba(52,152,219,0.3);border:3px solid #3498db;opacity:0.95}

.portada-titulo{font-size:38px;color:#5dade2;font-weight:bold;letter-spacing:3px;margin-bottom:12px;text-shadow:0 0 20px rgba(93,173,226,0.5)}
.portada-subtitulo{font-size:17px;color:#ecf0f1;margin-bottom:8px;letter-spacing:1px}
.portada-descripcion{font-size:13px;color:#bdc3c7;margin-bottom:4px;font-style:italic}
.portada-territorio{font-size:15px;color:#f39c12;margin:15px 0 5px 0;font-weight:bold;letter-spacing:1px}

/* IMPRONTA */
.impronta-frase{color:#f39c12;font-style:italic;font-size:13px;margin:18px 0;padding:12px 20px;background:linear-gradient(135deg,#2c3e50,#1e1e2e);border-radius:10px;border-left:4px solid #f39c12;border-right:4px solid #f39c12;max-width:750px}
.impronta-frase span{color:#5dade2;font-weight:bold;font-style:normal}
.impronta-portada{display:flex;gap:18px;margin:20px 0;flex-wrap:wrap;justify-content:center;align-items:center}
.impronta-portada-item{background:linear-gradient(135deg,#2c3e50,#1e1e2e);border-radius:12px;padding:16px 20px;display:flex;align-items:center;gap:12px;border:2px solid #34495e;min-width:270px}
.impronta-portada-item.humano{border-left:5px solid #3498db}
.impronta-portada-item.ia{border-left:5px solid #9b59b6}
.impronta-portada-avatar{font-size:44px;flex-shrink:0}
.impronta-portada-info{text-align:left}
.impronta-portada-rol{color:#f39c12;font-size:10px;font-weight:bold;letter-spacing:2px;margin-bottom:5px}
.impronta-portada-nombre{color:#5dade2;font-size:14px;font-weight:bold;margin-bottom:3px;line-height:1.3}
.impronta-portada-item.ia .impronta-portada-nombre{color:#c39bd3}
.impronta-portada-desc{color:#bdc3c7;font-size:11px;margin-bottom:2px}
.impronta-portada-link{color:#f39c12;font-size:10px;text-decoration:none;display:inline-block;margin-top:5px;padding:2px 8px;border:1px solid #f39c12;border-radius:4px}
.impronta-divisor{font-size:26px;color:#f39c12;font-weight:bold}

.portada-cita{font-size:12px;color:#bdc3c7;margin-top:15px;font-style:italic;max-width:700px;line-height:1.5}
.portada-btn{margin-top:25px;padding:15px 50px;font-size:16px;letter-spacing:2px}

/* BOTONES */
.btn{background:linear-gradient(135deg,#3498db,#2980b9);color:white;border:none;padding:12px 24px;border-radius:8px;cursor:pointer;font-size:15px;font-weight:bold;margin:6px;text-decoration:none;display:inline-block}
.btn-orange{background:linear-gradient(135deg,#f39c12,#e67e22)}
.btn-green{background:linear-gradient(135deg,#2ecc71,#27ae60)}

/* LOGIN */
.login-box{background:#2c3e50;border-radius:12px;padding:30px;max-width:550px;margin:40px auto;text-align:center;border:2px solid #34495e}
.login-box h2{color:#f39c12;margin-bottom:20px;font-size:20px}
.login-box input[type="text"]{width:100%;padding:12px;margin:8px 0;border:2px solid #3498db;border-radius:8px;background:#1e1e2e;color:#ecf0f1;font-size:14px}
.login-box input[type="text"]:focus{outline:none;border-color:#f39c12}
.campo-ayuda{color:#7f8c8d;font-size:11px;text-align:left;margin-top:-4px;margin-bottom:8px;padding-left:4px}

/* ROL */
.rol-selector{margin-bottom:18px;text-align:left}
.rol-selector label.titulo-rol{color:#f39c12;font-size:13px;font-weight:bold;display:block;margin-bottom:8px}
.rol-opciones{display:flex;gap:10px}
.rol-opcion{flex:1;background:#1e1e2e;border:2px solid #34495e;border-radius:8px;padding:12px;cursor:pointer;text-align:center;font-size:13px}
.rol-opcion.activa{border-color:#f39c12;background:#34495e}

/* PROYECTO ASIGNADO */
.proyecto-box{background:linear-gradient(135deg,#16a085,#1abc9c);border-radius:12px;padding:25px;margin:20px 0;border:2px solid #f39c12;text-align:center}
.proyecto-titulo{color:white;font-size:12px;font-weight:bold;letter-spacing:2px;margin-bottom:10px;opacity:0.9}
.proyecto-nombre{color:white;font-size:22px;font-weight:bold;margin-bottom:12px;text-shadow:0 2px 5px rgba(0,0,0,0.3)}
.proyecto-datos{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:12px}
.proyecto-dato{background:rgba(0,0,0,0.25);padding:6px 14px;border-radius:20px;font-size:12px;color:white;font-weight:bold}

/* HEADER */
.header{background:linear-gradient(135deg,#2c3e50,#1e1e2e);border-left:6px solid #f39c12;border-radius:12px;padding:25px;margin-bottom:20px;display:flex;align-items:center;gap:20px;flex-wrap:wrap;justify-content:center}
.header-logo{height:70px}
.header-imagenes{display:flex;align-items:center;gap:10px}
.header-imagen{height:70px;border-radius:8px;border:2px solid #f39c12}
.header-imagen-mini{height:50px;border-radius:8px;border:2px solid #3498db;opacity:0.9}
.header-texto{text-align:center;flex:1;min-width:280px}
.header h1{color:#5dade2;font-size:24px;margin-bottom:6px}
.header h2{color:#ecf0f1;font-size:13px;font-weight:normal;margin-bottom:4px}
.header h3{color:#bdc3c7;font-size:11px;font-weight:normal;font-style:italic}
.header p{color:#bdc3c7;font-style:italic;margin-top:8px;font-size:11px}

/* SECCIONES */
.seccion-titulo{color:#f39c12;font-size:20px;text-align:center;margin:35px 0 15px 0;padding-bottom:10px;border-bottom:2px solid #34495e}
.seccion-subtitulo{color:#bdc3c7;font-size:12px;text-align:center;margin-bottom:15px;font-style:italic}

/* GRIDS */
.modulos-grid,.recursos-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:15px}
.modulo-card{background:#2c3e50;border-left:5px solid #3498db;border-radius:10px;padding:18px;text-decoration:none;color:#ecf0f1;display:block;transition:transform 0.2s}
.modulo-card:hover{transform:translateY(-3px);border-left-color:#f39c12}
.modulo-card h3{color:#5dade2;margin-bottom:6px;font-size:15px}
.modulo-card .icon{font-size:28px;margin-bottom:6px}
.modulo-card .desc{color:#bdc3c7;font-size:12px;margin-top:6px}
.modulo-card .status{color:#2ecc71;font-size:11px;margin-top:8px;font-weight:bold}

.recurso-card{background:#2c3e50;border-radius:10px;padding:18px;text-decoration:none;color:#ecf0f1;display:flex;align-items:center;gap:12px;border-left:5px solid #f39c12}
.recurso-icon{font-size:32px;flex-shrink:0}
.recurso-info h4{color:#5dade2;font-size:14px;margin-bottom:3px}
.recurso-info p{color:#bdc3c7;font-size:11px}

/* PIE */
.pie-pagina{text-align:center;margin-top:35px;padding:20px;border-top:2px solid #34495e;color:#7f8c8d;font-size:11px}
.cita-final{color:#f39c12;font-style:italic;font-size:12px;text-align:center;margin-top:15px;padding:15px;background:#2c3e50;border-radius:8px;border-left:4px solid #f39c12;line-height:1.5}
.hidden{display:none}

/* ALERTA */
.alerta-error{background:#c0392b;color:white;padding:15px;border-radius:8px;margin:15px 0;text-align:center;font-weight:bold}
.alerta-ok{background:#27ae60;color:white;padding:15px;border-radius:8px;margin:15px 0;text-align:center;font-weight:bold}
</style>
</head>
<body>
<div class="container">

<!-- PANTALLA 1: PORTADA -->
<div id="pantalla-portada" class="portada">

<!-- DOS IMÁGENES: PRINCIPAL + SECUNDARIA -->
<div class="portada-imagenes">
<img src="portada_estructural.png" alt="Portada Principal" class="portada-imagen-principal">
<img src="portada_estructural_2.png" alt="Portada Secundaria" class="portada-imagen-secundaria">
</div>

<div class="portada-titulo">EL CONOCIMIENTO TRANSFORMA</div>
<div class="portada-subtitulo">PROYECTO DE FORMACIÓN MODULAR</div>
<div class="portada-descripcion">ESTRUCTURA I — ESTRUCTURA II</div>
<div class="portada-descripcion">Carrera de Ingeniería Civil — UNESUM</div>
<div class="portada-territorio">🎯 TERRITORIO PILOTO: AGUA DULCE</div>
<div class="portada-descripcion">Escuela Presidente Urbina (AMIE 13H04567)</div>
<div class="portada-descripcion">Parroquia La Unión, Jipijapa, Manabí</div>

<div class="impronta-frase">
🤝 <span>IMPRONTA DE AUTORÍA DESDE EL INICIO</span><br>
"Desde cero. Juntos. Con propósito."
</div>

<div class="impronta-portada">
<div class="impronta-portada-item humano">
<div class="impronta-portada-avatar">👨‍🏫</div>
<div class="impronta-portada-info">
<div class="impronta-portada-rol">AUTOR HUMANO</div>
<div class="impronta-portada-nombre">Ing. Gery Lorenzo Marcillo Merino, Msc.</div>
<div class="impronta-portada-desc">Docente — Estructura I / II</div>
<div class="impronta-portada-desc">Carrera de Ingeniería Civil — UNESUM</div>
</div>
</div>

<div class="impronta-divisor">×</div>

<div class="impronta-portada-item ia">
<div class="impronta-portada-avatar">🤖</div>
<div class="impronta-portada-info">
<div class="impronta-portada-rol">IA COLABORADORA</div>
<div class="impronta-portada-nombre">DeepSeek <span style="color:#7f8c8d;font-size:12px">深度求索</span></div>
<div class="impronta-portada-desc">Modelo V3 — Asistente de programación</div>
<a href="https://www.deepseek.com" target="_blank" class="impronta-portada-link">🌐 www.deepseek.com</a>
</div>
</div>
</div>

<div class="portada-cita">"La escuela que el sistema olvidó, la comunidad que la recuerda, la UNESUM que la recupera. Vamos a cambiar la historia."</div>

<button class="btn btn-orange portada-btn" onclick="irAlLogin()">🚀 COMENZAR</button>
</div>

<!-- PANTALLA 2: LOGIN -->
<div id="pantalla-login" class="hidden">
<div class="header">
<img src="logo_unesum.png" alt="UNESUM" class="header-logo">
<div class="header-texto">
<h1>EL CONOCIMIENTO TRANSFORMA</h1>
<h2>PROYECTO DE FORMACIÓN MODULAR</h2>
<h3>ESTRUCTURA I — ESTRUCTURA II</h3>
<p>Carrera de Ingeniería Civil — UNESUM</p>
</div>
<div class="header-imagenes">
<img src="portada_estructural.png" alt="Portada" class="header-imagen">
<img src="portada_estructural_2.png" alt="Portada 2" class="header-imagen-mini">
</div>
</div>

<div class="login-box">
<h2>🔐 Ingreso a la plataforma</h2>
<div class="rol-selector">
<label class="titulo-rol">Seleccione su rol:</label>
<div class="rol-opciones">
<label class="rol-opcion activa" id="rol-estudiante">
<input type="radio" name="rol" value="estudiante" checked onchange="cambiarRol()">
👤 Estudiante
</label>
<label class="rol-opcion" id="rol-docente">
<input type="radio" name="rol" value="docente" onchange="cambiarRol()">
🎓 Docente
</label>
</div>
</div>

<input type="text" id="input-nombre" placeholder="Nombre completo">
<input type="text" id="input-cedula" placeholder="Cédula / Matrícula">
<input type="text" id="input-codigo" placeholder="Código del proyecto (ej: ECT-002)">
<div class="campo-ayuda">💡 El docente le asignará un código. Ejemplos: ECT-001, ECT-002, AGUA-001</div>

<button class="btn" onclick="ingresar()">🚀 INGRESAR Y VER PROYECTO</button>

<div id="alerta-codigo"></div>
</div>
</div>

<!-- PANTALLA 3: MENÚ PRINCIPAL -->
<div id="pantalla-modulos" class="hidden">
<div class="header">
<img src="logo_unesum.png" alt="UNESUM" class="header-logo">
<div class="header-texto">
<h1>📚 PLATAFORMA DE FORMACIÓN MODULAR</h1>
<h2 id="saludo-estudiante"></h2>
<h3>EL CONOCIMIENTO TRANSFORMA — Estructura I / Estructura II</h3>
<p>Carrera de Ingeniería Civil — UNESUM</p>
</div>
<div class="header-imagenes">
<img src="portada_estructural.png" alt="Portada" class="header-imagen">
<img src="portada_estructural_2.png" alt="Portada 2" class="header-imagen-mini">
</div>
</div>

<!-- PROYECTO ASIGNADO -->
<div id="proyecto-asignado-box"></div>

<!-- MÓDULOS -->
<h2 class="seccion-titulo">📚 MÓDULOS DEL PROGRAMA</h2>
<p class="seccion-subtitulo">6 módulos temáticos con evaluación por competencias</p>
<div class="modulos-grid">
<a href="modulo_01_inercia_equivalente.html" class="modulo-card">
<div class="icon">🎯</div>
<h3>M01 — Inercia Equivalente</h3>
<div class="desc">Teorema de Steiner + Altura equivalente</div>
<div class="status">✅ 15 preguntas</div>
</a>
<a href="modulo_02_calculo_cargas.html" class="modulo-card">
<div class="icon">⚖️</div>
<h3>M02 — Cálculo de Cargas</h3>
<div class="desc">NEC-15 + ACI 318</div>
<div class="status">✅ 15 preguntas</div>
</a>
<a href="modulo_03_viga_sismo.html" class="modulo-card">
<div class="icon">🏗️</div>
<h3>M03 — Viga + Sismo</h3>
<div class="desc">Reacciones, cortantes, momentos</div>
<div class="status">✅ 15 preguntas</div>
</a>
<a href="modulo_04_acero_cortante.html" class="modulo-card">
<div class="icon">✂️</div>
<h3>M04 — Acero a Cortante</h3>
<div class="desc">Estribos + confinamiento</div>
<div class="status">✅ 15 preguntas</div>
</a>
<a href="modulo_05_diseno_columna.html" class="modulo-card">
<div class="icon">🏛️</div>
<h3>M05 — Diseño de Columna</h3>
<div class="desc">Flexo-compresión + P-M</div>
<div class="status">✅ 15 preguntas</div>
</a>
<a href="modulo_06_diseno_losa.html" class="modulo-card">
<div class="icon">🧱</div>
<h3>M06 — Diseño de Losa</h3>
<div class="desc">Nervios articulados + armadura</div>
<div class="status">✅ 15 preguntas</div>
</a>
</div>

<!-- RECURSOS -->
<h2 class="seccion-titulo">📚 RECURSOS DEL PROGRAMA</h2>
<div class="recursos-grid">
<a href="manual_programa.html" class="recurso-card" target="_blank">
<div class="recurso-icon">📘</div>
<div class="recurso-info"><h4>Manual del Programa</h4><p>Visión completa</p></div>
</a>
<a href="M01_guia_estudio.html" class="recurso-card" target="_blank">
<div class="recurso-icon">📗</div>
<div class="recurso-info"><h4>Guía de Estudio M01</h4><p>Material del estudiante</p></div>
</a>
<a href="tabla_nec15.html" class="recurso-card" target="_blank">
<div class="recurso-icon">📄</div>
<div class="recurso-info"><h4>Tabla NEC-15</h4><p>Cargas vivas y combinaciones</p></div>
</a>
<a href="tabla_aci318.html" class="recurso-card" target="_blank">
<div class="recurso-icon">📄</div>
<div class="recurso-info"><h4>Tabla ACI 318</h4><p>Factores de mayoración</p></div>
</a>
</div>

<!-- PIE -->
<div class="pie-pagina">
<p><b>EL CONOCIMIENTO TRANSFORMA — PROYECTO DE FORMACIÓN MODULAR</b></p>
<p>Estructura I / Estructura II — Carrera de Ingeniería Civil — UNESUM — PI 2026</p>
<p>Docente responsable: Ing. Gery Lorenzo Marcillo Merino</p>
</div>

<div class="cita-final">
"Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."<br>
— Proyecto ECT-UNESUM-2026
</div>

</div>
</div>

<script>
// ============================================================
// BASE DE DATOS DE PROYECTOS (integrada en el index.html)
// ============================================================
var PROYECTOS = {
  "ECT-001": {
    nombre: "U.E. Fiscal Alejo Lascano",
    amie: "13H04545",
    parroquia: "Jipijapa",
    sector: "Urbano",
    lat: -1.3486,
    lon: -80.5789,
    prioridad: "Alta",
    tipo: "Centro Académico"
  },
  "ECT-002": {
    nombre: "Escuela Presidente Urbina",
    amie: "13H04567",
    parroquia: "La Unión",
    sector: "Agua Dulce",
    lat: -1.0529420,
    lon: -80.0704134,
    prioridad: "Alta",
    tipo: "Centro Académico",
    estudiantes: 9,
    docentes: 1,
    destacado: true
  },
  "ECT-003": {
    nombre: "U.E. Quince de Octubre",
    amie: "POR_CONFIRMAR",
    parroquia: "Jipijapa",
    sector: "Urbano",
    lat: -1.3573,
    lon: -80.5835,
    prioridad: "Alta",
    tipo: "Centro Académico"
  },
  "ECT-004": {
    nombre: "U.E. Manuel Inocencio Parrales y Guale",
    amie: "POR_CONFIRMAR",
    parroquia: "Jipijapa",
    sector: "Urbano",
    lat: -1.3561,
    lon: -80.5963,
    prioridad: "Alta",
    tipo: "Centro Académico"
  },
  "ECT-005": {
    nombre: "U.E. Daniel López",
    amie: "13H01951",
    parroquia: "Jipijapa",
    sector: "Urbano",
    lat: -1.3480,
    lon: -80.5741,
    prioridad: "Alta",
    tipo: "Centro Académico"
  },
  "AGUA-001": {
    nombre: "Escuela Presidente Urbina (Agua Dulce)",
    amie: "13H04567",
    parroquia: "La Unión",
    sector: "Agua Dulce",
    lat: -1.0529420,
    lon: -80.0704134,
    prioridad: "Alta",
    tipo: "Centro Académico — Territorio Piloto",
    estudiantes: 9,
    docentes: 1,
    destacado: true,
    es_piloto: true
  }
};

// ============================================================
// CAMBIAR ROL
// ============================================================
function cambiarRol(){
  var rol = document.querySelector('input[name="rol"]:checked').value;
  var opEst = document.getElementById('rol-estudiante');
  var opDoc = document.getElementById('rol-docente');
  if(rol === 'docente'){
    opDoc.classList.add('activa');
    opEst.classList.remove('activa');
    document.getElementById('input-codigo').placeholder = 'Modo docente — No requiere código';
  } else {
    opEst.classList.add('activa');
    opDoc.classList.remove('activa');
    document.getElementById('input-codigo').placeholder = 'Código del proyecto (ej: ECT-002)';
  }
}

// ============================================================
// IR AL LOGIN
// ============================================================
function irAlLogin(){
  document.getElementById('pantalla-portada').classList.add('hidden');
  document.getElementById('pantalla-login').classList.remove('hidden');
}

// ============================================================
// INGRESAR
// ============================================================
function ingresar(){
  var rol = document.querySelector('input[name="rol"]:checked').value;
  var n = document.getElementById('input-nombre').value.trim();
  var c = document.getElementById('input-cedula').value.trim();
  var codigo = document.getElementById('input-codigo').value.trim().toUpperCase();
  var alerta = document.getElementById('alerta-codigo');

  if(!n || !c){
    alerta.innerHTML = '<div class="alerta-error">⚠️ Complete nombre y cédula</div>';
    return;
  }

  // Validar código (excepto docente)
  var proyecto = null;
  if(rol === 'estudiante'){
    if(!codigo){
      alerta.innerHTML = '<div class="alerta-error">⚠️ Escriba el código del proyecto</div>';
      return;
    }
    if(!PROYECTOS[codigo]){
      alerta.innerHTML = '<div class="alerta-error">❌ Código "' + codigo + '" no encontrado. Verifique con su docente.</div>';
      return;
    }
    proyecto = PROYECTOS[codigo];
    alerta.innerHTML = '<div class="alerta-ok">✅ Código válido: ' + codigo + '</div>';
  } else {
    // Docente: acceso completo
    proyecto = {
      nombre: "Acceso Docente — Todos los proyectos",
      amie: "—",
      parroquia: "Jipijapa",
      sector: "Todos",
      prioridad: "—",
      tipo: "Docente"
    };
  }

  // Guardar en localStorage
  localStorage.setItem('usuario_rol', rol);
  localStorage.setItem('estudiante_nombre', n);
  localStorage.setItem('estudiante_cedula', c);
  localStorage.setItem('codigo_proyecto', codigo);
  localStorage.setItem('proyecto_asignado', JSON.stringify(proyecto));

  // Cambiar de pantalla
  setTimeout(function(){
    document.getElementById('pantalla-login').classList.add('hidden');
    document.getElementById('pantalla-modulos').classList.remove('hidden');

    var saludo = (rol === 'docente') ? '🎓 Docente Expositor: ' : '👤 Estudiante: ';
    document.getElementById('saludo-estudiante').textContent = saludo + n;

    mostrarProyecto(proyecto, codigo, rol);
  }, 800);
}

// ============================================================
// MOSTRAR PROYECTO ASIGNADO
// ============================================================
function mostrarProyecto(p, codigo, rol){
  var contenedor = document.getElementById('proyecto-asignado-box');
  
  var html = '<div class="proyecto-box">';
  html += '<div class="proyecto-titulo">🎯 PROYECTO ASIGNADO</div>';
  html += '<div class="proyecto-nombre">' + p.nombre + '</div>';
  html += '<div class="proyecto-datos">';
  if(codigo) html += '<span class="proyecto-dato">🔑 ' + codigo + '</span>';
  if(p.amie && p.amie !== '—') html += '<span class="proyecto-dato">📋 AMIE: ' + p.amie + '</span>';
  if(p.parroquia) html += '<span class="proyecto-dato">📍 ' + p.parroquia + '</span>';
  if(p.sector) html += '<span class="proyecto-dato">🏘️ ' + p.sector + '</span>';
  if(p.prioridad && p.prioridad !== '—') html += '<span class="proyecto-dato">⚡ ' + p.prioridad + '</span>';
  if(p.estudiantes) html += '<span class="proyecto-dato">👥 ' + p.estudiantes + ' estudiantes</span>';
  if(p.docentes) html += '<span class="proyecto-dato">👨‍🏫 ' + p.docentes + ' docente</span>';
  html += '</div>';
  if(p.destacado){
    html += '<div style="color:#f39c12;font-size:13px;font-weight:bold;margin-top:10px">⭐ TERRITORIO PILOTO DEL MODELO ESTOCÁSTICO</div>';
  }
  html += '</div>';
  
  contenedor.innerHTML = html;
}

// ============================================================
// INICIALIZAR
// ============================================================
document.addEventListener('DOMContentLoaded', function(){
  console.log('✅ Plataforma ECT-UNESUM-2026 cargada');
  console.log('📋 Proyectos disponibles:', Object.keys(PROYECTOS).length);
  console.log('🔑 Códigos:', Object.keys(PROYECTOS).join(', '));
});
</script>
</body>
</html>
'''

if __name__ == "__main__":
    carpeta = Path(__file__).parent
    ruta = carpeta / "index.html"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(HTML)
    print("=" * 70)
    print("GENERADOR DEL INDEX.HTML - VERSIÓN CON DOS IMÁGENES")
    print("=" * 70)
    print(f"\n✅ Archivo generado: {ruta}")
    print("\n📊 Contenido del index.html:")
    print("   • Portada con DOS imágenes: principal + secundaria")
    print("   • Imagen principal: portada_estructural.png (400px)")
    print("   • Imagen secundaria: portada_estructural_2.png (200px)")
    print("   • Login con código del proyecto")
    print("   • Validación de códigos integrada")
    print("   • 6 Módulos (M01 → M06)")
    print("   • 4 Recursos")
    print("   • Sistema de códigos: ECT-001, ECT-002, AGUA-001")
    print("\n🔑 CÓDIGOS DISPONIBLES:")
    print("   • ECT-001 → U.E. Fiscal Alejo Lascano")
    print("   • ECT-002 → Escuela Presidente Urbina ⭐")
    print("   • ECT-003 → U.E. Quince de Octubre")
    print("   • ECT-004 → U.E. Manuel Inocencio Parrales y Guale")
    print("   • ECT-005 → U.E. Daniel López")
    print("   • AGUA-001 → Escuela Presidente Urbina (Territorio Piloto)")
    print("\n🚀 Ahora abra el index.html en el navegador:")
    print(f"   {ruta}")
    print("=" * 70)