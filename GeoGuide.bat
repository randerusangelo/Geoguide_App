@echo off
setlocal
title GeoGuide - Abastecimento
echo Abrindo no navegador ...
echo Apenas feche esta janela se desejar encerrar o sistema.
echo.

REM === vai para a pasta do projeto (onde o .bat está) ===
cd /d "%~dp0"

REM === ativa o ambiente virtual ===
call ".venv\Scripts\activate.bat"

REM === executa o Streamlit pelo Python do venv ===
python -m streamlit run "geoguide_abastecimento.py"

echo.
echo Para encerrar, feche esta janela.
pause
endlocal
