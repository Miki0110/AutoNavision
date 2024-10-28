@echo off

REM Change directory to the location of this script
cd /d "%~dp0"

REM Check if conda is installed
where conda >nul 2>&1
IF ERRORLEVEL 1 (
    echo Miniconda is not installed. Installing Miniconda...
    REM Download Miniconda installer
    powershell -Command "Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile Miniconda3-latest-Windows-x86_64.exe"
    REM Install Miniconda silently
    start /wait "" "Miniconda3-latest-Windows-x86_64.exe" /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3
    SET "PATH=%UserProfile%\Miniconda3;%UserProfile%\Miniconda3\Library\bin;%UserProfile%\Miniconda3\Scripts;%PATH%"
) ELSE (
    echo Miniconda is already installed.
)


REM Create the environment if it doesn't exist
echo Checking if conda environment exists...
conda env list | findstr AutoNavision_env >nul 2>&1
IF ERRORLEVEL 1 (
    echo Creating conda environment...
    conda env create -f "%~dp0environment.yml"
) ELSE (
    echo Conda environment already exists.
)