import os
import tempfile
from collections.abc import Callable
from pathlib import Path
from .detector import detect_rar_format
from .models import ConversionItem, ConversionStatus, RarFormat

class ConversionService:
    """Conversión segura con conversor inyectable; el backend RAR5 llegará después."""
    def __init__(self, converter: Callable[[Path, Path], None] | None = None):
        self.converter = converter

    def convert(self, item: ConversionItem) -> ConversionItem:
        if item.format != RarFormat.RAR4:
            item.status, item.message = ConversionStatus.SKIPPED, "No es RAR4."
            return item
        if self.converter is None:
            item.status, item.message = ConversionStatus.READY, "Conversor RAR5 pendiente."
            return item
        if item.destination.exists():
            item.status, item.message = ConversionStatus.FAILED, "El destino ya existe."
            return item
        item.status = ConversionStatus.CONVERTING
        item.destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            with tempfile.TemporaryDirectory(dir=item.destination.parent) as temp_dir:
                temporary = Path(temp_dir) / item.destination.name
                self.converter(item.source, temporary)
                if detect_rar_format(temporary) != RarFormat.RAR5:
                    raise ValueError("El resultado no tiene cabecera RAR5 válida.")
                fd = os.open(item.destination.parent, os.O_RDONLY)
                try:
                    os.replace(temporary, item.destination)
                    os.fsync(fd)
                finally:
                    os.close(fd)
            item.status = ConversionStatus.COMPLETED
        except (OSError, ValueError) as error:
            item.status, item.message = ConversionStatus.FAILED, str(error)
        return item
