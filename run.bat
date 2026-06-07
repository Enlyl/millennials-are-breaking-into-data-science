@echo off
chcp 65001 >nul
python -X utf8 run.py
if errorlevel 1 pause
