<p align="right"><a href="README.md">🇪🇸 Español</a></p>

<p align="center">
  <img src="cbr-rar5-converter.svg" alt="CBR RAR5 Converter logo" width="128">
</p>

<h1 align="center">CBR RAR5 Converter</h1>

<p align="center">
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter/releases"><img src="https://img.shields.io/github/v/release/seguidodoblado/CBR-RAR5-Converter" alt="release"></a>
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter/actions/workflows/ci.yml"><img src="https://github.com/seguidodoblado/CBR-RAR5-Converter/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter/actions/workflows/cd.yml"><img src="https://github.com/seguidodoblado/CBR-RAR5-Converter/actions/workflows/cd.yml/badge.svg" alt="CD"></a>
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter/blob/main/COPYING"><img src="https://img.shields.io/github/license/seguidodoblado/CBR-RAR5-Converter" alt="license"></a>
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter/commits/main/"><img src="https://img.shields.io/github/last-commit/seguidodoblado/CBR-RAR5-Converter" alt="last commit"></a>
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter/commits/main/"><img src="https://img.shields.io/github/commit-activity/t/seguidodoblado/CBR-RAR5-Converter" alt="total commits"></a>
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter/releases"><img src="https://img.shields.io/github/downloads/seguidodoblado/CBR-RAR5-Converter/total" alt="downloads"></a>
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter/stargazers"><img src="https://img.shields.io/github/stars/seguidodoblado/CBR-RAR5-Converter?style=flat" alt="stars"></a>
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter/issues"><img src="https://img.shields.io/github/issues/seguidodoblado/CBR-RAR5-Converter" alt="issues"></a>
  <a href="https://github.com/seguidodoblado/CBR-RAR5-Converter"><img src="https://img.shields.io/github/languages/top/seguidodoblado/CBR-RAR5-Converter" alt="language"></a>
  <a href="https://codetime.dev"><img alt="CodeTime Badge" src="https://shields.jannchie.com/endpoint?style=flat&color=0284c7&url=https%3A%2F%2Fcodetime.dev%2Fv3%2Fusers%2Fshield%3Fuid%3D36830"></a>
  <a href="https://wakatime.com/badge/github/seguidodoblado/CBR-RAR5-Converter"><img src="https://wakatime.com/badge/github/seguidodoblado/CBR-RAR5-Converter.svg" alt="wakatime"></a>
</p>

<p align="center">
  Safely converts <code>.cbr</code> files in RAR4 format to RAR5, without modifying the originals.
</p>

<p align="center">
  <img src="docs/screenshot.png" alt="CBR RAR5 Converter screenshot">
</p>

Desktop application (GTK 4 + PyGObject, interface in Spanish and English), for personal use: no server, no account,
everything happens on your own machine.

- **Detects** the format of each `.cbr` from its header, not from its extension.
- **Searches** individual files or whole folders, optionally walking through subfolders.
- **Converts** safely: temporary file, RAR5 header validation and atomic replacement, never overwriting existing
  destinations.
- **Never modifies the originals**: the result is saved in a `Corregido` subfolder, preserving the relative path.
- **Per-file and per-batch progress** when converting several comics at once.

## Documentation

Full documentation —installation, usage guide, technical specifications, troubleshooting and more— is on the
**[project wiki](https://github.com/seguidodoblado/CBR-RAR5-Converter/wiki)** (Spanish and English).

## Privacy

CBR RAR5 Converter has no server or account of its own, does not connect to the Internet and does not collect data. What is stored and where is in the **[privacy policy](PRIVACY.en.md)**.

## License

This project is distributed under the GNU General Public License, version 3 or later (see `COPYING`).
