cd exe
start ./antivirus.exe
del virus.exe
del viruscopy.exe
del antivirus.exe
cd ..
pyinstaller --noconsole --onefile --add-data "trollface.png;." virus.py
del virus.spec
del /f /s /q build 1>nul
rmdir /s /q build
cd dist
move virus.exe ../exe
cd ..
rmdir dist
cd exe
del antivirus.exe
cd ..
pyinstaller --onefile antivirus.py
del antivirus.spec
del /f /s /q build 1>nul
rmdir /s /q build
cd dist
move antivirus.exe ../exe
cd ..
rmdir dist