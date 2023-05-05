@echo off
setlocal

set GRAPHVIZ_PATH="%ProgramFiles%\Graphviz\bin\dot.exe"

if not exist %GRAPHVIZ_PATH% (
    echo ERROR: Graphviz is not installed on this system.
    echo Please install Graphviz from https://graphviz.org/download/ and ensure that Graphviz is added to your computer's PATH
    pause
) else (
    set GRAPHVIZ_EXE=dot.exe

    where %GRAPHVIZ_EXE% >nul 2>nul
    if %errorlevel% equ 0 (
        start cmd /k "python .\prometheusMain\runDataPrometheus.py"
        cd ./frontendGUI
        start /b cmd /c "python -m http.server"
    ) else (
        echo ERROR: Graphviz is installed but not in your PATH
        echo Please add Graphviz to your PATH
        pause
    )
)