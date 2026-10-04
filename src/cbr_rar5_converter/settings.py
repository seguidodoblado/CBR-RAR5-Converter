"""Ajustes del usuario (por ahora, solo el idioma), en ~/.config/cbr-rar5-converter/settings.json."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

LANGUAGES = ("es", "en")   # idiomas que se pueden elegir en Preferencias (None: el del sistema)
CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "cbr-rar5-converter"
SETTINGS_PATH = CONFIG_DIR / "settings.json"


def read_settings(path: Path = SETTINGS_PATH) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def write_settings(settings: dict[str, Any], path: Path = SETTINGS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")


def language(path: Path = SETTINGS_PATH) -> str | None:
    """El idioma elegido, o None para seguir el del sistema (un valor desconocido se ignora)."""
    value = read_settings(path).get("language")
    return value if value in LANGUAGES else None
