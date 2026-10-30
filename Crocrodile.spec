# -*- mode: python ; coding: utf-8 -*-
import glob
import os
from PyInstaller.utils.hooks import collect_all
block_cipher = None
datas = [
    ("book.bin", "."),
    ("basics_train.json", "."),
]
for f in glob.glob(os.path.join("nns", "0-*.csv")):
    datas.append((f, "nns"))
chess_datas, chess_binaries, chess_hidden = collect_all("chess")
datas += chess_datas
hidden = [
    "chess",
    "chess.polyglot",
    "chess.syzygy",
    "chess.engine",
    "numpy",
] + chess_hidden
a = Analysis(
    ["crocrodile_uci.py"],
    pathex=[],
    binaries=chess_binaries,
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib", "mpl_toolkits", "PIL", "scipy",
        "sphinx", "sphinx_rtd_theme", "docutils",
        "pytest", "_pytest", "nose",
        "tkinter", "Tkinter", "unittest",
        "email", "html", "http.server", "xmlrpc",
        "pydoc", "doctest",
        "berserk",
        "colorama",
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
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    optimize=2,
)
