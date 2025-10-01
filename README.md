# Coleta Automzatizada - Série histórica da Cotação do dólar (USD) em reais (BRL)

## Objetivo

O intuito desse projeto é demonstrar conhecimentos e práticas de automação em Python, em contextos distintos de API e web scraper (Selenium).

É realizada a coleta da série histórica da cotação do dólar (BRL/USD) de fontes e granularidades diferentes (dias/semanas), que estão em contextos de API e página web com Javascript interativo (alternância entre intervalos).

API: https://twelvedata.com/docs (Twelve Data)
Portal para scraping: https://www.investing.com/ (Investing)

Os dados coletados são devolvidos em um output único e normalizado, contendo a data da informação, fonte, valor de alta, baixa e fechamento.

## Instalação das dependências/Instalação

1. Clone o repositório em sua máquina:

   ````
   git clone https://github.com/WillOzBR/financial_report_rpa_demo.git
   ````
2. Crie um ambiente virtual (recomendado):

   ````
   # Cria ambiente .venv (pode ser utilizado uv também)
   python -m venv .venv

   # Ativa ambiente

   # Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ````
3. Instale as dependências do projeto (bibliotecas):

   ````
   # Considerando que arquivo está na root do projeto
   pip install -r requirements.txt
   ````

## Arquitetura

Para o projeto, foi adotada uma arquitetura de camadas (layered architecture), possuindo uma separação de responsabilidades entre camadas.

Visão macro das camadas adotadas e seus respectivos scripts:

- Modelo de dados: src/models/financial_data.py;
- Coleta de dados:
  - Para API:
    - src/api/client.py;
  - Para scraping:
    - src/scraping/scraper.py;
    - src/scraping/selenium_config.py;
    - src/scraping/selenium_helpers.py;
    - src/scraping/soup_parser.py;
- Utilitários: Scripts para normalização e apresentação:
  - src/utils/helpers.py;
  - src/utils/csv_writer.py;
- Configuração: src/config.py;
- Orquestração: app.py

## Execução

A execução do projeto ocorre a partir do script **app.py**, responsável por orquestrar a chamada dos demais scripts.
Conforme o sucesso da execução, é gerado um arquivo de output/relatório ('currency_report.csv' no caso dessa demo), no diretório 'data/'.
Sempre que chamado, o script iniciará um arquivo de log, que fica salvo em '/logs', para informações sobre a execução.

Abaixo estão exemplos de chamadas de execução, conforme os argumentos disponíveis:

````
# Executar ambos, scraping e API
python app.py all

# Executar apenas scraping
python app.py scraping

# Executar apenas chamada API
python app.py api
````

## Considerações

Visando uma melhor geração de valor, o projeto pode escalar para incorporar a captura de outros intervalos de tempo, moedas e informações, tal como gerar variações de output e apresentação das informações.

---
