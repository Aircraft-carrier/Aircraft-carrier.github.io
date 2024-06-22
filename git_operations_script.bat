@echo off
echo --- Git Pull ---
git pull

echo --- Updating Directory ---

:: Get current directory path
setlocal
cd /d %~dp0
set "currentDir=%CD%"
setlocal enabledelayedexpansion

:: Concatenate target folder path
set "blogDir=%currentDir%\blog"

:: Change to target folder
cd /d %blogDir%

:: Execute toc.exe
call toc.exe

:: Change back to the original folder
cd /d %currentDir%

echo --- Git Add ---
git add .

echo --- Git Commit ---
set /p commitMessage="Enter commit message: "
git commit -m "%commitMessage%"

echo --- Git Push ---
git push origin main

echo --- Done ---
pause