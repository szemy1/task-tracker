; TimeMeter – Inno Setup telepítő script

[Setup]
AppName=TimeMeter
AppVersion=1.0
DefaultDirName={pf}\TimeMeter
DefaultGroupName=TimeMeter
UninstallDisplayIcon={app}\TimeMeter.exe
Compression=lzma
SolidCompression=yes
OutputBaseFilename=TimeMeter_Installer
OutputDir=dist_installer
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
SetupIconFile=icon.ico

[Files]
Source: "dist\TimeMeter\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

; Opcionális: VC++ Runtime telepítés
; Source: "redist\vcredist_x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
; 
; [Run]
; Filename: "{tmp}\vcredist_x64.exe"; Parameters: "/quiet /norestart"; StatusMsg: "Telepítés: Visual C++ Redistributable..."

[Icons]
Name: "{group}\TimeMeter"; Filename: "{app}\TimeMeter.exe"
Name: "{group}\Eltávolítás - TimeMeter"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\TimeMeter.exe"; Description: "TimeMeter indítása"; Flags: nowait postinstall skipifsilent
