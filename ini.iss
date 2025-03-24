; TimeMeter Installer Script

[Setup]
AppName=TimeMeter
AppVersion=1.0
DefaultDirName={pf}\TimeMeter
DefaultGroupName=TimeMeter
UninstallDisplayIcon={app}\TimeMeter.exe
OutputDir=dist_installer
OutputBaseFilename=TimeMeter_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\TimeMeter\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "vcredist_x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Run]
Filename: "{tmp}\vcredist_x64.exe"; Parameters: "/quiet /norestart"; StatusMsg: "Telepítés: VC++ Redistributable..."

[Icons]
Name: "{group}\TimeMeter"; Filename: "{app}\TimeMeter.exe"
Name: "{group}\TimeMeter eltávolítása"; Filename: "{uninstallexe}"

[Fonts]
Source: "fonts\Roboto-Regular.ttf"; FontInstall: "Roboto"; Flags: onlyifdoesntexist uninsneveruninstall
