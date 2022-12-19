REM -----RunBat.bat-------
@echo off
setlocal enableextensions enabledelayedexpansion
cd %~dp0
if not exist "Results" mkdir Results

REM Take the exe in the folder. 
FOR %%F IN (*.exe) DO (
SET exe=%%F
SET name=%%~nF
)

REM arg is now the configuration file path.
set arg=%1

FOR %%i IN ("%arg%") DO (
set argFilename=%%~ni
)

SET LogPath=Results\Log_%name%_%argFilename%
echo %LogPath%
SET /A COUNT=1

REM for each line in configfile run exe with that line as parameters, and save output to a Log. 
for /f "tokens=*" %%a in (%arg%) do (
echo %COUNT%
CALL python.exe main.py %%a >> %LogPath%_!COUNT!.txt
SET /A COUNT+=1
)

REM move exe output files to Results Folder
REM move *.m "%~dp0Results"
REM move *.record "%~dp0Results"
REM timeout 5
REM --------------------
