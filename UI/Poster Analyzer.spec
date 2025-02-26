# -*- mode: python ; coding: utf-8 -*-

libBin = "appdev/Library/bin/"

a = Analysis(
    ['Main.py'],
    pathex=[
		"C:/Users/Virus5600/miniconda3/Library/bin"
		"appdev/Lib/scripts"
		"/Controllers",
		"/Services"
	],
    binaries=[
		("C:/Users/Virus5600/miniconda3/Library/bin/liblzma.dll", libBin),
		("C:/Users/Virus5600/miniconda3/Library/bin/libbz2.dll", libBin),
		("C:/Users/Virus5600/miniconda3/Library/bin/ffi-8.dll", libBin),
		("C:/Users/Virus5600/miniconda3/Library/bin/tk86t.dll", libBin),
		("C:/Users/Virus5600/miniconda3/Library/bin/tcl86t.dll", libBin),
	],
    datas=[('assets', 'assets')],
    hiddenimports=['tkinter', 'Views.MainViewClass', 'Controllers.getEventHandlerController', 'Controllers.EventHandlerControllerClass'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='Poster Analyzer',
    debug=True,
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
    icon=['assets//icon.ico'],
)