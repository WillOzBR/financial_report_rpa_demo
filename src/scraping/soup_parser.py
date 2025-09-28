from bs4 import BeautifulSoup

class SoupParser:
    def __init__(self, html: str):
        '''
            Inicializa o parser com o HTML fornecido

            Args:
                html (str): Conteúdo HTML da página a ser analisada
        '''
        self.soup = BeautifulSoup(html, "html.parser")

    def extract_table(self, table_selector: str):
        """
            Extrai uma tabela presente na pagina HTML.

            Args:
                table_selector (str): Seletor para localizar a tabela    
        """
        table = self.soup.select_one(table_selector)
        if not table:
            return []
        rows = []
        for tr in table.find_all("tr"):
            cols = [td.get_text(strip=True) for td in tr.find_all(["td","th"])]
            if cols:
                rows.append(cols)
        return rows

    def extract_text(self, selector: str):
        """
            Extrai texto a partir de um seletor
        
            Args:
                selector (str): Seletor para localizar o de texto
        """
        elem = self.soup.select_one(selector)
        return elem.get_text(strip=True) if elem else None
