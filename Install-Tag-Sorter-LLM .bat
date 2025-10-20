@echo off
echo ===============================================================
echo  Tag Sorter LLM - Dependency Installer
echo ===============================================================
echo.

echo [Step 1/2] Installing build tools (cmake, ninja, scikit-build-core)...
call "%~dp0python_embeded\python.exe" -m pip install cmake ninja scikit-build-core

echo.
echo [Step 2/2] Installing and compiling llama-cpp-python with CUDA support...
echo This may take a long time (5-15 minutes). Please be patient.
echo.

set CMAKE_ARGS=-DLLAMA_CUBLAS=on
call "%~dp0python_embeded\python.exe" -m pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python

echo.
echo ===============================================================
echo  Dependencies installed successfully!
echo  You can now launch ComfyUI.
echo ===============================================================
echo.
pause