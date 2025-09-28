from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.config import logger

class BrowserInteractions:
    def __init__(self, driver: webdriver.Chrome, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    def access_url(self, url: str):
        """Acessa uma URL"""
        self.driver.get(url)

    def click(self, by: By, selector: str):
        """Clica em um elemento visível"""
        try:
            elem = self.wait.until(EC.element_to_be_clickable((by, selector)))
            elem.click()
        except TimeoutException as e:
            logger.error(f"Elemento não encontrado para click: {selector}")
            raise

    def write(self, by: By, selector: str, text: str, clear_first=True):
        """Escreve em um campo de input"""
        try:
            elem = self.wait.until(EC.presence_of_element_located((by, selector)))
            if clear_first:
                elem.clear()
            elem.send_keys(text)
        except TimeoutException as e:
            logger.error(f"Elemento não encontrado para write: {selector}")
            raise

    def read(self, by: By, selector: str) -> str:
        """Lê o texto de um elemento"""
        try:
            elem = self.wait.until(EC.presence_of_element_located((by, selector)))
            return elem.text.strip()
        except TimeoutException as e:
            logger.error(f"Elemento não encontrado para read: {selector}")
            raise

    def exists(self, by: By, selector: str) -> bool:
        """Valida se o elemento existe na página após período de espera"""
        try:
            self.wait.until(EC.presence_of_element_located((by, selector)))
            return True
        except TimeoutException:
            return False
        
    def does_not_exist(self, by: By, selector: str) -> bool:
        """Valida se o elemento não existe na página após período de espera"""
        try:
            self.wait.until(EC.invisibility_of_element_located((by, selector)))
            return False
        except TimeoutException:
            return True
        
    def get_url(self) -> str:
        """Retorna a URL atual da página"""
        return self.driver.current_url

    def close(self):
        """Fecha a página do navegador"""
        self.driver.close()
