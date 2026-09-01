from pathlib import Path
from .detector import detect_rar_format
from .discovery import find_cbr_files
from .planning import plan_conversion

def run_gui() -> None:
    try:
        import gi
        gi.require_version("Gtk", "4.0")
        from gi.repository import Gtk
    except (ImportError, ValueError) as error:
        raise RuntimeError("GTK 4/PyGObject no está instalado.") from error

    class Window(Gtk.ApplicationWindow):
        def __init__(self, app):
            super().__init__(application=app, title="CBR RAR5 Converter")
            self.set_default_size(950, 500); self.items = []
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
            controls = Gtk.Box(spacing=8); self.recursive = Gtk.CheckButton(label="Búsqueda recursiva")
            add = Gtk.Button(label="Añadir archivos"); folder = Gtk.Button(label="Añadir carpeta"); start = Gtk.Button(label="Preparar / iniciar")
            for widget in (add, folder, self.recursive, start): controls.append(widget)
            self.list = Gtk.StringList.new([])
            factory = Gtk.SignalListItemFactory()
            factory.connect("setup", lambda _, item: item.set_child(Gtk.Label(xalign=0)))
            factory.connect("bind", lambda _, item: item.get_child().set_text(item.get_item().get_string()))
            box.append(controls); box.append(Gtk.ListView(model=Gtk.SingleSelection(model=self.list), factory=factory)); self.set_child(box)
            add.connect("clicked", lambda _: self._add([Path.cwd()])); folder.connect("clicked", lambda _: self._add([Path.cwd()]))
        def _add(self, roots):
            for source in find_cbr_files(roots, self.recursive.get_active()):
                item = plan_conversion(source, detect_rar_format(source)); self.items.append(item)
                self.list.append(f"{source} | {item.format.value} | {item.status.value} | {item.destination}")
    class App(Gtk.Application):
        def do_activate(self): Window(self).present()
    App(application_id="com.example.CbrRar5Converter").run(None)
