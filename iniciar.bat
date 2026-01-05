@echo off
TITLE Instalador e Iniciador do Web Scraper
CLS

echo ========================================================
echo   VERIFICANDO AMBIENTE PARA O WEB SCRAPER
echo ========================================================
echo.

:: 1. Verifica se o Python está instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale o Python 3.10 ou superior e marque a opcao "Add to PATH".
    pause
    exit
)

:: 2. Cria um ambiente virtual (venv) se não existir
:: Isso isola o projeto para não dar conflito com o PC do seu amigo
IF NOT EXIST "venv" (
    echo [INFO] Criando ambiente virtual (pode demorar um pouco)...
    python -m venv venv
    echo [OK] Ambiente virtual criado.
)

:: 3. Ativa o ambiente virtual
call venv\Scripts\activate

:: 4. Atualiza o PIP
echo [INFO] Verificando atualizacoes do instalador...
python -m pip install --upgrade pip >nul 2>&1

:: 5. Instala as bibliotecas do requirements.txt
if exist requirements.txt (
    echo [INFO] Instalando bibliotecas necessarias...
    pip install -r requirements.txt
) else (
    echo [ERRO] Arquivo requirements.txt nao encontrado!
    pause
    exit
)

:: 6. Instala os navegadores do Playwright (O PULO DO GATO)
echo [INFO] Verificando binarios do navegador Chromium...
playwright install chromium

echo.
echo ========================================================
echo   TUDO PRONTO! INICIANDO O APP...
echo   (Nao feche esta janela preta enquanto usar o App)
echo ========================================================
echo.

:: 7. Roda o Streamlit
streamlit run app.py

pause