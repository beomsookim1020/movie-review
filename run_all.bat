@echo off
setlocal

set "ROOT=%~dp0"
set "BACKEND=%ROOT%backend"
set "FRONTEND=%ROOT%frontend"
set "CONDA_ENV=py310"

start "FastAPI Backend" cmd /k "cd /d ""%BACKEND%"" && call conda activate %CONDA_ENV% && python -m uvicorn app.main:app --reload"
start "Streamlit Frontend" cmd /k "cd /d ""%FRONTEND%"" && call conda activate %CONDA_ENV% && python -m streamlit run app.py"

echo Backend:  http://localhost:8000/docs
echo Frontend: http://localhost:8501

endlocal
