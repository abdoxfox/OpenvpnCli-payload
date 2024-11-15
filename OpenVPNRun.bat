@echo off
echo Enter openvpn config PATH 
set /p sourcefile=path:
set "destPath=%PROGRAMFILES%\OpenVPN\config"

if not exist "%sourcefile%" echo no config found in this path & exit
copy "%sourcefile%" "%destPath%"
echo OpenVPN config copied successfully 

for %%F in ("%sourcefile%") do set cfgName=%%~nxF
"%PROGRAMFILES%\OpenVPN\bin\openvpn-gui.exe" --connect cfgName
del "%destPath%\client.ovpn"
pause