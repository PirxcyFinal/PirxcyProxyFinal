@echo off
title PirxcyProxy Launcher

:: Display the installer message
echo PirxcyProxy Installer...

:: Check for admin privileges
openfiles >nul 2>&1
if %errorLevel% == 0 (
    echo Running as administrator

    :: Set variables for Python installation
    setlocal enabledelayedexpansion
    set "PYTHON_VERSION=3.12.3"
    set "PYTHON_EXE=python-installer.exe"
    set "PYTHON_URL=https://www.python.org/ftp/python/!PYTHON_VERSION!/python-!PYTHON_VERSION!-amd64.exe"

    :: Download the Python installer
    echo Downloading Python from: !PYTHON_URL! and storing in !PYTHON_EXE!
    curl -L -o !PYTHON_EXE! !PYTHON_URL!

    :: Install Python
    cls
    echo Installing Python !PYTHON_VERSION!
    start /wait !PYTHON_EXE! /quiet /passive InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1 Include_doc=0

    :: Set variables for certificate installation
    set "CERTNAME=mitmproxy-ca-cert.p12"
    set "CERT_URL=https://cdn.pirxcy.dev/!CERTNAME!?name=!COMPUTERNAME!"

    :: Download the certificate
    cls
    echo Downloading certificate from: !CERT_URL! and storing in !CERTNAME!
    curl -L -o !CERTNAME! !CERT_URL!

    :: Install the certificate
    cls
    start /wait cmd /K "cd /d %cd% && title Storing Certificate... && curl -L -o !CERTNAME! !CERT_URL! && cls && echo Install the certificate then continue... && pause && exit"
    echo "%cd%\!CERTNAME!"

    cls
    echo Installing packages...
    
    :: Install Python packages
    start /wait cmd /K "cd /d %cd% && title Installing Packages && pip install -r requirements.txt && py -m pip install -r requirements.txt && exit"
    echo Installed!

    cls
) else (
    echo Run as Admin to install Python and the certificate
)

:: Launch PirxcyProxy
start /wait cmd /K "cd /d %cd% && title Launching PirxcyProxy... && python main.py && exit"
start /wait cmd /K "cd /d %cd% && title Launching PirxcyProxy... && py main.py && exit"
exit
