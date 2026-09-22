set PYTHONPATH=%UGII_BASE_DIR%\NXBIN\python;%PYTHONPATH%
set UGII_ENV_FILE=%UGII_BASE_DIR%\ugii_env.dat
set path=%UGII_BASE_DIR%\NXBIN;%UGII_BASE_DIR%\UGII;%UGII_BASE_DIR%\UGOPEN;%UGII_BASE_DIR%\NXBIN\python;%path%
code %~dp0%
REM for %%t in (".\sln") do "%DEVENV%" %%t
pause