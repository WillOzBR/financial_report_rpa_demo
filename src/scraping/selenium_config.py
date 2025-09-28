from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.config import RPA_DOWNLOAD_DIR, logger

class SeleniumBrowser:
    '''
        Classe para configuração do navegador Selenium com opções personalizadas visando
        otimização para downloads e robustez diante páginas responsivas.
    '''

    def __init__(self, 
                 download_dir: str = RPA_DOWNLOAD_DIR, 
                 headless: bool = False, 
                 extensions: list = None):
        '''
            Inicialização de configurações default do browser.

            Args:
                download_dir (str): Diretório padrão para downloads.
                headless (bool): Define se o navegador será iniciado em modo headless (sem tela).
                extensions (list): Lista de caminhos para extensões a serem carregadas. 
        '''

        self.download_dir = download_dir
        self.headless = headless
        self.extensions = extensions if extensions else []
    
    def _webdriver_options(self):
        '''
            Configurações do WebDriver para otimização de downloads e comportamento do navegador.

            return:
                options (webdriver.ChromeOptions): Opções do Chrome WebDriver.
        '''
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        if self.headless:
            options.add_argument("--headless=new")
        for ext in self.extensions:
            options.add_argument(f'--load-extension={ext}')
        options.add_argument('--no-sandbox')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-dev-shm-usage')
        return options
        
    def _get_chrome_service(self):
        '''
            Configuração do serviço do ChromeDriver utilizando o WebDriver Manager para
            gerenciar a versão correta do driver.

            return:
                service (Service): Serviço do ChromeDriver.
        '''
        chromedriver_path = ChromeDriverManager().install()
        if 'THIRD_PARTY_NOTICES.chromedriver' in chromedriver_path:
            chromedriver_path = chromedriver_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver')
        service = Service(chromedriver_path)
        return service
    

    def create_browser(self):
        '''
            Cria e retorna uma instância do navegador configurado.

            return:
                driver (webdriver.Chrome): Instância do Chrome WebDriver.
        '''
        try:
            options = self._webdriver_options()
            service = self._get_chrome_service()
            return webdriver.Chrome(service=service, options=options)
        except Exception as e:
            logger.error(f"Erro ao iniciar webdriver: {e}")
            raise
    

    def close_browser(self, driver):
        '''
            Fecha a instância do navegador.

            Args:
                driver (webdriver.Chrome): Instância do Chrome WebDriver a ser fechada.
        '''
        try:
            driver.quit()
        except Exception as e:
            logger.error(f"Erro ao fechar webdriver: {e}")
            raise