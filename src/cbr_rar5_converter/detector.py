from pathlib import Path

from .models import RarFormat

RAR4_SIGNATURE = b"Rar!\x1a\x07\x00"
RAR5_SIGNATURE = b"Rar!\x1a\x07\x01\x00"

def detect_rar_format(path: Path, read_size: int = 64) -> RarFormat:
    try:
        with Path(path).open("rb") as stream:
            header = stream.read(read_size)
    except OSError:
        return RarFormat.UNKNOWN
    if header.startswith(RAR5_SIGNATURE):
        return RarFormat.RAR5
    if header.startswith(RAR4_SIGNATURE):
        return RarFormat.RAR4
    return RarFormat.UNKNOWN
