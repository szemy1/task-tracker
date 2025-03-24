import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# 🔥 KÉZZEL megadott elérési út a venv-es markdown mappához
markdown_path = os.path.abspath('venv/Lib/site-packages/markdown')

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('config/*', 'config'),
        ('icons/*', 'icons'),
        ('fonts/*', 'fonts'),
        (markdown_path, 'markdown')  # 🔥 TELJES KÖNYVTÁR MÁSOLÁSA
    ],
    hiddenimports=collect_submodules('markdown'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TimeMeter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='TimeMeter'
)
