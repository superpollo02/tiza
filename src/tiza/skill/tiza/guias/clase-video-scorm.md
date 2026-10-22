# Guía: Sección «La Clase» con Mediación Audiovisual Dual y SCORM

Esta guía describe cómo diseñar y publicar la sección **«1. La Clase» (`# Clase:`)** combinando:
1. **Páginas y etiquetas Moodle mediante Tiza** (respetando la lista blanca de Bootstrap 4.6.2 y iframes responsivos de YouTube/Vimeo).
2. **Paquetes SCORM interactivos mediante `scorm_modern`** (admitiendo múltiples videos, `VIDEO_ADICIONAL:`, YouTube, Vimeo, Google Drive y archivos `.mp4` locales).

---

## 1. Metodología «Aula Tripartita» (Circular 5 / Kit Aula Lista)

Toda unidad didáctica se organiza en tres momentos pedagógicos:
- **1. La Clase (Activación y Encuadre)**: Banner temático, contextualización andragógica (3 preguntas: *¿Qué vamos a aprender?*, *¿Por qué es importante para mi trabajo diario?*, *¿Cómo se conecta con la práctica anterior?*) y **Mediación Audiovisual Dual**:
  - **Video 1 (Microlearning)**: Video corto de impacto (60–90 segundos).
  - **Video 2 (Video Adicional de la Clase)**: Video-lección magistral explicativa, cápsula de profundización o demostración clínica/práctica.
- **2. La Lectura (Profundización Teórica)**: Lecturas estructuradas, infografías y glosarios.
- **3. La Práctica (Consolidación Gamificada)**: Actividad Conectabloques (8 pares) y Cuestionario/Evaluación autocorregible.

---

## 2. Publicación en Moodle con Tiza (`tipo: pagina` y `tipo: etiqueta`)

### A. Etiqueta de Encuadre de «La Clase»
Se publica como `etiqueta` visible directamente en la sección del tema en Moodle:

```html
---
tipo: etiqueta
nombre: "1. La Clase — Encuadre y Activación"
seccion: "Unidad 1"
---

<div class="card border-primary mb-3">
  <div class="card-header bg-primary text-white font-weight-bold">
    <i class="fa-solid fa-chalkboard-user mr-2" aria-hidden="true"></i> 1. La Clase: Activación y Encuadre
  </div>
  <div class="card-body">
    <h5 class="card-title text-primary">Contextualización Andragógica</h5>
    <ul class="list-group list-group-flush mb-3">
      <li class="list-group-item"><strong>¿Qué aprenderemos?</strong> Conceptos esenciales y modelos comparados aplicables a la gestión.</li>
      <li class="list-group-item"><strong>¿Por qué es importante?</strong> Permite fundamentar decisiones estratégicas en evidencia sólida.</li>
      <li class="list-group-item"><strong>Conexión práctica:</strong> Integra los conocimientos previos con los desafíos operativos actuales.</li>
    </ul>
    <div class="alert alert-info mb-0">
      <i class="fa-solid fa-circle-info mr-1" aria-hidden="true"></i>
      Visualiza el <em>Video de Microlearning</em> y la <em>Video-Lección Principal</em> en la página interactiva a continuación.
    </div>
  </div>
</div>
```

### B. Página de la Clase con Mediación Audiovisual Dual
Para cumplir el filtro estricto de Tiza (`src/tiza/filtro.py`), los videos externos se insertan mediante `<iframe>` responsivos en contenedores con relación de aspecto 16:9 (`youtube-nocookie.com/embed/...` o `player.vimeo.com/video/...`):

```html
---
tipo: pagina
nombre: "Video-Lecciones: Microlearning y Clase Magistral"
seccion: "Unidad 1"
finalizacion: ver
---

<h3><i class="fa-solid fa-play text-primary mr-2" aria-hidden="true"></i> Mediación Audiovisual de la Unidad</h3>
<p class="lead">Explora las dos cápsulas audiovisuales antes de avanzar a las lecturas obligatorias:</p>

<!-- Video 1: Microlearning (60-90 s) -->
<div class="card mb-4 shadow-sm">
  <div class="card-header bg-dark text-white font-weight-bold">
    <i class="fa-solid fa-bolt mr-2 text-warning" aria-hidden="true"></i> Video 1: Microlearning Introductorio
  </div>
  <div class="card-body p-0">
    <div style="width:100%; aspect-ratio:16/9; background:#000;">
      <iframe src="https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ" title="Microlearning Unidad 1" style="width:100%; height:100%; border:0;" allowfullscreen></iframe>
    </div>
  </div>
  <div class="card-footer bg-light text-muted small">
    Resumen ejecutivo de 90 segundos con los conceptos clave de la unidad.
  </div>
</div>

<!-- Video 2: Video-Lección Adicional / Magistral -->
<div class="card mb-4 shadow-sm">
  <div class="card-header bg-dark text-white font-weight-bold">
    <i class="fa-solid fa-video mr-2 text-info" aria-hidden="true"></i> Video 2: Video-Lección Magistral Principal
  </div>
  <div class="card-body p-0">
    <div style="width:100%; aspect-ratio:16/9; background:#000;">
      <iframe src="https://player.vimeo.com/video/76979871" title="Clase Magistral Unidad 1" style="width:100%; height:100%; border:0;" allowfullscreen></iframe>
    </div>
  </div>
  <div class="card-footer bg-light text-muted small">
    Exposición magistral detallada con análisis comparado de casos prácticos.
  </div>
</div>
```

---

## 3. Integración en Paquetes SCORM Modernos (`scorm_modern`)

En los archivos fuente de cursos SCORM (`modulo_scorm.md` o checkpoints), la sección `# Clase:` admite **múltiples videos** y la directiva **`VIDEO_ADICIONAL:`**:

### Sintaxis en `modulo_scorm.md`:
```markdown
# Clase: Fundamentos y Comparativa de Sistemas Sanitarios

Esta lección inicial introduce los conceptos matrices que articularán la unidad.

:::apoyo
VIDEO: https://youtu.be/dQw4w9WgXcQ
VIDEO_ADICIONAL: https://vimeo.com/76979871 | Video-Lección Magistral Explicativa
VIDEO_ADICIONAL: media/video_microlearning_u1.mp4 | Cápsula Local de Microlearning (MP4)
:::

### Preguntas Guía para la Clase
1. ¿Qué variables diferencian un modelo Bismarck de uno Beveridge?
2. ¿Cómo impacta la descentralización en la equidad de acceso?
```

- **Plataformas soportadas para embeber**:
  - **YouTube**: `https://www.youtube.com/watch?v=...`, `https://youtu.be/...`, shorts y `youtube-nocookie.com`.
  - **Vimeo**: `https://vimeo.com/<id>`, `https://player.vimeo.com/video/<id>`.
  - **Google Drive**: `https://drive.google.com/file/d/<id>/view`.
  - **Archivos locales (`.mp4`, `.webm`)**: rutas relativas como `media/video.mp4` o `03_video_microlearning/short_u1.mp4`. El compilador SCORM copia el archivo local a la carpeta `media/` del paquete y renderiza un reproductor HTML5 con `<video controls preload="metadata">`.

---

## 4. Flujo de Trabajo Recomendado
1. Diseñar el guion del video principal y del video adicional con el docente.
2. Comprobar offline las páginas/etiquetas con `tiza comprobar <fichero.html>`.
3. Empaquetar el módulo interactivo con `scorm-course-generator` (`scorm_modern`).
4. Publicar en pruebas (`tiza publicar <fichero.html> --en pruebas`).
5. Tras confirmación del docente, publicar en real (`tiza publicar <fichero.html> --en real`).
