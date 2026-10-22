---
name: tiza-instalar
description: Guía al docente para instalar, configurar por primera vez y verificar el aislamiento del sistema Tiza en Antigravity. Úsala cuando el docente quiera poner en marcha Tiza, comprobar su aula Moodle o asegurar que su entorno respeta la privacidad de los datos.
---

# Asistente de Instalación y Puesta en Marcha de Tiza (Antigravity)

Esta skill guía al docente paso a paso para configurar Tiza en su aula virtual Moodle con total seguridad.

## 1. Verificación del CLI de Tiza

Comprueba si el comando `tiza` está instalado y accesible en la terminal del sistema:
```bash
tiza --version
```
- Si no está instalado, indícale al docente que ejecute:
  ```bash
  uv tool install tiza
  ```
  o en Windows con PowerShell:
  ```powershell
  winget install astral-sh.uv
  uv tool install tiza
  ```

## 2. Preparación de la Carpeta de la Asignatura

1. El docente debe situarse en la carpeta de su asignatura o crear una nueva:
   ```bash
   mkdir MiAsignatura
   cd MiAsignatura
   ```
2. Inicializar la configuración de tiza:
   ```bash
   tiza configurar
   ```
   *Nota*: El comando `tiza configurar` lo ejecuta **exclusivamente el docente** en su terminal interactiva. Nunca pidas ni introduzcas credenciales en el chat del agente.

## 3. Comprobación del Aislamiento y Seguridad

Verifica que el entorno de Antigravity cuenta con el hook de protección activo:
```bash
tiza revisar
```
- Si el reporte indica que falta aislamiento, el docente puede ejecutar:
  ```bash
  tiza aislar
  ```
- En Antigravity, la protección `PreToolUse` provista en `hooks.json` (`scripts/tiza_guard.py`) garantiza que:
  - El agente no pueda ejecutar comandos con privilegios docentes (`tiza empezar`, `tiza sesion`).
  - No se lean datos de perfiles de navegador ni contraseñas.
  - No se extraigan datos personales de alumnos desde copias de seguridad `.mbz`.

## 4. Primera Conexión y Apertura de Sesión

Para que el agente pueda comprobar la estructura o publicar borradores:
1. El docente ejecuta en su terminal:
   ```bash
   tiza empezar
   ```
2. Se abrirá el navegador institucional en la página de inicio de sesión de Moodle. El docente introduce su usuario y contraseña en el navegador oficial.
3. Una vez dentro, `tiza` sincroniza `.tiza/estructura.json` y el agente queda habilitado para preparar y publicar contenido a través del buzón seguro.
