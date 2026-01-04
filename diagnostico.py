import sys
import asyncio
import os
import traceback
from fake_useragent import UserAgent

print("--- INICIANDO DIAGNÓSTICO DO AMBIENTE ---")
print(f"Python Version: {sys.version}")
print(f"Platform: {sys.platform}")

# 1. TENTATIVA DE CORREÇÃO DE LOOP (CRÍTICO PARA WINDOWS)
try:
    if sys.platform == 'win32':
        print("[INFO] Sistema Windows detectado. Aplicando política ProactorEventLoop...")
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        print("[OK] Política aplicada.")
except Exception as e:
    print(f"[ERRO] Falha ao aplicar política de loop: {e}")

# 2. TESTE DE IMPORTAÇÃO E INSTALAÇÃO
try:
    print("[INFO] Tentando importar Playwright...")
    from playwright.sync_api import sync_playwright
    print("[OK] Playwright importado.")
except ImportError:
    print("[ERRO FATAL] Playwright não está instalado. Rode: pip install playwright")
    sys.exit(1)

# 3. TESTE DE EXECUÇÃO REAL
def run_test():
    url_teste = "https://example.com"
    print(f"[INFO] Iniciando teste de navegação para: {url_teste}")
    
    try:
        ua = UserAgent()
        user_agent_teste = ua.random
        print(f"[INFO] User Agent gerado: {user_agent_teste}")
    except Exception as e:
        print(f"[AVISO] Falha no fake-useragent (usando padrão): {e}")
        user_agent_teste = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    try:
        with sync_playwright() as p:
            print("[1/5] Playwright Context iniciado.")
            
            # Tenta lançar o navegador (Headless = False para ver se abre a janela)
            try:
                print("[2/5] Tentando lançar navegador Chromium...")
                browser = p.chromium.launch(headless=False) 
                print("[OK] Navegador lançado.")
            except Exception as e:
                print("\n[ERRO CRÍTICO NO BROWSER]")
                print("Provável causa: Binários não instalados.")
                print("SOLUÇÃO: No terminal, rode o comando -> playwright install")
                raise e

            context = browser.new_context(user_agent=user_agent_teste)
            page = context.new_page()
            print("[3/5] Página criada.")
            
            print(f"[4/5] Acessando {url_teste}...")
            response = page.goto(url_teste, timeout=10000)
            
            status = response.status if response else "Sem resposta"
            titulo = page.title()
            
            print(f"[5/5] Sucesso! Status: {status} | Título: {titulo}")
            
            browser.close()
            print("[INFO] Teste finalizado com SUCESSO ABSOLUTO.")
            
    except Exception as e:
        print("\n--- DETALHES DO ERRO ---")
        traceback.print_exc()
        print("------------------------")

if __name__ == "__main__":
    run_test()