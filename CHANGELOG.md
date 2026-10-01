# Changelog

## [Unreleased]

## [0.1.4] - 2026-10-01

### Añadido
- `README.en.md`: versión en inglés del README, con enlace de cambio de idioma en ambos.
- Archivos de comunidad: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md` y plantilla de Pull Request (`.github/PULL_REQUEST_TEMPLATE.md`), con el mismo contenido que en `comic-identify`.
- Logotipo y captura de pantalla en el README.

## [0.1.3] - 2026-09-30

### Cambiado
- Documentación reestructurada siguiendo la plantilla bilingüe (es/en) de `comic-identify`: la wiki del
  repositorio pasa a tener Home, `_Sidebar` y 9 páginas por idioma (descripción, interfaz, especificaciones
  técnicas, instalación, guía de uso, estructura de archivos, solución de problemas, glosario e historial de
  versiones), y el README se reduce a una presentación breve que enlaza a la wiki como documentación completa.

### Corregido
- `__version__` en `cbr_rar5_converter/__init__.py` estaba desincronizado (marcaba `0.1.0` desde hace dos
  versiones); ahora coincide con `pyproject.toml`.

## [0.1.2] - 2026-09-30

### Cambiado
- Desarrollo sin `venv`/`pip install`, sin ofrecer `pip` como alternativa, alineado con el flujo de `joseflix-request`, `telegraph-writer` y `comic-identify`. Se eliminan de `pyproject.toml` los extras `dev`/`gui` y la configuración de `ruff` (no empaquetado en Ubuntu/Mint), que quedaban ligados a ese flujo con pip.
- README: se elimina la sección separada "Instalación y ejecución en desarrollo"; la instalación y ejecución quedan cubiertas por "Construir e instalar el paquete DEB" (el usuario no teclea `python3` en ningún momento), y `python3 -m pytest` queda solo en "Comprobaciones" para quien desarrolle el núcleo.

## [0.1.1] - 2026-09-30

### Añadido
- `Recommends: rar` en el paquete DEB: el comando `rar` es necesario para la conversión real.
- Sección de requisitos en el README.

### Cambiado
- README actualizado al estado real: la conversión RAR4 → RAR5 (`rar x` + `rar a -ma5`) y las barras de progreso ya están implementadas.
- Instrucciones de desarrollo: el entorno virtual debe crearse con `--system-site-packages` para que `import gi` (PyGObject) funcione; se documenta el extra `gui`.
- Descripciones de `pyproject.toml`, `debian/control` y `build-deb.sh` reflejan la conversión, no solo la preparación.

## [0.1.0] - 2026-09-03

### Añadido
- Detección RAR4/RAR5 por cabecera, búsqueda de `.cbr` recursiva y exclusión de carpetas `Corregido`.
- Planificación de destinos preservando la ruta relativa bajo `Corregido`.
- Conversión con `rar`, validación de salida RAR5, sin sobrescribir y sustitución atómica.
- Interfaz GTK 4 en español con progreso por archivo y por lote.
- Empaquetado DEB con `build-deb.sh`.
