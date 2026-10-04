"""Ventana de Preferencias: idioma y tema, guardados en ~/.config/cbr-rar5-converter/settings.json."""
import subprocess

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import settings
from ..i18n import _

# Los nombres de idioma no se traducen (convención habitual en selectores de idioma):
# «English» se ve igual con la app en español, y viceversa.
LANGUAGE_CODES: list[str | None] = [None, "es", "en"]
THEME_VALUES: list[bool | None] = [None, False, True]   # Sistema, Claro, Oscuro (valor de dark_mode)


def language_labels() -> list[str]:
    return [_("Sistema"), "Español", "English"]


class PreferencesWindow(Gtk.Window):
    """Idioma y tema se aplican reiniciando la aplicación: los textos ya están fijados en los widgets y, en
    Cinnamon/Mint, cambiar gtk-theme-name en caliente no repinta la ventana."""

    def __init__(self, application: Gtk.Application, busy: bool) -> None:
        super().__init__(title=_("Preferencias"), transient_for=application.props.active_window,
                         modal=True, resizable=False)
        self._application = application
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_top=16,
                      margin_bottom=16, margin_start=16, margin_end=16)
        self.set_child(box)

        box.append(Gtk.Label(label=_("Idioma"), xalign=0))
        self._language = Gtk.DropDown.new_from_strings(language_labels())
        current = settings.language()
        self._language.set_selected(LANGUAGE_CODES.index(current))
        box.append(self._language)

        box.append(Gtk.Label(label=_("Tema"), xalign=0))
        self._theme = Gtk.DropDown.new_from_strings([_("Sistema"), _("Claro"), _("Oscuro")])
        self._theme.set_selected(THEME_VALUES.index(settings.dark_mode()))
        box.append(self._theme)

        hint = Gtk.Label(label=_("Los cambios se aplican reiniciando la aplicación."), xalign=0, wrap=True)
        hint.add_css_class("dim-label")
        box.append(hint)

        apply_button = Gtk.Button(label=_("Aplicar y reiniciar"))
        apply_button.add_css_class("suggested-action")
        apply_button.connect("clicked", self._on_apply)
        box.append(apply_button)
        if busy:
            # Reiniciar interrumpiría la conversión en curso
            apply_button.set_sensitive(False)
            hint.set_text(_("Hay una conversión en marcha: espera a que termine para cambiar el idioma o el tema."))

    def _on_apply(self, _button: Gtk.Button) -> None:
        config = settings.read_settings()
        config["language"] = LANGUAGE_CODES[self._language.get_selected()]
        config["dark_mode"] = THEME_VALUES[self._theme.get_selected()]
        settings.write_settings(config)
        # Un exec en el sitio conservaría los descriptores abiertos (y con ellos el registro D-Bus de
        # esta instancia): el proceso nuevo se vería como secundario y se cerraría sin ventana. Se
        # lanza un proceso aparte y se cierra este. El ejecutable se toma de /proc/self/exe, no de
        # sys.executable, porque el lanzador instalado usa «exec -a» y eso engaña a sys.executable.
        subprocess.Popen(["/proc/self/exe", "-m", "cbr_rar5_converter"], start_new_session=True)
        self._application.quit()
