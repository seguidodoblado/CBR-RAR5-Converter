import os
import stat
from pathlib import Path
from threading import Event

import pytest

from cbr_rar5_converter.conversion import ConversionService, RarConverter, rar_available
from cbr_rar5_converter.models import ConversionItem, ConversionStatus, RarFormat
from cbr_rar5_converter.queue import ConversionQueue

RAR4 = b"Rar!\x1a\x07\x00original"
RAR5 = b"Rar!\x1a\x07\x01\x00convertido"


def item(tmp_path: Path, fmt=RarFormat.RAR4) -> ConversionItem:
    source = tmp_path / "comic.cbr"
    source.write_bytes(RAR4)
    return ConversionItem(source, tmp_path / "Corregido" / "comic.cbr", fmt)


def fake_converter(content: bytes):
    def convert(source: Path, destination: Path) -> None:
        destination.write_bytes(content)
    return convert


def test_converts_and_keeps_the_original(tmp_path: Path):
    done = ConversionService(converter=fake_converter(RAR5)).convert(item(tmp_path))
    assert done.status is ConversionStatus.COMPLETED
    assert done.destination.read_bytes() == RAR5
    assert done.source.read_bytes() == RAR4   # el original no se toca


def test_leaves_no_temporary_files_behind(tmp_path: Path):
    ConversionService(converter=fake_converter(RAR5)).convert(item(tmp_path))
    assert [p.name for p in (tmp_path / "Corregido").iterdir()] == ["comic.cbr"]


def test_skips_what_is_not_rar4(tmp_path: Path):
    done = ConversionService(converter=fake_converter(RAR5)).convert(item(tmp_path, RarFormat.RAR5))
    assert done.status is ConversionStatus.SKIPPED
    assert not done.destination.exists()


def test_does_not_overwrite_an_existing_destination(tmp_path: Path):
    target = item(tmp_path)
    target.destination.parent.mkdir()
    target.destination.write_bytes(b"ya estaba")
    done = ConversionService(converter=fake_converter(RAR5)).convert(target)
    assert done.status is ConversionStatus.FAILED
    assert done.destination.read_bytes() == b"ya estaba"


def test_rejects_a_result_without_a_valid_rar5_header(tmp_path: Path):
    done = ConversionService(converter=fake_converter(RAR4)).convert(item(tmp_path))
    assert done.status is ConversionStatus.FAILED
    assert not done.destination.exists()
    assert [p.name for p in (tmp_path / "Corregido").iterdir()] == []   # ni el temporal


def test_a_failing_converter_marks_the_item_as_failed(tmp_path: Path):
    def broken(source: Path, destination: Path) -> None:
        raise RuntimeError("rar se rompió")
    done = ConversionService(converter=broken).convert(item(tmp_path))
    assert done.status is ConversionStatus.FAILED
    assert "rar se rompió" in done.message


def test_queue_converts_every_item(tmp_path: Path):
    first, second = item(tmp_path), item(tmp_path)
    second.destination = tmp_path / "Corregido" / "otro.cbr"
    results = ConversionQueue(ConversionService(converter=fake_converter(RAR5))).run([first, second])
    assert [r.status for r in results] == [ConversionStatus.COMPLETED] * 2


def test_without_the_rar_command_it_fails_cleanly(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path))
    assert not rar_available()
    done = ConversionService().convert(item(tmp_path))
    assert done.status is ConversionStatus.FAILED
    assert "rar" in done.message


def fake_rar(tmp_path: Path, script: str) -> str:
    path = tmp_path / "fake-rar"
    path.write_text("#!/bin/sh\n" + script, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return str(path)


def test_rar_converter_reports_progress_from_the_output(tmp_path: Path):
    progress: list[int] = []
    executable = fake_rar(tmp_path, 'echo "  10%"; echo " 55%"; echo "100%"\nexit 0\n')
    RarConverter(executable, progress.append)(tmp_path / "a.cbr", tmp_path / "b.cbr")
    assert progress[:3] == [10, 55, 100]


def test_rar_converter_raises_with_the_command_output_on_failure(tmp_path: Path):
    executable = fake_rar(tmp_path, 'echo "archivo dañado"; exit 3\n')
    with pytest.raises(RuntimeError, match="archivo dañado"):
        RarConverter(executable)(tmp_path / "a.cbr", tmp_path / "b.cbr")


def test_rar_converter_can_be_cancelled(tmp_path: Path):
    cancel = Event()
    cancel.set()
    executable = fake_rar(tmp_path, 'echo "5%"; sleep 5\n')
    with pytest.raises(RuntimeError, match="cancelada"):
        RarConverter(executable, cancel=cancel)(tmp_path / "a.cbr", tmp_path / "b.cbr")


def test_the_temp_directory_of_rar_converter_is_removed(tmp_path: Path):
    executable = fake_rar(tmp_path, 'pwd >> "$0.log"\nexit 0\n')
    RarConverter(executable)(tmp_path / "a.cbr", tmp_path / "b.cbr")
    seen = Path(executable + ".log").read_text(encoding="utf-8").split()
    assert seen and not any(os.path.exists(p) and "cbr-rar5-" in p for p in seen)
