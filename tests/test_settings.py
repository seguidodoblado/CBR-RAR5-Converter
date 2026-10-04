from pathlib import Path

from cbr_rar5_converter import settings


def test_without_a_file_the_language_follows_the_system(tmp_path: Path):
    assert settings.read_settings(tmp_path / "no-existe.json") == {}
    assert settings.language(tmp_path / "no-existe.json") is None


def test_the_chosen_language_is_saved_and_read_back(tmp_path: Path):
    path = tmp_path / "config" / "settings.json"
    settings.write_settings({"language": "en"}, path)
    assert settings.language(path) == "en"


def test_an_unknown_language_or_a_broken_file_is_ignored(tmp_path: Path):
    path = tmp_path / "settings.json"
    path.write_text('{"language": "klingon"}', encoding="utf-8")
    assert settings.language(path) is None
    path.write_text("esto no es json", encoding="utf-8")
    assert settings.read_settings(path) == {}
    path.write_text("[1, 2]", encoding="utf-8")
    assert settings.read_settings(path) == {}
