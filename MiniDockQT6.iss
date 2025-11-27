; Script de ejemplo para Inno Setup (no compilado aún)
; Abre este archivo con Inno Setup (iscc) para generar el instalador.

[Setup]
AppName=MiniDockQT6
AppVersion=1.0.0
AppPublisher=Tu Nombre
DefaultDirName={autopf}\\MiniDockQT6
DefaultGroupName=MiniDockQT6
OutputBaseFilename=MiniDockQT6_Setup
SetupIconFile=icons\\favicon.ico
Compression=lzma
SolidCompression=yes
LicenseFile=LICENSE.txt

[Files]
; Ejecutable generado por PyInstaller
Source="dist\\MiApp.exe"; DestDir="{app}"; Flags: ignoreversion

[Icons]
Name="{group}\\MiniDockQT6"; Filename="{app}\\MiApp.exe"; WorkingDir="{app}"
Name="{userdesktop}\\MiniDockQT6"; Filename="{app}\\MiApp.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear icono en el Escritorio"; GroupDescription: "Iconos adicionales:"; Flags: unchecked