@echo off

net use \\%1 /user:%2 %3 >nul 2>&1
if %errorlevel%==0 (
    echo %3
    net use \\%1 /d /y >nul 2>&1
)