# CBR RAR5 Converter

Primera fase de una aplicación de escritorio para Linux Mint que prepara la conversión segura de archivos `.cbr` RAR4 a RAR5.

## Instalación y ejecución

Requiere Python 3.10 o posterior:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Para la interfaz, instala las dependencias del sistema GTK 4/PyGObject de tu distribución y el extra `gui` cuando esté disponible. Ejecuta:

```bash
cbr-rar5-converter
# o: python -m cbr_rar5_converter
```

## Estado actual

El núcleo detecta RAR4/RAR5 mediante cabecera, busca `.cbr`, excluye cualquier carpeta `Corregido` y planifica destinos. La planificación recursiva preserva la ruta relativa bajo `Corregido`. La GUI GTK4 inicial está en español y muestra archivo, formato, estado y destino.

`ConversionService` está encapsulado e inyectable: usa temporal, valida que la salida sea RAR5, evita sobrescribir destinos y realiza sustitución atómica. El backend de conversión real queda pendiente; mientras tanto los elementos se mantienen como preparados sin modificar originales.

La cola, los modelos de estado y los puntos de extensión dejan preparada la evolución hacia progreso, cancelación, drag & drop, Nemo y logging.

## Comprobaciones

Ejecuta `pytest` para las pruebas unitarias y `ruff check .` para estilo. En este entorno esas herramientas no estaban instaladas; la sintaxis del paquete se comprobó con `python -m compileall`.

## Construir e instalar el paquete DEB

El flujo sigue el patrón de `joseflix-request` y `telegraph-writer`: empaquetado directo con `dpkg-deb`, aplicación e icono fuente en `/opt/cbr-rar5-converter`, lanzador en `/usr/bin`, icono registrado en `hicolor` y entrada de menú/panel.

```bash
chmod +x build-deb.sh
./build-deb.sh
sudo apt install ../cbr-rar5-converter_0.1.0_all.deb
```

El paquete depende de `python3-gi` y `gir1.2-gtk-4.0`, que se instalan automáticamente mediante APT.

Si el icono no aparece tras actualizar una instalación anterior, reinstala el paquete para ejecutar el refresco de caché:

```bash
sudo apt install --reinstall ../cbr-rar5-converter_0.1.0_all.deb
```

La entrada de escritorio incluye `StartupWMClass` coincidente con el identificador GTK de la aplicación para que el panel del sistema no la agrupe como `python3`.
