# 🕷️ Universal Web Scraper Pro

Um aplicativo de Web Scraping de última geração, construído em Python e Streamlit. Diferente de scrapers tradicionais que quebram se o site mudar o layout, este app utiliza heurísticas para detectar dados estruturados automaticamente, sendo capaz de extrair informações de tabelas clássicas (`<table>`) e grades modernas baseadas em Divs (comuns em sites de apostas, e-commerce e dashboards).

## 🚀 Funcionalidades

- **Extração Universal**: Funciona em Wikipedia, Amazon, Bet365, Betano, Sites de Finanças, etc.
- **Detector de "Div Tables"**: Algoritmo inteligente que identifica estruturas repetitivas (grids/listas) que simulam tabelas.
- **Navegação Real (Headless)**: Usa Playwright para simular um navegador real, processando JavaScript e Lazy Loading.
- **Anti-Bloqueio Básico**: Rotatividade de User-Agents e delays aleatórios para evitar detecção imediata.
- **Arquitetura Assíncrona**: A interface não congela enquanto o robô trabalha.
- **Exportação Fácil**: Visualização em abas e download de qualquer tabela encontrada em CSV.

## 🛠️ Pré-requisitos

- **Python**: Versão 3.9 até 3.12 (Recomendado).
  > **Nota**: O Python 3.13 ainda pode apresentar instabilidades com algumas bibliotecas assíncronas no Windows.
- **Navegador**: Chromium (instalado automaticamente via Playwright).

## 📦 Instalação

1. Clone ou baixe este repositório:
   ```bash
   git clone https://github.com/seu-usuario/universal-web-scraper-pro.git
   cd universal-web-scraper-pro
   ```

2. Instale as dependências do Python:
   ```bash
   pip install -r requirements.txt
   ```

   **requirements.txt:**
   ```
   streamlit
   playwright
   pandas
   fake-useragent
   beautifulsoup4
   lxml
   html5lib
   ```

3. Instale os binários do navegador:
   ```bash
   playwright install
   ```

## ▶️ Como Utilizar

1. **Inicie o Aplicativo**: No terminal, dentro da pasta do projeto:
   ```bash
   streamlit run app.py
   ```

2. **Na Interface Web**:
   - Uma aba do navegador abrirá automaticamente (geralmente em `http://localhost:8501`).
   - Cole a URL (ou várias URLs, uma por linha) na caixa de texto.
   - Clique em **🚀 Extração Profunda**.

3. **Analisando os Resultados**: O app divide os dados encontrados em 3 abas:
   - **🧩 Tabelas Dinâmicas (Divs)**: AQUI ESTÁ A MÁGICA. Verifique esta aba para sites modernos (Apostas, Lojas). O app tenta reconstruir tabelas baseadas em repetições visuais.
   - **📋 Tabelas Clássicas**: Exibe dados encontrados dentro de tags `<table>` (comum em Wikipedia).
   - **🔗 Links**: Lista todos os links clicáveis encontrados na página.

4. **Exportação**: Cada tabela encontrada possui um botão "Baixar CSV" logo abaixo dela.

## 🧠 Como Funciona (Arquitetura Técnica)

O aplicativo segue um fluxo linear de dados:

1. **Scheduler**: Recebe as URLs e cria uma fila de execução.

2. **Downloader (Async Playwright)**:
   - Abre uma instância "invisível" do Chromium.
   - Aplica um User-Agent falso para parecer um usuário real.
   - Carrega a página e espera o evento `networkidle` (rede calma) ou `domcontentloaded`.
   - Executa um Scroll automático para forçar o carregamento de imagens e dados "Lazy Load".

3. **Parser Universal (Heurístico)**:
   - **HTML Tables**: Usa o `pandas.read_html` para varrer tags `<table>`.
   - **Div Tables (Lógica Customizada)**: O algoritmo varre o HTML buscando elementos "Pai" que tenham muitos elementos "Filhos" diretos. Se os filhos tiverem estrutura de texto similar, eles são convertidos em linhas de um DataFrame.

4. **Interface (Streamlit)**: Renderiza os DataFrames e gerencia o loop de eventos assíncronos (com correção `ProactorEventLoop` para Windows).

## ⚠️ Resolução de Problemas Comuns

### Erro: `NotImplementedError` ou falha no Loop de Eventos (Windows)

**Causa**: O Windows usa um loop padrão que não suporta subprocessos assíncronos.

**Solução**: O código já inclui a correção automática:
```python
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
```

### Erro: Tabela vem "suja" ou com colunas estranhas

**Causa**: A extração via "Divs" é heurística. Ela tenta separar colunas visualmente.

**Solução**: Baixe o CSV e faça a limpeza final no Excel. É melhor ter os dados sujos do que não ter dados.

## ⚖️ Aviso Legal e Ético

- Este software foi criado para fins educacionais e de automação pessoal.
- Verifique sempre o arquivo `robots.txt` do site alvo.
- Não utilize para sobrecarregar servidores (ataques DoS).
- Respeite a privacidade e os Termos de Uso dos sites que você acessar.

---

Desenvolvido com Python 🐍 e Streamlit 🎈
