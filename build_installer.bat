@echo off
echo ===========================================
echo TimeMeter - MSI telepítő készítése
echo ===========================================

REM --- Lépjünk a script könyvtárába
cd /d %~dp0

REM --- Régi build törlése
echo 🧹 Régi build és dist mappák törlése...
rmdir /s /q build
rmdir /s /q dist

REM --- cx_Freeze build futtatása
echo 🚧 Telepítő buildelése...
python setup.py bdist_msi

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Hiba történt a build során!
    pause
    exit /b 1
)

echo ✅ MSI fájl létrehozva a dist mappában!
start dist
pause
