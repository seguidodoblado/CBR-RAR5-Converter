#!/bin/sh
set -eu
base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
stage="$base/.deb-stage"
version=$(sed -n '1s/^[^ ]* (\([^)]*\)).*/\1/p' "$base/debian/changelog")
test -n "$version" || { echo "No se pudo leer la versión de debian/changelog" >&2; exit 1; }
upstream=${version%-*}
project_version=$(sed -n 's/^version = "\([^"]*\)"/\1/p' "$base/pyproject.toml")
init_version=$(sed -n 's/^__version__ = "\([^"]*\)"/\1/p' "$base/src/cbr_rar5_converter/__init__.py")
test "$upstream" = "$project_version" -a "$upstream" = "$init_version" || {
    echo "Versiones distintas: debian/changelog ($upstream), pyproject.toml ($project_version), __init__.py ($init_version)." >&2
    exit 1
}
package="$base/../cbr-rar5-converter_${version}_all.deb"
command -v dpkg-deb >/dev/null 2>&1 || { echo "Falta dpkg-deb (instala dpkg-dev)." >&2; exit 1; }
sh "$base/i18n-compile.sh"
rm -rf "$stage"
doc="$stage/usr/share/doc/cbr-rar5-converter"
mkdir -p "$stage/DEBIAN" "$stage/usr/share/cbr-rar5-converter" "$stage/usr/bin" "$stage/usr/share/applications" "$stage/usr/share/icons/hicolor/scalable/apps" "$doc"
cp -a "$base/src/cbr_rar5_converter" "$stage/usr/share/cbr-rar5-converter/"
find "$stage/usr/share/cbr-rar5-converter" -type d -name __pycache__ -prune -exec rm -rf {} +
cp "$base/debian/cbr-rar5-converter-launcher" "$stage/usr/bin/cbr-rar5-converter"
cp "$base/debian/cbr-rar5-converter.desktop" "$stage/usr/share/applications/"
cp "$base/cbr-rar5-converter.svg" "$stage/usr/share/icons/hicolor/scalable/apps/"
cp "$base/debian/copyright" "$doc/copyright"
gzip -9n -c "$base/debian/changelog" > "$doc/changelog.Debian.gz"
# Páginas de manual (inglés en man1, español en es/man1); la versión se rellena aquí
mkdir -p "$stage/usr/share/man/man1" "$stage/usr/share/man/es/man1"
sed "s/@VERSION@/${version}/" "$base/debian/cbr-rar5-converter.1" | gzip -9n > "$stage/usr/share/man/man1/cbr-rar5-converter.1.gz"
sed "s/@VERSION@/${version}/" "$base/debian/cbr-rar5-converter.es.1" | gzip -9n > "$stage/usr/share/man/es/man1/cbr-rar5-converter.1.gz"
cp "$base/debian/postinst" "$stage/DEBIAN/postinst"
# Permisos fijos (no dependen de la umask de quien construye): 755 en directorios, 644 en ficheros
find "$stage" -type d -exec chmod 755 {} +
find "$stage" -type f -exec chmod 644 {} +
cat > "$stage/DEBIAN/control" <<EOF
Package: cbr-rar5-converter
Version: ${version}
Section: graphics
Priority: optional
Architecture: all
Depends: python3, python3-gi, gir1.2-gtk-4.0
Recommends: rar
Maintainer: Jose Antonio Seguido Doblado <jose.antonio.seguido@gmail.com>
Homepage: https://github.com/seguidodoblado/CBR-RAR5-Converter
Description: Conversor seguro de archivos CBR RAR4 a RAR5
 Aplicación GTK para detectar y convertir archivos RAR4 a RAR5 sin
 modificar los originales.
EOF
chmod 644 "$stage/DEBIAN/control"
chmod 755 "$stage/usr/bin/cbr-rar5-converter"
chmod 755 "$stage/DEBIAN/postinst"
(cd "$stage" && find . -type f ! -path './DEBIAN/*' -printf '%P\n' | LC_ALL=C sort | xargs -d '\n' md5sum > DEBIAN/md5sums)
chmod 644 "$stage/DEBIAN/md5sums"
dpkg-deb --build --root-owner-group "$stage" "$package"
rm -rf "$stage"
echo "Paquete generado: $package"
