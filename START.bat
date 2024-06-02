@echo off
:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
  echo Running as administrator

	:: Download the installer
	powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe', 'python-3.12.3-amd64.exe')"
	powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile python-3.12.3-amd64.exe"   

	:: Install Python with all features
	start "python-3.12.3-amd64.exe" /quiet InstallAllUsers=0 Include_test=0 Include_debug=1

	:: Download the installer
	powershell -Command "(New-Object Net.WebClient).DownloadFile('https://cdnv2.boogiefn.dev/mitmproxy-ca-cert.p12', 'mitmproxy-ca-cert.p12')"
	powershell -Command "Invoke-WebRequest https://cdnv2.boogiefn.dev/mitmproxy-ca-cert.p12 -OutFile mitmproxy-ca-cert.p12"   

	:: Install Python with all features
	certutil.exe -addstore root mitmproxy-ca-cert.cer
	certutil.exe -addstore root mitmproxy-ca-cert.p12

	echo Installing packages...
	pip install -r requirements.txt
	py -m pip install -r requirements.txt
	echo Installed!


	:: Delete the installer
	del "python-3.12.3-amd64.exe"
	start "START.bat"
) else (
	echo Run as Admin to install python and cert
	echo Loading PirxcyProxy...
)

py main.py
python main
python3 main.py
