@echo off
cd /d "%~dp0"
if exist "dist\WindowMoverTool.exe" (
    start "" "dist\WindowMoverTool.exe"
) else (
    echo 错误：找不到 WindowMoverTool.exe
    echo 请先运行打包脚本 build_exe.py
    pause
)