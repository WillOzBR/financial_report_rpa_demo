import os
import sys
import pandas as pd
from typing import List

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, root_dir)

from src.config import PORTAL_URL, logger, js_error_supression

from selenium.webdriver.common.by import By

from src.models.financial_data import FinancialData

from src.utils.helpers import treat_float
from src.scraping.selenium_config import SeleniumBrowser
from src.scraping.selenium_helpers import BrowserInteractions
from src.scraping.soup_parser import SoupParser


def get_portal_html():
    '''
        Realiza acesso ao portal web para extração do HTML da página.

        return:
            str | None: Conteúdo HTML da página caso o carregamento seja bem-sucedido.
            Retorna None em caso de falha.
    '''
    driver = SeleniumBrowser(headless=True).create_browser()
    bot = BrowserInteractions(driver)
    try:
        bot.access_url(PORTAL_URL)

        loaded = bot.exists(By.XPATH, "//div[@data-test='instrument-price-last']")

        if not loaded:  # Valida carregamento por elemento na página.
            logger.error("Página não carregou corretamente.")
            return None
        else:
            bot.execute_script("window.stop();")
            bot.execute_script(js_error_supression)
            bot.click(By.XPATH, "//div[contains(@class, 'historical-data-v2_selection-arrow')]")
            bot.click(By.XPATH, "//div[span[text()='Weekly']]")

            logger.info("Carregando dados da tabela...")

            max_scrolls = 15
            for scroll_attempt in range(max_scrolls):
                bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll até o final

                # Espera aumentar o número de linhas (ou timeout de 3s)
                if not bot.wait_for_count_increase(By.CSS_SELECTOR, "table tbody tr", timeout=3):
                    logger.info("Não há mais linhas para carregar")
                    break

                logger.info(f"Scroll {scroll_attempt + 1}/{max_scrolls}")

            html = bot.get_html()  # Retorna estrutura html da página
            return html

    except Exception as e:
        logger.exception(f"Erro ao obter HTML do portal: {e}")
        return None

    finally:
        driver.quit()


def normalize_data(html: str) -> List[FinancialData]:
    """
    Usa BeautifulSoup para extrair a tabela, Pandas para limpar e normalizar,
    e converte para uma lista de objetos FinancialData.
    """
    logger.info("Iniciando normalização da tabela raspada.")
    
    soup = SoupParser(html)
    table_data = soup.extract_table("table.freeze-column-w-1")

    if not table_data or len(table_data) < 2:
        logger.warning("Nenhuma tabela ou dados insuficientes encontrados para normalização.")
        return []

    # Criação do dataframe
    df = pd.DataFrame(table_data[1:], columns=table_data[0])

    # NORMALIZAÇÃO:
    # Renomear colunas para corresponder ao dataclass
    df.rename(columns={'Date': 'data_coleta', 
                       'Price': 'valor_fechamento',
                       'High': 'valor_alta', 
                       'Low': 'valor_baixa'}, inplace=True)
    
   
    # Conversão da data para o formato padronizado (AAAA-MM-DD)
    df['data_coleta'] = pd.to_datetime(df['data_coleta']).dt.strftime('%d/%m/%Y')
    
    # Trata valores numéricos
    numeric_cols = ['valor_fechamento', 'valor_alta', 'valor_baixa']

    for col in numeric_cols:
        df[col] = df[col].apply(treat_float) 

    # CONSOLIDAÇÃO
    normalized_list: List[FinancialData] = []
    
    # Seleciona apenas as colunas necessárias para o FinancialData
    required_cols = ['data_coleta', 'valor_alta', 'valor_baixa', 'valor_fechamento']

    # Itera sobre os registros limpos
    for record in df[required_cols].to_dict('records'):
        # Adiciona o campo de metadado 'fonte_informacao' fixo
        record['fonte_informacao'] = "Investing.com" # Ou o nome do portal que você está usando
        
        try:
            # Cria a instância do dataclass
            normalized_list.append(FinancialData(**record))
        except Exception as e:
            logger.warning(f"Erro ao criar FinancialData para {record['data_coleta']}: {e}")
            continue
    
    logger.info(f"Normalização concluída. {len(normalized_list)} registros FinancialData criados.")
    return normalized_list



def get_usd_brl_weekly_data() -> list[FinancialData]:
    """
    Orquestra a coleta do HTML bruto via Selenium e a normalização
    da tabela raspada para o formato FinancialData semanal.

    return:
        list[FinancialData]: Lista de objetos normalizados
        Em caso de erro, retorna uma lista vazia ([])
    """    
    # Coleta HTML bruto do portal (fetch)
    raw_html = get_portal_html() 
    
    # Valida retorno
    if not raw_html:
        logger.error("Coleta do HTML bruto falhou. Retornando lista vazia.")
        return []
    
    # Rerorna dados parseados e normalizados para consumo
    return normalize_data(raw_html)
