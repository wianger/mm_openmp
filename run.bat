@echo off
rem  usage:  build.bat  N  ITERATIONS
setlocal enabledelayedexpansion

set "N=%~1"
set "ITERATIONS=%~2"

if "%~2"=="" (
    echo Usage: %~nx0 N ITERATIONS
    exit /b 1
)

for %%f in (build\*.exe) do (
    echo %%f:
    "%%f" %N% %ITERATIONS%
    echo.
)