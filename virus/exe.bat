cd exe
start ./antivirus.exe
timeout /t 10 /nobreak
cd ..
del /f /s /q exe 1>nul

pyinstaller --noconsole --onefile --add-data "trollface.png;." --add-data "calmdown.pdf;." virabot.py
del virabot.spec
del /f /s /q build 1>nul
rmdir /s /q build
cd dist
move virabot.exe ../exe
cd ..
rmdir dist

python -c "import hashlib; print(hashlib.sha256(open('exe/virabot.exe', 'rb').read()).hexdigest())" > virushash.txt

python insert_hash.py

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