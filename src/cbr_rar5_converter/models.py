from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .i18n import _


class RarFormat(str, Enum):
    RAR4 = "RAR4"
    RAR5 = "RAR5"
    UNKNOWN = "Desconocido"

    @property
    def label(self) -> str:
        """El nombre que ve el usuario; el valor del enumerado es una clave estable."""
        return _("Desconocido") if self is RarFormat.UNKNOWN else self.value

class ConversionStatus(str, Enum):
    DETECTED = "Detectado"
    READY = "Preparado"
    SKIPPED = "Omitido"
    CONVERTING = "Convirtiendo"
    COMPLETED = "Completado"
    FAILED = "Error"

    @property
    def label(self) -> str:
        """El estado que ve el usuario; el valor del enumerado es una clave estable."""
        return {
            ConversionStatus.DETECTED: _("Detectado"),
            ConversionStatus.READY: _("Preparado"),
            ConversionStatus.SKIPPED: _("Omitido"),
            ConversionStatus.CONVERTING: _("Convirtiendo"),
            ConversionStatus.COMPLETED: _("Completado"),
            ConversionStatus.FAILED: _("Error"),
        }[self]

@dataclass
class ConversionItem:
    source: Path
    destination: Path
    format: RarFormat
    status: ConversionStatus = ConversionStatus.DETECTED
    message: str = ""
