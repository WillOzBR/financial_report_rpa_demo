import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, root_dir)

from src.config import PORTAL_URL, logger, js_error_supression

from selenium.webdriver.common.by import By

from src.scraping.selenium_config import SeleniumBrowser
from src.scraping.selenium_helpers import BrowserInteractions
from src.scraping.soup_parser import SoupParser


def get_portal_html():
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
