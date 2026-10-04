# Changelog

## [Unreleased]

## [0.2.0] - 2026-10-05

### Añadido
- **Interfaz en español e inglés** (`gettext`): el español es el idioma fuente y el inglés está en `po/en.po`. Se elige en el nuevo menú de la cabecera → **Preferencias** (Sistema, Español o English; reinicia la aplicación). Con «Sistema» se usa el idioma del escritorio o `$LANGUAGE`
- Menú de la cabecera con **Preferencias** y **Acerca de** (ventana estándar de GNOME: licencia GPL-3.0 o posterior predefinida de GTK, autor con enlace al correo y créditos de traducción)
- `ruff` y más pruebas (de 3 a 28): conversión, cola, progreso y cancelación de `rar`, ajustes, traducciones
- Integración continua (`ci.yml`: ruff, pytest y `.deb` con lintian) y despliegue (`cd.yml`: al subir una etiqueta `vX.Y.Z` ejecuta el CI y, solo si pasa, deja la release en borrador con el mismo `.deb` que construyó el CI)
- `PRIVACY.md` y `PRIVACY.en.md` (política de privacidad), y versión en inglés de `CONTRIBUTING`, `SECURITY` y `SUPPORT`, con selector de idioma

### Cambiado
- La licencia pasa a **GPL-3.0 o posterior** (antes, solo versión 3), como en el resto de proyectos: `debian/copyright` (GPL-3+), `pyproject.toml`, README y «Acerca de»
- El código pasa a `src/cbr_rar5_converter/`, con la interfaz en su propio paquete `ui/`
- Empaquetado conforme a Debian: la aplicación se instala en `/usr/share/cbr-rar5-converter` (antes en `/opt/cbr-rar5-converter`), con `copyright`, `changelog.Debian.gz`, páginas de manual en inglés y español y `md5sums`; el `.deb` pasa lintian sin errores. La versión del paquete sale ahora de `debian/changelog` (`0.1.4-1`)
- Los estados y formatos se comparan por su valor estable y no por su texto, para no depender del idioma
- El progreso de cada archivo del lote deja de depender de la variable del bucle (aviso B023 de `ruff`); el comportamiento no cambia
- Los badges del README se ordenan según el estándar de los demás proyectos y se corrige el cierre de su bloque HTML

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
