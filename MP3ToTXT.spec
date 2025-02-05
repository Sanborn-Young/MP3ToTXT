# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
import speechbrain
import os

# Collect non‐Python data files from lightning_fabric (e.g. version.info)
lightning_datas = collect_data_files("lightning_fabric", include_py_files=False)

# Collect the entire "utils" folder from speechbrain
speechbrain_utils_datas = collect_data_files("speechbrain", subdir="utils", include_py_files=True)

# Collect the entire "dataio" folder from speechbrain
speechbrain_dataio_datas = collect_data_files("speechbrain", subdir="dataio", include_py_files=True)

a = Analysis(
    ['MP3ToTXT.py'],
    pathex=[],
    binaries=[('resources/ffmpeg.exe', 'resources')],
    # Combine the collected data so that both "utils" and "dataio" (plus lightning_fabric)
    # are present in the bundle.
    datas = lightning_datas + speechbrain_utils_datas + speechbrain_dataio_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MP3ToTXT',
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
    icon=['icon.ico'],
)
