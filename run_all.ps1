$ErrorActionPreference = "Stop"

$RootPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendPath = Join-Path $RootPath "backend"
$FrontendPath = Join-Path $RootPath "frontend"
$CondaEnv = "py310"

Start-Process powershell -WindowStyle Normal -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd `"$BackendPath`"; conda activate $CondaEnv; python -m uvicorn app.main:app --reload"
)

Start-Process powershell -WindowStyle Normal -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd `"$FrontendPath`"; conda activate $CondaEnv; python -m streamlit run app.py"
)

Write-Host "Backend:  http://localhost:8000/docs"
Write-Host "Frontend: http://localhost:8501"
