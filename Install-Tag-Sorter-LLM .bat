@echo off
:: Вмикаємо кодову сторінку для коректного відображення символів
chcp 65001 > nul
:: Вмикаємо відкладене розширення змінних, необхідне для циклів
setlocal enabledelayedexpansion

echo ===============================================================
echo  Tag Sorter LLM - Smart Dependency Installer
echo ===============================================================
echo.

:: --- Налаштування змінних ---
set "PYTHON_EXE=%~dp0python_embeded\python.exe"
set "TARGET_FOLDER=ComfyUI\custom_nodes\Tag-Sorter-LLM"
set "ALL_DEPS_INSTALLED=true"
set "PACKAGES_TO_CHECK=cmake ninja scikit-build-core llama-cpp-python huggingface-hub packaging requests hf_xet"

:: --- Крок 1: Перевірка наявності всіх залежностей ---
echo [Step 1/4] Checking for all required dependencies...
for %%p in (%PACKAGES_TO_CHECK%) do (
    echo   - Checking for %%p...
    call "%PYTHON_EXE%" -m pip show %%p > nul 2>&1
    if !errorlevel! neq 0 (
        echo     -> ⚠️ Not found.
        set "ALL_DEPS_INSTALLED=false"
    ) else (
        echo     -> ✅ Found.
    )
)

:: --- Умовний перехід: якщо все встановлено, завершуємо роботу ---
if "!ALL_DEPS_INSTALLED!"=="true" (
    echo.
    echo ✅ All dependencies are already installed. Nothing to do.
    goto :success_end
)

echo.
echo ⚠️ Some dependencies are missing. Proceeding with installation...
echo.


:: --- Крок 2: Клонування репозиторію (якщо його немає) ---
echo [Step 2/4] Checking repository...
if exist "%TARGET_FOLDER%\.git" (
    echo 📁 Repository already exists.
) else (
    echo 📥 Cloning repository...
    git clone https://github.com/FruityAnon/Tag-Sorter-LLM.git "%TARGET_FOLDER%"
    if %errorlevel% neq 0 (
        echo ❌ Failed to clone repository! Please check your internet connection and Git installation.
        goto :fail_end
    )
)
echo ✅ Repository check complete.
echo.

:: --- Крок 3: Встановлення базових залежностей ---
echo [Step 3/4] Installing base dependencies (pip will skip installed ones)...
call "%PYTHON_EXE%" -m pip install huggingface-hub>=0.20.0 packaging>=24.0 requests>=2.32.3 hf_xet cmake ninja scikit-build-core
if %errorlevel% neq 0 (
    echo ❌ Failed to install base dependencies!
    goto :fail_end
)
echo ✅ Base dependencies are up to date.
echo.

:: --- Крок 4: Встановлення llama-cpp-python (тільки якщо його не було) ---
echo [Step 4/4] Installing and compiling llama-cpp-python...
echo This may take a long time (5-15 minutes). Please be patient.
echo.

echo ---> Attempting installation with modern CUDA flag (GGML_CUDA)...
set CMAKE_ARGS=-DGGML_CUDA=on
call "%PYTHON_EXE%" -m pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python>=0.2.79

if %errorlevel% neq 0 (
    echo.
    echo ---> Modern flag failed. Retrying with legacy CUDA flag (LLAMA_CUBLAS)...
    set CMAKE_ARGS=-DLLAMA_CUBLAS=on
    call "%PYTHON_EXE%" -m pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python>=0.2.79
    
    if %errorlevel% neq 0 (
        echo ❌ Critical Error: Failed to install llama-cpp-python.
        echo Please check if you have Microsoft C++ Build Tools installed.
        goto :fail_end
    )
)
echo ✅ llama-cpp-python installed successfully!
echo.

:success_end
echo ===============================================================
echo  All dependencies are configured successfully!
echo  You can now launch ComfyUI.
echo ===============================================================
echo.
pause
exit /b 0

:fail_end
echo ❌ Installation failed. Please check the error messages above.
echo.
pause
exit /b 1