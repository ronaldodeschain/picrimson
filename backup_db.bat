@echo off
setlocal

:: ── Configuração ──────────────────────────────────────────────
set DB_NAME=crimson_db
set DB_USER=postgres
set DB_PASS=postgres
set DB_HOST=localhost
set DB_PORT=5432
set BACKUP_DIR=%~dp0backups\db

:: ── Timestamp ─────────────────────────────────────────────────
for /f "tokens=1-3 delims=/" %%a in ("%date%") do set DATE_STR=%%c%%b%%a
for /f "tokens=1-3 delims=:." %%a in ("%time: =0%") do set TIME_STR=%%a%%b%%c
set FILENAME=%BACKUP_DIR%\crimson_db_%DATE_STR%_%TIME_STR%.dump

:: ── Cria pasta se não existir ─────────────────────────────────
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: ── Executa pg_dump dentro do container Docker ─────────────────
set CONTAINER=crimson-postgres
docker exec -e PGPASSWORD=%DB_PASS% %CONTAINER% pg_dump -U %DB_USER% -F c -b -v %DB_NAME% > "%FILENAME%"

if %ERRORLEVEL% == 0 (
    echo.
    echo [OK] Backup gerado: %FILENAME%
) else (
    echo.
    echo [ERRO] Falha ao gerar backup. Verifique se o container '%CONTAINER%' esta rodando.
)

:: ── Retenção: apaga backups com mais de 7 dias ────────────────
forfiles /p "%BACKUP_DIR%" /s /m *.dump /d -7 /c "cmd /c del @path" 2>nul

endlocal
pause
