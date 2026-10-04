from pathlib import Path

from cbr_rar5_converter.detector import detect_rar_format
from cbr_rar5_converter.discovery import find_cbr_files
from cbr_rar5_converter.models import RarFormat
from cbr_rar5_converter.planning import plan_conversion, plan_recursive

RAR4 = b"Rar!\x1a\x07\x00rest"
RAR5 = b"Rar!\x1a\x07\x01\x00rest"


def test_detect_headers(tmp_path: Path):
    (tmp_path / "a.cbr").write_bytes(RAR4)
    (tmp_path / "b.cbr").write_bytes(RAR5)
    (tmp_path / "c.cbr").write_bytes(b"bad")
    assert detect_rar_format(tmp_path / "a.cbr") == RarFormat.RAR4
    assert detect_rar_format(tmp_path / "b.cbr") == RarFormat.RAR5
    assert detect_rar_format(tmp_path / "c.cbr") == RarFormat.UNKNOWN


def test_detect_missing_file_is_unknown(tmp_path: Path):
    assert detect_rar_format(tmp_path / "no-existe.cbr") == RarFormat.UNKNOWN


def test_search_excludes_corregido(tmp_path: Path):
    (tmp_path / "a.cbr").write_bytes(b"")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.CBR").write_bytes(b"")
    (tmp_path / "Corregido").mkdir()
    (tmp_path / "Corregido" / "c.cbr").write_bytes(b"")
    assert [p.name for p in find_cbr_files([tmp_path], True)] == ["a.cbr", "b.CBR"]


def test_search_is_not_recursive_by_default(tmp_path: Path):
    (tmp_path / "a.cbr").write_bytes(b"")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.cbr").write_bytes(b"")
    assert [p.name for p in find_cbr_files([tmp_path])] == ["a.cbr"]


def test_search_accepts_single_files_and_ignores_other_extensions(tmp_path: Path):
    (tmp_path / "a.cbr").write_bytes(b"")
    (tmp_path / "b.cbz").write_bytes(b"")
    assert find_cbr_files([tmp_path / "a.cbr", tmp_path / "b.cbz", tmp_path / "no-existe"]) == [tmp_path / "a.cbr"]


def test_plan(tmp_path: Path):
    item = plan_conversion(tmp_path / "comic.cbr", RarFormat.RAR4)
    assert item.destination == tmp_path / "Corregido" / "comic.cbr"
    assert plan_conversion(item.source, RarFormat.RAR5).status.value == "Omitido"


def test_plan_recursive_keeps_the_subfolder_structure(tmp_path: Path):
    (tmp_path / "serie").mkdir()
    source = tmp_path / "serie" / "n1.cbr"
    source.write_bytes(RAR4)
    (item,) = plan_recursive(tmp_path, [source], {source.resolve(): RarFormat.RAR4})
    assert item.destination == tmp_path.resolve() / "Corregido" / "serie" / "n1.cbr"
    assert item.status.value == "Preparado"
