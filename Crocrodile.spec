# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec optimizado para Crocrodile UCI en Windows 64-bit.
Uso: pyinstaller Crocrodile.spec  (o doble clic a build_windows.bat)
Resultado: dist/Crocrodile-UCI-Windows.exe  (~15-20 MB, un solo archivo)
"""
import glob
import os

block_cipher = None

# Datos que el motor abre con rutas relativas:
#   ./book.bin, basics_train.json, nns/0-*.csv
datas = [
    ("book.bin", "."),
    ("basics_train.json", "."),
]
# Solo la red 0 (la que carga EngineBase con load_layers(0)). ~400 KB.
# Si usas otra red, agrega sus CSV aqui.
for f in glob.glob(os.path.join("nns", "0-*.csv")):
    datas.append((f, "nns"))

a = Analysis(
    ["crocrodile_uci.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "chess",
        "chess.polyglot",
        "chess.syzygy",
        "numpy",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Recortan ~100+ MB del bundle:
        "matplotlib", "mpl_toolkits", "PIL", "scipy",
        "sphinx", "sphinx_rtd_theme", "docutils",
        "pytest", "_pytest", "nose",
        "tkinter", "Tkinter", "unittest",
        "email", "html", "http.server", "xmlrpc",
        "pydoc", "doctest",
        "berserk",  # solo se usa en modo lichess-bot, no en UCI
        "colorama",  # idem
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="Crocrodile-UCI-Windows",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,          # True si tienes MinGW/strip; en MSVC se deja False
    upx=True,             # Requiere UPX instalado; si no, PyInstaller lo ignora
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,         # OBLIGATORIO en True: UCI se comunica por consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    optimize=2,           # python -O -O: quita asserts y docstrings
)
