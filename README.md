# CBR RAR5 Converter

Aplicación de escritorio para Linux Mint que convierte de forma segura archivos `.cbr` RAR4 a RAR5.

## Requisitos

- Python 3.10 o posterior.
- GTK 4 y PyGObject del sistema: `sudo apt install python3-gi gir1.2-gtk-4.0`.
- El comando `rar` (software propietario de RARLAB, paquete `rar` en Debian/Ubuntu/Mint) para la conversión real. Sin él, los elementos fallan con «No se encontró el comando 'rar'». El paquete DEB lo declara como `Recommends`, así que APT lo instala si está disponible en tus repositorios, pero la instalación no falla si falta.

## Funcionamiento

El núcleo detecta RAR4/RAR5 mediante cabecera, busca `.cbr`, excluye cualquier carpeta `Corregido` y planifica destinos. La planificación recursiva preserva la ruta relativa bajo `Corregido`. La GUI GTK4 está en español y muestra archivo, formato, estado y destino, con barras de progreso del archivo actual y del lote.

Solo se convierten los archivos RAR4; el resto se omite. `RarConverter` extrae el original con `rar x` a un directorio temporal y lo vuelve a empaquetar con `rar a -ma5`. `ConversionService` (encapsulado e inyectable) trabaja sobre un temporal junto al destino, valida que la salida tenga cabecera RAR5, evita sobrescribir destinos existentes y realiza la sustitución atómica. Los originales no se modifican.

La cola, los modelos de estado y los puntos de extensión dejan preparada la evolución hacia drag & drop, Nemo y logging.

## Comprobaciones

```bash
sudo apt install python3-pytest
python3 -m pytest
```

`ruff` no está empaquetado para Ubuntu/Mint, así que el lint no forma parte del flujo estándar de este proyecto.

## Construir e instalar el paquete DEB

El flujo sigue el patrón de `joseflix-request` y `telegraph-writer`: empaquetado directo con `dpkg-deb`, aplicación e icono fuente en `/opt/cbr-rar5-converter`, lanzador en `/usr/bin`, icono registrado en `hicolor` y entrada de menú/panel.

```bash
chmod +x build-deb.sh
./build-deb.sh
sudo apt install ../cbr-rar5-converter_0.1.2_all.deb
```

El paquete depende de `python3-gi` y `gir1.2-gtk-4.0`, que se instalan automáticamente mediante APT, y recomienda `rar`, necesario para convertir.

Si el icono no aparece tras actualizar una instalación anterior, reinstala el paquete para ejecutar el refresco de caché:

```bash
sudo apt install --reinstall ../cbr-rar5-converter_0.1.2_all.deb
```

La entrada de escritorio incluye `StartupWMClass` coincidente con el identificador GTK de la aplicación para que el panel del sistema no la agrupe como `python3`.
