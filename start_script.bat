@echo off
cd /d "%~dp0"
cd src

call conda activate AutoNavision_env
IF ERRORLEVEL 1 (
    powershell -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; [System.Windows.Forms.MessageBox]::Show('Error activating conda environment.');"
    exit /b 1
)

python main.py
IF ERRORLEVEL 1 (
    powershell -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; [System.Windows.Forms.MessageBox]::Show('Error running the Python script.');"
    exit /b 1
)
