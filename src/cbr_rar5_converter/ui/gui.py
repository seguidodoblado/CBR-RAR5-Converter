"""Interfaz GTK4; coordina la selección y presenta el dominio."""
from pathlib import Path
from threading import Thread

from .. import __version__
from ..conversion import ConversionService
from ..detector import detect_rar_format
from ..discovery import find_cbr_files
from ..i18n import _
from ..models import ConversionStatus
from ..planning import plan_conversion

AUTHOR = "Jose Antonio Seguido Doblado"
AUTHOR_EMAIL = "jose.antonio.seguido@gmail.com"
REPO_URL = "https://github.com/seguidodoblado/CBR-RAR5-Converter"


def row_text(item) -> str:
    """La línea de la lista de un archivo, con el formato y el estado en el idioma del usuario."""
    return _("Archivo: {path} | Formato: {format} | Estado: {status} | Destino: {destination}").format(
        path=item.source, format=item.format.label, status=item.status.label, destination=item.destination)


def run_gui() -> None:
    try:
        import gi
        gi.require_version("Gtk", "4.0")
        from gi.repository import Gdk, Gio, Gtk
    except (ImportError, ValueError) as error:
        raise RuntimeError(_("GTK 4/PyGObject no está instalado.")) from error

    css = Gtk.CssProvider()
    css.load_from_data(b"progressbar trough { min-height: 28px; } progressbar progress { min-height: 28px; }")
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    class Window(Gtk.ApplicationWindow):
        def __init__(self, app):
            super().__init__(application=app, title="CBR RAR5 Converter")
            self.set_default_size(1100, 600)
            self.set_resizable(True)
            self.set_decorated(True)
            self.items, self.sources = [], set()
            self.converting = False
            header = Gtk.HeaderBar()
            header.pack_end(self._build_menu_button())
            self.set_titlebar(header)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
            controls = Gtk.Box(spacing=8)
            self.add_files_button = Gtk.Button(label=_("Añadir archivos"))
            self.add_folder_button = Gtk.Button(label=_("Añadir carpeta"))
            self.recursive = Gtk.CheckButton(label=_("Buscar subcarpetas"))
            self.start_button = Gtk.Button(label=_("Preparar / iniciar"))
            for widget in (self.add_files_button, self.add_folder_button, self.recursive, self.start_button): controls.append(widget)
            self.info = Gtk.Label(label=_("Añade uno o varios archivos CBR, o una carpeta completa."), xalign=0)
            self.file_progress = Gtk.ProgressBar(show_text=True)
            self.batch_progress = Gtk.ProgressBar(show_text=True)
            for progress in (self.file_progress, self.batch_progress):
                progress.set_hexpand(True)
                progress.set_size_request(500, 28)
            self.file_progress.set_text(_("Archivo actual"))
            self.batch_progress.set_text(_("Progreso del lote"))
            self.list = Gtk.StringList.new([])
            factory = Gtk.SignalListItemFactory()
            # La ruta completa debe seguir siendo consultable mediante scroll horizontal.
            factory.connect("setup", lambda _factory, row: row.set_child(Gtk.Label(xalign=0, margin_top=5, margin_bottom=5)))
            factory.connect("bind", lambda _factory, row: row.get_child().set_text(row.get_item().get_string()))
            view = Gtk.ListView(model=Gtk.SingleSelection(model=self.list), factory=factory)
            view.set_vexpand(True)
            scroll = Gtk.ScrolledWindow()
            scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            scroll.set_min_content_height(300)
            scroll.set_vexpand(True)
            scroll.set_child(view)
            box.append(controls); box.append(self.info)
            box.append(self.file_progress); box.append(self.batch_progress)
            box.append(scroll); self.set_child(box)
            self.add_files_button.connect("clicked", self._choose_files)
            self.add_folder_button.connect("clicked", self._choose_folder)
            self.start_button.connect("clicked", self._prepare)

        def _build_menu_button(self):
            # Botones con icono del sistema (simbólico, con el normal como alternativa) y etiqueta
            popover = Gtk.Popover()
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2, margin_start=6, margin_end=6,
                          margin_top=6, margin_bottom=6)
            entries = ((_("Preferencias"), ("preferences-system-symbolic", "preferences-system"), self._open_preferences),
                       (_("Acerca de CBR RAR5 Converter"), ("help-about-symbolic", "help-about"), self._open_about))
            for label, icon_names, callback in entries:
                item = Gtk.Button(halign=Gtk.Align.FILL)
                content = Gtk.Box(spacing=8)
                content.append(Gtk.Image.new_from_gicon(Gio.ThemedIcon.new_from_names(list(icon_names))))
                content.append(Gtk.Label(label=label, xalign=0))
                item.set_child(content)
                item.connect("clicked", lambda _b, fn=callback: (popover.popdown(), fn()))
                box.append(item)
            popover.set_child(box)
            menu = Gtk.MenuButton(icon_name="open-menu-symbolic", tooltip_text=_("Menú principal"))
            menu.set_popover(popover)
            return menu

        def _open_preferences(self):
            from .preferences import PreferencesWindow
            PreferencesWindow(self.get_application(), self.converting).present()

        def _open_about(self):
            about = Gtk.AboutDialog(
                transient_for=self, modal=True, program_name="CBR RAR5 Converter", version=__version__,
                logo_icon_name="cbr-rar5-converter",
                comments=_("Convierte de forma segura archivos CBR en formato RAR4 al formato RAR5, "
                           "sin modificar los originales."),
                website=REPO_URL, website_label=REPO_URL.removeprefix("https://"),
                authors=[f"{AUTHOR} <{AUTHOR_EMAIL}>"], copyright=f"© 2026 {AUTHOR}",
                license_type=Gtk.License.GPL_3_0_ONLY, translator_credits=_("translator-credits"))
            about.present()

        @staticmethod
        def _dialog():
            return Gtk.FileDialog(title=_("Seleccionar archivos CBR"))

        def _choose_files(self, _button):
            self._dialog().open_multiple(self, None, self._files_chosen)

        def _files_chosen(self, dialog, result):
            try:
                files = dialog.open_multiple_finish(result)
                paths = [files.get_item(i).get_path() for i in range(files.get_n_items())]
            except Exception as error:  # noqa: BLE001 - cancelar el diálogo o un fallo de GLib no debe cerrar la app
                self.info.set_text(_("Selección cancelada o fallida: {error}").format(error=error)); return
            self._add_paths(paths)

        def _choose_folder(self, _button):
            self._dialog().select_folder(self, None, self._folder_chosen)

        def _folder_chosen(self, dialog, result):
            try:
                folder = dialog.select_folder_finish(result)
            except Exception as error:  # noqa: BLE001 - cancelar el diálogo o un fallo de GLib no debe cerrar la app
                self.info.set_text(_("Selección cancelada o fallida: {error}").format(error=error)); return
            self._add_paths([folder.get_path()])

        def _add_paths(self, paths):
            added = 0
            for path in find_cbr_files([Path(path) for path in paths], self.recursive.get_active()):
                path = path.resolve()
                if path in self.sources: continue
                item = plan_conversion(path, detect_rar_format(path))
                self.sources.add(path); self.items.append(item)
                self.list.append(row_text(item))
                added += 1
            self._update_summary(added)

        def _prepare(self, _button):
            ready_items = [item for item in self.items if item.status is ConversionStatus.READY]
            if not ready_items:
                self.info.set_text(_("No hay archivos RAR4 preparados para convertir.")); return
            self.start_button.set_sensitive(False)
            self.converting = True
            self.info.set_text(_("Iniciando lote de {count} archivo(s)…").format(count=len(ready_items)))
            Thread(target=self._run_batch, args=(ready_items,), daemon=True).start()

        def _run_batch(self, items):
            from gi.repository import GLib
            total = len(items)

            def progress_for(index):
                def update(value):
                    GLib.idle_add(self.file_progress.set_fraction, value / 100)
                    GLib.idle_add(self.file_progress.set_text, _("Archivo {index}/{total}: {value}%").format(index=index, total=total, value=value))
                    GLib.idle_add(self.batch_progress.set_fraction, (index - 1 + value / 100) / total)
                return update

            for index, item in enumerate(items, 1):
                ConversionService(progress=progress_for(index)).convert(item)
                GLib.idle_add(self._refresh_row, index - 1, item)
            GLib.idle_add(self._batch_done)

        def _refresh_row(self, index, item):
            self.list.splice(index, 1, [row_text(item)])

        def _batch_done(self):
            self.start_button.set_sensitive(True)
            self.converting = False
            self._update_summary()
            self.info.set_text(self.info.get_text() + " " + _("Lote finalizado."))

        def _update_summary(self, added=0):
            total = len(self.items)
            ready = sum(item.status is ConversionStatus.READY for item in self.items)
            skipped = sum(item.status is ConversionStatus.SKIPPED for item in self.items)
            errors = sum(item.status is ConversionStatus.FAILED for item in self.items)
            suffix = _("; {added} añadido(s) en esta selección").format(added=added) if added else ""
            message = _("{total} archivo(s) en la lista: {ready} preparado(s), {skipped} omitido(s)").format(
                total=total, ready=ready, skipped=skipped)
            if errors:
                message += _(", {errors} con error").format(errors=errors)
            self.info.set_text(message + suffix + ".")

    class App(Gtk.Application):
        def do_activate(self): Window(self).present()
    App(application_id="com.example.CbrRar5Converter").run(None)
