@echo off
:: Встановлюємо кодову сторінку UTF-8
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ======================================================================
echo  Tag Sorter LLM - Smart Pre-compiled Dependency Installer
echo  (Supports Python 3.12 and 3.13 on Windows x64)
echo ======================================================================
echo.

:: --- Налаштування змінних ---
set "PYTHON_EXE=%~dp0python_embeded\python.exe"
set "TARGET_FOLDER=ComfyUI\custom_nodes\Tag-Sorter-LLM"
set "PACKAGES_TO_CHECK=llama-cpp-python huggingface-hub packaging requests hf_xet"
set "WHEEL_URL_PY312=https://github.com/FruityAnon/Tag-Sorter-LLM/releases/download/v1.2/llama_cpp_python-0.3.16-cp312-cp312-win_amd64.whl"
set "WHEEL_URL_PY313=https://github.com/FruityAnon/Tag-Sorter-LLM/releases/download/v1.2/llama_cpp_python-0.3.16-cp313-cp313-win_amd64.whl"
set "ALL_DEPS_INSTALLED=true"
set "LLAMA_CPP_INSTALLED=false"

:: --- Встановлюємо змінні середовища для запобігання створення файлів ---
set "PIP_NO_CACHE_DIR=1"
set "PYTHONDONTWRITEBYTECODE=1"

:: --- Крок 1: Попередня перевірка ---
echo [Step 1/3] Checking for required dependencies...
for %%p in (%PACKAGES_TO_CHECK%) do (
    call "%PYTHON_EXE%" -m pip show %%p > nul 2>&1
    if !errorlevel! neq 0 (
        echo    - Checking for %%p... [!] Not found.
        set "ALL_DEPS_INSTALLED=false"
    ) else (
        if "%%p"=="llama-cpp-python" set "LLAMA_CPP_INSTALLED=true"
    )
)

if "!ALL_DEPS_INSTALLED!"=="true" (
    echo.
    echo [OK] All dependencies are already installed. Nothing to do.
    goto :cleanup
)

echo [!] Some dependencies are missing. Proceeding with installation...
echo.

:: --- Крок 2: Клонування репозиторію (якщо його немає) ---
echo [Step 2/3] Checking repository...
if exist "%TARGET_FOLDER%\.git" (
    echo [INFO] Repository already exists.
) else (
    echo [INFO] Cloning repository...
    git clone https://github.com/FruityAnon/Tag-Sorter-LLM.git "%TARGET_FOLDER%" > nul 2>&1
    if not exist "%TARGET_FOLDER%\.git" (
        echo [ERROR] Failed to clone repository!
        goto :fail_end
    )
)
echo [OK] Repository check complete.
echo.

:: --- Крок 3: Встановлення залежностей ---
echo [Step 3/3] Installing dependencies...

echo    -> Installing base packages (huggingface-hub, requests, etc.)...
call "%PYTHON_EXE%" -m pip install --no-cache-dir huggingface-hub>=0.20.0 packaging>=24.0 requests>=2.32.3 hf_xet > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install base dependencies!
    goto :fail_end
)
echo    -> Base packages installed.
echo.

:: Встановлюємо Llama CPP, тільки якщо його не вистачає
if "!LLAMA_CPP_INSTALLED!"=="false" (
    echo    -> Installing pre-compiled llama-cpp-python...
    
    :: Визначаємо версію Python
    for /f "tokens=*" %%i in ('"%PYTHON_EXE%" --version 2^>^&1') do set "PYTHON_VERSION_STRING=%%i"

    if "!PYTHON_VERSION_STRING:3.12=!" NEQ "!PYTHON_VERSION_STRING!" (
        echo       -> Python 3.12 detected. Downloading wheel...
        call "%PYTHON_EXE%" -m pip install --no-cache-dir "%WHEEL_URL_PY312%" > nul 2>&1
    ) else if "!PYTHON_VERSION_STRING:3.13=!" NEQ "!PYTHON_VERSION_STRING!" (
        echo       -> Python 3.13 detected. Downloading wheel...
        call "%PYTHON_EXE%" -m pip install --no-cache-dir "%WHEEL_URL_PY313%" > nul 2>&1
    ) else (
        echo [ERROR] Unsupported Python version: !PYTHON_VERSION_STRING!
        echo This installer only supports pre-compiled wheels for Python 3.12 and 3.13.
        echo Please use the manual compilation installer.
        goto :fail_end
    )

    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install from the pre-compiled wheel.
        goto :fail_end
    )
    echo    -> llama-cpp-python installed successfully.
)

echo.
echo ===============================================================
echo  All dependencies are configured successfully!
echo  You can now launch ComfyUI.
echo ===============================================================
goto :cleanup

:fail_end
echo [ERROR] Installation failed. Please check the error messages above.
pause
goto :cleanup

:cleanup
:: --- Очищення залишкових файлів ---
del "Installing*" > nul 2>&1
del "Base*" > nul 2>&1
del "Python*" > nul 2>&1
del "llama-cpp-python*" > nul 2>&1
del "Collecting*" > nul 2>&1
del "Downloading*" > nul 2>&1

:success_end
echo.
pause