from pathlib import Path
from cbr_rar5_converter.detector import detect_rar_format
from cbr_rar5_converter.discovery import find_cbr_files
from cbr_rar5_converter.models import RarFormat
from cbr_rar5_converter.planning import plan_conversion

def test_detect_headers(tmp_path: Path):
    (tmp_path / "a.cbr").write_bytes(b"Rar!\x1a\x07\x00rest")
    (tmp_path / "b.cbr").write_bytes(b"Rar!\x1a\x07\x01\x00rest")
    (tmp_path / "c.cbr").write_bytes(b"bad")
    assert detect_rar_format(tmp_path / "a.cbr") == RarFormat.RAR4
    assert detect_rar_format(tmp_path / "b.cbr") == RarFormat.RAR5
    assert detect_rar_format(tmp_path / "c.cbr") == RarFormat.UNKNOWN

def test_search_excludes_corregido(tmp_path: Path):
    (tmp_path / "a.cbr").write_bytes(b""); (tmp_path / "sub").mkdir(); (tmp_path / "sub" / "b.CBR").write_bytes(b"")
    (tmp_path / "Corregido").mkdir(); (tmp_path / "Corregido" / "c.cbr").write_bytes(b"")
    assert [p.name for p in find_cbr_files([tmp_path], True)] == ["a.cbr", "b.CBR"]

def test_plan(tmp_path: Path):
    item = plan_conversion(tmp_path / "comic.cbr", RarFormat.RAR4)
    assert item.destination == tmp_path / "Corregido" / "comic.cbr"
    assert plan_conversion(item.source, RarFormat.RAR5).status.value == "Omitido"
