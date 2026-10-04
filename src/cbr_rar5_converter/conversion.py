import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path
from threading import Event

from .detector import detect_rar_format
from .i18n import _
from .models import ConversionItem, ConversionStatus, RarFormat

ProgressCallback = Callable[[int], None]


def rar_available() -> bool:
    return shutil.which("rar") is not None


class RarConverter:
    """Extrae con rar y vuelve a crear el archivo usando el formato RAR5."""

    def __init__(self, executable: str = "rar", progress: ProgressCallback | None = None,
                 cancel: Event | None = None):
        self.executable, self.progress, self.cancel = executable, progress, cancel or Event()

    def __call__(self, source: Path, destination: Path) -> None:
        with tempfile.TemporaryDirectory(prefix="cbr-rar5-") as directory:
            work = Path(directory)
            self._run([self.executable, "x", "-idq", "-o-", str(source), str(work)], None)
            self._run([self.executable, "a", "-ma5", "-r", str(destination), "."], work)

    def _run(self, command: list[str], cwd: Path | None) -> None:
        process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, bufsize=1)
        output = []
        for line in process.stdout or ():
            output.append(line)
            match = re.search(r"(\d{1,3})%", line)
            if match and self.progress:
                self.progress(min(100, int(match.group(1))))
            if self.cancel.is_set():
                process.terminate()
                raise RuntimeError(_("Conversión cancelada."))
        if process.wait() != 0:
            raise RuntimeError(_("rar no pudo procesar el archivo: {detail}").format(detail="".join(output).strip()))


class ConversionService:
    """Servicio seguro con temporales, validación y sustitución atómica."""
    def __init__(self, converter: Callable[[Path, Path], None] | None = None,
                 progress: ProgressCallback | None = None, cancel: Event | None = None):
        self.converter = converter
        self.progress = progress
        self.cancel = cancel or Event()

    def convert(self, item: ConversionItem) -> ConversionItem:
        if item.format != RarFormat.RAR4:
            item.status, item.message = ConversionStatus.SKIPPED, _("No es RAR4.")
            return item
        converter = self.converter or RarConverter(progress=self.progress, cancel=self.cancel)
        if self.converter is None and not rar_available():
            item.status, item.message = ConversionStatus.FAILED, _("No se encontró el comando 'rar'.")
            return item
        if item.destination.exists():
            item.status, item.message = ConversionStatus.FAILED, _("El destino ya existe.")
            return item
        item.status = ConversionStatus.CONVERTING
        item.destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            with tempfile.TemporaryDirectory(dir=item.destination.parent) as temp_dir:
                temporary = Path(temp_dir) / item.destination.name
                converter(item.source, temporary)
                if detect_rar_format(temporary) != RarFormat.RAR5:
                    raise ValueError(_("El resultado no tiene cabecera RAR5 válida."))
                fd = os.open(item.destination.parent, os.O_RDONLY)
                try:
                    os.replace(temporary, item.destination)
                    os.fsync(fd)
                finally:
                    os.close(fd)
            item.status = ConversionStatus.COMPLETED
        except (OSError, ValueError, RuntimeError) as error:
            item.status, item.message = ConversionStatus.FAILED, str(error)
        return item
