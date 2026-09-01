#!/bin/sh
set -eu
base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
stage="$base/.deb-stage"
version=$(sed -n 's/^version = "\([^"]*\)"/\1/p' "$base/pyproject.toml")
package="$base/../cbr-rar5-converter_${version}_all.deb"
command -v dpkg-deb >/dev/null 2>&1 || { echo "Falta dpkg-deb (instala dpkg-dev)." >&2; exit 1; }
rm -rf "$stage"
mkdir -p "$stage/DEBIAN" "$stage/usr/share/cbr-rar5-converter" "$stage/usr/bin" "$stage/usr/share/applications" "$stage/usr/share/icons/hicolor/scalable/apps"
cp -a "$base/cbr_rar5_converter" "$stage/usr/share/cbr-rar5-converter/"
find "$stage/usr/share/cbr-rar5-converter" -type d -name __pycache__ -prune -exec rm -rf {} +
cp "$base/debian/cbr-rar5-converter-launcher" "$stage/usr/bin/cbr-rar5-converter"
cp "$base/debian/cbr-rar5-converter.desktop" "$stage/usr/share/applications/"
cp "$base/cbr-rar5-converter.svg" "$stage/usr/share/icons/hicolor/scalable/apps/"
cat > "$stage/DEBIAN/control" <<EOF
Package: cbr-rar5-converter
Version: ${version}-1
Section: graphics
Priority: optional
Architecture: all
Depends: python3, python3-gi, gir1.2-gtk-4.0
Maintainer: CBR RAR5 Converter <localhost>
Description: Conversor seguro de archivos CBR RAR4 a RAR5
 Aplicación GTK para detectar y preparar conversiones sin modificar originales.
EOF
chmod 755 "$stage/usr/bin/cbr-rar5-converter"
dpkg-deb --build --root-owner-group "$stage" "$package"
echo "Paquete generado: $package"
