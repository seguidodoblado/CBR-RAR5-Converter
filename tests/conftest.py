import os

# Las pruebas comprueban los textos en español (el idioma fuente), vengan los .mo compilados o no:
# se fija antes de importar nada del paquete.
os.environ["LANGUAGE"] = "es"
