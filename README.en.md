<p align="right"><a href="README.md">🇪🇸 Español</a></p>

<p align="center">
  <img src="cbr-rar5-converter.svg" alt="CBR RAR5 Converter logo" width="128">
</p>

<h1 align="center">CBR RAR5 Converter</h1>

![release](https://img.shields.io/github/v/release/seguidodoblado/CBR-RAR5-Converter) ![license](https://img.shields.io/github/license/seguidodoblado/CBR-RAR5-Converter) ![last commit](https://img.shields.io/github/last-commit/seguidodoblado/CBR-RAR5-Converter) ![downloads](https://img.shields.io/github/downloads/seguidodoblado/CBR-RAR5-Converter/total) ![stars](https://img.shields.io/github/stars/seguidodoblado/CBR-RAR5-Converter?style=flat) ![issues](https://img.shields.io/github/issues/seguidodoblado/CBR-RAR5-Converter) ![language](https://img.shields.io/github/languages/top/seguidodoblado/CBR-RAR5-Converter)

<p align="center">
  Safely converts <code>.cbr</code> files in RAR4 format to RAR5, without modifying the originals.
</p>

<p align="center">
  <img src="docs/screenshot.png" alt="CBR RAR5 Converter screenshot">
</p>

Desktop application (GTK 4 + PyGObject, Spanish-language interface), for personal use: no server, no account,
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

## License

This project is distributed under the GNU General Public License, version 3 (see `LICENSE`).
