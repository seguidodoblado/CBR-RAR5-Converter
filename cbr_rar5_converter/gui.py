"""Interfaz GTK4; coordina la selección y presenta el dominio."""
from pathlib import Path
from threading import Event, Thread
from .detector import detect_rar_format
from .discovery import find_cbr_files
from .planning import plan_conversion
from .conversion import ConversionService

def run_gui() -> None:
    try:
        import gi
        gi.require_version("Gtk", "4.0")
        from gi.repository import Gdk, Gtk
    except (ImportError, ValueError) as error:
        raise RuntimeError("GTK 4/PyGObject no está instalado.") from error

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
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
            controls = Gtk.Box(spacing=8)
            self.add_files_button = Gtk.Button(label="Añadir archivos")
            self.add_folder_button = Gtk.Button(label="Añadir carpeta")
            self.recursive = Gtk.CheckButton(label="Buscar subcarpetas")
            self.start_button = Gtk.Button(label="Preparar / iniciar")
            for widget in (self.add_files_button, self.add_folder_button, self.recursive, self.start_button): controls.append(widget)
            self.info = Gtk.Label(label="Añade uno o varios archivos CBR, o una carpeta completa.", xalign=0)
            self.file_progress = Gtk.ProgressBar(show_text=True)
            self.batch_progress = Gtk.ProgressBar(show_text=True)
            for progress in (self.file_progress, self.batch_progress):
                progress.set_hexpand(True)
                progress.set_size_request(500, 28)
            self.file_progress.set_text("Archivo actual")
            self.batch_progress.set_text("Progreso del lote")
            self.list = Gtk.StringList.new([])
            factory = Gtk.SignalListItemFactory()
            # La ruta completa debe seguir siendo consultable mediante scroll horizontal.
            factory.connect("setup", lambda _, row: row.set_child(Gtk.Label(xalign=0, margin_top=5, margin_bottom=5)))
            factory.connect("bind", lambda _, row: row.get_child().set_text(row.get_item().get_string()))
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

        @staticmethod
        def _dialog():
            return Gtk.FileDialog(title="Seleccionar archivos CBR")

        def _choose_files(self, _button):
            self._dialog().open_multiple(self, None, self._files_chosen)

        def _files_chosen(self, dialog, result):
            try:
                files = dialog.open_multiple_finish(result)
                paths = [files.get_item(i).get_path() for i in range(files.get_n_items())]
            except Exception as error:
                self.info.set_text(f"Selección cancelada o fallida: {error}"); return
            self._add_paths(paths)

        def _choose_folder(self, _button):
            self._dialog().select_folder(self, None, self._folder_chosen)

        def _folder_chosen(self, dialog, result):
            try:
                folder = dialog.select_folder_finish(result)
            except Exception as error:
                self.info.set_text(f"Selección cancelada o fallida: {error}"); return
            self._add_paths([folder.get_path()])

        def _add_paths(self, paths):
            added = 0
            for path in find_cbr_files([Path(path) for path in paths], self.recursive.get_active()):
                path = path.resolve()
                if path in self.sources: continue
                item = plan_conversion(path, detect_rar_format(path))
                self.sources.add(path); self.items.append(item)
                self.list.append(f"Archivo: {path} | Formato: {item.format.value} | Estado: {item.status.value} | Destino: {item.destination}")
                added += 1
            self._update_summary(added)

        def _prepare(self, _button):
            ready_items = [item for item in self.items if item.status.value == "Preparado"]
            if not ready_items:
                self.info.set_text("No hay archivos RAR4 preparados para convertir."); return
            self.start_button.set_sensitive(False)
            self.info.set_text(f"Iniciando lote de {len(ready_items)} archivo(s)…")
            Thread(target=self._run_batch, args=(ready_items,), daemon=True).start()

        def _run_batch(self, items):
            import gi
            from gi.repository import GLib
            for index, item in enumerate(items, 1):
                def update(value, current=index, total=len(items)):
                    GLib.idle_add(self.file_progress.set_fraction, value / 100)
                    GLib.idle_add(self.file_progress.set_text, f"Archivo {current}/{total}: {value}%")
                    GLib.idle_add(self.batch_progress.set_fraction, (index - 1 + value / 100) / total)
                ConversionService(progress=update).convert(item)
                GLib.idle_add(self._refresh_row, index - 1, item)
            GLib.idle_add(self._batch_done)

        def _refresh_row(self, index, item):
            self.list.splice(index, 1, [f"Archivo: {item.source} | Formato: {item.format.value} | Estado: {item.status.value} | Destino: {item.destination}"])

        def _batch_done(self):
            self.start_button.set_sensitive(True)
            self._update_summary()
            self.info.set_text(self.info.get_text() + " Lote finalizado.")

        def _update_summary(self, added=0):
            total = len(self.items)
            ready = sum(item.status.value == "Preparado" for item in self.items)
            skipped = sum(item.status.value == "Omitido" for item in self.items)
            errors = sum(item.status.value == "Error" for item in self.items)
            suffix = f"; {added} añadido(s) en esta selección" if added else ""
            message = f"{total} archivo(s) en la lista: {ready} preparado(s), {skipped} omitido(s)"
            if errors:
                message += f", {errors} con error"
            self.info.set_text(message + suffix + ".")

    class App(Gtk.Application):
        def do_activate(self): Window(self).present()
    App(application_id="com.example.CbrRar5Converter").run(None)
