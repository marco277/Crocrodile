#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crocrodile UCI - Punto de entrada optimizado para .exe Windows.

- Corrige rutas cuando corre como ejecutable PyInstaller (sys._MEIPASS).
- Silencia los prints ruidosos del __init__ original (rompen el protocolo UCI).
- Mantiene consola (UCI la necesita).
"""
import os
import sys

def _base_dir():
    # Cuando PyInstaller --onefile corre, los datos estan en sys._MEIPASS
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE = _base_dir()

# Los datos (book.bin, basics_train.json, nns/) estan junto al .py o dentro del bundle.
# Cambiamos cwd ahi para que las rutas relativas originales ("./book.bin", "nns/...") funcionen.
try:
    if os.path.isdir(BASE):
        os.chdir(BASE)
except Exception:
    pass

# Acelerar inicio: no cargar matplotlib/sphinx aunque esten instalados
for _mod in ("matplotlib", "sphinx", "pytest", "tkinter"):
    sys.modules.pop(_mod, None)

import io
import contextlib

# Los print() a nivel de modulo del paquete original (os.getcwd, sys.path)
# tambien contaminan el protocolo UCI: se importan con stdout silenciado.
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    from crocrodile.uci import UCI

def main():
    # El __init__ original hace: print(os.getcwd()), print(sys.path),
    # print(name, author). Eso contamina el protocolo UCI y rompe GUIs
    # (Arena, Cutechess, etc.). Lo silenciamos, el loop UCI sigue intacto.
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        uci = UCI()
    uci.run()

if __name__ == "__main__":
    main()
