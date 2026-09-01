from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class RarFormat(str, Enum):
    RAR4 = "RAR4"
    RAR5 = "RAR5"
    UNKNOWN = "Desconocido"

class ConversionStatus(str, Enum):
    DETECTED = "Detectado"
    READY = "Preparado"
    SKIPPED = "Omitido"
    CONVERTING = "Convirtiendo"
    COMPLETED = "Completado"
    FAILED = "Error"

@dataclass
class ConversionItem:
    source: Path
    destination: Path
    format: RarFormat
    status: ConversionStatus = ConversionStatus.DETECTED
    message: str = ""
