# 🕷️ Universal Web Scraper Pro
### Versão Portátil para Windows

Um aplicativo de Web Scraping inteligente e universal. Diferente de robôs tradicionais, este app utiliza inteligência heurística para detectar dados em qualquer site — desde tabelas clássicas na Wikipedia até grids modernos e complexos em sites de apostas e e-commerce — sem precisar de configurações manuais.

**Esta versão foi otimizada para rodar facilmente em qualquer computador Windows com o mínimo de configuração prévia.**

## 🚀 O que ele faz?

1. **Extração Universal**: Jogue qualquer link (Bet365, Amazon, Wikipedia, Finance sites) e ele varre os dados.
2. **Detector de "Div Tables"**: Reconhece listas e grids que parecem tabelas mas são feitos de `<div>` (muito comum em sites modernos que bloqueiam scrapers antigos).
3. **Instalação Automática**: O sistema configura seu próprio ambiente, baixa as bibliotecas e o navegador necessário automaticamente na primeira execução.
4. **Exportação**: Permite baixar os dados encontrados (Tabelas, Grids ou Links) diretamente em CSV.

## 📋 Pré-requisitos

Para usar este aplicativo, você só precisa de uma coisa instalada no computador:

- **Python** (Versão 3.10 ou superior)
  > **Nota**: Ao instalar o Python, lembre-se de marcar a caixinha: ☑️ **"Add Python to PATH"**.

## ▶️ Como Instalar e Rodar (Modo Fácil)

**Não é necessário abrir terminal ou digitar comandos de programação.**

1. **Baixe e Extraia**: Certifique-se de que todos os arquivos (`app.py`, `requirements.txt`, `iniciar.bat`) estejam juntos na mesma pasta.

2. **Execute o Iniciador**: Dê um clique duplo no arquivo:
   ```
   iniciar.bat
   ```

3. **Aguarde a Configuração Automática** (Apenas na 1ª vez): Uma tela preta abrirá. O script irá automaticamente:
   - Criar um ambiente isolado (para não bagunçar seu Windows).
   - Baixar as ferramentas necessárias.
   - Instalar o navegador Chromium.
   - Isso pode levar de 1 a 2 minutos na primeira vez.

4. **Use o App**: Assim que terminar, o seu navegador padrão abrirá com o aplicativo pronto para uso.

## 🛠️ Como Usar a Ferramenta

1. **Cole a URL**: Na caixa de texto, cole o link do site que deseja raspar (ex: uma página de jogo da Bet365 ou lista de produtos).

2. **Clique em "🚀 Extração Profunda"**: O robô vai navegar até o site invisivelmente.

3. **Analise as Abas**:
   - **🧩 Tabelas Dinâmicas (Divs)**: *(Mais Importante)* Verifique aqui se estiver buscando Odds de apostas ou produtos. O robô tenta montar tabelas baseadas no visual do site.
   - **📋 Tabelas Clássicas**: Dados vindos de estruturas `<table>` tradicionais.
   - **🔗 Links**: Lista de todos os links encontrados.

4. **Baixe**: Clique no botão "Baixar CSV" abaixo da tabela desejada.

## 📂 Estrutura dos Arquivos

```
universal-web-scraper-pro/
├── app.py              # Código fonte principal (Lógica do Robô + Interface)
├── iniciar.bat         # Script de automação para Windows
├── requirements.txt    # Lista de bibliotecas necessárias
└── venv/              # Pasta criada automaticamente (ambiente isolado)
```

- **`app.py`**: O código fonte principal (Lógica do Robô + Interface).
- **`iniciar.bat`**: Script de automação para Windows. Ele garante que tudo rode sem erros.
- **`requirements.txt`**: Lista de ingredientes (bibliotecas) que o `iniciar.bat` usa.
- **`venv/`** *(Pasta criada automaticamente)*: Onde o programa guarda as ferramentas dele. Se deletar, ele cria de novo.

## ❓ Solução de Problemas Comuns

### 1. O arquivo `iniciar.bat` abre e fecha imediatamente

**Causa**: Você provavelmente não tem o Python instalado ou não marcou a opção "Add to PATH" na instalação.

**Solução**: Reinstale o Python baixando do [site oficial](https://python.org) e marque a opção de PATH.

### 2. O App diz "Nenhuma tabela encontrada"

**Causa**: O site pode usar uma estrutura muito complexa ou bloquear robôs agressivamente.

**Solução**: Tente verificar a aba "Tabelas Dinâmicas". Se ainda assim falhar, o site pode exigir interação humana (login/captcha) que este robô automátizado evita por segurança.

### 3. Tela preta travada em "Instalando..."

Se for a primeira vez, pode demorar dependendo da sua internet (ele baixa cerca de 150MB do navegador). Tenha paciência.

## ⚖️ Aviso Legal

Esta ferramenta é destinada para **fins educacionais e automação de tarefas pessoais**. Respeite os Termos de Uso e o arquivo `robots.txt` dos sites que você acessar. O autor não se responsabiliza pelo uso indevido da ferramenta.

---

Desenvolvido com Python 🐍, Streamlit 🎈 e Playwright 🎭
