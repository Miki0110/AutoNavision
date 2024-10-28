@echo off
cd /d "%~dp0"
cd src
call conda activate AutoNavision_env
python main.py
