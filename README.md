<p align="right"><a href="README.en.md">🇺🇸 English</a></p>

<p align="center">
  <img src="cbr-rar5-converter.svg" alt="Logotipo de CBR RAR5 Converter" width="128">
</p>

<h1 align="center">CBR RAR5 Converter</h1>

![release](https://img.shields.io/github/v/release/seguidodoblado/CBR-RAR5-Converter) ![license](https://img.shields.io/github/license/seguidodoblado/CBR-RAR5-Converter)

<p align="center">
  Convierte de forma segura archivos <code>.cbr</code> en formato RAR4 al formato RAR5, sin modificar los
  originales.
</p>

<p align="center">
  <img src="docs/screenshot.png" alt="Captura de CBR RAR5 Converter">
</p>

Aplicación de escritorio (GTK 4 + PyGObject, interfaz en español), de uso personal: sin servidor ni cuenta,
todo ocurre en tu equipo.

- **Detecta** el formato de cada `.cbr` por su cabecera, no por la extensión.
- **Busca** archivos o carpetas completas, con opción de recorrer subcarpetas.
- **Convierte** de forma segura: temporal, validación de la cabecera RAR5 y sustitución atómica, sin
  sobrescribir destinos existentes.
- **No modifica los originales**: el resultado se guarda en una subcarpeta `Corregido`, preservando la ruta
  relativa.
- **Progreso por archivo y por lote** al convertir varios cómics a la vez.

## Documentación

Toda la documentación —instalación, guía de uso, especificaciones técnicas, solución de problemas y más— está en
la **[wiki del proyecto](https://github.com/seguidodoblado/CBR-RAR5-Converter/wiki)** (español e inglés).

## Licencia

Este proyecto se distribuye bajo la GNU General Public License, versión 3 (ver `LICENSE`).
