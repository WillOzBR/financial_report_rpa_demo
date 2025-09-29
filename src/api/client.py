import requests
from urllib.parse import urljoin
from src.config import TWELVE_API_KEY, logger

from src.models.financial_data import FinancialData
from src.utils.helpers import format_date, treat_float

BASE_URL = 'https://api.twelvedata.com/'
ENDPOINT = 'time_series'

def fetch_brl_usd_currency_by_day() -> dict:
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
    

def parse_currency_data(data: dict) -> list[FinancialData]:
    '''
        Transforma dados brutos da API Twelve Data para uma lista FinancialData, no formato esperado.

        Args:
            data (dict): JSON retornado pela API Twelve Data.

        return:
            list[FinancialData]: Lista com objetos estruturados contendo os dados da cotação.
                        Retorna lista vazia se não houver dados válidos.
    '''
    if not data or "values" not in data:
        logger.error("Dados inválidos ou vazios para parsear.")
        return []
    
    parsed_data = []
    for item in data["values"]:
        try:
            parsed = FinancialData(
                data_coleta=format_date(item["datetime"]),
                fonte_informacao='Twelve Data',
                valor_alta=treat_float(item["high"]),
                valor_baixa=treat_float(item["low"]),
                valor_fechamento=treat_float(item["close"])
            )
            parsed_data.append(parsed)

        except (ValueError, TypeError) as e:
            logger.error(f"Erro ao parsear entrada: {item}. Erro: {e}")
            continue
    
    return parsed_data


def get_usd_brl_daily_data() -> list[FinancialData]:
    """
    Orquestra a coleta do JSON bruto e a normalização
    para o formato FinancialData.

    return:
        list[FinancialData]: Lista de objetos normalizados
        Em caso de erro, retorna uma lista vazia ([])
    """
    # Coleta dados brutos da API
    raw_data = fetch_brl_usd_currency_by_day() 
    
    # Valida retorno
    if not raw_data:
        return []
    
    # Rerorna dados parseados para consumo
    return parse_currency_data(raw_data)