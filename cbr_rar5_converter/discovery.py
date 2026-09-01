from collections.abc import Iterable
from pathlib import Path

def find_cbr_files(roots: Iterable[Path], recursive: bool = False) -> list[Path]:
    found: set[Path] = set()
    for root in roots:
        root = Path(root)
        if root.is_file():
            if root.suffix.lower() == ".cbr" and "Corregido" not in root.parts:
                found.add(root)
            continue
        if not root.is_dir():
            continue
        for path in (root.rglob("*") if recursive else root.iterdir()):
            if "Corregido" not in path.parts and path.is_file() and path.suffix.lower() == ".cbr":
                found.add(path)
    return sorted(found, key=lambda p: str(p).casefold())
