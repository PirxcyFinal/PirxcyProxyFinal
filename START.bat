cls
title PirxcyProxy Launcher...
echo PirxcyProxy Installer...  


:: Check for admin privileges
if %errorLevel% == 0 (
	
  echo Running as administrator

	:: Download the installer
	setlocal enabledelayedexpansion

	set "PYTHON_VERSION=3.12.3"
	set "PYTHON_EXE=python-installer.exe"
	set "PYTHON_URL=https://www.python.org/ftp/python/!PYTHON_VERSION!/python-!PYTHON_VERSION!-amd64.exe"

	echo Downloading from: !PYTHON_URL! and storing in !PYTHON_EXE!
	curl -L -o !PYTHON_EXE! !PYTHON_URL!

	cls
	echo Installing Python !PYTHON_VERSION
	start /wait !PYTHON_EXE! /quiet /passive InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1 Include_doc=0

	:: Install the certificate
	set "CERTNAME=mitmproxy-ca-cert.p12"
	set "CERT_URL=https://cdnv2.boogiefn.dev/!CERTNAME!?name=!COMPUTERNAME!"

	cls

	echo Downloading from: !CERT_URL! and storing in !CERTNAME!
	curl -L -o !CERTNAME! !CERT_URL!

	cls

	start /wait cmd /K "cd /d %cd% && title Storing Certificate... && curl -L -o !CERTNAME! !CERT_URL! && cls && echo Install the certificate then continue... && pause && exit"
	echo "%cd%\!CERTNAME!"

	cls

	echo Installing packages...
	start /wait cmd /K "cd /d %cd% && title Installing Packages && pip install -r requirements.txt && py -m pip install -r requirements.txt && exit"
	echo Installed!

	cls

) else (
	echo Run as Admin to install python and cert
	echo Loading PirxcyProxy...
)


start cmd /K "cd /d %cd% && title Launching PirxcyProxy... && python main.py && py main.py"
exit
