<p align="right"><a href="PRIVACY.md">🇪🇸 Español</a></p>

# Privacy Policy

Last updated: October 5, 2026.

CBR RAR5 Converter is a desktop application for personal use. It has no server or account of its own, does
not connect to the Internet, and its author does not receive any data from the people who use it.

## What data it handles

- **Your `.cbr` files:** the application reads their header to know whether they are RAR4 or RAR5 and, when
  converting, the `rar` program extracts them to a temporary folder and builds a new file from them. The
  originals are not modified.
- **The paths** of the folders and files you choose, which are only shown in the window.
- **Your settings:** the interface language.

## Where it is stored

Everything stays on your computer:

- The converted files, in a `Corregido` folder next to the originals.
- The conversion's temporary files, which are deleted when it finishes.
- The chosen language, in `~/.config/cbr-rar5-converter/settings.json`.

The application keeps no history of files or paths.

## Who it is shared with

No one. It includes no analytics, telemetry, advertising or third-party services, and it makes no network
requests.

## How to delete your data

Remove `~/.config/cbr-rar5-converter/` and any `Corregido` folders you no longer want. Uninstalling the
application does not delete that data by itself.

## Changes to this policy

If it changes, this document and the date above will be updated; the history is in the repository.

## Contact

Jose Antonio Seguido Doblado · jose.antonio.seguido@gmail.com
