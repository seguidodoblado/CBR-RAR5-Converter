# Changelog

## [Unreleased]

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
