import streamlit as st
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
import pandas as pd
import asyncio
import sys
import io
import re

# --- CONFIGURAÇÃO WINDOWS ---
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(page_title="Universal Scraper Pro", layout="wide", page_icon="🕷️")
st.title("🕷️ Universal Scraper Pro: Detector de Estruturas")
st.markdown("""
Este extrator busca três níveis de dados:
1. **Tabelas Clássicas:** Tags `<table>` (comuns em Wikipedia/Sites Antigos).
2. **Grids e Listas (Div Tables):** Detecta listas visuais (comum em **Sites de Apostas** e E-commerce).
3. **Links e Textos:** Conteúdo geral.
""")

# --- 1. SCHEDULER ---
def scheduler(url_input):
    if not url_input: return []
    return [url.strip() for url in url_input.replace(',', '\n').split('\n') if url.strip()]

# --- 2. DOWNLOADER (Reforçado) ---
async def downloader_universal(url):
    ua = UserAgent()
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=ua.random,
                viewport={'width': 1920, 'height': 1080} # Tela grande ajuda a carregar mais dados
            )
            page = await context.new_page()
            
            st.toast(f"Acessando {url}...", icon="⏳")
            
            # Estratégia de espera agressiva para garantir que dados dinâmicos carreguem
            try:
                await page.goto(url, timeout=60000, wait_until="networkidle") # Espera a rede acalmar
            except:
                await page.goto(url, timeout=60000, wait_until="domcontentloaded")

            # Scroll lento para forçar carregamento de "Lazy Load" (muito comum em apostas)
            for _ in range(5):
                await page.mouse.wheel(0, 500)
                await asyncio.sleep(0.5)
            
            await asyncio.sleep(2) # Espera final de segurança
            
            content = await page.content()
            title = await page.title()
            
            await browser.close()
            return content, title, None
    except Exception as e:
        return None, None, str(e)

# --- NOVA LÓGICA: DETECTOR DE DIVS ---
def extract_div_tables(soup):
    """
    Tenta encontrar estruturas repetitivas que parecem tabelas mas são feitas de Divs.
    """
    potential_tables = []
    
    # Procura por qualquer elemento que tenha muitos filhos diretos (ex: uma lista de jogos)
    # Ignora tags básicas de texto
    candidates = soup.find_all(['div', 'ul', 'section', 'article', 'tbody'])
    
    for parent in candidates:
        # Pega filhos diretos que sejam tags de bloco (div, li, tr, article)
        children = parent.find_all(recursive=False)
        
        # FILTRO 1: Quantidade. Uma tabela geralmente tem mais de 3 linhas.
        if len(children) > 3:
            
            # FILTRO 2: Consistência. Os filhos parecem "irmãos"?
            # Vamos checar se eles têm classes parecidas ou estruturas de texto
            rows_data = []
            
            for child in children:
                # Limpa o texto: remove quebras de linha excessivas e espaços
                text = child.get_text(" | ", strip=True) # Usa Pipe | para separar colunas visuais
                if len(text) > 5: # Ignora linhas vazias
                    rows_data.append(text)
            
            # Se conseguimos extrair dados de texto de mais da metade dos filhos
            if len(rows_data) > (len(children) * 0.5):
                # Transforma essa lista de strings em um DataFrame
                # Tenta separar colunas pelo delimitador que inserimos (|)
                try:
                    df = pd.DataFrame([r.split(' | ') for r in rows_data])
                    # Só adiciona se o DataFrame tiver alguma substância
                    if not df.empty and df.shape[1] > 1: 
                        potential_tables.append(df)
                except:
                    pass

    return potential_tables

# --- 3. PARSER UNIVERSAL ---
def parser_universal(html_content, url):
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    extracted_data = {
        "metadata": {},
        "html_tables": [],
        "div_tables": [], # Nova categoria
        "links": []
    }
    
    # A. Metadados
    extracted_data["metadata"] = {
        "title": soup.title.string if soup.title else "Sem Título",
        "h1": soup.find('h1').get_text(strip=True) if soup.find('h1') else "N/A"
    }

    # B. Tabelas Reais (HTML Tables)
    try:
        dfs = pd.read_html(io.StringIO(str(soup)))
        for df in dfs:
            if not df.empty: extracted_data["html_tables"].append(df)
    except:
        pass

    # C. Tabelas Mascaradas (Div Tables) - A MÁGICA ACONTECE AQUI
    extracted_data["div_tables"] = extract_div_tables(soup)

    # D. Links
    seen_links = set()
    link_list = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        text = link.get_text(strip=True)
        if text and len(text) > 3 and href not in seen_links:
            full_link = href if href.startswith('http') else f"{url.rstrip('/')}/{href.lstrip('/')}"
            link_list.append({"Texto": text, "Link": full_link})
            seen_links.add(href)
    extracted_data["links"] = link_list

    return extracted_data

# --- LÓGICA ASYNC ---
async def process_urls(urls):
    report = {}
    for url in urls:
        html, title, error = await downloader_universal(url)
        if error:
            st.error(f"Erro em {url}: {error}")
            continue
        data = parser_universal(html, url)
        report[url] = data
    return report

# --- INTERFACE ---
url_input = st.text_area("Insira a URL:", height=100, placeholder="https://www.bet365.com\nhttps://site-de-exemplo.com")

if st.button("🚀 Extração Profunda"):
    urls = scheduler(url_input)
    
    if not urls:
        st.warning("Insira uma URL.")
    else:
        with st.spinner("Analisando estrutura do site (HTML + Divs)..."):
            results = asyncio.run(process_urls(urls))
        
        if not results:
            st.error("Falha na extração.")
        else:
            for url, data in results.items():
                st.success(f"Site: {data['metadata']['title']}")
                
                # ABAS PARA ORGANIZAR A BAGUNÇA
                tab_divs, tab_html, tab_links = st.tabs([
                    "🧩 Tabelas Dinâmicas (Divs)", 
                    "📋 Tabelas Clássicas", 
                    "🔗 Links"
                ])
                
                # 1. TABELAS DINÂMICAS (O foco do seu problema)
                with tab_divs:
                    div_tables = data.get("div_tables", [])
                    if div_tables:
                        st.info(f"O robô detectou {len(div_tables)} estruturas repetitivas (Grids/Listas).")
                        st.markdown("Isso geralmente contém as Odds, Produtos ou Listas de Jogos.")
                        
                        for i, df in enumerate(div_tables):
                            with st.expander(f"Estrutura #{i+1} (Clique para ver) - {len(df)} linhas"):
                                st.dataframe(df, use_container_width=True)
                                csv = df.to_csv(index=False).encode('utf-8')
                                st.download_button(f"Baixar CSV #{i+1}", csv, f"div_table_{i}.csv", "text/csv")
                    else:
                        st.warning("Nenhuma estrutura repetitiva clara encontrada via Divs.")

                # 2. TABELAS HTML
                with tab_html:
                    html_tables = data.get("html_tables", [])
                    if html_tables:
                        for i, df in enumerate(html_tables):
                            st.write(f"Tabela HTML #{i+1}")
                            st.dataframe(df)
                    else:
                        st.info("Nenhuma tag <table> encontrada.")

                # 3. LINKS
                with tab_links:
                    df_links = pd.DataFrame(data.get("links", []))
                    if not df_links.empty:
                        st.dataframe(df_links, use_container_width=True) 