@setlocal enableextensions enabledelayedexpansion
@echo off
set file=config\settings.conf
set area=[DEFAULT]
set key=headless_mode
set currarea=
for /f "usebackq delims=" %%a in ("%file%") do (
    set ln=%%a
    if "x!ln:~0,1!"=="x[" (
        set currarea=!ln!
    ) else (
        for /f "tokens=1,2 delims==" %%b in ("!ln!") do (
            set currkey=%%b
            set currval=%%c
            if "x!area!"=="x!currarea!" if "x!key!"=="x!currkey!" (
                set headless=!currval!
            )
        )
    )
)

if "%headless%"=="True" (
    py -m ensurepip --default-pip
    pip install -U opendeliverybot
    python -m opendeliverybot
) else (
    streamlit run src\__initweb__.py
)
