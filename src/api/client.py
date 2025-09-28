import requests
from urllib.parse import urljoin
from src.config import TWELVE_API_KEY, logger

BASE_URL = 'https://api.twelvedata.com/'
ENDPOINT = 'time_series'

def get_brl_usd_currency_by_day():
    '''
        Função para obter a cotação atual do dólar em relação ao real (BRL) utilizando a API Twelve Data.

        return:
            dict: Dados da cotação USD/BRL (valores em BRL).
            Em caso de erro, retorna um dicionário vazio.
            
    '''
    url = urljoin(BASE_URL, ENDPOINT)

    params = {
        'symbol': 'USD/BRL',
        'interval': '1day',
        'outputsize': 30,
        'apikey': TWELVE_API_KEY,
        'format': 'JSON'
    }

    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "error":
                code = data.get("code")
                message = data.get("message")
                logger.error(f"Erro na API: Code {code}, Message: {message}")
                return {}
            else:
                return data
            
        elif response.status_code == 404:
            logger.error(f"Página não encontrada: Code {response.status_code}")
            return {}
        else:
            logger.error(f"Erro inesperado: Code {response.status_code}")
            return {}
        
    except requests.RequestException as e:
        logger.error(f"Erro ao acessar a API Twelve Data: {e}")
        return {}
    
