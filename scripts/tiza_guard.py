#!/usr/bin/env python3
"""tiza_guard.py - Hook de seguridad PreToolUse para el plugin tiza en Antigravity.

Intercepta llamadas a herramientas (run_command, read_file, view_file, write_file, edit_file)
para evitar:
1. Ejecución de comandos exclusivos del docente (tiza empezar, sesion, configurar, autoprueba, aislar, actualizar, python -m tiza.ventana).
2. Descompresión o lectura manual de archivos de respaldo .mbz (obligando a usar 'tiza importar').
3. Lectura o manipulación de directorios privados de configuración/caché de tiza o perfiles de navegadores.
4. Modificación no autorizada de tiza.toml o metadatos protegidos de tiza (.tiza/verificados.json, .tiza/copia.json).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Comandos exclusivos del docente que el agente tiene estrictamente prohibido invocar
COMANDOS_PROHIBIDOS = {
    "empezar",
    "sesion",
    "configurar",
    "autoprueba",
    "aislar",
    "actualizar",
}

# Substrings o patrones de utilidades de descompresión sobre ficheros .mbz
PATRON_MBZ_MANUAL = re.compile(
    r"\b(tar|unzip|7z|7za|gunzip|bunzip2|expand-archive)\b.*\.mbz\b|\.mbz\b.*(tar|unzip|7z|7za|gunzip|bunzip2|expand-archive)",
    re.IGNORECASE,
)

# Nombres de navegadores y directorios sensibles que jamás deben ser leídos por el agente
RUTAS_SENSIBLES = [
    "AppData/Local/Google/Chrome",
    "AppData/Local/Microsoft/Edge",
    "AppData/Roaming/Mozilla/Firefox",
    "AppData/Local/BraveSoftware",
    "AppData/Local/Vivaldi",
    "AppData/Local/tiza",
    "AppData/Roaming/tiza",
    ".config/tiza",
    ".cache/tiza",
    ".config/google-chrome",
    ".config/chromium",
    ".mozilla/firefox",
]


def responder(decision: str, reason: str = "") -> None:
    output = {"decision": decision}
    if reason:
        output["reason"] = reason
    print(json.dumps(output))
    sys.exit(0)


def normalizar_ruta(ruta: str) -> str:
    return ruta.replace("\\", "/").lower()


def verificar_run_command(command_line: str) -> None:
    cmd_strip = command_line.strip()
    cmd_lower = cmd_strip.lower()

    # 1. Comprobar comandos tiza
    tokens = cmd_strip.split()
    if tokens:
        # Detectar python -m tiza o ejecutable tiza
        subcmd = None
        if len(tokens) >= 2 and (tokens[0].lower().endswith("tiza") or tokens[0].lower().endswith("tiza.exe")):
            subcmd = tokens[1].lower()
        elif len(tokens) >= 4 and "tiza" in tokens[1].lower() and tokens[2].lower() == "-m" and "tiza" in tokens[3].lower():
            if len(tokens) >= 5:
                subcmd = tokens[4].lower()
        elif "tiza.ventana" in cmd_lower:
            responder(
                "deny",
                "Comando prohibido: 'python -m tiza.ventana' es la interfaz gráfica del docente y no debe ser invocada por el agente.",
            )

        # Si se detectó un subcomando de tiza
        if subcmd:
            # Eliminar posibles flags
            subcmd_clean = subcmd.lstrip("-")
            if subcmd_clean in COMANDOS_PROHIBIDOS:
                responder(
                    "deny",
                    f"Comando prohibido para el agente: 'tiza {subcmd_clean}'. Este comando requiere interacción exclusiva del docente.",
                )

    # 2. Comprobar intentos de abrir .mbz manualmente
    if ".mbz" in cmd_lower and PATRON_MBZ_MANUAL.search(cmd_lower):
        responder(
            "deny",
            "Extracción manual de .mbz prohibida para proteger datos del alumnado (RGPD). Utiliza 'tiza importar <archivo.mbz>'.",
        )


def verificar_acceso_fichero(herramienta: str, path_str: str) -> None:
    if not path_str:
        return

    path_norm = normalizar_ruta(path_str)

    # 1. Protección contra lectura de navegadores y configuración privada
    for sensible in RUTAS_SENSIBLES:
        if sensible.lower() in path_norm:
            responder(
                "deny",
                f"Acceso denegado a rutas privadas del sistema/navegador ({sensible}) por motivos de seguridad y privacidad.",
            )

    # 2. Protección contra modificación de ficheros de configuración de tiza
    if herramienta in {"write_file", "edit_file"}:
        basename = Path(path_str).name.lower()
        if basename == "tiza.toml":
            responder(
                "deny",
                "Modificación no permitida: 'tiza.toml' contiene la configuración del aula virtual del docente y no debe ser alterada por el agente.",
            )
        if basename in {"verificados.json", "copia.json"} and ".tiza" in path_norm:
            responder(
                "deny",
                f"Modificación no permitida: '{basename}' es un registro interno gestionado exclusivamente por el CLI de tiza.",
            )


def main() -> None:
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            responder("allow")

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})

        if tool_name == "run_command":
            cmd = args.get("CommandLine", "") or args.get("command", "")
            verificar_run_command(cmd)

        elif tool_name in {"read_file", "view_file", "write_file", "edit_file"}:
            path_val = args.get("Path", "") or args.get("path", "")
            verificar_acceso_fichero(tool_name, str(path_val))

        responder("allow")

    except Exception:
        # En caso de error inesperado en el hook, permitir para no bloquear el entorno
        responder("allow")


if __name__ == "__main__":
    main()
