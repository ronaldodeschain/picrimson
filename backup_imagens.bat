@echo off
setlocal

:: ── Configuração ──────────────────────────────────────────────
set SOURCE_DIR=%~dp0app\static\uploads
set BACKUP_DIR=%~dp0backups\imagens

:: ── Timestamp ─────────────────────────────────────────────────
for /f "tokens=1-3 delims=/" %%a in ("%date%") do set DATE_STR=%%c%%b%%a
for /f "tokens=1-3 delims=:." %%a in ("%time: =0%") do set TIME_STR=%%a%%b%%c
set ZIPNAME=%BACKUP_DIR%\uploads_%DATE_STR%_%TIME_STR%.zip

:: ── Cria pasta se não existir ─────────────────────────────────
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: ── Compacta uploads com PowerShell ──────────────────────────
powershell -NoProfile -Command "Compress-Archive -Path '%SOURCE_DIR%\*' -DestinationPath '%ZIPNAME%' -Force"

if %ERRORLEVEL% == 0 (
    echo.
    echo [OK] Backup gerado: %ZIPNAME%
) else (
    echo.
    echo [ERRO] Falha ao compactar imagens.
)

:: ── Retenção: apaga backups com mais de 7 dias ────────────────
forfiles /p "%BACKUP_DIR%" /s /m *.zip /d -7 /c "cmd /c del @path" 2>nul

endlocal
pause
