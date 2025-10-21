@echo off
echo ===============================================================
echo  Tag Sorter LLM - Universal Dependency Installer
echo ===============================================================
echo.

set "TARGET_FOLDER=ComfyUI\custom_nodes\Tag-Sorter-LLM"

echo [Step 1/3] Checking repository...
if exist "%TARGET_FOLDER%\.git" (
    echo 📁 Repository already exists. Skipping clone step.
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

echo [Step 2/3] Installing build tools (cmake, ninja, scikit-build-core)...
call "%~dp0python_embeded\python.exe" -m pip install cmake ninja scikit-build-core
if %errorlevel% neq 0 (
    echo ❌ Failed to install build tools!
    goto :fail_end
)
echo ✅ Build tools installed successfully!
echo.

echo [Step 3/3] Installing and compiling llama-cpp-python with CUDA support...
echo This may take a long time (2-15 minutes). Please be patient.
echo.

:: --- УНІВЕРСАЛЬНА ЛОГІКА ВСТАНОВЛЕННЯ ---
echo ---> Attempting installation with modern CUDA flag (GGML_CUDA)...
set CMAKE_ARGS=-DGGML_CUDA=on
call "%~dp0python_embeded\python.exe" -m pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python

:: Перевіряємо, чи перша спроба не вдалася
if %errorlevel% neq 0 (
    echo.
    echo ---> Modern flag failed. Retrying with legacy CUDA flag (LLAMA_CUBLAS)...
    set CMAKE_ARGS=-DLLAMA_CUBLAS=on
    call "%~dp0python_embeded\python.exe" -m pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python
    
    :: Перевіряємо, чи друга спроба також не вдалася
    if %errorlevel% neq 0 (
        echo ❌ Critical Error: Failed to install llama-cpp-python with both modern and legacy CUDA flags.
        goto :fail_end
    )
)
:: -----------------------------------------

echo ✅ llama-cpp-python installed successfully!
echo.
echo ===============================================================
echo  All dependencies installed successfully!
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