from pathlib import Path
from .models import ConversionItem, ConversionStatus, RarFormat

def plan_conversion(source: Path, detected: RarFormat) -> ConversionItem:
    source = Path(source)
    destination = source.parent / "Corregido" / source.name
    ready = detected == RarFormat.RAR4
    return ConversionItem(source, destination, detected,
                          ConversionStatus.READY if ready else ConversionStatus.SKIPPED,
                          "" if ready else "Solo se convierten archivos RAR4.")

def plan_recursive(root: Path, files: list[Path], formats: dict[Path, RarFormat] | None = None) -> list[ConversionItem]:
    root = Path(root).resolve()
    formats = formats or {}
    result = []
    for source in files:
        source = Path(source).resolve()
        relative = source.relative_to(root)
        if "Corregido" in relative.parts:
            continue
        result.append(plan_conversion(root / relative, formats.get(source, RarFormat.UNKNOWN)))
        result[-1].destination = root / "Corregido" / relative
    return result
