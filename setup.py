from cx_Freeze import setup, Executable
import sys
import os

# Program neve és verziója
product_name = "TimeMeter"
version = "1.0"
main_script = "main.py"
icon_file = "icon.ico"

# Shortcut beállítások
shortcut_table = [
    (
        "DesktopShortcut",        # Shortcut identifier
        "DesktopFolder",          # Directory_
        product_name,             # Name
        "TARGETDIR",              # Component_
        f"[TARGETDIR]{main_script}",  # Target
        None,                     # Arguments
        f"Task tracking application",  # Description
        None, None, icon_file, None, None, None
    ),
    (
        "StartMenuShortcut",
        "StartMenuFolder",
        product_name,
        "TARGETDIR",
        f"[TARGETDIR]{main_script}",
        None,
        f"Task tracking application",
        None, None, icon_file, None, None, None
    )
]

# MSI telepítő beállításai
msi_data = {
    "Shortcut": shortcut_table
}

build_exe_options = {
    "packages": ["os", "sys", "markdown", "PySide6", "sklearn", "matplotlib"],
    "include_files": ["icon.ico", "config/", "notes/", "templates/"],
    "excludes": ["tkinter"],
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name=product_name,
    version=version,
    description="Task tracking application",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": {
            "data": msi_data
        }
    },
    executables=[
        Executable(main_script, base=base, icon=icon_file, target_name="TimeMeter.exe")
    ]
)
